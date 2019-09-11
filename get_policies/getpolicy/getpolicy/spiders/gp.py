import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from twisted.internet.error import TimeoutError, TCPTimedOutError
import re
from bs4 import BeautifulSoup

from getpolicy.items import GetpolicyItem

'''gp_db, gp_user;test1, table:scraped'''


class PrivacyPolicyCrawl(CrawlSpider):
    name = 'getpolicy'

    custom_settings = {
        'DOWNLOAD_TIMEOUT': '10',
    }

    file = '/home/user/Scrapy/ready_merged.csv'
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
        if 'privacy' in response.url:
            item = GetpolicyItem()
            raw_policy = response.xpath(
                "//*[contains(text(), 'Policy') or contains(text(), 'Privacy')]"
                "/following-sibling::*[not(self::script)][not(self::meta)][not(self::link)]//text()").extract()
            catch_regex = response.url
            domain = re.sub(r'/\w+/\S.+|/~+.\w+/\S+', '', catch_regex)
            item['domain'] = domain
            item['url'] = response.url
            item['privacy'] = raw_policy
            yield item
        elif 'terms' in response.url:
            item = GetpolicyItem()
            raw_policy = response.xpath(
                "//*[contains(text(), 'Terms') or contains(text(), 'Conditions')]"
                "/following-sibling::*[not(self::script)][not(self::meta)][not(self::link)]//text()").extract()
            catch_regex = response.url
            domain = re.sub(r'/\w+/\S.+|/~+.\w+/\S+', '', catch_regex)
            item['domain'] = domain
            item['url'] = response.url
            item['terms'] = raw_policy
            yield item
        else:
            item = GetpolicyItem()
            item['rest_url'] = response.url
            catch_regex = response.url
            domain = re.sub(r'/\w+/\S.+|/~+.\w+/\S+', '', catch_regex)
            item['domain'] = domain
            yield item

    def errback_f(self, failure):
        if failure.check(TimeoutError):
            request = failure.request
            item = GetpolicyItem()
            item['url'] = request.url
            item['fail'] = 'FAIL'
            yield item
