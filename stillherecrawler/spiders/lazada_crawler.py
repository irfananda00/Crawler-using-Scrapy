# -*- coding: utf-8 -*-
import scrapy
import logging

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from stillherecrawler.items import ProductItem


class LazadaCrawlerSpider(CrawlSpider):
    search = "PS 4"
    name = 'lazada_crawler'
    allowed_domains = ['lazada.co.id']
    BASE_URL = r"http://www.lazada.co.id/catalog/?q={search}&price=1000000-99000000"
    start_urls = [BASE_URL.format(search=search)]

    def parse_start_url(self, response):
        products = response.xpath('//div[@class="product-card new_ outofstock installments_1 "]')
        yield self.printLog('PRODUCTS SIZE : ' + str(len(products)))

        for product in products:
            item = ProductItem()
            item['title'] = product.xpath('a/div[@class="product-card__description"]/div[@class="product-card__name-wrap"]/span/text()').extract()[0]
            item['url'] = product.xpath('a/@href').extract()[0]
            item['price'] = self.getVal(product.xpath('a/div[@class="product-card__description"]/div[@class="price-block--grid"]/div[@class="product-card__price"]/text()').extract()[0],' RPrp.,')
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
