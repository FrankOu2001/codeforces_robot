import sys
import httpx
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from plugins import time

__plugin_name__ = 'weather'
__plugin_usage__ = '拉取中国各地(市/区(县))天气'

__key__ = '7a32b1049b374cb39269f7529f506366'


async def getRequest(url):
    try:
        request = httpx.get(url, timeout=3)
        get = request.json()
        return get
    except httpx.HTTPError as e:
        print(e, file=sys.stderr)


async def getWeather(location):
    global __key__
    weather_url = 'https://devapi.qweather.com/v7/weather/now?key={}&location={}'.format(__key__, location)
    get = await getRequest(weather_url)
    return get['now']


async def getLocation(city):
    global __key__
    location_url = 'https://geoapi.qweather.com/v2/city/lookup?key={}&location={}&range=cn'.format(__key__, city)
    get = await getRequest(location_url)
    if get['code'] == '200':
        return get['location']
    else:
        return False


session = on_command("天气", rule=to_me(), priority=3)


@session.handle()
async def Weather(bot: Bot, event: Event, state: T_State):
    city = str(event.get_message()).strip()
    if city == '兔头':
        await session.send('兔头已被光明伟大正义聪慧的我，bot，夺舍了desu！')
    elif city in ('乃琳', '珈乐', '嘉然', '向晚', '贝拉'):
        city = '枝江'

    if not city:
        await session.reject('请输入地区名称！')

    city = await getLocation(city)
    if type(city) == bool:
        await session.reject('请检查地区名称是否正确后重新输入！')
    else:
        message = "查询时间 %s" % await time.get_current_time()
        #         for i in city:
        text = """名称: {}
实时气温: {}℃
相对湿度: {}%
能见度: {}km
风向风力：{} {}级"""
        city_id = city[0]['id']
        weather = await getWeather(city_id)
        message += text.format(city[0]['name'], weather['temp'],
                               weather['humidity'], weather['vis'],
                               weather['windDir'], weather['windScale'])
        await session.finish(message)
