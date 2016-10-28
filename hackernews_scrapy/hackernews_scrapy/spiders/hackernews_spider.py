# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from hackernews_scrapy.items import HackerNewsScrapyItem	


class HackerNewsSpider(CrawlSpider):
	name = "hackernews"
	allowed_domains = ["ycombinator.com"]
	start_urls = [
		"https://news.ycombinator.com/"
		]
	rules = (
		Rule(LinkExtractor(allow="news.ycombinator.com/newest"), callback="parse_item", follow=True),
		)

	def parse_item(self, response):
		self.log("Scraping: " + response.url)

		articles = response.xpath('//tr[@class="athing"]')

		for article in articles:
			item = HackerNewsScrapyItem()
			item["link_title"] = article.xpath('td[@class="title"]/a/text()').extract()[0]
			item["url"] = article.xpath('td[@class="title"]/a/@href').extract()[0]

			yield item