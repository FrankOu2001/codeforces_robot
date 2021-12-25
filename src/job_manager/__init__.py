import nonebot
import nonebot.rule
from nonebot import require, Bot, on_command, logger
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.event import Event


scheduler = require("nonebot_plugin_apscheduler").scheduler
session = on_command("manage", priority=1, permission=SUPERUSER)


@session.handle()
async def handler(bot: Bot, event: Event):
    """
    对scheduler进行的各种任务的查看和管理
    :param bot:
    :param event:
    :return:
    """
    args = str(event.get_message()).strip().split()
    if args[0] == 'jobs':
        await list_jobs(bot, event)
    elif args[0] == 'stop':
        await pause_jobs(args[1::])
    elif args[0] == 'review':
        await resume_jobs(args[1::])
    elif args[0] == 'remove':
        await remove_jobs(args[1::])
    else:
        pass


async def list_jobs(bot: Bot, event: Event):
    jobs = '\n\n'.join([str(x) for x in scheduler.get_jobs()])
    await session.finish(jobs)


async def pause_jobs(jobs):
    for job in jobs:
        if scheduler.get_job(job) is None:
            logger.error(f'{job} is not a scheduled job')
        else:
            scheduler.pause_job(job)


async def resume_jobs(jobs):
    for job in jobs:
        if scheduler.get_job(job) is None:
            logger.error(f'{job} is not a scheduled job')
        else:
            scheduler.resume_job(job)


async def remove_jobs(jobs):
    for job in jobs:
        if scheduler.get_job(job) is None:
            logger.error(f'{job} is not a scheduled job')
        else:
            scheduler.remove_job(job)
