# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
# Import necessary modules
from datetime import datetime

from openpyxl import Workbook
from pymongo import MongoClient


class BeikePipeline:
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        settings = crawler.settings

        return cls(*args, **kwargs)

    def __init__(self):
        self.fileName = ''
        self.client = MongoClient('127.0.0.1', 27017)
        self.beike_db = self.client['beike']
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = '贝壳网'
        self.ws.append(['名称', '装修朝向', '楼层', '地址', '成交历史', '单价', '时间', '成交价格', '其他信息'])

    def process_item(self, item, spider):
        try:
            # 使用字典推导式简化数据提取
            item_data = {key: item.get(key, '') for key in
                         ['title', 'decorate', 'floor', 'address', 'history', 'price', 'time', 'transaction_price',
                          'msg']}
            # Excel 插入
            self.ws.append(list(item_data.values()))
            self.fileName = item['fileName']
            # MongoDB 插入
            # col = self.beike_db['chengjiao']
            # col.insert_one(item_data)
        except Exception as e:
            spider.logger.error(f"Error processing item: {e}")

        return item

    def close_spider(self, spider):
        now = datetime.now()
        self.client.close()
        formatted_now = now.strftime("%Y年%m月%d日 %H时%M分%S秒 ")
        # Save and close the workbook
        self.wb.save(formatted_now + self.ws.title + self.fileName + '成交数据.xlsx')
        self.wb.close()
