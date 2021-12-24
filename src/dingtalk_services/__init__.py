import sys

import httpx
import time
from nonebot import logger
from datetime import datetime, timedelta
from alibabacloud_dingtalk.oauth2_1_0 import models as dingtalk_models
from alibabacloud_dingtalk.oauth2_1_0.client import Client as dingtalkClient
from alibabacloud_tea_openapi import models as open_api_models


class DingTalk_Client:
    __accessToken = str()
    __accessToken_end_time = datetime(1970, 1, 1, 0, 0, 0)

    def __init__(self):
        pass

    @staticmethod
    def __create_client() -> dingtalkClient:
        """
        创建和钉钉API的客户端
        :return: 钉钉API的客户端
        """
        config = open_api_models.Config()
        config.protocol = "https"
        config.region_id = "central"
        return dingtalkClient(config)

    @staticmethod
    async def __get_token() -> dict:
        """
        调用客户端，发送获取accessToken的http post
        :return: 返回获取的包含accessToke的post信息: {accessToken, expireIn(accessToken的过期时间，单位秒)}
        """
        client = DingTalk_Client.__create_client()
        get_access_token_request = dingtalk_models.GetAccessTokenRequest(
            app_key=f'your app_key',
            app_secret=f'you app_secret'
        )
        try:
            request = await client.get_access_token_async(get_access_token_request)
            return request.to_map()['body']
        except Exception as err:
            print(err, file=sys.stderr)

    async def get_access_token(self) -> str:
        """
        获取accessToken

        注意：
        accessToken的有效期为7200秒（2小时），
        有效期内重复获取会返回相同结果并自动续期，
        过期后获取会返回新的accessToken。
        :return: accessToken
        """
        if self.__accessToken_end_time < datetime.now():
            req = await self.__get_token()
            self.__accessToken = req["accessToken"]

        # 这里为了减少网络延迟造成的影响，将7200s的有效期缩短为7100s
        self.__accessToken_end_time = datetime.now() + timedelta(seconds=7100)
        logger.success('Get AccessToken from DingTalk Client Successfully at %s' % datetime.now())

        return self.__accessToken


__TOKEN = DingTalk_Client()


async def get_users() -> list[str: str]:
    """
    获取用户的name和userid
    :return:
    """
    global __TOKEN

    access_token = await __TOKEN.get_access_token()
    users = []

    cursor = 0
    req_url = "https://oapi.dingtalk.com/topapi/user/listsimple?access_token=" + access_token
    req_body = {
        "dept_id": 1,  # 由于集训队没有下属部门，所以采用默认的根部门(id=1)
        "cursor": cursor,
        "size": 100
    }
    try:
        post_get = httpx.post(url=req_url, json=req_body, timeout=3).json()
        result = post_get['result']
        users.extend(result['list'])

        while result['has_more'] is True:
            cursor += 100
            post_get = httpx.post(url=req_url, json=req_body, timeout=3).json()
            result = post_get['result']
            users.extend(result['list'])

        id_to_name = {x['userid']: x['name'] for x in users}

        # 第0个用户是鹿老师，没必要获取
        # id_to_name 是通过user_id来获得名字
        logger.success('Successfully get {} users'.format(len(users)))
        return users[1::], id_to_name

    except httpx.HTTPError as e:
        logger.error('获取用户name和id时出现错误', e)


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

    global __TOKEN
    access_token = await __TOKEN.get_access_token()

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


async def get_vacation(absence: list, query_time) -> list:
    """
    获取缺勤中请假的人群
    :param absence: 缺勤列表
    :param query_time: 查询日期范围
    :return: 缺勤人员中请假的人群
    """
    def unix_time(_time: datetime) -> int:
        return int(time.mktime(_time.timetuple())) * 1000

    global __TOKEN
    accessToken = await __TOKEN.get_access_token()

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
