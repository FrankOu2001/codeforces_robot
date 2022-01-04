import asyncio
import sys

import mariadb
from datetime import datetime
from nonebot import logger, require
from . import codeforces, atcoder, nowcoder


def get_connect() -> mariadb.connection:
    """
    获取数据库的连接
    :return: 数据库的连接
    """
    try:
        conn = mariadb.connect(
            user='bot',
            host='localhost',
            database='bot',
            passwd='robot',
            port=3306
        )
    except mariadb.Error as e:
        print(e)
        sys.exit(-1)

    return conn


async def __update__(typename) -> bool:
    """
    更新比赛
    :param typename: 更新的比赛的类型
    :return:
    """
    global connect
    contest = await __get_contest__(typename)
    status = False

    if len(contest) == 0:
        logger.warning(f'未获取{typename}最近的比赛')
        return status

    try:
        connect = get_connect()
        cur = connect.cursor()
        cur.execute(f"TRUNCATE TABLE {typename}")

        for x in contest:
            name = x['name']
            link = x['link']
            contest_time = list(map(str, x['contest_time']))
            data = {
                'name': name,
                'link': link,
                'contest_time': contest_time
            }
            cur.execute(f'INSERT INTO {typename} (data) VALUES (\"{data}\")')
        status = True
    except mariadb.Error as e:
        print(e, file=sys.stderr)
    finally:
        connect.close()
        return status


async def __get_contest__(contest_type: str) -> list:
    """
    爬取各个平台的比赛

    目前支持的平台:
    codeforces
    atcoder
    nowcoder

    :param contest_type:
    :return:
    """
    if contest_type == 'cf':
        return await codeforces.get_contests()
    elif contest_type == 'at':
        return await atcoder.get_contests()
    elif contest_type == 'nk':
        return await nowcoder.get_contests()
    elif contest_type == '':
        s = []
        s.extend(await codeforces.get_contests())
        s.extend(await atcoder.get_contests())
        s.extend(await nowcoder.get_contests())
        return s

    return []


async def update(typename) -> bool:
    if typename == '':
        return await __update__('codeforces') and \
               await __update__('atcoder') and \
               await __update__('nowcoder')
    elif typename == 'codeforces':
        return await __update__('codeforces')
    elif typename == 'atcoder':
        return await __update__('atcoder')
    elif typename == 'nowcoder':
        return await __update__('nowcoder')
    else:
        logger.error('unknown type when update recent contests')
        return False


async def pull_data(typename='') -> list:
    connect = get_connect()
    cur = connect.cursor()

    if typename != '':
        cur.execute(f'SELECT data FROM {typename}')
    else:
        cur.execute(f'SELECT data FROM codeforces')
        cur.execute(f'SELECT data FROM atcoder')
        cur.execute(f'SELECT data FROM nowcoder')
    data = []
    for i in cur:
        x = eval(i[0])
        x['contest_time'] = tuple(map(lambda it: datetime.strptime(it, '%Y-%m-%d %H:%M:%S'), x['contest_time']))
        data.append(x)

    return data


scheduler = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job("cron", id="database_update", hour='3, 15')
async def database_update():
    await update('')


if __name__ == '__main__':
    # asyncio.run(update(''))
    asyncio.run(pull_data('codeforces'))
else:
    asyncio.get_event_loop().run_until_complete(update(''))
