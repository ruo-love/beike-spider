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
        self.cookie_string = "lianjia_uuid=eaed024b-2396-42d0-b4df-f8c558125852; crosSdkDT2019DeviceId=-rpj3ax--ics2qa-notqb90fgkbyhmf-kwcuhkzxf; ftkrc_=753fd0e2-9693-407f-a45b-cd3a4093a2bf; lfrc_=a6f40f23-e845-4542-86c8-073da862c2a7; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218d02254e59581-0e2d039f0e42db-26031051-2073600-18d02254e5a649%22%2C%22%24device_id%22%3A%2218d02254e59581-0e2d039f0e42db-26031051-2073600-18d02254e5a649%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_referrer_host%22%3A%22www.google.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyshanghai%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; select_city=310000; lianjia_ssid=dfab3e6b-9a5e-4f89-9aa0-9db63abbe8aa; login_ucid=2000000285030762; lianjia_token=2.00134e0c8c7ad2580a02e325bd9906ceff; lianjia_token_secure=2.00134e0c8c7ad2580a02e325bd9906ceff; security_ticket=lmvGTgT0l3N8tvC4yTAYwt8D+US/8xrBIcH3WZc+dW9puOvbXzfGH4RV1pXWgZ4aUOZpelnp3perqVeyIxP/Tk7D41T/er/e+n03nZQTRW8wlLR5tGUfe8AZcwmco789xXP3Y5D0sTcCyRFTGX/sTEAQwt3dOd3j60IBxIEW9ps=; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1711068831; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1711069185; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiZjc3MjNjMjZlMjc1NzBjMzYwOWY0ODIxODc3NzUwNDQxMTEwZGVjZmNkMTk3NjU2OGI1NTJjOTY4MjYyYmIyNDc3NjAwZjljNGJmNzI5NjRjMTIzOWZhMGUxMzFkMGY2NDE2ZjE2Y2I2ZmQ4NmM2MWNkYjE2N2MxZjUzYThkZjkyM2ZlZjM2YzkyNDNjYzEyZGEwY2NjZjczZmE3MDUyOGY4NzYxNDdlZjdjYTQ4MTFjMzVjOTA4NTRmZmYxNzljMzc3YzUxZDJkZDg4NTEzOTFkYzE3ZTA1ZDJiMTY2NDdjZDcyNGE2M2I1ZjgxYmFmOWEwMjMxMzI4MGIzNDhiNVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIxNzYwOGRiNlwifSIsInIiOiJodHRwczovL3NoLmtlLmNvbS9jaGVuZ2ppYW8vcnMlRTUlOTglODklRTUlQUUlOUElRTYlOTYlQjAlRTUlOUYlOEUvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0="
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
