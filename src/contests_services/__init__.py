import src.contests_services.nowcoder
import src.contests_services.atcoder
import src.contests_services.codeforces


async def get_contest(contest_type: str = "") -> list:
    contest = []
    if contest_type == '':
        await codeforces.get_contests(contest)
        await nowcoder.get_contests(contest)
        await atcoder.get_contests(contest)
    elif contest_type == 'cf':
        await codeforces.get_contests(contest)
    elif contest_type == 'nk':
        await nowcoder.get_contests(contest)
    elif contest_type == 'at':
        await atcoder.get_contests(contest)

    return contest
