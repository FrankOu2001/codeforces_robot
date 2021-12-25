import sys

import nonebot
from datetime import datetime, timedelta
from nonebot import logger
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot import require, Bot, on_command
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp import GROUP_OWNER, GROUP_ADMIN
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
    await bot.send(event=event, message=vacation)


@session.handle()
async def group_message_adapter(bot: Bot, event: GroupMessageEvent):
    """
    处理 查询考勤命令
    :param bot:
    :param event:
    :return:
    """
    logger.info('Get attendance check from %s' % event.group_id)

    async def permission_checker_() -> bool:
        """
        判断是否有查询该命令的权限

        由于涉及到集训队的信息，因此必须要严格控制查询的权限
        而且该命令会输出很多的文字，所以一定要限制查询者
        防止滥用刷屏
        :return:
        """
        # 在这里设置可以使用的群
        if event.group_id not in [516991226, 539756695]:
            logger.warning('{} 不在处理的群号中，无法调用考勤查询'.format(event.group_id))
            return False
        elif await GROUP_OWNER(bot, event) | await GROUP_ADMIN(bot, event) | await SUPERUSER(bot, event):
            return True
        logger.warning(f'{event.get_user_id} 没有权限调用考勤查询')

        return False

    if not await permission_checker_():
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
