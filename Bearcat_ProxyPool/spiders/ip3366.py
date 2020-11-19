import scrapy
from ..items import BearcatProxypoolItem


class Ip3366Spider(scrapy.Spider):
    name = 'ip3366'

    start_urls = [f'http://www.ip3366.net/free/?stype=1&page={i}' for i in range(1, 8)]

    def parse(self, response):
        tbody = response.xpath('//tbody')
        for td in tbody:
            ip = td.xpath('./tr/td[1]/text()').get()
            post = td.xpath('./tr/td[2]/text()').get()
            proxies = ip + ':' + post
            yield BearcatProxypoolItem(proxies=proxies)
