from . import codeforces, nowcoder, atcoder


async def get_contest(contest_type: str) -> list:
    """
    获取各个平台的比赛

    目前支持的平台:
    codeforces
    atcoder
    nowcoder

    :param contest_type:
    :return:
    """
    if contest_type == 'cf':
        return await codeforces.get_contests()
    elif contest_type == 'at':
        return await atcoder.get_contests()
    elif contest_type == 'nk':
        return await nowcoder.get_contests()
    elif contest_type == '':
        s = []
        s.extend(await codeforces.get_contests())
        s.extend(await atcoder.get_contests())
        s.extend(await nowcoder.get_contests())
        return s

    return []
