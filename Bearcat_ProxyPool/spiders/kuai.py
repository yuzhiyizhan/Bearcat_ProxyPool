import scrapy
from ..items import BearcatProxypoolItem


class KuaiSpider(scrapy.Spider):
    name = 'kuai'
    start_urls = [f'https://www.kuaidaili.com/free/inha/{i}/' for i in range(1, 21)]

    def parse(self, response):
        tboby = response.xpath('//tr')[1:]
        for i in tboby:
            proxy = i.xpath('./td/text()')[2].get()
            if '高匿' in proxy:
                ip = i.xpath('./td/text()')[0].get()
                post = i.xpath('./td/text()')[1].get()
                proxies = ip + ':' + post
                yield BearcatProxypoolItem(proxies=proxies)
