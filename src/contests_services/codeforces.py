import httpx
from httpx import HTTPError

from nonebot import logger
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


async def get_contests():
    """
    爬取Cf的比赛
    :return: 返回(状态， 比赛/http_code)
    """
    try:
        origin_data = httpx.get('https://codeforces.com/contests', timeout=5)
    except HTTPError as e:
        logger.error(f'拉取cf比赛失败 http_code={e}')
        return

    s = BeautifulSoup(origin_data, 'html.parser').find(id='pageContent').div.div.table
    tr = s.find_all('tr')[1::]

    contest = []

    for i in tr:
        k = i.find_all('td')
        # name
        name = k[0].string.replace('\r', '').replace('\n', '').strip()

        # begin_time
        t = k[2].a['href']
        t = t[t.index('?') + 1:]
        begin_time = timedelta(hours=+5) + \
                     datetime.strptime(t, 'day=%d&month=%m&year=%Y&hour=%H&min=%M&sec=%S&p1=166')

        # length
        hour, minute = map(int, k[3].string.split(':'))
        end_time = begin_time + timedelta(hours=hour, minutes=minute)

        # link
        link = "None"
        if k[5].a:
            link = 'https://codeforces.com' + k[5].a['href']

        contest.append({
            'name': name,
            'link': link,
            'contest_time': (begin_time, end_time)
        })

        return contest

