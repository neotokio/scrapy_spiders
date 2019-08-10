import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from stackq.items import StackqItem

class myquestionsCralwer(CrawlSpider):
    name = "stckq"

    rules = (
        Rule(LinkExtractor(),
             callback="parse",
             follow=False),)

    def start_requests(self):
        file = '/home/user/Scrapy/stackq/stackq/spiders/urls.txt'
        with open(file, 'rt') as f:
            start_urls = [url.strip() for url in f.readlines()]

        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = StackqItem()
        item['url'] = response.url
        item['title'] = response.xpath('.//div[@class="container"]//div[@id="question-header"]//a[@class="question-hyperlink"]//text()').extract()
        item['tags'] = response.xpath('//div[@class="grid ps-relative d-block"]/a/text()').extract()
        yield item