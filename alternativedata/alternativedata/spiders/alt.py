import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
#from urlparse import urljoin Py2.7
from urllib.parse import urljoin #Py3.5
from scrapy import Selector

from alternativedata.items import AlternativedataItem


class altSpider(CrawlSpider):
    name = "altdata"
    allowed_domains = ["alternativedata.org"]
    with open("altdata", "rt") as f:
       start_urls = [url.strip() for url in f.readlines()]
    custom_settings = {
    'FEED_EXPORT_FIELDS': ['CompanyName','DataSource','YearFounded','AssetManagerCustomers','Employees','TickersCoverage','Sectors','Funding','ClientFocus','HqLocation','DataDeliveryTypes','Website','Pricing','DatasetCoverage','GeographyCovered'],
  }

    def parse(self, response):
       item = AlternativedataItem()
       item['CompanyName'] = response.xpath('//div[contains(@class, "col-12")]//following-sibling::h1//text()').extract_first() or 'None'
       item['DataSource'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(), "main")]//preceding-sibling::p//text()').extract() or ['None']
       item['YearFounded'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(), "Year")]//preceding-sibling::p//text()').extract() or ['None']
       item['AssetManagerCustomers'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(), "Discretionary")]//preceding-sibling::p//text()').extract() or ['None']
       item['Employees'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(),"employees")]/following-sibling::p/text()').extract() or ['None']
       item['TickersCoverage'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(),"ticker")]/following-sibling::p/text()').extract() or ['None']
       item['Sectors'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(),"sector")]/following-sibling::p/text()').extract() or ['None']
       item['Funding'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(),"funding")]/following-sibling::p/text()').extract() or ['None']
       item['ClientFocus'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(),"client focus")]/following-sibling::p/text()').extract() or ['None']
       item['HqLocation'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(),"HQ")]/following-sibling::p/text()').extract() or ['None']
       item['DataDeliveryTypes'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(),"data delivery")]/following-sibling::p/text()').extract() or ['None']
       item['Website'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(),"website")]/following-sibling::p/a/@href').extract() or ['None']
       item['Pricing'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(),"pricing")]/following-sibling::p/text()').extract() or ['None']
       item['DatasetCoverage'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(),"Dataset Coverage")]/following-sibling::p/text()').extract() or ['None']
       item['GeographyCovered'] = response.xpath('//div[contains(@class, "infobox")]//span[contains(text(),"geography covered")]/following-sibling::p/text()').extract() or ['None']
       item['url'] = response.url
       yield item

#Spider reads files grabbed by parse_start_urls.py script earlier. Start_urls are provided from JSON API to avoid scraping Javascript content.
#Fields are sorted according to preferable schema.
#Spider outputs are in two file formats. CSV file format specified in settings.py by FEED_URI parameter (output to /%spidername/ folder) and JSON format specified as a pipeline in pipelines.py (output to ~/ of spider)
#Use urlparse import for Python 2.7 or urlib.parse for Python 3.5 > ...
