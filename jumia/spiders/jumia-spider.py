import scrapy


class JumiaSpider(scrapy.Spider):
    name = 'JumiaSpider'
    allowed_domains = ['jumia.com.ng']
    # start_urls = ['https://www.jumia.com.ng/televisions/']
    start_urls = ['https://www.jumia.com.ng/printers-scanners/']

    def check_if_product_price_meets(self, product):
        old_price = product.get('old_price', 0)
        new_price = product.get('new_price', 0)
        if new_price < 4000 or (old_price - new_price / old_price) * 100 > 90 or new_price == 3500 or old_price == 3500 or old_price == 339990 or new_price == 339990:
            return True
        return False

    def go_to_next_page(self, response):
        pass

    def parse(self, response):
        products = response.css('.sku.-gallery')
        for product in products:
            link = {
                'link': product.css('a::attr(href)').extract_first(),
                'old_price': product.css(
                    'a .price-container .price:nth-child(2) span:nth-child(2)::attr(data-price)').extract_first(),
                'new_price': product.css(
                    'a .price-container .price:first-child span:nth-child(2)::attr(data-price)').extract_first(),
            }
            if self.check_if_product_price_meets(link):
                yield link
        next_page_url = response.css('.pagination .item:last-child a::attr(href)').extract_first()
        yield scrapy.Request(url=next_page_url, callback=self.parse)


