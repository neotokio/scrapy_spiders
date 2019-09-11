import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin

from alexachive.items import AlexachiveItem

class archivecrawler(CrawlSpider):
    name = "alex"
    allowed_domains = ['web.archive.org']
    start_urls = ['https://web.archive.org/web/20160703213156/http://www.alexa.com/topsites/category/Top/Kids_and_Teens',
                  'https://web.archive.org/web/20160703213156/http://www.alexa.com/topsites/category/Top/News',
                  'https://web.archive.org/web/20160703213156/http://www.alexa.com/topsites/category/Top/Recreation',
                  'https://web.archive.org/web/20160703213156/http://www.alexa.com/topsites/category/Top/Reference',
                  'https://web.archive.org/web/20160703213156/http://www.alexa.com/topsites/category/Top/Science',
                  'https://web.archive.org/web/20160703213156/http://www.alexa.com/topsites/category/Top/Shopping',
                  'https://web.archive.org/web/20160703213156/http://www.alexa.com/topsites/category/Top/Society',
                  'https://web.archive.org/web/20160703213156/http://www.alexa.com/topsites/category/Top/Sports'
                  ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="subcat_div"]//ul'),),
             callback="parse",
             follow=True),)


    def parse(self, response):
        links = response.xpath('//div[@id="subcat_div"]//ul//a[contains(@href, "web")]//@href').extract()

        for link in links:
            url = urljoin(response.url, link)
            yield scrapy.Request(url, callback=self.content)

    def content(self, response):
        item = AlexachiveItem()
        item['category'] = response.xpath('//span[@class="page-title-text"]//a//text()').extract()
        for items in response.xpath('.//section[@class="td col-r"]//ul//li'):
            item['url'] = items.xpath('.//a[contains(@href, "web")]//@href').extract()
            item['description'] = items.xpath('.//div[@class="description"]//text()').extract()
            yield item

        nextpage = response.xpath('//div[@class="alexa-pagination"]//a[@class="next"]//@href').extract_first()
        if nextpage is not None:
            nextpage = urljoin(response.url, nextpage)
            yield scrapy.Request(nextpage, callback=self.parse)
