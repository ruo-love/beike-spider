import scrapy
import re
import math
from tqdm import tqdm
import sys
from beike.items import BeikeItem


## scrapy crawl beike -a area=pudong -a area_label=浦东 -a page_size=100 -a cookie=xxx -a file_name=xxx
class QuotesSpider(scrapy.Spider):
    def __init__(self, area='pudong', area_label='浦东', page_size=100, cookie="", file_name="", *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.area = area
        self.area_label = area_label
        self.page_size = page_size
        self.cookie = cookie
        self.file_name = file_name
    name = "beike"
    allowed_domains = ['bj.ke.com', 'sh.ke.com']
    # start_urls = ['https://sh.ke.com/chengjiao/pg{}']
    start_url = 'https://sh.ke.com/chengjiao/'
    area_urls = []
    plate_map = {}
    v_map = {
        'l1/': '一居',
        'l2/': '二居',
        'l3/': '三居',
        'l4/': '四居',
        'l5/': '五居',
        'l6/': '五居以上'
    }
    c_map = {
        'lc1': '低层',
        'lc2': '中层',
        'lc3': '高层',
    }

    def start_requests(self):
        # yield scrapy.Request(url=self.start_url, callback=self.parse_area)
        yield scrapy.Request(url='https://sh.ke.com/chengjiao/pudong/', callback=self.parse_plate,
                             meta={'area': self.area, 'area_label': self.area_label})

    # 获取区域
    def parse_area(self, response, **kwargs):
        links = response.css('div[data-role="ershoufang"] > div > a')
        for link in tqdm(links, desc='区域链接', unit='links'):
            url = link.xpath('./@href').get()
            label = link.xpath('./text()').get()
            url = 'https://sh.ke.com/' + url
            area = re.search(r'/([^/]+)/?$', url).group(1)
            self.area_urls.append(url)
            self.plate_map[area] = []
            yield scrapy.Request(url=url, callback=self.parse_plate, meta={'area': area, 'area_label': label})

    # 获取板块
    def parse_plate(self, response, **kwargs):
        area = response.meta['area']
        area_label = response.meta['area_label']
        links = response.css('div[data-role="ershoufang"] > div:nth-child(2) > a')
        for link in tqdm(links, desc='板块链接', unit='links'):
            url = link.xpath('./@href').get()
            label = link.xpath('./text()').get()
            plate_label = label
            url = 'https://sh.ke.com/' + url
            ls = ['l1/', 'l2/', 'l3/', 'l4/', 'l5/', 'l6/']  # 分户型爬取
            for v in tqdm(ls, desc='户型链接', unit='links'):
                lc = ['lc1', 'lc2', 'lc3']  # 分楼层爬取
                for c in tqdm(lc, desc='楼层链接', unit='links'):
                    # 为ls中的每个值创建URL的副本
                    modified_url = url
                    modified_url += 'pg{}' + c + v
                    # 将修改后的URL附加到self.plate_map[area]
                    self.plate_map.get(area, []).append(modified_url)
                    yield scrapy.Request(url=modified_url, callback=self.parse_page,
                                         meta={'v': self.v_map[v], 'area_label': area_label,
                                               'plate_label': plate_label, 'modified_url': modified_url,
                                               'c': self.c_map[c]})

    # 解析分页、计算最大页面
    def parse_page(self, response, **kwargs):
        v = response.meta['v']
        area_label = response.meta['area_label']
        c = response.meta['c']
        plate_label = response.meta['plate_label']
        modified_url = response.meta['modified_url']
        total_el = response.css('div.resultDes > div.total > span').get()
        total = int(re.search(r'\d+', total_el).group())
        page_size = min(math.ceil(total / 30), self.page_size)
        for i in tqdm(range(1, page_size + 1), desc='分页', unit='page'):
            url = modified_url.format(i)
            yield scrapy.Request(url=url, callback=self.parse, meta={'v': v, 'c': c, 'area_label': area_label,
                                                                     'plate_label': plate_label,
                                                                     'page_size': page_size})

    # 解析列表页数据
    def parse(self, response, **kwargs):
        li_els = response.css(
            '#beike > div.dealListPage > div.content > div.leftContent > div:nth-child(4) > ul.listContent > li')
        for El in li_els:
            info_el = El.css('div.info')
            detail_url = El.xpath('.//a[@class="img CLICKDATA maidian-detail"]/@href').get()
            # 创建 BeikeItem 实例>
            item = BeikeItem()
            item['area'] = response.meta['area_label']
            item['plate'] = response.meta['plate_label']
            item['v'] = response.meta['v']
            item['floor'] = response.meta['c']
            item['fileName'] = f" [全部] "
            title = info_el.css('div.title > a::text').get().strip()
            item['title'] = title
            decorate = info_el.xpath('normalize-space(.//div[@class="houseInfo"])').get()
            item['decorate'] = decorate
            # floor = info_el.xpath('normalize-space(.//div[@class="positionInfo"])').get()
            # item['floor'] = floor
            time = info_el.xpath('normalize-space(.//div[@class="dealDate"])').get()
            item['time'] = time
            deal_house_txt = info_el.xpath('.//span[@class="dealHouseTxt"]')
            address = ''.join(deal_house_txt.xpath('.//span/text()').getall())
            item['address'] = address
            total_price = info_el.xpath('.//div[@class="totalPrice"]/span[@class="number"]/text()').get()
            item['total_price'] = total_price
            unit_price = info_el.xpath('.//div[@class="unitPrice"]/span[@class="number"]/text()').get()
            item['price'] = unit_price
            deal_cycle_txt = info_el.xpath('.//span[@class="dealCycleTxt"]')
            history = ''.join(deal_cycle_txt.xpath('.//span/text()').getall())
            item['history'] = history
            yield item
            # if detail_url:
            #     print('detail_url', detail_url)
            #     yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item})

    # 详情页数据
    def parse_detail(self, response, **kwargs):
        item = response.meta['item']
        info_el = response.css('div.overview div.info')
        transaction_price = info_el.xpath('normalize-space(.//span[@class="dealTotalPrice"])').get()
        item['transaction_price'] = transaction_price
        msg = info_el.xpath('normalize-space(.//div[@class="msg"])').getall()
        item['msg'] = ' '.join(msg)
        yield item
