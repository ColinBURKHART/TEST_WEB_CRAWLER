import scrapy

# domaine et site accepter
class SpiderSpider(scrapy.Spider):
    name = 'tests'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']


    def parse(self, response):
        # Recherche d'une section
        all_books = response.xpath('//article[@class="product_pod"]')

        # Demande d'extraction d'information
        for book in all_books:
            title = book.xpath('.//h3/a/@title').extract_first()
            price = book.xpath('.//div/p[@class="price_color"]/text()').extract_first()
            print(title)
            print(price)
