# -*- coding: utf-8 -*-
#importing necessary packages
import scrapy
import re

#Creating a stock class, which we will use later for every scraped element. Specyfing what fields are we going to need.
class Stock(scrapy.Item):
    name = scrapy.Field()
    short_name = scrapy.Field()
    previous_close = scrapy.Field()
    open = scrapy.Field()
    bid = scrapy.Field()
    ask = scrapy.Field()
    days_range = scrapy.Field()
    fifty_two_week_range = scrapy.Field()
    volume = scrapy.Field()
    avg_volume = scrapy.Field()
    market_cap = scrapy.Field()
    beta_five_monthly = scrapy.Field()
    PE_ratio_TTM = scrapy.Field()
    EPS_TTM = scrapy.Field()
    earning_date = scrapy.Field()
    forward_dividend_yield = scrapy.Field()
    ex_dividend_date = scrapy.Field()
    one_y_target_est = scrapy.Field()

#Creating a spider to scrap data for each company using links that were scrapped before
class LinksSpider(scrapy.Spider):
    name = 'stocks'
    allowed_domains = ['https://finance.yahoo.com/']
    custom_settings = {
            'FEED_URI': 'stocks.csv',
            'FEED_FORMAT': 'csv',
            'FEED_EXPORT_FIELDS': [
                "name",
                "short_name",
                "previous_close",
                "open",
                "bid",
                "ask",
                "days_range",
                "fifty_two_week_range",
                "volume",
                "avg_volume",
                "market_cap",
                "beta_five_monthly",
                "PE_ratio_TTM",
                "EPS_TTM",
                "earning_date",
                "forward_dividend_yield",
                "ex_dividend_date",
                "one_y_target_est",
            ],
         }
    try:
        with open("link_list.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []
    # Callback function used to parse the response and return item objects (stock data)
    def parse(self, response):
        s = Stock()
        #Using two diffrent xpaths because some information are located in span class and others are not
        temp = "//td[@class='Ta(end) Fw(600) Lh(14px)']/span/text()"
        temp_1 = "//td[@class='Ta(end) Fw(600) Lh(14px)']/text()"
        xpath_name = "//h1[@class='D(ib) Fz(18px)']/text()"
        check = response.xpath(temp).getall()[13]
        regex = re.compile('(.*)\s\((.*)\)')
        company_all = response.xpath(xpath_name).getall()[0]

        #Assigning each field to the s object and yielding the object instance:
        s['name'], s['short_name'] = re.findall(regex, company_all)[0]
        s['previous_close'] = response.xpath(temp).getall()[0]
        s['open'] = response.xpath(temp).getall()[1]
        s['bid'] = response.xpath(temp).getall()[2]
        s['ask'] = response.xpath(temp).getall()[3]
        s['days_range'] = response.xpath(temp_1).getall()[0]
        s['fifty_two_week_range'] = response.xpath(temp_1).getall()[1]
        s['volume'] = response.xpath(temp).getall()[4]
        s['avg_volume'] = response.xpath(temp).getall()[5]
        s['market_cap'] = response.xpath(temp).getall()[6]
        s['beta_five_monthly'] = response.xpath(temp).getall()[7]
        s['PE_ratio_TTM'] = response.xpath(temp).getall()[8]
        s['EPS_TTM'] = response.xpath(temp).getall()[9]
        s['earning_date'] = response.xpath(temp).getall()[10:12] if check else response.xpath(temp).getall()[10]
        s['forward_dividend_yield'] = response.xpath(temp_1).getall()[2]
        s['ex_dividend_date'] = response.xpath(temp).getall()[12] if check else response.xpath(temp).getall()[11]
        s['one_y_target_est'] = response.xpath(temp).getall()[13] if check else response.xpath(temp).getall()[12]
        yield s
