import nonebot
from nonebot import logger, Bot
from nonebot.adapters.cqhttp import GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER


async def permission_checker(bot: Bot, event: GroupMessageEvent) -> bool:
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
    logger.debug(f'{event.get_user_id} 没有权限调用考勤查询')

    return False

