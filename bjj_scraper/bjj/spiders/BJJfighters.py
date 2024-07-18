from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor 

class BJJfightersSpider(CrawlSpider):
    name = 'BJJfighters'
    allowed_domains = ['bjjheroes.com']
    start_urls = ['https://www.bjjheroes.com/a-z-bjj-fighters-list']

    rules = (
        Rule(LinkExtractor(allow=r'/?p'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        yield { 
            'URL':response.url
        }

       
