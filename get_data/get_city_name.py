import json
import time
import requests
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




if __name__ == '__main__':
    city = get_city_name()
    with open("database_info.json", 'r', encoding='utf-8') as f:
        database_info = json.load(f)
    database = mysql_connection(database_info['host'], database_info['user'], database_info['password'],
                                database_info['database'])

    database.clear_table("province")
    province = [(item[0], item[1]) for item in city]
    database.insert_many("province", ("province_name", "province_ID"), province)

    database.clear_table("city")
    city_data = list()
    for province_name, province_ID, province_city in city:
        for item in province_city:
            city_data.append((item[1], item[0], province_ID))

    database.insert_many("city", ("city_ID", "city_name", "province_ID"), city_data)


