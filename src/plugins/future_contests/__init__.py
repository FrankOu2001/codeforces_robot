from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from src.contests_services import get_contest

session = on_command("contests", rule=to_me(), priority=2)


@session.handle()
async def get_future_contests(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip().lower()

    if args == '':
        await send('cf', bot, event)
        await send('at', bot, event)
        await send('nk', bot, event)
    else:
        if args in ['cf', 'codeforces']:
            await send('cf', bot, event)
        elif args in ['atcoder', 'at', 'atc']:
            await send('at', bot, event)
        elif args in ['牛客', 'nowcoder', 'nk', 'nc', '牛客竞赛']:
            await send('nk', bot, event)
        else:
            await send(args, bot, event)


async def send(args: str, bot: Bot, event: Event):
    contest = await get_contest(args)
    if len(contest) == 0:
        await session.finish(f'无法获取比赛{args}')
    else:
        msg = ''
        for x in contest:
            name = x['name']
            link = x['link']
            begin, end = x['contest_time']
            msg += f"{name}\n" \
                   f"Link: {link}\n" \
                   f"Time: {begin} - {end}\n\n"
        msg = msg.strip('\n')

        await session.send(msg)
