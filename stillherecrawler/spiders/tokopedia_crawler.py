# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import locale

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from stillherecrawler.items import ProductItem

class TokopediaCrawlerSpider(CrawlSpider):
    search = "PS 4"
    name = 'tokopedia_crawler'
    allowed_domains = ['tokopedia.com']
    BASE_URL = r"https://ace.tokopedia.com/search/v1/product?pmin=1000000&q={search}&vi=2&page=1&full_domain=www.tokopedia.com&scheme=https&device=desktop&source=directory&fshop=1&rows=200&sc=65&start=0&ob=100"
    start_urls = [BASE_URL.format(search=search)]

    def parse_start_url(self, response):
        products = json.loads(response.body_as_unicode())
        yield self.printLog('PRODUCTS SIZE : ' + str(len(products["data"])))

        for product in products["data"]:
            item = ProductItem()
            item['title'] = product["name"]
            item['url'] = product["uri"]
            item['price'] = self.getVal(product["price"],' Rrp.')
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
