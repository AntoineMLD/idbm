import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MonspiderSpider(CrawlSpider):
    name = "monspider"
    allowed_domains = ["www.imdb.com"]
    #start_urls = ["https://www.imdb.com/"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    rules = (
        Rule(LinkExtractor(allow=(r'/title/tt\d+/')), callback="parse_film", follow=True),
    )

    def parse_start_url(self, response):
        # Cibler le <ul> contenant la liste des films
        liste_films = response.xpath('//ul[contains(@class, "ipc-metadata-list") and contains(@class, "compact-list-view")]')
        
        # Itérer sur chaque <li> qui représente un film dans la liste
        for film in liste_films.xpath('./li'):
        
            


            yield {
                
                
            }

    def parse_film(self, response):
        '''Titre
            Titre original
            Score
            Genre
            Année
            Durée
            Descriptions(synopsis)
            Acteurs(Casting principal)
            Public
            Pays
            [facultatif] Langue d’origine
            '''
        # Titre du film
        titre_film = response.xpath('//span[@data-testid="hero__primary-text"]/text()').get()

        # Score du film
        score_film = response.xpath('//div[contains(@data-testid, "AggregateRatingButton__RatingScore")]/text()').get()

        # Nombre de vote
        nbre_vote_film = response.xpath('//div[contains(@class, "sc-bde20123-")]/text()').get()

        # Genre du film
        genre_film = response.xpath('.//span[contains(@class, "ipc-chip__text")]/text()').get()

        # récolte dans un même champ : année et pegi
        ul_selector = response.xpath("//ul[contains(@class, 'ipc-inline-list') and contains(@class, 'ipc-inline-list--show-dividers') and contains(@class, 'sc-d8941411-2') and contains(@class, 'cdJsTz') and contains(@class, 'baseAlt')]")

        annee_pegi = ul_selector.xpath('.//li/a/text()').getall()

        # Durée du film
        duree_film = response.xpath('.//li[contains(@class, "ipc-inline-list__item")]/text()').get()



        yield {
            'titre': titre_film,
            'score': score_film,
            'nombre_vote': nbre_vote_film,
            'genre': genre_film,
            'année, pegi': annee_pegi,
            'durée' : duree_film
            
        }
            
        
