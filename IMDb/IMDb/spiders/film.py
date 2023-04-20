import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImdbItem
from ..utils import *
import logging

class FilmSpider(CrawlSpider):
    name = "film"
    allowed_domains = ["www.imdb.com"]
    # start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]
    
    film_details = LinkExtractor(restrict_css='.titleColumn > a')
    rule_film_details = Rule(film_details,
                             callback='parse_item',
                             follow=False,
                             )
    rules = (rule_film_details,)
    
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
            'User-Agent': self.user_agent
        })

    def parse_item(self, response):
        try:
            titre = response.css('.sc-afe43def-1.fDTGTb::text').getall()
            titre_original = response.css('.sc-afe43def-3.EpHJp::text').getall()
            score = response.css('.sc-bde20123-1.iZlgcd::text').get()
            genre = response.css('.ipc-chip__text::text').getall()
            annee = response.xpath('//div[@class="sc-385ac629-3 kRUqXl"]/div/ul/li/a/text()').get()
            duree= response.css('.ipc-inline-list__item::text').get()
            descriptions = response.css('.sc-5f699a2-1.cfkOAP::text').get().strip()
            acteurs = response.xpath("(//li[@data-testid='title-pc-principal-credit'])[last()]//a/text()")[1:].getall()
            public = response.xpath('//div[@class="sc-385ac629-3 kRUqXl"]/div/ul/li[2]/a/text()').get()
            pays = response.xpath('//div[@data-testid="title-details-section"]//ul//li[@data-testid="title-details-origin"]//div/ul//li[@role="presentation"]/a/text()').get()
            langue = response.xpath('//div[@data-testid="title-details-section"]//ul//li[@data-testid="title-details-languages"]/div/ul/li/a/text()').get()
            # items = ImdbItem()
            yield {
                'titre' :  ''.join(titre),
                'titre_original' : titre_original,
                'score' : score,
                'genre' : drop_back_to_top(str(genre)),
                'annee' : annee,
                'duree':temps_en_minutes(duree),
                'descriptions' : descriptions,
                'acteurs' : split_comma(str(acteurs)),
                'public' : public,
                'pays': pays,
                'langue': langue,
            }
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            logging.error(f"URL causing the error: {response.url}")
