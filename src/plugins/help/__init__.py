from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Event, Bot
from nonebot.typing import T_State


session = on_command("help", rule=to_me(), priority=1)


@session.handle()
async def Help(bot: Bot, event: Event, state: T_State):
    totalHelp = """一只很不完善的机器人DA⭐ZE！

〇 机器人也是有名字的！你可以叫他‘cf’/'ybbbot'(好奇怪的名字)
〇 以 ”bot名字(或者@bot)+空格(非必要)+命令“ 的格式使bot接收指令=v=
===================
● info 'Codeforces’ID' # 查询指定Codeforces'ID的基本信息
● contests # 查询Codeforces/AcCoder/牛客 近期的比赛
● 考勤 # 查询今日钉钉的未出勤及请假人员
● 出勤统计 # 查询本周钉钉成员的出勤情况
● time # 查询当前时间(并没有什么用)
● 天气 '地点' # 查询'地点'的实时天气
※ bot会在工作日下午七点发送考勤情况
※ bot会在检测到的比赛开始前30min发送消息提醒（开发中）
===================
以下是现支持的命令，目前仍处于开发阶段，更多功能敬请期待()
"""
    await session.finish(totalHelp)
