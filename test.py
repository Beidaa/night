import random
from time import localtime
import sys
import os
from requests import get, post



def get_weather(region):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    # 获取地区的location--id
    location_id = "101230207"
    weather_url = "https://devapi.qweather.com/v7/weather/3d?location={}&key={}".format(location_id, key)
    response = get(weather_url, headers=headers).json()
    # daily.sunset 日落时间
    sunset = response["now"]["sunset"]
    print (sunset)
    # 当前温度
    temp = response["now"]["temp"] + u"\N{DEGREE SIGN}" + "C"
    # 风向
    wind_dir = response["now"]["windDir"]

 