import json
import time
import requests
from datetime import datetime, timedelta
from collections import Counter
import statistics
from logging import info, warning, error
from lxml import html
from mysql_tools.mysqlDatabase import mysql_connection


def get_city_name():
    city_code_tree = html.fromstring("""
          <li data-value="ABJ">北京市</li>
          <li data-value="ATJ">天津市</li>
          <li data-value="AHE">河北省</li>
          <li data-value="ASX">山西省</li>
          <li data-value="ANM">内蒙古自治区</li>
          <li data-value="ALN">辽宁省</li>
          <li data-value="AJL">吉林省</li>
          <li data-value="AHL">黑龙江省</li>
          <li data-value="ASH">上海市</li>
          <li data-value="AJS">江苏省</li>
          <li data-value="AZJ">浙江省</li>
          <li data-value="AAH">安徽省</li>
          <li data-value="AFJ">福建省</li>
          <li data-value="AJX">江西省</li>
          <li data-value="ASD">山东省</li>
          <li data-value="AHA">河南省</li>
          <li data-value="AHB">湖北省</li>
          <li data-value="AHN">湖南省</li>
          <li data-value="AGD">广东省</li>
          <li data-value="AGX">广西壮族自治区</li>
          <li data-value="AHI">海南省</li>
          <li data-value="ACQ">重庆市</li>
          <li data-value="ASC">四川省</li>
          <li data-value="AGZ">贵州省</li>
          <li data-value="AYN">云南省</li>
          <li data-value="AXZ">西藏自治区</li>
          <li data-value="ASN">陕西省</li>
          <li data-value="AGS">甘肃省</li>
          <li data-value="AQH">青海省</li>
          <li data-value="ANX">宁夏回族自治区</li>
          <li data-value="AXJ">新疆维吾尔自治区</li>
          <li data-value="AXG">香港特别行政区</li>
          <li data-value="AAM">澳门特别行政区</li>
          <li data-value="ATW">台湾省</li>
    """)

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
    }
    city = list()
    for city_name, city_code in zip(city_code_tree.xpath('li/text()'), city_code_tree.xpath('li/@data-value')):
        url = f'https://weather.cma.cn/api/dict/province/{city_code}'
        response = requests.get(url, headers=headers)
        data = [item.split(',')[::-1] for item in response.json()['data'].split('|')]
        city.append([city_name, city_code, data])

        print(city_name, city_code, data)
        time.sleep(0.5)

    print(city)

    return city


def git_html_tree(url: str):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    return html.fromstring(response.text)


def get_city_weather(city_code: str):
    url = f'https://weather.cma.cn/web/weather/{city_code}.html'
    tree = git_html_tree(url)
    # get date
    date = datetime.today().date()
    # get weather data
    data = tree.xpath(
        '/html/body/div[1]/div[2]/div[1]/div[1]/div[3]/table/tbody/tr[position() >= 3]/td[position() >= 2]/text()')

    # Group by weather type
    data_each_type = [data[i: i + 8] for i in range(0, len(data), 8)]
    # Group by date
    data_each_day = list()
    d = 0
    for i in range(0, len(data_each_type), 7):
        data_each_day.append([city_code, date + timedelta(days=d), *data_each_type[i: i + 7]])
        d = d + 1

    for item in data_each_day:
        for i in range(2, len(item)):
            if i == 2:
                for j in range(0, len(item[i])):
                    item[i][j] = float(item[i][j][0:-1])
            if i == 3:
                for j in range(0, len(item[i])):
                    if item[i][j] == '无降水':
                        item[i][j] = 0
                    else:
                        item[i][j] = float(item[i][j][0:-2])
            if i == 4 or i == 6:
                for j in range(0, len(item[i])):
                    item[i][j] = float(item[i][j][0:-3])
            if i == 7 or i == 8:
                for j in range(0, len(item[i])):
                    item[i][j] = float(item[i][j][0:-1])/100

    return data_each_day


def update_province_and_city_name(host, user, password, database):
    city = get_city_name()

    database = mysql_connection(host, user, password, database)

    database.clear_table("province")
    province = [(item[0], item[1]) for item in city]
    database.insert_many("province", ("province_name", "province_ID"), province)

    database.clear_table("city")
    city_data = list()
    for province_name, province_ID, province_city in city:
        for item in province_city:
            city_data.append((item[1], item[0], province_ID))

    database.insert_many("city", ("city_ID", "city_name", "province_ID"), city_data)



def update_weather(host, user, password, database):
    database = mysql_connection(host, user, password, database)
    city_ID = database.sql("select city_ID from weather_sys.city")

    # 测试
    # city_ID = city_ID[0:10]

    weather_data = list()

    for city_id in city_ID:
        weather = get_city_weather(city_id[0])

        for item_day in weather:
            # temperature
            item_day[2] = statistics.mean(item_day[2])
            # precipitation
            item_day[3] = statistics.mean(item_day[3])
            # wind spend
            item_day[4] = statistics.mean(item_day[4])
            # wind direction
            item_day[5] = Counter(item_day[5]).most_common(1)[0][0]
            # air pressure
            item_day[6] = statistics.mean(item_day[6])
            # humidity
            item_day[7] = statistics.mean(item_day[7])
            # cloud cover
            item_day[8] = statistics.mean(item_day[8])
            weather_data.append(tuple(item_day))

        # time.sleep(0.5)

        info(f"get city {database.sql(f'select city_name from {database}.city where city_ID = %s', city_id)} weather")

    database.clear_table("weather_data")
    database.insert_many("weather_data", ("city_ID", "date", "temperature", "precipitation", "wind_speed", "wind_direction", "air_pressure", "humidity", "cloud_cover"), weather_data)

    return weather_data

if __name__ == '__main__':
    with open("database_info.json", 'r', encoding='utf-8') as f:
        database_info = json.load(f)

    # update_province_and_city_name(database_info['host'], database_info['user'], database_info['password'], database_info['database'])

    # get_city_weather("54774")

    update_weather(database_info['host'], database_info['user'], database_info['password'], database_info['database'])
