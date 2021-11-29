import sys
import json
import urllib.request
import urllib.parse

from nonebot import on_command, CommandSession
from plugins.time import get_last_login_time

__plugin_name = 'codeforces_data'
__plugin_usage__ = '拉取codeforces的相关数据'


async def get_request(url):
    try:
        request = urllib.request.urlopen(url, timeout=5)
        get = json.loads(request.read())

        print(get)
        print(type(get['status']), get['status'])
        if get['status'] == 'OK':
            return get['result'][0]
        else:
            return False
    except urllib.error.HTTPError as exception:
        print(exception.code, file=sys.stderr)


@on_command('get_user_info', aliases=['查询', 'info'])
async def get_user_info(session: CommandSession):
    user_url = "https://codeforces.com/api/user.info?handles="
    user_name = session.current_arg_text.strip()
    if user_name.isspace():
        return None

    info = await get_request(user_url + user_name)

    sent_message = ""
    if not info:
        sent_message = "%s不存在，请重新尝试" % user_name

    else:
        sent_message = """Name: {name}
        Last visit: {time}
        Rank: {rank}
        Rating: {rating}
        Score change in the last game: {scoreChange}
        Max rating: {maxRating}
        """.format(name=info['handle'],
                   time=await get_last_login_time(info['lastOnlineTimeSeconds']),
                   rank=info['rank'], rating=info['rating'],
                   scoreChange='coming soon', maxRating=info['maxRating'])

    await session.send(sent_message)
