import scrapy


class ScrapemeSpider(scrapy.Spider):
    name = "scrapeme"
    allowed_domains = ["scrapeme.live"]
    start_urls = ["https://scrapeme.live/shop/"]

    def parse(self, response):
        products =  response.css('li.product')
        for product in products:
            # get the two price text nodes (currency + cost) and
            # contatenate them
            price_text_elements = product.css(".price *::text").getall()
            price = "".join(price_text_elements)

            # return a generator for the scraped item
            yield {
                "name": product.css("h2::text").get(),
                "image": product.css("img").attrib["src"],
                "price": price,
                "url": product.css("a").attrib["href"],
            }

        next_page = response.css('a.next  ::attr(href)').get()
        if next_page is not None:
            next_page_url = next_page
            yield response.follow(next_page_url, callback=self.parse)