import scrapy


class JumiaSpider(scrapy.Spider):
    name = 'JumiaSpider'
    allowed_domains = ['jumia.com.ng']
    start_urls = ['https://www.jumia.com.ng/televisions/']
    results = []
    # start_urls = ['https://www.jumia.com.ng/printers-scanners/']

    def check_if_product_price_meets(self, product):
        old_price = product.get('old_price', 0)
        new_price = product.get('new_price', 0)
        old_price = float(old_price) if old_price else 0
        new_price = float(new_price) if new_price else 0
        
        discount = 0
        if old_price > 0:
            discount = ((old_price - new_price) / old_price) * 100
            
        if discount > 90 or 3499 < new_price <= 3502 or 3499 < old_price <= 3502 or old_price == 339990:
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
                self.results.append(link['link'])
                yield link
        next_page_url = response.css('.pagination .item:last-child a::attr(href)').extract_first()
        yield scrapy.Request(url=next_page_url, callback=self.parse)
        print(self.results)


