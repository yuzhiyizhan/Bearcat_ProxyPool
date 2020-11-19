import scrapy
from ..items import BearcatProxypoolItem


class NimaSpider(scrapy.Spider):
    name = 'nima'
    start_urls = [f'http://www.nimadaili.com/gaoni/{i}/' for i in range(1, 21)]

    def parse(self, response):
        proxy = response.xpath('//tbody/tr')
        for i in proxy:
            http = i.xpath('./td/text()')[2].get()
            if '高匿' in http:
                proxies = i.xpath('./td/text()')[0].get()
                yield BearcatProxypoolItem(proxies=proxies)
