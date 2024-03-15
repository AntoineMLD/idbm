import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from imdb.items import FilmItem


class MonspiderSpider(CrawlSpider):
    name = "monspider"
    allowed_domains = ["www.imdb.com"]
    
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]
    titres_vu = set()

    rules = (
        Rule(LinkExtractor(allow=(r'/title/tt\d+/')), callback="parse_film", follow=True),
    )

    
    def parse_film(self, response):
        
        # Titre du film
        titre_film = response.xpath('//h1[@data-testid="hero__pageTitle"]//span/text()').get()
        if not titre_film:
            titre_film = "titre inconnu"
        # Verifie si le titre a déjà été vu par le spider
        if titre_film in self.titres_vu:
            #si oui alors ne fait rien
            return
        else:
            # si non ajoute dans le set
            self.titres_vu.add(titre_film)

        # Score du film
        score_film = response.xpath('//div[contains(@data-testid, "hero-rating-bar__aggregate-rating__score")]/span/text()').get()
        if not score_film:
            score_film = "score inconnu"

        # Nombre de vote
        nbre_vote_film = response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/following-sibling::div[2]/text()').get()
        if not nbre_vote_film:
            nbre_vote_film = "vote inconnu"

        # Genre du film
        genre_film = response.xpath('//div[@data-testid="genres"]//div//a/span/text()').getall()
        if not genre_film:
            genre_film = "genre inconnu"
        
        # Année, pegi et durée du film
        annee_pegi_duree = response.xpath('//h1/following-sibling::ul[1]//text()').getall()
        if not annee_pegi_duree:
            annee_pegi_duree = "annee, pegi, duree inconnu"
        
        
        # Description du film
        description_film = response.xpath('.//span[contains(@data-testid, "plot-xl")]/text()').get()
        if not description_film:
            description_film = "description inconnu"

        # Extraction des noms des acteurs principaux
        casting_principal = response.xpath('//div[@data-testid="title-cast-item"]//a[@data-testid="title-cast-item__actor"]/text()').extract()
        if not casting_principal:
            casting_principal = "casting inconnu"

        # Language du film
        langue = response.xpath('//li[contains(@data-testid, "title-details-languages")]//a/text()').getall()
        if not langue:
            langue = "langue inconnu"

        # Pays d'origine
        pays = response.xpath('//li[contains(@data-testid, "title-details-origin")]//a/text()').getall()        
        if not pays:
            pays = "pays inconnu"



        item = FilmItem(
        titre=titre_film,
        score=score_film,
        nombre_vote=nbre_vote_film,
        genre=genre_film,
        annee_pegi_duree= annee_pegi_duree,
        description=description_film,
        casting_principal=casting_principal,
        langue=langue,
        pays=pays,
    )

        yield item
            
        
