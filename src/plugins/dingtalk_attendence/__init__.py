import sys

import nonebot
from datetime import datetime, timedelta
from nonebot import logger
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot import require, Bot, on_command
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp import GROUP_OWNER
from src.dingtalk_services import get_vacation, get_absence

# 浪在ACM群号: 516991226
scheduler = require("nonebot_plugin_apscheduler").scheduler
session = on_command('考勤', rule=to_me(), priority=2)


@scheduler.scheduled_job("cron", id="__reminder_adapter", day_of_week='mon-fri, sun', hour=19)
async def __reminder_adapter():
    # 每周天到周一的打卡提醒
    logger.info('Operate cycling task: daily attendance')
    bot = nonebot.get_bot()
    event = GroupMessageEvent
    event.group_id = 516991226
    absence, vacation = await attendance_result()
    await bot.send(event=event, message=absence)
    await bot.send(event=event, message=absence)


@session.handle()
async def group_message_adapter(bot: Bot, event: GroupMessageEvent):
    logger.info('Get attendance check from %s' % event.group_id)

    # 判断发送拉取考勤的信息的群是否是指定的群
    if not (event.group_id in [516991226, 539756695] and (SUPERUSER | await GROUP_OWNER(bot, event))):
        logger.warning('{} 不在处理的群号中，无法调用'.format(event.group_id))
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
            print("illegal format: %s" % msg, file=sys.stderr)
            await session.finish("输入的日期不合法，合法格式为：年.月.日")

    absence, vacation = await attendance_result(query_time)
    await session.send(absence)
    await session.finish(vacation)


async def attendance_result(query_time: datetime = datetime.today()) -> tuple[str, str]:
    """
    发送集训队的考勤状况
    :return: 缺勤和请假的信息
    """

    absence = await get_absence(query_time)

    # 请假
    in_vacation = await get_vacation(absence, query_time)
    logger.warning(f'{len(absence)} people are absent')
    # 缺勤
    bad_guys = [x for x in absence
                if x not in in_vacation]

    absence_msg = query_time.strftime("%Y年%m月%d日")
    if len(bad_guys) == 0:
        absence_msg += "全员出勤"
    else:
        absence_msg += "未出勤的有:\n"
        for i in range(len(bad_guys)):
            absence_msg += bad_guys[i][0] + '\t'
            if (i + 1) % 3 == 0:
                absence_msg += '\n'

    vacation_msg = query_time.strftime("%Y年%m月%d日")
    if len(in_vacation) == 0:
        vacation_msg += "无人请假"
    else:
        vacation_msg += "请假的人有:\n"
        for i in range(len(in_vacation)):
            vacation_msg += in_vacation[i][0] + '\t'
            if (i + 1) % 3 == 0:
                vacation_msg += '\n'

    return absence_msg, vacation_msg
