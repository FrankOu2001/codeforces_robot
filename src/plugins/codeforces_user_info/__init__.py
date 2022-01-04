import sys
import httpx

from nonebot import on_command, logger
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import MessageSegment
from nonebot.typing import T_State
from src.plugins.time import timestamp_convert

__plugin_name__ = 'codeforces_user_info'
__plugin_usage__ = '拉取codeforces的相关数据'


async def get_request(url):
    try:
        request = httpx.get(url, timeout=3)
        get = request.json()

        if request.status_code == httpx.codes.OK and get['status'] == 'OK' and len(get['result']):
            logger.debug(get['result'])
            return True, get['result'][0]
        else:
            return False, request.status_code
    except httpx.HTTPError as e:
        logger.error(e, file=sys.stderr)
        return False, e


session = on_command("info", rule=to_me(), priority=5)


@session.handle()
async def get_user_info(bot: Bot, event: Event, state: T_State):
    user_url = "https://codeforces.com/api/user.info?handles="
    user_name = str(event.get_message()).strip()
    print('user_name=%s' % user_name)
    if user_name == "":
        await session.reject("查询名称不能为空, 请重新输入要查找的用户名")
        return

    status, info = await get_request(user_url + user_name)
    if status:
        sent_message = """Name: {name}
Last visit: {time}
Rank: {rank}
Rating: {rating}
Max rating: {maxRating}""" \
            .format(name=info.get('handle', 'anonymous'),
                    time=await timestamp_convert(info.get('lastOnlineTimeSeconds', 'very long')),
                    rank=info.get('rank', 'unknown'), rating=info.get('rating', 'unknown'),
                     maxRating=info.get('maxRating', 'unknown'))
        title_img_url = info.get('titlePhoto')
        await session.send(MessageSegment.image(title_img_url, timeout=3))
    else:
        if info == 200 or 400:
            sent_message = "用户: %s不存在" % user_name
            pass
        else:
            sent_message = "http code=%d" % info

    await session.finish(sent_message)
