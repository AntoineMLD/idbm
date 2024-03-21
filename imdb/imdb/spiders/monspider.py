import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from imdb.items import FilmItem
from urllib.parse import urlparse, parse_qs
import re

class MonspiderSpider(CrawlSpider):
    name = "monspider"
    handle_httpstatus_list = [503]
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]
    urls_vues = set() 
    rules = (
        Rule(LinkExtractor(allow=(r'/title/tt\d+/'), deny=(r'/title/tt\d+/[a-z]+')), callback="parse_film", follow=True),)
    

    def parse_film(self, response):

        
        url = response.url

        if re.search(r'ref_=tt_sims_tt_[it]_\d{1,2}', response.url):
            self.logger.info(f"URL exclue à cause des paramètres de requête spécifiques : {response.url}")
            return  # Ignore cette page si elle contient les paramètres spécifiés

        if response.url in self.urls_vues:
            self.logger.info(f"URL déjà visitée : {response.url}")
            return

        self.urls_vues.add(response.url)

                        
        # Titre du film
        titre_film = response.xpath('//h1[@data-testid="hero__pageTitle"]//span/text()').get() or "No Title"
        
            

        # Score du film
        score_film = response.xpath('//div[contains(@data-testid, "hero-rating-bar__aggregate-rating__score")]/span/text()').get() or "0"

        # Nombre de vote
        nbre_vote_film = response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/following-sibling::div[2]/text()').get() or "0"

        # Genre du film
        genre_film = response.xpath('//div[@data-testid="genres"]//div//a/span/text()').getall() or ["No kind"]
        
        # Description du film
        description_film = response.xpath('.//span[contains(@data-testid, "plot-xl")]/text()').get() or "No Description"

        # Casting principal
        casting_principal = response.xpath('//div[@data-testid="title-cast-item"]//a[@data-testid="title-cast-item__actor"]/text()').extract() or ["No Casting"]

        # Langue du film
        langue = response.xpath('//li[contains(@data-testid, "title-details-languages")]//a/text()').getall() or ["No Language"]

        # Pays d'origine
        pays = response.xpath('//li[contains(@data-testid, "title-details-origin")]//a/text()').getall() or ["No Country"]

        # Pegi du film et séries
        pegi_serie = response.xpath('//h1/following-sibling::ul/li[3]/a/text()').get() or "No Pegi"
        pegi_film = response.xpath('//h1/following-sibling::ul[1]/li[2]//text()').get() or "No Pegi"
        
        # Heure du film et séries
        duree_serie = response.xpath('//h1/following-sibling::ul/li[4]/text()').get() or response.xpath('//h1/following-sibling::ul/li[3]/text()') or "0"
        duree_film = response.xpath('//h1/following-sibling::ul[1]/li[3]//text()').get() or "0"

        # Saisons des séries
        saisons = response.xpath('//div[@data-testid="episodes-browse-episodes"]/div/following-sibling::div/a/following-sibling::span/span/label/text()').get() or "No saisons"

        annee_serie = response.xpath('//div[@data-testid="title-details-section"]/following-sibling::ul[2]/li/text()').get() or response.xpath('//h1/following-sibling::ul/li[2]/a/text()').get() or "0"
        
        annee_film = response.xpath('//h1/following-sibling::ul[1]/li[1]//text()').get() or "0"

        # détermine si c'est une série ou un film
        is_type = response.xpath('//h1/following-sibling::ul[1]/li[contains(., "TV Series")]')
        if is_type:
            type_ = "Série TV"
            annee = annee_serie
            pegi = pegi_serie
            duree = duree_serie
            saisons = saisons
        else:
            type_ = "Film"
            annee = annee_film
            pegi = pegi_film
            duree = duree_film
            saisons = None
        
        
        if type_ == "Video Game":
            self.logger.info(f"Skipping video game page: {response.url}")
            return
        

        
        item = FilmItem(
            titre=titre_film,
            genre=genre_film,
            type_=type_,
            pegi=pegi,
            duree=duree,
            saisons=saisons,
            annee=annee,
            score=score_film,
            nombre_vote=nbre_vote_film,
            description=description_film,
            casting_principal=casting_principal,
            langue=langue,
            pays=pays,
            url=url,
            
            
            
        )

        yield item


