from . import codeforces, nowcoder, atcoder


async def get_contest(type: str) -> list:
    """
    获取各个平台的比赛

    目前支持的平台:
    codeforces
    atcoder
    nowcoder

    :param type:
    :return:
    """
    if type == 'cf':
        return await codeforces.get_contests()
    elif type == 'at':
        return await atcoder.get_contests()
    elif type == 'nk':
        return await nowcoder.get_contests()

    return []
