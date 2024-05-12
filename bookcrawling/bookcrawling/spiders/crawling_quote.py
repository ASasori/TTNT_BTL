from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
class QuoteSpider(CrawlSpider):
    name = 'quote-spider'
    allowed_domains = ["toscrape.com"]
    start_urls = ['https://quotes.toscrape.com']

    rules = (
        #Rule(LinkExtractor(allow=""), callback="parse"),
        Rule(LinkExtractor(allow=""), callback="parse_tag"),
    )

    def parse(self, response):
        QUOTE_SELECTOR = '.quote'
        TEXT_SELECTOR = '.text::text'
        AUTHOR_SELECTOR = '.author::text'
        
        for quote in response.css(QUOTE_SELECTOR):
            yield {
                #'quote': quote.css(TEXT_SELECTOR).get(),
                'text': quote.css(TEXT_SELECTOR).get(),
                'author': quote.css(AUTHOR_SELECTOR).get(),
            }
    def parse_tag(self, response):
        QUOTE_SELECTOR = '.quote'
        TEXT_SELECTOR = '.text::text'
        AUTHOR_SELECTOR = '.author::text'
        ABOUT_SELECTOR = '.author + a::attr("href")'
        TAGS_SELECTOR = '.tags > .tag::text'
        NEXT_SELECTOR = '.next a::attr("href")'

        for quote in response.css(QUOTE_SELECTOR):
            yield {
                'text': quote.css(TEXT_SELECTOR).extract_first(),
                'author': quote.css(AUTHOR_SELECTOR).extract_first(),
                'about': 'https://quotes.toscrape.com' + 
                        quote.css(ABOUT_SELECTOR).extract_first(),
                'tags': quote.css(TAGS_SELECTOR).extract(),
            }

        next_page = response.css(NEXT_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
            )