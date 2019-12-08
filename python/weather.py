#encoding utf-8

import pandas as pd
import numpy as np
import time, sys
import yagmail
import requests
from lxml import etree

def send_email(subjects, contents, send_to = 'receiver_email@xx.com'):
    #登录邮箱，设置登录的账号，密码和port等信息
    yag = yagmail.SMTP(user = 'sample@qq.com',password = 'xxx', host = 'smtp.qq.com', port = 465)
    yag.send(to = send_to, subject = subjects, contents = contents)
    
    print('发送成功！~')
    # print('subjects: \n' + subjects)
    # print('contents: \n' + contents)

def getContent(city):
    url = 'https://www.tianqi.com/' + city
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    html = requests.get(url,headers = headers)
    bs = etree.HTML(html.text)

    # 城市中文名
    city_name = bs.xpath("//dd[@class='name']//h2/text()")[0]

    # 空气质量、PM
    weather_quality = bs.xpath("//dd[@class='kongqi']//h5/text()")[0]
    weather_pm = bs.xpath("//dd[@class='kongqi']//h6/text()")[0]
    
    #今天天气相关数据：日期，星期几，天气，最低气温，最高气温
    today_date = bs.xpath('//ul[@class = "week"]/li[1]/b/text()')[0]
    today_week = bs.xpath('//ul[@class = "week"]/li[1]/span/text()')[0]
    today_weather = bs.xpath('//ul[@class = "txt txt2"]/li[1]/text()')[0]
    today_low = bs.xpath('//div[@class = "zxt_shuju"]/ul/li[1]/b/text()')[0]
    today_high = bs.xpath('//div[@class = "zxt_shuju"]/ul/li[1]/span/text()')[0]

    #明天天气相关数据
    tomorrow_date = bs.xpath('//ul[@class = "week"]/li[2]/b/text()')[0]
    tomorrow_week = bs.xpath('//ul[@class = "week"]/li[2]/span/text()')[0]
    tomorrow_weather = bs.xpath('//ul[@class = "txt txt2"]/li[2]/text()')[0]
    tomorrow_low = bs.xpath('//div[@class = "zxt_shuju"]/ul/li[2]/b/text()')[0]
    tomorrow_high = bs.xpath('//div[@class = "zxt_shuju"]/ul/li[2]/span/text()')[0]

    today_weather = ('今天是%s,%s,%s,%s至%s度,温差%d度,%s,%s')% \
          (today_date,today_week,today_weather,today_low,today_high,int(int(today_high)-int(today_low)),weather_quality,weather_pm)

    tomorrow_weater = ('明天是%s,%s,%s,%s至%s度,温差%d度')% \
          (tomorrow_date,tomorrow_week,tomorrow_weather,tomorrow_low,tomorrow_high,int(int(tomorrow_high)-int(tomorrow_low)))

    #计算今明两天温度差异，这里用的是最高温度
    temperature_distance = int(tomorrow_high) - int(today_high)
    
    if temperature_distance > 0:
        tomorrow_distance = '明日升温%d度' % temperature_distance
    elif temperature_distance < 0:
        tomorrow_distance = '明日降温%d度' % temperature_distance
    else:
        tomorrow_distance = '今明最高气温不变'

    return city_name, today_weather + '\n\n' + tomorrow_weater + '\n\n' + tomorrow_distance

if __name__ == '__main__':
    city = sys.argv[1]
    now = int(time.time()) 
    nowDate = time.strftime("%Y-%m-%d", time.localtime(now)) 

    city_name, message = getContent(city)

    subject = '[{}]{}天气预报'.format(nowDate, city_name)

    send_email(subject, message, send_to = sys.argv[2])
