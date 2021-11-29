from nonebot import on_command, CommandSession
from datetime import datetime

__plugin_name = 'get_time'
__plugin_usage__ = '获取服务器当前的系统时间'


@on_command('get_time', aliases=['时间', '当前时间'])
async def get_time(session: CommandSession):
    current_time = await get_current_time()
    await session.send(current_time)


async def get_current_time() -> str:
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")


async def get_last_login_time(time_stamp: int) -> str:
    current_time_stamp = datetime.timestamp(datetime.now())
    if abs(current_time_stamp - time_stamp) <= 3:
        return "Online"
    else:
        return datetime.utcfromtimestamp(time_stamp).\
            strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    s = get_last_login_time(datetime.now().timestamp())
    print(s)