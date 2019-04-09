# -*- coding:utf-8 _*-  
""" 
@author: ronething 
@time: 2019-04-09 01:58
@mail: axingfly@gmail.com

Less is more.
"""

import requests
import json
import re
import pymysql

from utils import get_value


class PetSpider(object):
    headers = {
        "Referer": "http://www.yc.cn/api/searchPetData.do?petRaceId=1&pageNum=1&pageSize=8&keyword=&baseInfo=&detailInfo=&jsonCallback=jQuery11130879826298049732_1554727081494&_=1554727081497",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    }

    def scrape_pet_introduction(self, page=1):
        """抓取数据"""
        url = "http://www.yc.cn/api/searchPetData.do?petRaceId=1&pageNum={num}&pageSize=8&keyword=&baseInfo=&detailInfo=&jsonCallback=jQuery11130879826298049732_1554727081494&_=1554727081497".format(
            num=page)
        print(url)
        res = requests.get(url, headers=self.headers)
        return res.text

    def scrape_pet_cat_introduction(self, page=1):
        """抓取数据"""
        url = "http://www.yc.cn/api/searchPetData.do?petRaceId=2&pageNum={num}&pageSize=8&keyword=&baseInfo=&detailInfo=&jsonCallback=jQuery11130879826298049732_1554727081494&_=1554727081497".format(
            num=page)
        print(url)
        res = requests.get(url, headers=self.headers)
        return res.text

    def loads_jsonp(self, jsonp_data):
        """
        解析jsonp数据格式为json
        :return:
        """
        try:
            return json.loads(re.match(".*?({.*}).*", jsonp_data, re.S).group(1))
        except:
            raise ValueError('Invalid Input')

    def get_pet_list(self, data):
        data = self.loads_jsonp(data)
        return data['list']

    def insert_data_to_db(self, data, pet_type='dog'):
        """插入数据库"""
        db = pymysql.connect("localhost", "root", "root", "pet")
        cursor = db.cursor()
        try:
            for tmp in data:
                name = get_value(tmp, 'name')
                base_info = {i['id']: i['value'] for i in get_value(tmp, 'baseData')}
                eng_name = get_value(base_info, '1')
                iq_rank = get_value(base_info, '2')
                location = get_value(base_info, '3')
                weight = get_value(base_info, '4')
                life = get_value(base_info, '5')
                price = get_value(tmp, 'price')
                height = get_value(base_info, '7')
                hair_color = get_value(base_info, '14')
                pet_func = get_value(base_info, '15')
                body_type = get_value(tmp, 'bodyType')
                wool_length = get_value(tmp, 'woolLength')
                alias_name = get_value(tmp, 'alisName')

                feed_info = get_value(tmp, 'feedInfo')
                maintenance_knowledge = get_value(feed_info, '养护知识')
                domesticating_knowledge = get_value(feed_info, '驯养知识')

                base_data = get_value(tmp, 'baseInfo')
                variety_introduction = get_value(base_data, '品种介绍')
                origin_of_development = get_value(base_data, '发展起源')

                breed_info = get_value(tmp, 'breedInfo')
                identification = get_value(breed_info, '形态特征及鉴别')
                life_habit = get_value(breed_info, '生活习性')
                suitable_population = get_value(breed_info, '适养人群')

                banner = get_value(tmp, 'showImage')

                sql = "INSERT INTO `pet_introduction`(name,eng_name,iq_rank,\
                        location,weight,life,price,height,hair_color,pet_func,\
                        body_type,wool_length,alias_name,maintenance_knowledge,\
                        domesticating_knowledge,variety_introduction,origin_of_development,\
                        identification,life_habit,suitable_population,\
                        pet_type,banner) \
                       VALUES ('%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s', '%s','%s', '%s', '%s', '%s')" % \
                      (name, eng_name, iq_rank, location, weight, life, price, height, hair_color, pet_func, body_type,
                       wool_length, alias_name,
                       maintenance_knowledge, domesticating_knowledge, variety_introduction, origin_of_development,
                       identification, life_habit, suitable_population, pet_type, banner)
                cursor.execute(sql)
            db.commit()
            print('success')
        except Exception as e:
            print(e)
            db.rollback()
        finally:
            db.close()


if __name__ == '__main__':
    pet = PetSpider()
    # dog
    for i in range(1, 20):
        data = pet.scrape_pet_introduction(page=i)
        json_list = pet.get_pet_list(data)
        pet.insert_data_to_db(json_list)
    # cat
    for i in range(1, 20):
        data = pet.scrape_pet_cat_introduction(page=i)
        json_list = pet.get_pet_list(data)
        pet.insert_data_to_db(json_list, pet_type='cat')
