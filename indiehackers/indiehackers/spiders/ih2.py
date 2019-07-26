import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
#from urlparse import urljoin Py2.7
from urllib.parse import urljoin #Py3.5
from scrapy import Selector
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader

from indiehackers.items import IndiehackersItem

class altSpider(CrawlSpider):
    name = "indiehackers2"
    with open('test.txt', 'rt') as f:
        start_urls = [url.strip() for url in f.readlines()]
    custom_settings = {
    'FEED_EXPORT_FIELDS': ['CompanyName','Tags','Tagline','Revenue','Updates','Followers','Website','Twitter','Facebook','Description','CreatorName','City','Age','CreatorMail','CreatorTwitter', 'Joined', 'Followers', 'Following', 'Points'],
  }

    rules = (
        Rule(LinkExtractor( ),
             callback="parse",
             follow=False),)
    
    def start_requests(self):
             
        for url in self.start_urls:
           
           yield SplashRequest(url,callback=self.parse_attr, endpoint='render.html', args={'wait':7.5})
    
    def parse_attr(self, response):
        item = IndiehackersItem()
        item['CompanyName'] = response.xpath('.//div[contains(@class, "product-header__content")]//h1[contains(@class, "product-header__title")]//a//text()').extract()
        item['Tags'] = response.xpath('//div[contains(@class, "tag-list__tags")]//div[contains(@class, "tag-list__tag")]//text()').extract()
        item['Revenue'] = response.xpath('//div[contains(@class, "product-metrics__content")]//a[contains(@class, "product-metrics__stat--revenue")]//span[contains(@class, "product-metrics__stat-number")]//text()').extract()
        item['Tagline'] = response.xpath('.//p[contains(@class, "product-header__tagline")]//text()').extract()
        item['Updates'] = response.xpath('//div[contains(@class, "product-metrics__content")]//a[contains(@class, "product-metrics__stat--updates")]//span[contains(@class, "product-metrics__stat-number")]//text()').extract()
        item['Followers'] = response.xpath('//div[contains(@class, "product-metrics__content")]//a[contains(@class, "product-metrics__stat--followers")]//span[contains(@class, "product-metrics__stat-number")]//text()').extract()
        item['Website'] = response.xpath('//div[contains(@class, "product-metrics__content")]//a[contains(@class, "product-metrics__stat--website")]//@href').extract() or 'None'
        item['Twitter'] = response.xpath('//div[contains(@class, "product-metrics__content")]//a[contains(@class, "product-metrics__stat--twitter")]//@href').extract() or 'None'
        item['Facebook'] = response.xpath('//div[contains(@class, "product-metrics__content")]//a[contains(@class, "product-metrics__stat--facebook")]//@href').extract() or 'None'
        item['Description'] = response.xpath('//div[contains(@class, "product__content")]//section[contains(@id, "ember")]//section[contains(@class, "product-sidebar__description")]//following-sibling::p//text()').extract() or 'None'
        
        profile_page = response.xpath('//div[contains(@class, "product__content")]//div[contains(@class, "product-sidebar__users")]//div[contains(@class, "user-link")]//a//@href').extract_first()
        profile_page = response.urljoin(profile_page)
        request = SplashRequest(profile_page, endpoint = 'render.html', callback = self.profile_data, meta={'item':item}, args={'wait':7.5})
        return request
        
    def profile_data(self, response):
        
        item = response.meta['item']
        item ['CreatorName'] = response.xpath('//div[contains(@class, "user-header")]//h1[contains(@class, "user-header__username")]//text()').extract()
        item['CreatorMail'] = response.xpath('//div[contains(@class, "user-header__satellites")]//a[contains(@class, "user-header__satellite")and contains(@href, "mail")]//@href').extract() or 'None'
        item['CreatorTwitter'] = response.xpath('//div[contains(@class, "user-header__satellites")]//a[contains(@class, "user-header__satellite")and contains(@href, "twitter")]//@href').extract() or 'None'        
        item['Followers'] = response.xpath('//div[contains(@class, "user-sidebar")]//section[contains(@class, "user-stats")]//div[contains(@class, "user-stats__stat")]//span[contains(@class, "user-stats__number")]//text()').extract()[0]
        item['Points'] = response.xpath('//div[contains(@class, "user-sidebar")]//section[contains(@class, "user-stats")]//div[contains(@class, "user-stats__stat")]//span[contains(@class, "user-stats__number")]//text()').extract()[1]
        item['Following'] = response.xpath('//div[contains(@class, "user-sidebar")]//section[contains(@class, "following")]//span[contains(@class, "user-sidebar__section-supplement")]//text()').extract()
        item['Joined'] = response.xpath('//div[contains(@class, "user-header__metadata")]//p[contains(@class, "user-header__metadata-item")and starts-with(., "\n") and contains(.,"joined")]//text()').extract()
        item['City'] = response.xpath('//div[contains(@class, "user-header__metadata")]//p[contains(@class, "user-header__metadata-item")and contains(., ",")]//text()').extract() or 'None'
        item['Age'] = response.xpath('//div[contains(@class, "user-header__metadata")]//p[contains(@class, "user-header__metadata-item")and not(contains(., "joined"))]//text()').re('[0-9]+') or 'None'
        yield item
