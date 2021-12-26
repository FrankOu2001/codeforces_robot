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
            logger.error(err)

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


async def get_access_token():
    global __TOKEN
    if __TOKEN is None:
        __TOKEN = DingTalk_Client()
    return await __TOKEN.get_access_token()
