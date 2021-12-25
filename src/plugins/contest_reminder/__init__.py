import sys

from datetime import datetime, timedelta

import nonebot
import nonebot.rule
from nonebot import logger
from nonebot import require
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from src.contests_services import get_contest

scheduler = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job("cron", id="__monitor__", hour='4, 12, 20')
# @scheduler.scheduled_job('interval', id='__monitor__', seconds=10) # for debug
async def __monitor__():
    contests = await get_contest()

    if len(contests) is 0:
        logger.error("Failed to get contests %d" % contests)
        return

    for i in contests:
        time: datetime = i['contest_time'][0]
        if (time - datetime.now()) <= timedelta(hours=12):
            if datetime.now().hour == 20:
                await __add_job__([i])
            job_id = i['name']
            if not scheduler.get_job(job_id):
                broadcast_time: datetime = time - timedelta(minutes=20)
                scheduler.add_job(__add_job__, "date", id=job_id, args=[i],
                                  run_date=broadcast_time)


async def __add_job__(args):
    contest = args[0]

    bot = nonebot.get_bot()
    event = GroupMessageEvent
    count: timedelta = contest['contest_name'][0] - datetime.now()

    msg = (f"{contest['name']}\n" +
           f"在{int(count.total_seconds() // 60)}分钟后开始\n" +
           f"比赛链接{contest['link']}")
    logger.debug(msg)

    send_groups = [926293131, 516991226]
    for i in send_groups:
        event.group_id = i
        await bot.send(event=event, message=msg)
