import nonebot

from datetime import datetime, timedelta, date
from nonebot import logger
from nonebot.rule import to_me
from nonebot import require, Bot, on_command
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from src.dingtalk_services.checker import permission_checker
from src.dingtalk_services.report import get_report

session = on_command('出勤统计', rule=to_me(), priority=2)


@session.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global begin, end
    if not await permission_checker(bot, event):
        await session.finish()
        return

    args = str(event.get_message()).strip()
    logger.debug(args)
    msg = ''

    if args in ['', '这个月', '本月']:
        end = datetime.now()
        begin = datetime.today().replace(day=1, second=0, microsecond=0)

    elif args in ['上个月', '上月']:
        end = datetime.today().replace(day=1)
        begin = (end - timedelta(hours=48)).replace(day=1)
    else:
        try:
            time = datetime.strptime(args, "%Y.%m")
            begin = time.replace(day=1)
            if begin.month == 12:
                end = datetime(begin.year+1, 1, 1)
            else:
                end = begin.replace(month=begin.month+1)
        except ValueError as e:
            logger.error(e)
            await session.finish(r'无法解析输入, 正确的格式为:"年.月"')
        finally:
            return

    result = await get_report((begin, end))
    for name, absence, attendance in result:
        msg += f'{name}\t缺勤次数:{absence}\t出勤天数:{attendance}\n'

    await session.finish(msg)
