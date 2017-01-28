# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

from stillherecrawler.items import ProductItem

class BlibliCrawlerSpider(CrawlSpider):
    search = "Nexus 6"
    page = 1
    name = 'blibli_crawler'
    allowed_domains = ['blibli.com']
    BASE_URL = r"https://www.blibli.com/search?s={search}&o=10&c=HA-1000002"
    start_urls = [BASE_URL.format(search=search,page=page)]

    def parse_start_url(self, response):
        products = response.xpath('//div[@class="large-4 medium-5 small-8 columns"]')
        yield self.printLog('PRODUCTS SIZE : ' + str(len(products)))

        for product in products:
            item = ProductItem()
            if product.xpath('div/a/div/div/div/div[@class="product-price"]/div/span/text()').extract()[0] != 'Segera Hadir':
                item['price'] = self.getVal(product.xpath('div/a/div/div/div/div[@class="product-price"]/div/span/text()').extract()[0],' RPrp.,')
                item['title'] = product.xpath('div/a/div/div/div/div[@class="product-title"]/@title').extract()[0]
                item['url'] = product.xpath('div/a/@href').extract()[0]
                yield item

    def printLog(self, msg):
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.debug(msg)

    def getVal(self,v,t):
        s = v
        trash = t
        for char in trash:
            s = s.replace(char,'')
        return int(s)
