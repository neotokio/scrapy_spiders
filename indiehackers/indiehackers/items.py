# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class ScrapingTestingLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

class IndiehackersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    CompanyName = scrapy.Field()
    Revenue = scrapy.Field()
    Tagline = scrapy.Field()
    Tags = scrapy.Field()
    Updates = scrapy.Field()
    Followers = scrapy.Field()
    Website = scrapy.Field()
    Twitter = scrapy.Field()
    Facebook = scrapy.Field()
    Description = scrapy.Field()
    CreatorName = scrapy.Field()
    CreatorMail = scrapy.Field()
    CreatorTwitter = scrapy.Field()
    Followers = scrapy.Field()
    Points = scrapy.Field()
    Following = scrapy.Field()
    Joined = scrapy.Field()
    City = scrapy.Field()
    Age = scrapy.Field()
