import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from urlparse import urljoin
from scrapy import Selector

from tradekey.items import TradekeyItem

#Xpaths to figure out, because they dont work! scrapy shell would be best
#LinkExtractor rules for category_page
# response.xpath('//*[@id="list_1"]//table//tr//h2//a//text()').extract() #NameOfProduct in list_1

class Trade(CrawlSpider):
    name = "companies"
    allowed_domains = ["tradekey.com"]
    with open("link.txt", "rt") as f:
       start_urls = [url.strip() for url in f.readlines()]


    rules = (
        Rule(LinkExtractor(restrict_xpaths = ('/html/body/div[9]/div[2]/div[2]/div[2]/form', '//*[@id="paging"]'), ),
             callback="category_page",
             follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//html/body/div[9]/div[2]/div[2]/div[2]/form'), ),
             callback="parse_attr",
             follow=False),
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="main-info"]', '//*[@id="nav_bar_fixed"]'), ),
             callback="company_data",
             follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="main-info"]', '//*[@id="nav_bar_fixed"]'), ),
             callback="product_data",
             follow=False),
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="main-info"]', '//*[@id="nav_bar_fixed"]'), ),
             callback="sell_data",
             follow=False),
        Rule(LinkExtractor(restrict_xpaths=('//*[@class="main-container-right"]'), ),
             callback="trust_data",
             follow=False),
         )

    BASE_URL = 'https://www.go4worldbusiness.com'

    def category_page(self,response):
         next_page = response.xpath('//*[@id="paging"]/@href').extract()
         
         for item in self.parse_attr(response):
             yield item

         if next_page:
             path = next_page.extract_first()
             nextpage = response.urljoin(path)
             yield scrapy.Request(nextpage,callback=category_page)

    def parse_attr(self, response):
        item = TradekeyItem()
        item['Country'] = response.xpath('//li[contains(@id, "list_")]//span[contains(@class, "c_flag")]/font/text()').extract_first().strip()
        
        company_page = response.xpath('//li[contains(@id, "list_")]//a[contains(@class, "company")]/@href').extract_first()
        company_page = response.urljoin(company_page)
        request = scrapy.Request(company_page, callback = self.company_data)
        request.meta['item'] = item
        yield request
   
    def company_data(self, response):
        item = response.meta['item']
        item['Address'] = response.xpath('//h1[contains(@class, "company-heading")]/following-sibling::p//text()').extract()[1]
        item['NameOfCompany'] = response.xpath('//a[contains(@id, "company-link-heading")]//text()').extract()[1]
        item['url'] = response.url
        
        product_page = response.xpath('//ul[contains(@class, "navbar-nav")]//li[contains(@class, "nopadding-left-right")]//a/@href').extract()[1]
        product_page = response.urljoin(product_page)
        request = scrapy.Request(product_page, callback = self.product_data, meta={'item': item})
        return request
            
    def product_data(self, response):
        item = response.meta['item']
        item ['SoldProducts'] = response.xpath('//a[contains(@class, "offerHeading")]//text()').extract()
        sell_page = response.xpath('//ul[contains(@class, "navbar-nav")]//li[contains(@class, "nopadding-left-right")]//a/@href').extract()[2]
        sell_page = response.urljoin(sell_page)
        request = scrapy.Request(sell_page, callback = self.sell_data, meta={'item': item})
        return request
	
    def sell_data(self, response):
        item = response.meta['item']
        item ['SellOffers'] = response.xpath('//a[contains(@class, "offerHeading")]//text()').extract()
        trust_page = response.xpath('//ul[contains(@class, "navbar-nav")]//li[contains(@class, "nopadding-left-right")]//a/@href').extract()[4]       
        trust_page = response.urljoin(trust_page)
        request = scrapy.Request(trust_page, callback = self.trust_data, meta={'item': item})
        return request

    def trust_data(self, response):
        item = response.meta['item']
        item ['Joined'] = response.xpath('//div[contains(@id, "bi-body")]//label[contains(@class, "text-bold")]//following-sibling::p//text()').extract()[1]
        item ['Feedbacks'] = response.xpath('//div[contains(@id, "bi-body")]//label[contains(@class, "text-bold")]//following-sibling::p//text()').extract()[2]     
        texts = response.xpath('//div[contains(@id, "bi-body")]//label[contains(@class, "text-bold")]//following-sibling::p//text()').getall()

        item['BusinessType'] = texts[3] if len(texts) >= 4 else 'None'
        item['BusinessArea'] = texts[4] if len(texts) >= 5 else 'None'
        

        yield item

#response.xpath('//h1[contains(@class, "company-heading")]/following-sibling::p//text()').extract() This gets addres from corp page
#product_page = response.xpath('//div[contains(@class, "nav_bar_fixed")]//li[contains(@class, "nopadding-left-right")]//a[contains(@title, "Products")]//@href').extract_first() 
#different approach - scrap only members OR visit product page and scrap here - best to do both
#response.xpath('//ul[contains(@class, "navbar-nav")]//li[contains(@class, "nopadding-left-right")]//a/@href').extract()[5] WORKS! [5] selects
#response.xpath('//div[contains(@id, "bi-body")]//label[contains(@class, "text-bold")]//following-sibling::p[1]//text()').extract() (this selects values from trust profile)
#response.xpath('//div[contains(@id, "bi-body")]//label[contains(@class, "text-bold")]//text()').extract() this selects variables from trust profile
#response.xpath('//div[contains(@id, "bi-body")]//label[contains(@class, "text-bold")]//following-sibling::p[1]//text() | //div[contains(@id, "bi-body")]//label[contains(@class, "text-bold")]//text()').extract()
#EXTRACT ALLN NICLEY!

