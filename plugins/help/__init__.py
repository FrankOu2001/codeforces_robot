from nonebot import on_command, CommandSession


@on_command('help', aliases=['帮助'])
async def Help(session: CommandSession):
    totalHelp = """如果在群聊中，你可以直接@此bot来开始命令，例如：
@bot echo BOKI
或者，你可以用' '(一个空格)/'伞兵'/'cf'来让bot接收你的命令，例如：
伞兵 echo BOKI/ echo BOKI/ cf echo BOKI
=======================
目前bot拥有的命令：
echo XXXX 让bot来说XXXXXX，图片或表情也可
time 发送当前的时间
天气 XXX 获取某地在此刻的天气 (weather 也可以)
info XXXXX 读取并发送你在codeforces的账号的基本信息
contests 显示codeforces近期的比赛以及链接
以上！
======================="""
    await session.send(totalHelp)
