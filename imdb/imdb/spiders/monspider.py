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
        titre_film = response.xpath('//h1[@data-testid="hero__pageTitle"]//span/text()').get() or "No Title"
        if titre_film is None or titre_film in self.titres_vu:
            # Si le titre est inconnu ou déjà vu, ne fait rien
            return
        else:
            self.titres_vu.add(titre_film)
            

        # Score du film
        score_film = response.xpath('//div[contains(@data-testid, "hero-rating-bar__aggregate-rating__score")]/span/text()').get() or "No Score"

        # Nombre de vote
        nbre_vote_film = response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/following-sibling::div[2]/text()').get() or "No vote's number"

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
        duree_serie = response.xpath('//h1/following-sibling::ul/li[4]/text()').get() or "No Time"
        duree_film = response.xpath('//h1/following-sibling::ul[1]/li[3]//text()').get() or "No Time"

        # Saisons des séries
        saisons = response.xpath('//div[@data-testid="episodes-browse-episodes"]/div/following-sibling::div/a/following-sibling::span/span/label/text()').get() or "No saisons"

        # déterminer si c'est une série ou un film
        is_serie = response.xpath('//h1/following-sibling::ul[1]/li[contains(., "TV Series")]')
        if is_serie:
            serie = "Série TV"
            annee_serie = response.xpath('//h1/following-sibling::ul/li[2]/a/text()').get() or "No years"
            annee_film = None  
            pegi = pegi_serie
            duree = duree_serie
            saisons = saisons
        else:
            serie = "Film"
            annee_film = response.xpath('//h1/following-sibling::ul[1]/li[1]//text()').get() or "No years"
            annee_serie = None
            pegi = pegi_film
            duree = duree_film
            saisons = None

        
        

        
        item = FilmItem(
            titre=titre_film,
            genre=genre_film,
            serie=serie,
            pegi=pegi,
            duree=duree,
            saisons=saisons,
            annee=annee_film,
            annee_serie=annee_serie,
            score=score_film,
            nombre_vote=nbre_vote_film,
            description=description_film,
            casting_principal=casting_principal,
            langue=langue,
            pays=pays,
        )

        yield item
