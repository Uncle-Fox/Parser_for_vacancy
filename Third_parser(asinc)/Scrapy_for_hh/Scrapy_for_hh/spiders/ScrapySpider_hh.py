from typing import Iterable
import scrapy
from urllib.parse import urlparse
import time
from scrapy.http import Request


class ScrapyspiderHhSpider(scrapy.Spider):
    name = "ScrapySpider_hh"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?text=программист+python&area=113&customDomain=1&page="]

    def start_requests(self) -> Iterable[Request]:
        base_url = self.start_urls[0]
        for page_number in range (1, 40):
            url = f"{base_url}{page_number}"
            yield scrapy.Request(url=url, callback=self.parse)
            time.sleep(1)

    def parse(self, response):
        vacancys = response.xpath('//div[contains(@class, "vacancy-serp-item")]')
        processed_urls = set()
        for vacancy in vacancys:
            url = vacancy.xpath('.//span/a[contains(@data-qa, "serp-item__title") and contains(@class, "serp-item__title")]/@href').extract_first()
            if url and url not in processed_urls:
                processed_urls.add(url)
                yield {
                    'name': vacancy.xpath('.//span/a[contains(@data-qa, "serp-item__title") and contains(@class, "serp-item__title")]/text()').get(),
                    'salary': ' '.join(vacancy.xpath('.//span[contains(@data-qa, "vacancy-serp__vacancy-compensation")]/text()').getall()),
                    'company': vacancy.xpath('.//a[@class="bloko-link bloko-link_kind-tertiary"]/text()').get(),
                    'city': vacancy.xpath('.//div[@class="bloko-text"]/text()').get(),
                    'exp': vacancy.xpath('//div[contains(@class, "bloko-text") and contains(@data-qa, "vacancy-serp__vacancy-work-experience")]/text()').get(),
                    'url': url.split('?')[0]
                }