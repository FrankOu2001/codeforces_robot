import codeforces
import nowcoder
import atcoder


async def get_contest(contest_type: str = "all") -> list:
    contest = []
    if contest_type == 'all':
        await codeforces.get_contests(contest)
        await nowcoder.get_contests(contest)
        await atcoder.get_contests(contest)
    elif str == 'cf':
        await codeforces.get_contests(contest)
    elif str == 'nk':
        await nowcoder.get_contests(contest)
    elif str == 'at':
        await atcoder.get_contests(contest)

    return contest
