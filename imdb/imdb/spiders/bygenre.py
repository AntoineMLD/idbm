import scrapy


class BygenreSpider(scrapy.Spider):
    name = "bygenre"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/feature/genre/?ref_=nv_ch_gr"]

    def parse(self, response):
        pass
