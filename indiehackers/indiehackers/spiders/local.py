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

#response.xpath('//div[contains(@class, "product-card__revenue")]//span[contains(@class, "product-card__revenue-number")]//text()').extract() Revenue works

#TO RESOLVE:
#1. Saving to separate items (SOLVED!)
#2. Passing ALL of the website with log-in
#3. Navigating to futher URLS to scrape more data
#4. Login session

#It can be also resolved by navigating to each individual page, passing meta item, extracting information fromt there
#div id="ember85" class="product-card ember-view"><a href="/product/browserless" id="ember86" class="product-card__link ember-view">
