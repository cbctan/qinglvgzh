from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
# 获取当前时间
today = datetime.now()
# 获取变量设置的值
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

# 获取天气,【墨迹天气】
def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']),weather['wind']

# 计算开始到现在天数
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

# 生日倒计时
def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days


# 获取彩虹屁语句
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

# 返回随机颜色
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

# 微信公众号APPID和秘钥
client = WeChatClient(app_id, app_secret)

# 微信公众号消息
wm = WeChatMessage(client)
# 变量赋天气返回数据值 wea天气晴 temperature温度 wind风向
wea, temperature, wind = get_weather()
# 公众号设置返回消息
data = {"humidity":{"value":city},"wind":{"value":wind},"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
# 返回消息
res = wm.send_template(user_id, template_id, data)
# 打印消息
print(res)
