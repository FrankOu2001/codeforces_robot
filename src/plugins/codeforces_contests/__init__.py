from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from aiocqhttp.message import MessageSegment
from src.codeforces_services import get_contests

session = on_command("contests", rule=to_me(), priority=2)


@session.handle()
async def get_future_contests(bot: Bot, event: Event, state: T_State):
    status, contests = await get_contests()
    if not status:
        if contests == 404:
            await session.finish('当前无法访问Codeforces, 请稍后重试(404)')
        elif contests == 302:
            await session.finish('当前即将进入比赛或正在进行比赛中, 无法查询(302)')
        else:
            await session.finish('未知的错误http code=%d' % contests)
    else:

        msg = "Recent Contests:\n\n"
        for contest in contests:
            msg += "{contestName}\n" \
                   "Start Time:{contestTime}\n" \
                   "Register Link:{registerLink}\n\n". \
                format(contestName=contest['contestName'],
                       contestTime=contest['contestTime'].strftime("%Y-%m-%d %H:%M:%S"),
                       registerLink=contest['registerLink'])
        await session.finish(MessageSegment.text(msg.strip('\n')))
