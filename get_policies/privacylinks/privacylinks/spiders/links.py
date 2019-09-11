import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from twisted.internet.error import TimeoutError, TCPTimedOutError
from bs4 import BeautifulSoup
from privacylinks.items import PrivacylinksItem


class privacyPolicyLinksCrawl(CrawlSpider):
   name = 'second'
   file = '/data/second/no_priv_comp.csv'
   with open(file, 'rt') as f:
      start_urls = [url.strip() for url in f.readlines()]

   rules = (
      Rule(
         LinkExtractor(),
         callback='parse', follow=False),)

   def start_requests(self):
      for url in self.start_urls:
         yield scrapy.Request(url, callback=self.parse, meta={'download_timeout': 5}, errback=self.errback_f)

   def parse(self, response):
      if b'privacy' not in response.body:
         item = PrivacylinksItem()
         item['url'] = response.url
         item['fail'] = 'NO PRIVACY IN BODY'
         yield item
      else:
         extractor = LinkExtractor(allow=['privacy','terms','legal'])
         for link in extractor.extract_links(response):
            item = PrivacylinksItem()
            item['url'] = link.url
            yield item

   def errback_f(self, failure):
      if failure.check(TimeoutError):
         request = failure.request
         item = PrivacylinksItem()
         item['url'] = request.url
         item['fail'] = 'TIMEOUT'
         yield item
