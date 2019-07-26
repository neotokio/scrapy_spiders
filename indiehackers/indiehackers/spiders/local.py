import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
#from urlparse import urljoin Py2.7
from urllib.parse import urljoin #Py3.5
from scrapy import Selector
from scrapy_splash import SplashRequest

from indiehackers.items import IndiehackersItem


class altSpider(CrawlSpider):
    name = "local"
    start_urls = ["file:///home/user/Scrapy/indiehackers/indiehackers/spiders/Indiehackers_links_all.html"]
        
    def parse_attr(self, response):
       
      item = IndiehackersItem()
      item['Tagline'] = items.xpath('.//div[contains(@class, "product-card ember-view")]//a//@href').extract()

      yield item
