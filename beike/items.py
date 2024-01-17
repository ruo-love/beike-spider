# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BeikeItem(scrapy.Item):
    # define the fields for your item here like: '名称', '装修朝向', '楼层', '地址', '成交历史', '单价', '时间'
    fileName = scrapy.Field()  # 文件名
    title = scrapy.Field()  # '名称'
    decorate = scrapy.Field()  # '装修朝向'
    floor = scrapy.Field()  # '楼层'
    address = scrapy.Field()  # 地址'
    history = scrapy.Field()  # '成交历史'
    price = scrapy.Field()  # '单价'
    time = scrapy.Field()  # '时间'
    transaction_price = scrapy.Field()  # '成交价格’
    msg = scrapy.Field()  # 'msg’
    pass
