import scrapy

from beike.items import BeikeItem
## scrapy crawl beike -a address="普陀" -a max=20
class QuotesSpider(scrapy.Spider):
    name = "beike"

    def __init__(self, address="松江新城松江大学城", max=100, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.address = address
        self.max = max

    allowed_domains = ['bj.ke.com', 'sh.ke.com']
    start_urls = ['https://sh.ke.com/chengjiao/pg{}rs{}/']

    def start_requests(self):
        for page in range(int(self.max)):
            url = self.start_urls[0].format(page + 1, self.address)
            print('start_requests-----------------------------', url)
            yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        li_els = response.css(
            '#beike > div.dealListPage > div.content > div.leftContent > div:nth-child(4) > ul.listContent > li')
        for El in li_els:
            info_el = El.css('div.info')
            detail_url = El.xpath('.//a[@class="img CLICKDATA maidian-detail"]/@href').get()
            # 创建 BeikeItem 实例>
            item = BeikeItem()
            item['fileName'] = f" [{self.address}] "
            title = info_el.css('div.title > a::text').get().strip()
            item['title'] = title
            decorate = info_el.xpath('normalize-space(.//div[@class="houseInfo"])').get()
            item['decorate'] = decorate
            floor = info_el.xpath('normalize-space(.//div[@class="positionInfo"])').get()
            item['floor'] = floor
            time = info_el.xpath('normalize-space(.//div[@class="dealDate"])').get()
            item['time'] = time
            deal_house_txt = info_el.xpath('.//span[@class="dealHouseTxt"]')
            address = ''.join(deal_house_txt.xpath('.//span/text()').getall())
            item['address'] = address
            unit_price = info_el.xpath('.//div[@class="unitPrice"]/span[@class="number"]/text()').get()
            item['price'] = unit_price
            deal_cycle_txt = info_el.xpath('.//span[@class="dealCycleTxt"]')
            history = ''.join(deal_cycle_txt.xpath('.//span/text()').getall())
            item['history'] = history
            if detail_url:
                print('detail_url', detail_url)
                yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response, **kwargs):
        item = response.meta['item']
        info_el = response.css('div.overview div.info')
        transaction_price = info_el.xpath('normalize-space(.//span[@class="dealTotalPrice"])').get()
        item['transaction_price'] = transaction_price
        msg = info_el.xpath('normalize-space(.//div[@class="msg"])').getall()
        item['msg'] = ' '.join(msg)
        yield item
