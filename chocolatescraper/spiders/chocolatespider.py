import scrapy
from chocolatescraper.items import ChocolateProduct
from chocolatescraper.itemloaders import ChocolateProductLoader


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://chocolate.co.uk/collections/all/"]

    def parse(self, response):

        products = response.css("product-item")

        # product_item = ChocolateProduct()

        for product in products:
            
            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=product)
            chocolate.add_css('name', 'a.product-item-meta__title::text'),
            chocolate.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>'),
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)'),
            
            # product_item['name'] = product.css("a.product-item-meta__title::text").get(),
            # product_item['price'] = product.css("span.price").get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>', '').replace('</span>', ''),
            # product_item['url'] = product.css("div.product-item-meta a").attrib["href"],

            yield chocolate.load_item()
            # yield product_item

        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url =  'https://www.chocolate.co.uk' + next_page

            yield response.follow(next_page_url, callback=self.parse)
