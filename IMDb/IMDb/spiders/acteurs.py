import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImdbItem

class FilmSpider(CrawlSpider):
    name = "films_top_250_only_actors"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]
    
    film_details = LinkExtractor(restrict_css='.titleColumn > a')
    rule_film_details = Rule(film_details,
                             callback='parse_item',
                             follow=False,
                             )
    rules = (rule_film_details,)
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
            'User-Agent': self.user_agent
        })

    def parse_item(self, response):
        # all_responses = response.css('.titleColumn a')
        # items = ImdbItem()
        yield {
        # for response in all_responses:
        
        # 'acteurs' : response.css('.ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link::text').extract(),
        'acteurs' : response.xpath("(//li[@data-testid='title-pc-principal-credit'])[last()]//a/text()")[1:].extract(),
        }
           

       