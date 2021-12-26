import httpx
import time

from datetime import datetime
from nonebot import logger
from . import get_access_token
from .user import get_users


async def get_columns():
    """
    获取考勤报表列定义
    :return:
    """

    url = f'https://oapi.dingtalk.com/topapi/attendance/getattcolumns?access_token={get_access_token()}'
    res = []

    try:
        res = httpx.get(url)

    except httpx.HTTPError as e:
        logger.error(e)

    return res['result']['columns']


async def get_report(date_range: tuple[datetime, datetime]) -> list[(str, int, int)]:
    """
    获取集训队所有成员的出勤次数和旷工次数
    结果按照旷工次数从大到小返回
    :param date_range: 查询的时间范围
    :return: (姓名, 旷工次数, 出勤天数)
    """
    url = f'https://oapi.dingtalk.com/topapi/attendance/getcolumnval?access_token={await get_access_token()}'

    # 这两个值是可以通过调用API查询的，上面的函数就可以获取
    absence_id = "335106609"
    attendance_id = "335106597"
    users = (await get_users())[-1].items()
    from_date, to_date = map(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'),
                             date_range)

    result = []
    for user_id, name in users:
        post = {
            "column_id_list": f"{absence_id}, {attendance_id}",
            "from_date": from_date,
            "to_date": to_date,
            "userid": user_id
        }

        post_get = httpx.post(url, json=post).json()
        s = post_get['result']['column_vals']

        absence_count = sum([eval(x['value']) for x in s[0]['column_vals']])
        attendance_count = sum([eval(x['value']) for x in s[1]['column_vals']])
        result.append((name, absence_count, attendance_count))
        pass

    result.sort(key=lambda x: (-x[1], x[2]))
    return result
