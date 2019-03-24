# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from collections import OrderedDict

class AlternativedataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    url = scrapy.Field()
    CompanyName = scrapy.Field()
    DataSource = scrapy.Field()
    YearFounded = scrapy.Field()
    AssetManagerCustomers = scrapy.Field()
    Employees = scrapy.Field()
    TickersCoverage = scrapy.Field()
    Sectors = scrapy.Field()
    Funding = scrapy.Field()
    ClientFocus = scrapy.Field()
    HqLocation = scrapy.Field()
    DataDeliveryTypes = scrapy.Field()
    Website = scrapy.Field()
    Pricing = scrapy.Field()
    DatasetCoverage = scrapy.Field()
    GeographyCovered = scrapy.Field()
