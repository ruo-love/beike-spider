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
        self.cookie_string = ("SECKEY_ABVK=4MCefpI6M30a+UHh30UkIydeer1R6QeipHnez6Brp5Q%3D; BMAP_SECKEY=Oq7s6km5-pvlt7ERPplUt4jjp56oWecueo7-zU1mkzspZyI097QUnJspoko0394xh4eSeXipDo-vbFQ991huQE_anUGdpVlZVDfg9xlkKIRZzcvxkO2IueMVbJuNciHzJTakqgXjBzSz82wgPyu33pMRKOHKNCjVMCj0TXGkMxeLmlUG1JskOKKjjB2qsoo6; lianjia_uuid=eaed024b-2396-42d0-b4df-f8c558125852; crosSdkDT2019DeviceId=-rpj3ax--ics2qa-notqb90fgkbyhmf-kwcuhkzxf; ftkrc_=753fd0e2-9693-407f-a45b-cd3a4093a2bf; lfrc_=a6f40f23-e845-4542-86c8-073da862c2a7; _ga=GA1.2.1736741741.1711070582; __xsptplus788=788.1.1711070625.1711070625.1%234%7C%7C%7C%7C%7C%23%23%23; hy_data_2020_id=18e9840bb2fc3-0868c242d52f15-26001a51-2073600-18e9840bb30a0b; hy_data_2020_js_sdk=%7B%22distinct_id%22%3A%2218e9840bb2fc3-0868c242d52f15-26001a51-2073600-18e9840bb30a0b%22%2C%22site_id%22%3A341%2C%22user_company%22%3A236%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%2218e9840bb2fc3-0868c242d52f15-26001a51-2073600-18e9840bb30a0b%22%7D; select_city=310000; lianjia_ssid=b7c023a2-da3e-4d45-92ac-59c167b1ca8c; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1711950835,1711952427,1711954247,1713160340; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218d02254e59581-0e2d039f0e42db-26031051-2073600-18d02254e5a649%22%2C%22%24device_id%22%3A%2218d02254e59581-0e2d039f0e42db-26031051-2073600-18d02254e5a649%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_referrer_host%22%3A%22www.google.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyshanghai%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; login_ucid=2000000285030762; lianjia_token=2.00121d399b7b816d1d03b010aa3955bd76; lianjia_token_secure=2.00121d399b7b816d1d03b010aa3955bd76; security_ticket=hFHcFQf2bbxOq+5aZHW6GSs7Tm7BS7NKS2gXWchM6WOOtbfTIHgt8jhB8n1C7E7X0ZHfCwVTx/d8c6zLYwON0bSH69FMNaaP5z0CeKbI5NkjRk+qxMrD20yR58vYd8CWwZJ7/uuu5wgzwVB/kr+P1w3v3laFUkQ5DBward/WLvc=; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1713160383; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiZjc3MjNjMjZlMjc1NzBjMzYwOWY0ODIxODc3NzUwNDQxMTEwZGVjZmNkMTk3NjU2OGI1NTJjOTY4MjYyYmIyNDc3NjAwZjljNGJmNzI5NjRjMTIzOWZhMGUxMzFkMGY2NDE2ZjE2Y2I2ZmQ4NmM2MWNkYjE2N2MxZjUzYThkZjkyM2ZlZjM2YzkyNDNjYzEyZGEwY2NjZjczZmE3MDUyODlkNDNhYzQzOWI4ZjU5MzAwNDliMzZmNDc2NTNkNjVhYWI5ZGJmOGU5YjJhNTg3ZDA2MjNlMmY2OTI2ZTUwNDI5ZjZiYzgxYTAwMWY2NTg1OGNmMjFiZmVlMDgyMWNjY1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI4Yzg4YWFlOFwifSIsInIiOiJodHRwczovL3NoLmtlLmNvbS9jaGVuZ2ppYW8vIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=")
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
