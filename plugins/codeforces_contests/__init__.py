from nonebot import on_command, CommandSession

from plugins.codeforces_contests.contests_info import get_contests


@on_command('get_future_contests', aliases=['近期比赛', 'contests'])
async def get_future_contests(session: CommandSession):
    status, contests = await get_contests()
    if not status:
        if contests == 404:
            await session.send('当前无法访问Codeforces, 请稍后重试(404)')
        elif contests == 302:
            await session.send('当前即将进入比赛或正在进行比赛中, 无法查询(302)')
        else:
            await session.end('http code=%d' % contests)
    else:

        msg = "Recent Contests:\n\n"
        await session.send(msg)
        for contest in contests:
            s = "{contestName}\n" \
                "Start Time:{contestTime}\n" \
                "Register Link:{registerLink}\n\n". \
                format(contestName=contest['contestName'],
                       contestTime=contest['contestTime'],
                       registerLink=contest['registerLink'])
            await session.send(s)
