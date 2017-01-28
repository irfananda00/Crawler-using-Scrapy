# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

from stillherecrawler.items import ProductItem


class BukalapakCrawlerSpider(CrawlSpider):
    search = "PS 4"
    page = 1
    name = 'bukalapak_crawler'
    allowed_domains = ['bukalapak.com']
    BASE_URL = r"https://www.bukalapak.com/c/handphone/hp-smartphone?page={page}&search%5Bcity%5D=&search%5Bcourier%5D=&search%5Bfree_shipping_coverage%5D=&search%5Binstallment%5D=0&search%5Bkeywords%5D={search}&search%5Bnew%5D=1&search%5Bpremium_seller%5D=0&search%5Bprice_max%5D=&search%5Bprice_min%5D=1000000&search%5Bprovince%5D=&search%5Btodays_deal%5D=0&search%5Btop_seller%5D=0&search%5Bused%5D=1&search%5Bwholesale%5D=0"
    start_urls = [BASE_URL.format(search=search,page=page)]

    def parse_start_url(self, response):
        products = response.xpath('//li[@class="col-12--2"]')
        yield self.printLog('PRODUCTS SIZE : ' + str(len(products)))

        for product in products:
            item = ProductItem()
            item['title'] = product.xpath('div/article/div[@class="product-description"]/h3/a/@title').extract()[0]
            item['url'] = 'www.bukalapak.com' + product.xpath('div/article/div[@class="product-media"]/a/@href').extract()[0]
            if len(product.xpath('div/article/div[@class="product-description"]/div[@class="product-price"]/span[@class="product-price__installment"]/span[@class="amount positive"]/text()').extract()) == 0:
                item['price'] = self.getVal(product.xpath('div/article/div[@class="product-description"]/div[@class="product-price"]/span[@class="product-price__installment product-price__reduced"]/span[@class="amount positive"]/text()').extract()[0],' RPrp.,')
            else:
                item['price'] = self.getVal(product.xpath('div/article/div[@class="product-description"]/div[@class="product-price"]/span[@class="product-price__installment"]/span[@class="amount positive"]/text()').extract()[0],' RPrp.,')
            yield item

        # TODO : next page
        if len(response.xpath('//a[@class="next_page"]').extract()) != 0:
            self.page += self.page
            yield self.printLog('NEXT PAGE : ' + str(self.page))
            yield Request(self.BASE_URL.format(search=self.search,page=self.page), callback=self.parse_start_url)

    def printLog(self, msg):
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.debug(msg)

    def getVal(self,v,t):
        s = v
        trash = t
        for char in trash:
            s = s.replace(char,'')
        return int(s)
