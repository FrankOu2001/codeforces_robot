import sys
import httpx

from nonebot import on_command, CommandSession
from plugins.codeforces_contests.contests_info import get_contests
from plugins.time import timestamp_convert
from aiocqhttp.message import MessageSegment

__plugin_name = 'codeforces_user_info'
__plugin_usage__ = '拉取codeforces的相关数据'


async def get_request(url):
    try:
        request = httpx.get(url, timeout=3)
        get = request.json()

        if request.status_code == httpx.codes.OK and get['status'] == 'OK' and len(get['result']):
            print(get['result'])
            return True, get['result'][0]
        else:
            return False, request.status_code
    except httpx.HTTPError as e:
        print(e, file=sys.stderr)
        return False, e


@on_command('get_user_info', aliases=['查询', 'info'])
async def get_user_info(session: CommandSession):
    user_url = "https://codeforces.com/api/user.info?handles="
    user_name = session.current_arg_text.strip()
    if user_name.isspace():
        await session.send("查询名称不能为空")
        return

    status, info = await get_request(user_url + user_name)
    if status:
        sent_message = """Name: {name}
Last visit: {time}
Rank: {rank}
Rating: {rating}
Score change in the last game: {scoreChange}
Max rating: {maxRating}""" \
            .format(name=info.get('handle', 'anonymous'),
                    time=await timestamp_convert(info.get('lastOnlineTimeSeconds', 'very long')),
                    rank=info.get('rank', 'unknown'), rating=info.get('rating', 'unknown'),
                    scoreChange='coming soon', maxRating=info.get('maxRating', 'unknown'))
        title_img_url = info.get('titlePhoto')
        await session.send(MessageSegment.image(title_img_url, timeout=3))
    else:
        if info == 200 or 400:
            sent_message = "用户: %s不存在" % user_name
            pass
        else:
            sent_message = "http code=%d" % info

    await session.send(sent_message)
