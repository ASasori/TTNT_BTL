from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "myfirstcrawler"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    #PROXY_SERVER = "127.0.0.1"
    rules = (
        Rule(LinkExtractor(allow="catalogue/category")),
        Rule(LinkExtractor(allow="catalogue",deny="category"), callback="parse_item")
    )
    def parse_item(self,response):
        yield {
            "title":response.css(".product_main h1::text").get(),
            "price":response.css(".price_color::text").get(),
            "availability":response.css(".availability::text")[1].get().replace("\n","").replace(" ",""),
            "description":response.xpath("//p[string-length(normalize-space(text())) > 100]/text()").get()
        }