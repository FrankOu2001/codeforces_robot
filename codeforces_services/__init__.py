import httpx

from bs4 import BeautifulSoup
from datetime import datetime, timedelta


async def __get_contest(data) -> dict:
    tags = data.find_all('td')
    constestName: str = tags[0].string
    constestName = constestName.replace(r'\n', '').replace(r'\r', '').strip()
    href = [i.find_all('a') for i in tags]

    time_info: str = href[2][0]['href']
    time_info = time_info[time_info.index('?') + 1:]
    contestTime = datetime.strptime(time_info, 'day=%d&month=%m&year=%Y&hour=%H&min=%M&sec=%S&p1=166')
    contestTime += timedelta(hours=+5)
    contestTime = contestTime.strftime("%Y-%m-%d %H:%M:%S")

    registerLink = 'none'
    if len(href[-1]) > 0:
        registerLink = 'https://codeforces.com/' + \
                       href[-1][0]['href']

    return {'contestName': constestName, 'contestTime': contestTime, 'registerLink': registerLink}


async def get_contests():
    global origin_data
    try:
        origin_data = httpx.get('https://codeforces.com/contests', timeout=5)
    except Exception as e:
        print(e)
        return False, 408

    if origin_data.status_code != 200:
        return False, origin_data.status_code
    s = BeautifulSoup(origin_data, 'html.parser')
    body = s.find(id='pageContent')
    table = body.table.find_all('tr')

    recent_contests = list()
    for i in table[1:]:
        recent_contests.append(await __get_contest(i))

    return True, recent_contests
