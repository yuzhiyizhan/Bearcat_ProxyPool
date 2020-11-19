import scrapy
from ..items import BearcatProxypoolItem


class IhuanSpider(scrapy.Spider):
    name = 'ihuan'

    start_urls = ['https://ip.ihuan.me/']

    def parse(self, response):
        tbody = response.xpath('//tbody')
        for tr in tbody:
            ip = tr.xpath('./tr/td/a/text()').get()
            post = tr.xpath('./tr/td/text()').get()
            proxies = ip + ':' + post
            yield BearcatProxypoolItem(proxies=proxies)
        urls = response.xpath('//div[@class="col-md-10"]/nav/ul/li')
        for i in urls:
            url = response.urljoin(i.xpath('./a/@href').get())
            yield scrapy.Request(url=url, callback=self.parse)
