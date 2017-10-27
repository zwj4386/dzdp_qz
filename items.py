# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DzdpQzItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    addr = scrapy.Field()
    phone = scrapy.Field()
    fdcount = scrapy.Field()#分店数量
    comcou = scrapy.Field() #评论数
    cjmc = scrapy.Field()
    city = scrapy.Field()
    href = scrapy.Field()
    pass
