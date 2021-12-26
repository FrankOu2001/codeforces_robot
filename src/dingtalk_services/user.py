import httpx

from nonebot import logger
from . import get_access_token


async def get_users() -> list[str: str]:
    """
    获取用户的name和userid
    :return: ([用户信息], {userid: 姓名})
    """

    access_token = await get_access_token()
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

        # 第0个用户是鹿老师，没必要获取
        id_to_name = {x['userid']: x['name'] for x in users[1::]}

        # id_to_name 是通过user_id来获得名字
        logger.success('Successfully get {} users'.format(len(users)))
        return users, id_to_name

    except httpx.HTTPError as e:
        logger.error('获取用户name和id时出现错误', e)
