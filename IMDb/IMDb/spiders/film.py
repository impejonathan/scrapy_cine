import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImdbItem

class FilmSpider(CrawlSpider):
    name = "film"
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
        'titre' :  response.css('.sc-afe43def-1.fDTGTb::text').extract(),
        'titre_original' : response.css('.sc-afe43def-3.EpHJp::text').extract(),
        'score' : response.css('.sc-bde20123-1.iZlgcd::text').extract_first(),
        'genre' : response.css('.ipc-chip__text::text').extract(),
        'annee' : response.xpath('//div[@class="sc-385ac629-3 kRUqXl"]/div/ul/li/a/text()').extract_first(),
        'duree': response.css('.ipc-inline-list__item::text').extract_first(),
        'descriptions' : response.css('.sc-5f699a2-1.cfkOAP::text').extract_first().strip(),
        'acteurs' : response.xpath("(//li[@data-testid='title-pc-principal-credit'])[last()]//a/text()")[1:].extract(),
        'public' : response.xpath('//div[@class="sc-385ac629-3 kRUqXl"]/div/ul/li[2]/a/text()').extract(),
        'pays' : response.xpath('//div[@data-testid="title-details-section"]//ul//li[@data-testid="title-details-origin"]//div/ul//li[@role="presentation"]/a/text()').extract_first(),
        
        'langue' : response.xpath('//div[@data-testid="title-details-section"]//ul//li[@data-testid="title-details-languages"]/div/ul/li/a/text()').extract_first()
        }

       