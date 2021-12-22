import sys

from datetime import datetime, timedelta

import nonebot
import nonebot.rule
from nonebot import require, Bot, on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.event import GroupMessageEvent, Event
from nonebot.typing import T_State
from codeforces_services import get_contests

scheduler = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job("interval", hours=2, id="__monitor__")
async def __monitor__():
    status, contests = await get_contests()

    if not status:
        print("Failed to get contests %d" % contests, file=sys.stderr)
        return

    for i in contests:
        time = i['contestTime']
        if (time - datetime.now()) < timedelta(hours=2):
            job_id = i['contestName']
            end_time: datetime = time - timedelta(minutes=20)
            begin_time: datetime = end_time - timedelta(seconds=30)
            if not scheduler.get_job(job_id):
                scheduler.add_job(__add_job__, "interval", id=job_id, args=i, seconds=20,
                                  start_date=begin_time.strftime("%Y-%m-%d %H:%M:%S"),
                                  end_date=end_time.strftime("%Y-%m-%d %H:%M:%S"))


async def __add_job__(args):
    contest, job_id = args

    bot = nonebot.get_bot()
    event = GroupMessageEvent
    msg = ("{}\n"
           "在20分钟后开始\n"
           "比赛链接{}\n").format(contest['contestName'], contest['registerLink'])

    send_groups = [926293131]
    for i in send_groups:
        event.group_id = i
        await bot.send(event=event, message=msg)


session = on_command("jobs", rule=nonebot.rule.to_me(), priority=1, permission=SUPERUSER)


@session.handle()
async def _(bot: Bot, event: Event, state: T_State):
    scheduler.print_jobs()
