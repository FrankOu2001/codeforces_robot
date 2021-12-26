import httpx
from httpx import HTTPError
from nonebot import logger
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


async def get_contests():
    """
    爬取atcoder的比赛
    :return: 返回(状态， 比赛/http_code)
    """
    global data
    try:
        data = httpx.get("https://atcoder.jp/contests", timeout=5)
    except HTTPError as e:
        logger.error(f'获取atcoder比赛失败 http_code={e}')
        return

    contest = []
    soup = BeautifulSoup(data, 'html.parser').body.div
    tr = soup.find(id="contest-table-upcoming").tbody.find_all('tr')

    for i in tr:
        k = i.find_all('td')
        # time
        t = k[0].time.string
        # 小鬼子比咱快一个小时，得减去
        begin_time = datetime.strptime(t, '%Y-%m-%d %H:%M:%S+0900') - timedelta(hours=1)
        # name
        name = k[1].a.string
        # link
        link = 'https://atcoder.jp' + k[1].a['href']
        # length
        hour, minute = map(int, k[2].string.split(':'))
        end_time = begin_time + timedelta(hours=hour, minutes=minute)

        contest.append({
            'name': name,
            'link': link,
            'contest_time': (begin_time, end_time)
        })

    return contest
