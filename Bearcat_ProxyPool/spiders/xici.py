import scrapy
from ..items import BearcatProxypoolItem


class XiciSpider(scrapy.Spider):
    name = 'xici'
    start_urls = [f'https://www.xicidaili.com/nn/{i}/' for i in range(1, 21)]

    def parse(self, response):
        proxy = response.xpath('//tr')[1:]
        for i in proxy:
            http = i.xpath('./td/text()')[4].get()
            if '高匿' in http:
                ip = i.xpath('./td/text()')[0].get()
                host = i.xpath('./td/text()')[1].get()
                save = ip, host
                proxies = save[0] + ':' + save[1]
                yield BearcatProxypoolItem(proxies=proxies)
