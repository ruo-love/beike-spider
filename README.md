1. 进入二手房成交数据列表首页
2. 获取上海所有区域的链接 
3. 进入各个区域的链接，获取该区域的板块链接
4. 进入各个板块的链接，获取该板块的各种户型结构
5. 以单独户型为最终条件，获取二手房成交数据，最大页码100，超出100则继续增加过虑条件，以规避链接3000条数据的限制

``` python

scrapy crawl beike

```