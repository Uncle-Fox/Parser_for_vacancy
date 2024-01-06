from typing import Iterable
import scrapy
from urllib.parse import urlparse
import time
from scrapy.http import Request
import logging

logging.basicConfig(level=logging.INFO, filename="Scrapy_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

# logging.debug("A DEBUG Message")
# logging.info("An INFO")
# logging.warning("A WARNING")
# logging.error("An ERROR")
# logging.critical("A message of CRITICAL severity")

class ScrapyspiderSecondversionHhSpider(scrapy.Spider):
    name = "ScrapySpider_SecondVersion_hh"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?text=программист+python&area=113&customDomain=1&page="]

    def start_requests(self) -> Iterable[Request]:
        logging.info("An INFO: Start to Scrapy")
        count = 1
        base_url = self.start_urls[0]
        for page_number in range (1, 40):
            url = f"{base_url}{page_number}"
            yield scrapy.Request(url=url, callback=self.parse)
            logging.info(f"Successfully finished scrap № {count}")
            count += 1
            #time.sleep(1)

    def parse(self, response):
        vacancys = response.xpath('//div[contains(@class, "vacancy-serp-item")]')
        processed_urls = set()
        for vacancy in vacancys:
            url = vacancy.xpath('.//span/a[contains(@data-qa, "serp-item__title") and contains(@class, "serp-item__title")]/@href').extract_first()
            if url and url not in processed_urls:
                processed_urls.add(url)
                yield scrapy.Request(url=url, callback=self.parse_details, cb_kwargs={'url': url})
                
                
    def parse_details(self, response, url):
        yield {
            'name': response.xpath('.//span/a[contains(@data-qa, "serp-item__title") and contains(@class, "serp-item__title")]/text()').get(),
            'salary': ' '.join(response.xpath('.//span[contains(@data-qa, "vacancy-serp__vacancy-compensation")]/text()').getall()),
            'company': response.xpath('.//a[@class="bloko-link bloko-link_kind-tertiary"]/text()').get(),
            'city': response.xpath('.//div[@class="bloko-text"]/text()').get(),
            'exp': response.xpath('//div[contains(@class, "bloko-text") and contains(@data-qa, "vacancy-serp__vacancy-work-experience")]/text()').get(),
            'skills': ' '.join(response.xpath('//span[@class="bloko-tag__section bloko-tag__section_text"]/text()').getall()),
            'url': url.split('?')[0]
        }

#запрос для всех навыков: ' '.join(response.xpath('//span[@class="bloko-tag__section bloko-tag__section_text"]/text()').getall()) 