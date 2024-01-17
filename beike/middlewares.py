# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from fake_useragent import UserAgent

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class BeikeSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BeikeDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.cookie_string = "lianjia_uuid=eaed024b-2396-42d0-b4df-f8c5581258521; crosSdkDT2019DeviceId=-rpj3ax--ics2qa-notqb90fgkbyhmf-kwcuhkzxf; ftkrc_=753fd0e2-9693-407f-a45b-cd3a4093a2bf; lfrc_=a6f40f23-e845-4542-86c8-073da862c2a7; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218d02254e59581-0e2d039f0e42db-26031051-2073600-18d02254e5a649%22%2C%22%24device_id%22%3A%2218d02254e59581-0e2d039f0e42db-26031051-2073600-18d02254e5a649%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyshanghai%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; select_city=310000; lianjia_ssid=4b9ebd6b-9099-431a-807c-784cc2995320; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1705138016,1705284296,1705455204; login_ucid=2000000285030762; lianjia_token=2.0012288da77bb4d9210385a4969a77a0a0; lianjia_token_secure=2.0012288da77bb4d9210385a4969a77a0a0; security_ticket=hbRCAwpVvSfzzC5sv1/1rfrJHtI7HGgyI6qysJuKdp2zeLSQfejUmQ0jbHvNe2W9IT0MoO56N0dJ9djfPYeY74RG6V/UbtphH6QSvTknZAevcYk6/JpGDZD31PjL8nR21UvOmxj15hOiX5GMHEEk+FFNcomElt0h0VXRKnoHyzI=; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1705456389; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiZjM4MjMzODZjNmY0ZTQ4ZWQxZDUyYzhmMjNmYzA5M2YxMTNlNzZjMzYwN2Y3Y2FiZmViYTgxNWQxMmY5YmU1ZDNlMzQ2ZGI0NTliZGQ2MmZkYzI3ZWIyODI1M2Y1NjU4OWYxYjE1Mzg5MzY3NThiZTAyODU5NTFiODhiNjJhZDFhMjAwNTgxYTFkODY1MjZhZDBhNjkzZWM0ZTI2MDBmOTUwNWM4MDhlM2NmMjFiMGQxMmIzZWJjNzU1MTM3ZWI2OGY2ODQ5NTAzNTg3MGVhMmNjYTUyOWZkYTEzMWI4ZTBlY2IzNzgyNThjODlkNGM3ZGY4ZGNiZjAzMTZjMWFmMlwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI1NDk0MWU1MlwifSIsInIiOiJodHRwczovL3NoLmtlLmNvbS9jaGVuZ2ppYW8vcnMlRTYlOTklQUUlRTklOTklODAvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0"
        self.referer = "https://sh.ke.com/chengjiao/"

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        cookie_dict = self.get_cookie()
        request.cookies = cookie_dict
        request.headers['User-Agent'] = UserAgent().random,
        request.headers["referer"] = self.referer
        return None

    def get_cookie(self):
        cookie_dict = {}
        for kv in self.cookie_string.split(";"):
            k = kv.split('=')[0]
            v = kv.split('=')[1]
            cookie_dict[k] = v
        return cookie_dict

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
