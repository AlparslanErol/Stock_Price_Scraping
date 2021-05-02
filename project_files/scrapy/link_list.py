# -*- coding: utf-8 -*-
import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()

class LinkListsSpider(scrapy.Spider):
    name = 'link_lists'
    allowed_domains = ['https://finance.yahoo.com/']
    start_urls = ['https://finance.yahoo.com/most-active']
    def parse(self, response):
        xpath = '//a[@class="Fw(600) C($linkColor)"]/@href'
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://finance.yahoo.com/' + s.get()
            yield l