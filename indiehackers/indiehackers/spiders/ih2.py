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
        
        
        #item['BusinessType'] = texts[3] if len(texts) >= 4 else 'None'
        #item['BusinessArea'] = texts[4] if len(texts) >= 5 else 'None'
        #item['CreatorName'] = response.xpath('.//div[contains(@class, "product__content")]//div[contains(@class, "product-sidebar__users")]//div[contains(@class, "user-link")]//a//span[contains(@class, "user-link__name")]//text()').extract()
        #or item ['CreatorNameFromProfilePage'] = response.xpath('//div[contains(@class, "user-header")]//h1[contains(@class, "user-header__username")]//text()').extract()
        #item['LinkToProfile'] = response.xpath('.//div[contains(@class, "product__content")]//div[contains(@class, "product-sidebar__users")]//div[contains(@class, "user-link")]//a//@href').extract()
        #item['CreatorTwitter'] = response.xpath('//div[contains(@class, "user-header__satellites")]//a[contains(@class, "user-header__satellite")]//@href').extract()[1] or [2] = item['CreatorMail']
        #item['AgeCityJoinDate'] = response.xpath('//div[contains(@class, "user-header__metadata")]//p[contains(@class, "user-header__metadata-item")]//text()').extract()
        #item['Followers'] = response.xpath('//div[contains(@class, "user-sidebar")]//section[contains(@class, "user-stats")]//div[contains(@class, "user-stats__stat")]//span[contains(@class, "user-stats__number")]//text()').extract()[0] or [1] = item['Points']
        #item['Following'] response.xpath('//div[contains(@class, "user-sidebar")]//section[contains(@class, "following")]//span[contains(@class, "user-sidebar__section-supplement")]//text()').extract()
        
#        >>> response.xpath('//div[contains(@class, "user-header__metadata")]//p[contains(@class, "user-header__metadata-item")]//text()').extract()[0]
#'\n                  31\n                  \n                '
#>>> response.xpath('//div[contains(@class, "user-header__metadata")]//p[contains(@class, "user-header__metadata-item")]//text()').extract()[1]
#'Singapore, Singapore'
#>>> response.xpath('//div[contains(@class, "user-header__metadata")]//p[contains(@class, "user-header__metadata-item")]//text()').extract()[2]
#'\n                joined 2 years ago\n              '

#response.xpath('//div[contains(@class, "user-header__metadata")]//p[contains(@class, "user-header__metadata-item")and contains(., "joined")]//text()').extract()
#https://www.indiehackers.com/moe?id=CAMrajTi60QMSXJZqp0sG7IptAH2 - CITY + JOINED, no age
#https://www.indiehackers.com/levelsio?id=FfqtvHZDDnebVFkWD8hvZmWZVJJ2 - JOINED, no city
#https://www.indiehackers.com/johnonolan?id=TTNpIuNSsnNlltrLHqLaQMzeHxa2 - ALL
#response.xpath('//div[contains(@class, "user-header__metadata")]//p[contains(@class, "user-header__metadata-item")and contains(., "joined")]//text()').extract()
#Visit https://www.indiehackers.com/products > Click Log-in button > Render form > enter to input id > Load products page > infinite scroll
#No need to play with cookies, let scrapy handle it
#Make Scrapy click button(DONE!), navigate to form rendered(partialy?), fill form and send, render /products page, make scroll
#response.xpath('.//div[contains(@class, "product-header__content")]//h1[contains(@class, "product-header__title")]//p//text()').extract()

#scrapy shell 'http://localhost:8050/render.html?url=https://www.indiehackers.com/product/worfor&timeout=10&wait=7.5'
#response.xpath('//div[contains(@class, "product-metrics__content")]//a[contains(@class, "product-metrics__stat--revenue")]//span[contains(@class, "product-metrics__stat-number")]//text()').extract()
