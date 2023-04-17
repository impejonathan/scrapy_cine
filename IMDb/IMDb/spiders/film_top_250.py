import scrapy


class ImbdSpiderSpider(scrapy.Spider):
    name = "imbd_spider"
    allowed_domains = ["imbd.com"]
    start_urls = ["http://imbd.com/"]

    def parse(self, response):
        pass
