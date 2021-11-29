import sys
import json
import urllib.request
import urllib.parse

from nonebot import on_command, CommandSession

__plugin_name = 'codeforces_data'
__plugin_usage__ = '拉取codeforces的相关数据'


async def get_request(url):
    try:
        request = urllib.request.urlopen(url, timeout=5)
        get = json.loads(request.read())

        if get['status'] != 'OK':
            return get['result']
        else:
            return -1
    except urllib.error.HTTPError as exception:
        print(exception.code, file=sys.stderr)
    finally:
        print(url, file=sys.stderr)
        return -2


@on_command('get_user_info', aliases=['查询', 'info'])
async def get_user_info(session: CommandSession):
    user_url = "https://codeforces.com/api/user.info?handles="
    user_name = session.current_arg_text.strip()
    if user_name.isspace():
        return None

    info = await get_request(user_url + user_name)

