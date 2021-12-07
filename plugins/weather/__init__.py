import sys
import httpx
from nonebot import on_command, CommandSession
from plugins import time

__plugin_name = 'weather'
__plugin_usage = '拉取中国各地(市/区(县))天气'

__key = '7a32b1049b374cb39269f7529f506366'


async def getRequest(url):
    try:
        request = httpx.get(url, timeout=3)
        get = request.json()
        print(request)
        return get
    except httpx.HTTPError as e:
        print(e, file=sys.stderr)


async def getWeather(location):
    global __key
    weather_url = 'https://devapi.qweather.com/v7/weather/now?key={}&location={}'.format(__key, location)
    get = await getRequest(weather_url)
    return get['now']


async def getLocation(city):
    global __key
    location_url = 'https://geoapi.qweather.com/v2/city/lookup?key={}&location={}&range=cn'.format(__key, city)
    get = await getRequest(location_url)
    if get['code'] == '200':
        return get['location']
    else:
        return False


@on_command('weather', aliases=['天气', 'weather_info'])
async def Weather(session: CommandSession):
    city = session.current_arg_text.strip()
    if city == '兔头':
        await session.send('兔头已被光明伟大正义聪慧的我，bot，夺舍了desu！')
        return
    if city == '乃琳' or city == '珈乐' or city == '嘉然' or city == '向晚' or city == '贝拉':
        city = '枝江'
    if not city:
        await session.send('请输入地区名称！')
        return
    city = await getLocation(city)
    if type(city) == bool:
        await session.send('请检查地区名称是否正确！')
    else:
        message = """查询时间: {}
""".format(await time.get_current_time())
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
#             city_id = i['id']
#             weather = await getWeather(city_id)
#             message += text.format(i['name'], weather['temp'],
#                                    weather['humidity'], weather['vis'],
#                                    weather['windDir'], weather['windScale'])
        print(message)
        await session.send(message)
