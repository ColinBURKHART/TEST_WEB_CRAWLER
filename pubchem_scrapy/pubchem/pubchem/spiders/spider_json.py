import scrapy
import scra
from scrapy_headless import SeleniumRequest
import time


class Spider(scrapy.Spider):
    name = "scrapy_selenium"

    def start_requests(self):
        search_value = '57-27-2'
        start_url = "https://pubchem.ncbi.nlm.nih.gov/#query=" + search_value
        yield SeleniumRequest(
            url= start_url,
            wait_time=3,
            screenshot=True,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        time.sleep(10)
        result = response.xpath('//*[@id="collection-results-container"]/div/div/div[1]/div/div[1]/div/div[1]/span')
        print(result)



