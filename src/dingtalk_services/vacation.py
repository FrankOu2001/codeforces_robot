import time

import httpx
from nonebot import logger
from datetime import datetime, timedelta
from . import get_access_token
from .user import get_users


async def get_vacation(absence: list, query_time) -> list:
    """
    获取缺勤中请假的人群
    :param absence: 缺勤列表
    :param query_time: 查询日期范围
    :return: 缺勤人员中请假的人群
    """

    def unix_time(_time: datetime) -> int:
        return int(time.mktime(_time.timetuple())) * 1000

    accessToken = await get_access_token()

    __ignore, id_to_name = await get_users()
    in_vacation = []

    req_url = 'https://oapi.dingtalk.com/topapi/attendance/getleavestatus?access_token=' + accessToken

    for i in range(0, len(absence), 20):
        absence_list = [x[-1] for x in absence[i:i + 20:]]
        req_post = {
            # 获取查询的时间范围
            "start_time": unix_time(query_time + timedelta(hours=18)),
            "end_time": unix_time(query_time + timedelta(hours=18, minutes=30)),
            "offset": 0,
            "size": 20,
            "userid_list": ','.join([str(x) for x in absence_list])
        }
        try:
            req = httpx.post(url=req_url, json=req_post).json()
            result = req["result"]
            for x in result['leave_status']:
                userid = x['userid']
                in_vacation.append((id_to_name[userid], userid))

        except httpx.HTTPError as e:
            print(e)
    logger.info('There are {} users are in vacation'.format(len(in_vacation)))
    return in_vacation
