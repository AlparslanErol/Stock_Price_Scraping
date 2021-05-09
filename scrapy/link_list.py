# -*- coding: utf-8 -*-
import scrapy

#Specifying link field which we will use later
class Link(scrapy.Item):
    link = scrapy.Field()

#Creating a spider to scrap links for each company from most actives
class LinkListsSpider(scrapy.Spider):
    name = 'link_list'
    allowed_domains = ['https://finance.yahoo.com/']
    start_urls = ['https://finance.yahoo.com/most-active']

    #Callback function used to parse the response and return item objects (links)
    def parse(self, response):
        xpath = '//a[@class="Fw(600) C($linkColor)"]/@href'
        selection = response.xpath(xpath)
        #Using xpath to extract the links, assigning each field to the l object and yielding the object instance:
        for s in selection:
            l = Link()
            #Creating links by adding an ending specified for each company to the initial link
            l['link'] = 'https://finance.yahoo.com/' + s.get()
            yield l
