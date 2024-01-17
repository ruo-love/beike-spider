# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# Import necessary modules
from openpyxl import Workbook

from datetime import datetime


class BeikePipeline:
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        settings = crawler.settings
        FILE_NAME = settings.get('FILE_NAME')
        return cls(FILE_NAME, *args, **kwargs)

    def __init__(self, FILE_NAME):
        self.FILE_NAME = FILE_NAME
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = self.FILE_NAME
        self.ws.append(['名称', '装修朝向', '楼层', '地址', '成交历史', '单价', '时间', '成交价格', '其他信息'])

    def process_item(self, item, spider):
        title = item.get('title', '')
        decorate = item.get('decorate', '')
        floor = item.get('floor', '')
        address = item.get('address', '')
        history = item.get('history', '')
        price = item.get('price', '')
        time = item.get('time', '')
        transaction_price = item.get('transaction_price', '')
        msg = item.get('msg', '')
        # Append the data as a list
        self.ws.append([title, decorate, floor, address, history, price, time, transaction_price, msg])

        return item

    def close_spider(self, spider):
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d__%H-%M-%S")
        # Save and close the workbook
        self.wb.save(formatted_now+self.ws.title+'.xlsx')
        self.wb.close()
