import scrapy
from shutil import which

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    search_compound = 'C1=CC=C(C=C1)C=O'
    allowed_domains = ['pubchem.ncbi.nlm.nih.gov/']
    start_urls = ['http://pubchem.ncbi.nlm.nih.gov//#query='+search_compound]

    def parse(self, response):
        print(response.status)
        print(response.xpath('//div]'))

