import httpx
from nonebot import logger
from . import get_access_token
from .user import get_users


async def get_absence(query_time) -> list[tuple]:
    """
    获取出勤情况
    由于当前集训队只有一个出勤组，所以只需要查询一个组的出勤情况即可
    目前设定的考勤时间为18:00-19:00

    判定方法:
    time_result 和 location_result都不为NotSigned的人为正常出勤的人，
    除此之外的都是缺勤的人
    :param 查询的时间
    :return: 每个缺勤用户的name, user_id
    """

    access_token = await get_access_token()

    req_url = 'https://oapi.dingtalk.com/attendance/list?access_token=' + access_token
    users_info, id_to_name = await get_users()
    today = query_time.strftime('%Y-%m-%d')

    attendance = set()

    for i in range(0, len(users_info), 50):
        req_body = {
            "workDateFrom": "%s 18:00:00" % today,
            "offset": 0,
            "userIdList": [x['userid'] for x in users_info[i:i + 50:]],
            "limit": 50,
            "isI18n": False,
            "workDateTo": "%s 19:00:00" % today
        }
        req_result = httpx.post(url=req_url, json=req_body).json()

        for x in req_result["recordresult"]:
            if x['checkType'] == 'OffDuty':
                continue
            userid = x['userId']
            time_result = x['timeResult']
            location_result = x['locationResult']
            if time_result != 'NotSigned' and location_result != 'NotSigned':
                attendance.add(userid)

    absence = [(x['name'], x['userid']) for x in users_info
               if x['userid'] not in attendance]
    logger.warning('{} people are absent'.format(len(absence)))

    return absence
