import scrapy


class JumiaSpider(scrapy.Spider):
    name = 'JumiaSpider'
    allowed_domains = ['jumia.com.ng']
    # start_urls = ['https://www.jumia.com.ng/televisions/']
    start_urls = ['https://www.jumia.com.ng/printers-scanners/']
    search_term = 'infinix'

    def check_if_product_matches_user_term(self, product):
        brand = product.css('a .title .brand::text').extract_first()
        name = product.css('a .title .name::text').extract_first()
        is_match = str(self.search_term).lower() in str(brand).lower() or str(self.search_term).lower() in str(name).lower()
        return is_match

    def go_to_next_page(self, response):
        pass

    def parse(self, response):
        products = response.css('.sku.-gallery')
        for product in products:
            if self.check_if_product_matches_user_term(product):
                link = {
                    'link': product.css('a::attr(href)').extract_first(),
                    'old_price': product.css('a .price-container .price:nth-child(2) span:nth-child(2)::attr(data-price)').extract_first(),
                    'new_price': product.css('a .price-container .price:first-child span:nth-child(2)::attr(data-price)').extract_first(),
                }
                yield link
        next_page_url = response.css('.pagination .item:last-child a::attr(href)').extract_first()
        yield scrapy.Request(url=next_page_url, callback=self.parse)


