# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FilmItem(scrapy.Item):
    
    titre=scrapy.Field()
    genre = scrapy.Field()
    type_= scrapy.Field()
    pegi= scrapy.Field()
    duree= scrapy.Field()
    saisons= scrapy.Field()
    annee= scrapy.Field()
    score= scrapy.Field()
    nombre_vote= scrapy.Field()
    description= scrapy.Field()
    casting_principal= scrapy.Field()
    langue= scrapy.Field()
    pays= scrapy.Field()
    details= scrapy.Field()
    url=scrapy.Field()
    

    

