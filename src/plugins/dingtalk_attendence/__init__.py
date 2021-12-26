import nonebot

from datetime import datetime, timedelta
from nonebot import logger
from nonebot.rule import to_me
from nonebot import require, Bot, on_command
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from src.dingtalk_services.checker import permission_checker
from .attendance import attendance_result

# 浪在ACM群号: 516991226
scheduler = require("nonebot_plugin_apscheduler").scheduler
session = on_command('考勤', rule=to_me(), priority=2)


@scheduler.scheduled_job("cron", id="__reminder_adapter", day_of_week='mon-fri, sun', hour=19)
async def __reminder_adapter():
    # 每周天到周一的打卡提醒
    logger.info('Operate cycling task: daily attendance')
    bot = nonebot.get_bot()
    _event = GroupMessageEvent
    _event.group_id = 516991226
    absence, vacation = await attendance_result()
    await bot.send(event=_event, message=absence)
    await bot.send(event=_event, message=vacation)


@session.handle()
async def group_message_adapter(bot: Bot, event: GroupMessageEvent):
    """
    处理 查询考勤命令
    :param bot:
    :param event:
    :return:
    """
    logger.info('Get attendance check from %s' % event.group_id)

    if not await permission_checker(bot, event):
        await session.finish()
        return

    msg = str(event.get_message()).strip()
    query_time = datetime.today()

    # 这里自定义一些查询关键词
    if msg == '':
        pass
    elif msg in ['昨天', '昨日']:
        query_time -= timedelta(days=1)
    elif msg in ['前天']:
        query_time -= timedelta(days=2)
    else:
        try:
            query_time = datetime.strptime(msg, "%Y.%m.%d")
        except:
            logger.error("illegal format: %s" % msg)
            await session.finish("输入的日期不合法，合法格式为：年.月.日")

    absence, vacation = await attendance_result(query_time)
    await session.send(absence)
    await session.finish(vacation)
