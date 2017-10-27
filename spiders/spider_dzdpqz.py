# coding=utf-8
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import sys
import os
from dzdp_qz.items import DzdpQzItem
import pymysql
reload(sys)
sys.setdefaultencoding('utf-8')

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class spider_dzdp(scrapy.Spider):
    name = 'dzdp_qz'#亲子栏目
    start_urls = ['http://www.dianping.com/search/category/110/70/g193']
    allowed_domain = 'www.dianping.com'

    conn = pymysql.connect(host='192.168.3.232', port=3306, user='zwj', passwd='123456', db='caiji',
                           charset='utf8')
    cursor = conn.cursor()

    def parse(self, response):
        #从选项栏获取单个种类的src yield Request一个50页的列表 再请求进一个子网页拿数据
        #到韩国料理 。。。
        sql_sel = 'select cityName,cityNum from CITY_AH'
        self.cursor.execute(sql_sel)
        rs = self.cursor.fetchall()
        for n in range(0,len(rs)):
            cityName = rs[n][0]
            cityNum = rs[n][1]
            urls = [
                'http://www.dianping.com/search/category/'+cityNum+'/70/g193',
                'http://www.dianping.com/search/category/'+cityNum+'/70/g188',
                'http://www.dianping.com/search/category/'+cityNum+'/70/g258',
                'http://www.dianping.com/search/category/'+cityNum+'/70/g161',
                'http://www.dianping.com/search/category/'+cityNum+'/70/g27769'
            ]
            for i in urls:
                yield Request(i, meta={'cityName':cityName}, callback=self.getDetailUrl)


    def getDetailUrl(self,response):
        xp = Selector(response)
        cityName = response.meta['cityName']
        div = xp.xpath('//ul[@class="shop-list"]/li/a/@href').extract()
        for j in div:
            i = 'http://www.dianping.com'+j
            sql = 'select 1 from DZDP_QZ where HREF="%s"'%i #数据库查重
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
            if len(rs)==0:
                yield Request(i, meta={'href':i,'cityName':cityName},callback=self.getItem)
            else:
                continue

        next = xp.xpath('//a[@class="NextPage"]/@href').extract()
        if len(next)!=0:
            next_url='http://www.dianping.com'+''.join(next)
            yield Request(next_url, meta={'href': next_url,'cityName':cityName},callback=self.getDetailUrl)

    def getItem(self,response):
        item = DzdpQzItem()
        hx = Selector(response)
        href = response.meta['href']
        cityName = response.meta['cityName']
        name = ''.join(hx.xpath("//h1[@class='shop-title']/text()").extract()).encode('utf-8').replace('\n','').strip()
        isfendian = hx.xpath('//div[@class="add-subbranch"]/a[@class="more"]')
        if len(isfendian)<>0:
            fdcount = ''.join(hx.xpath('//div[@class="add-subbranch"]/a[@class="more"]/text()').extract())\
                .encode('utf-8').replace('查看全部','').strip()
        else:
            fdcount = ''
        comcou = ''.join(hx.xpath('//div[@class="rst-taste"]/a/span/text()').extract())
        if len(comcou)==0:
            comcou = ''.join(hx.xpath('//div[@class="comment-rst"]/a/span/text()').extract())
        else:
            comcou=""
        addr = ''.join(hx.xpath('//div[@class="shop-addr"]/span/text()').extract()).encode('utf-8').replace('\n','').strip()
        if len(addr)==0:
            addr=''.join(hx.xpath('//span[@itemprop="street-address"]/text()').extract()).strip()
        else:
            addr =''
        phone = ''.join(hx.xpath('//div[@class="shopinfor"]/p/span[1]/text()').extract())
        if len(phone)==0:
            phone = ''.join(hx.xpath('//dd[@class="shop-info-content"]/a/@data-real').extract())
        else:
            phone=''
        cjmc = '亲子'
        city = cityName
        item['name'] = name
        item['fdcount'] = fdcount
        item['comcou'] = comcou
        item['addr'] = addr
        item['phone'] = phone
        item['cjmc'] = cjmc
        item['city'] = city
        item['href'] = href

        if item['name']<>'' and item['name']<>None:
            yield item
        else:
            pass



