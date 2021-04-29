import scrapy
from scrapy_selenium import SeleniumRequest


class Spider(scrapy.Spider):
    name = "scrapy_selenium"

    def start_requests(self):
        search_value = 'InChI=1S/C3H6O/c1-3(2)4/h1-2H3'
        start_url = "https://pubchem.ncbi.nlm.nih.gov/#query=" + search_value
        yield SeleniumRequest(
            url= start_url,
            wait_time=3,
            screenshot=True,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response:
        print(response.request.meta['driver'].title)
