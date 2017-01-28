# -*- coding: utf-8 -*-
import scrapy
import logging

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from stillherecrawler.items import ProductItem


class MataharimallCrawlerSpider(CrawlSpider):
    search = "PS 4"
    name = 'mataharimall_crawler'
    allowed_domains = ['mataharimall.com']
    BASE_URL = r"https://www.mataharimall.com/products?category_id=1&query={search}&page=1&per_page=100&fq=category_ids_1:2"
    start_urls = [BASE_URL.format(search=search)]

    def parse_start_url(self, response):
        products = response.xpath('//div[@class="product-item-wrapper item-product-list"]')
        yield self.printLog('PRODUCTS SIZE : ' + str(len(products)))

        for product in products:
            item = ProductItem()
            item['title'] = product.xpath('a/div/div[@class="itembox-inner clearfix col-xs-16 col-sm-16 col-md-24"]/div[@class="item-name"]/text()').extract()[0]
            item['url'] = product.xpath('a/@href').extract()[0]
            item['price'] = self.getVal(product.xpath('a/div/div[@class="itembox-inner clearfix col-xs-16 col-sm-16 col-md-24"]/div[@class="item-price"]/div/text()').extract()[0],' Rrp.,')
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
