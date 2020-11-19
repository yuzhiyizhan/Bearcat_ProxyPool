import scrapy
from ..items import BearcatProxypoolItem


class XilaSpider(scrapy.Spider):
    name = 'xila'
    start_urls = [f'http://www.xiladaili.com/gaoni/{i}/' for i in range(1, 21)]

    def parse(self, response):
        proxys = response.xpath('//tbody/tr')
        for i in proxys:
            proxy = i.xpath('./td/text()')[2].get()
            if '高匿' in proxy:
                proxies = i.xpath('./td/text()')[0].get()
                yield BearcatProxypoolItem(proxies=proxies)
