# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IngatlanItem(scrapy.Item):
    id = scrapy.Field()
    cim = scrapy.Field()
    terulet = scrapy.Field()    # int
    szobak = scrapy.Field()     # [int (egesz szoba), int (felszoba)]
    ar = scrapy.Field()         # int
    tipus = scrapy.Field()      # tegla, panel, csusztatott zsalus

    allapot = scrapy.Field()    # jo allapotu, felujitott, ujszeru, jo allapotu
    komfort = scrapy.Field()    # osszkomfortos, duplakomfortos
    emelet = scrapy.Field()     # foldszint, felemelet, int
    szintek = scrapy.Field()
    lift = scrapy.Field()
    belmagassag = scrapy.Field()
    futes = scrapy.Field()  # gaz (konvertor), gaz (cirko), kozponti egyedi mukodessel, kozponti,
    legkondi = scrapy.Field()
    akadaly = scrapy.Field()
    wc = scrapy.Field()
    tajolas = scrapy.Field()
    kilatas = scrapy.Field()    # udvari, kertre nezo, utcai
    kert = scrapy.Field()
    tetoter = scrapy.Field()    # nem, nem tetoteri, igen
    parkolas = scrapy.Field()
    erkely = scrapy.Field()

    mezok = scrapy.Field()