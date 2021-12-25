from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import MessageSegment
from src.contests_services import get_contest

session = on_command("contests", rule=to_me(), priority=2)


@session.handle()
async def get_future_contests(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    contests = await get_contest(args)

    if not len(contests):
        await session.finish('比赛无法正常拉取, 详细信息请看控制台')
    else:

        msg = "Recent Contests:\n"
        for x in contests:
            name = x['name']
            link = x['link']
            begin, end = x['contest_time']
            msg += f"\n{name}\n" \
                   f"RegisterLink: {link}\n" \
                   f"Time: {begin} - {end}"
        await session.finish(MessageSegment.text(msg))
