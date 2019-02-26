import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from urlparse import urljoin
from scrapy import Selector

from go4world.items import Go4WorldItem


class ElectronicsSpider(CrawlSpider):
    name = "test"
    allowed_domains = ["go4worldbusiness.com"]
    start_urls = [
        'https://www.go4worldbusiness.com/find?searchText=greenhouse&entityTypeFilter%5B0%5D=M&pg_buyers=1&pg_suppliers=1&_format=html&BuyersOrSuppliers=suppliers',
    ]

    rules = (
        Rule(LinkExtractor(allow=('&pg_buyers=1&pg_suppliers=', 'find?searchText=elevators-escalators.html'),restrict_xpaths=('//div[4]/div[1]/div[2]/div/div[2]/div/div/div[23]/ul'), ),
             callback="category_page",
             follow=True),
        Rule(LinkExtractor(allow=('/member/'), deny=('/inquiries/send/members/', '/rate/'), ), 
             callback="parse_attr",
             follow=False),
        Rule(LinkExtractor(restrict_xpaths=('/div[4]/div[1]/..'), ),
             callback="company_data",
             follow=False),
         )

    BASE_URL = 'https://www.go4worldbusiness.com'

    def category_page(self,response):
         next_page = response.xpath('//div[4]/div[1]/div[2]/div/div[2]/div/div/div[23]/ul/@href').extract()

         if next_page:
             path = next_page.extract_first()
             nextpage = response.urljoin(path)
             yield scrapy.Request(nextpage,callback=category_page)

    def parse_attr(self, response):
        item = Go4WorldItem()
        item['NameOfCompany'] = response.xpath('//div[4]/div[1]/div[1]/div/h1/text()').extract()
        item['Contact'] = response.xpath('//div[4]/div[1]/div[5]/div/address/text()').extract()
        item['Gold'] = response.xpath('/html/body/div[4]/div[1]/div[2]/div[1]/span[2]/text()').extract() 
        item['Category'] = response.xpath('/html/body/div[4]/div[1]/div[6]/div/div[1]/a//text()').extract()
        item['Date'] = response.xpath('/html/body/div[4]/div[1]/div[3]/div/div[3]/small/text()').extract()
        item['Country'] = response.xpath('//div[4]/div[1]/div[3]/div/div[1]/text()').extract()
        item['Logo'] = response.xpath('/html/body/div[4]/div[1]/div[4]/div/img/@alt').extract()
        item['CompanyInfo'] = response.xpath('/html/body/div[4]/div[1]/div[5]/div/h3/following-sibling::node()/descendant-or-self::text()').extract()
        item['url'] = response.url
        company_page = response.xpath('//div[4]/div[1]/div[4]/div/ul/li[2]/a/@href').extract_first() #navigate to PRODUCTS>>>
        
        if company_page:  #IT SKIPS IF IT DOESNT FIND 'PRODUCT' TAB!!!!
            company_page = response.urljoin(company_page)
            request = scrapy.Request(company_page, callback = self.company_data)
            request.meta['item'] = item
            yield request
        else:
			yield item
   
    def company_data(self, response):
        item = response.meta['item']
        item['ProductsSold'] = response.xpath('//div[4]/div[1]/div[5]/div/div/div[*]/div[1]/a/h5/span/descendant-or-self::*/text()').extract()
        yield item

