import httpx

from datetime import datetime
from httpx import HTTPError
from nonebot import logger
from bs4 import BeautifulSoup


async def get_contests():
    """
    爬取牛客网的比赛
    :return: 返回(状态， 比赛/http_code)
    """

    # nk_url是牛客系列赛, school_url是高校系列赛
    nk_url = 'https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=13'
    # school_url = 'https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=14'
    try:
        nk_get = httpx.get(url=nk_url, timeout=3)
        # school_get = httpx.get(url=school_url, timeout=3)
    except HTTPError as e:
        logger.error(f'获取牛客比赛失败 http_code={e}')
        return

    data = BeautifulSoup(nk_get, 'html.parser'). \
        find_all('div', 'platform-item js-item')

    contest = []

    for i in data:
        h4 = i.h4
        status = h4.span.string

        # 不记录正在进行的比赛
        if status == '比赛中':
            continue

        name = h4.a.string
        link = 'https://ac.nowcoder.com/acm' + h4.a['href']
        _ = [x.string.strip().replace('\n', '').replace('：', ' ').split()
             for x in i.ul.find_all('li')]

        register_time = (
            datetime.strptime(' '.join(_[0][1:3:]), '%Y-%m-%d %H:%M'),
            datetime.strptime(' '.join(_[0][4:6:]), '%Y-%m-%d %H:%M')
        )
        contest_time = (
            datetime.strptime(' '.join(_[1][1:3:]), '%Y-%m-%d %H:%M'),
            datetime.strptime(' '.join(_[1][4:6:]), '%Y-%m-%d %H:%M')
        )
        holder = _[2][-1]

        contest.append({
            'name': name,
            'link': link,
            # 'holder': holder,
            # 'register_time': register_time,
            'contest_time': contest_time
        })

    return contest
