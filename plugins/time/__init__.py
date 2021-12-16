from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from datetime import datetime

__des__ = "获取当前日期"
__cmd__ = "time"


async def timestamp_convert(time_stamp: int) -> str:
    return datetime.fromtimestamp(time_stamp). \
        strftime("%Y-%m-%d %H:%M:%S")


async def get_current_time() -> str:
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")


_time = on_command("time", rule=to_me(), priority=5)


@_time.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
    await _time.finish(await get_current_time())
