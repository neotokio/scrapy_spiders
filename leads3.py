import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from urlparse import urljoin
from scrapy import Selector

from go4world.items import Go4WorldItem


class ElectronicsSpider(CrawlSpider):
    name = "leads3"
    allowed_domains = ["go4worldbusiness.com"]
    start_urls = [
        'https://www.go4worldbusiness.com/buyleads/agri-food-processing-machinery-equipment.html?region=worldwide&country=all&pg_buyers=1&pg_suppliers=1',
        'https://www.go4worldbusiness.com/buyleads/alcoholic-beverages-tobacco-related-products.html?region=worldwide&country=all&pg_buyers=1&pg_suppliers=1',
        'https://www.go4worldbusiness.com/buyleads/bar-accessories-and-related-products.html?region=worldwide&country=all&pg_buyers=1&pg_suppliers=1',
        'https://www.go4worldbusiness.com/buyleads/farm-inputs---fertilizers-pesticides-seeds.html?region=worldwide&country=all&pg_buyers=1&pg_suppliers=1'
    ]

    rules = (
        Rule(LinkExtractor(allow=('/buyleads/*', '&pg_suppliers=1'), deny=('/find?searchText', '/inquiries/send/'), restrict_xpaths=('//*[@id="Buyers"]'), ),
             callback="category_page",
             follow=True),
        Rule(LinkExtractor(allow=('/buylead/view/'), restrict_xpaths=('//div[4]/div[1]/..'), ), 
             callback="parse_attr",
             follow=False),
         )

    def category_page(self,response):
         next_page = response.xpath('//div[4]/div[1]/div[2]/div/div[2]/div/div/div[23]/ul/@href').extract()

         for item in self.parse_attr(response):
             yield item

         if next_page:
             path = next_page.extract_first()
             nextpage = response.urljoin(path)
             yield scrapy.Request(nextpage,callback=category_page)

    def parse_attr(self, response):
        item = Go4WorldItem()
        item['Wanted'] = response.xpath('//div[4]/div[1]/div[1]/div/h1/text()').extract()
        item['Country'] = response.xpath('//div[4]/div[1]/div[3]/div/div[1]/text()').extract()
        item['Description'] = response.xpath('//div[4]/div[1]/div[5]/div/text()').extract()
        item['Category'] = response.xpath('//div[4]/div[1]/div[6]/div/div[2]/a/text()').extract()
        item['Verified'] = response.xpath('//div[4]/div[1]/div[3]/div/div[2]/span/small/text()').extract()
        item['Date'] = response.xpath('//div[4]/div[1]/div[3]/div/div[3]/small/text()').extract()
        yield item
####
