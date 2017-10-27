# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class DzdpQzPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host='192.168.3.232', port=3306, user='zwj', passwd='123456', db='caiji',
                               charset='utf8')
        cursor = conn.cursor()

        sql = "insert into DZDP_QZ(NAME,ADDR,PHONE,FDCOUNT,COMCOU,CJMC,CITY,HREF) values('%s','%s','%s','%s','%s','%s','%s','%s')" \
              % (
              item['name'], item['addr'], item['phone'], item['fdcount'], item['comcou'],
              item['cjmc'], item['city'], item['href'])
        print(sql)
        cursor.execute(sql)
        conn.commit()
        return item
