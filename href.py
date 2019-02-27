import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from urlparse import urljoin
from scrapy import Selector

from tradelinks.items import TradelinksItem

class Trade(CrawlSpider):
    name = "href"
    allowed_domains = ["tradekey.com"]
    start_urls = [
          'https://www.tradekey.com/Agriculture_pd1216.htm',
          'https://www.tradekey.com/Apparel-Clothing_pd1539.htm',
          'https://www.tradekey.com/Automobiles_pd1815.htm'
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths = ('//div[contains(@class, "cateMenu")]'), ),
             callback="parse_item",
             follow=False), )
             

    def parse_item(self, response):
        item = TradelinksItem()
        item['href'] = response.url #response.xpath('//div[contains(@class, "cateMenu")]//a//@href').extract()
        yield item
