from .database import pull_data


async def get_contest(contest_type: str) -> list:
    if contest_type == 'cf':
        return await pull_data('codeforces')
    elif contest_type == 'at':
        return await pull_data('atcoder')
    elif contest_type == 'nk':
        return await pull_data('nowcoder')
    elif contest_type == '':
        return await pull_data('')

    return []
