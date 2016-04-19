# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IngatlanItem(scrapy.Item):
    cim = scrapy.Field()
    terulet = scrapy.Field()
    szobak = scrapy.Field()
    ar = scrapy.Field()

    allapot = scrapy.Field()
    komfort = scrapy.Field()
    emelet = scrapy.Field()
    szintek = scrapy.Field()
    lift = scrapy.Field()
    belmagassag = scrapy.Field()
    futes = scrapy.Field()
    legkondi = scrapy.Field()
    akadaly = scrapy.Field()
    wc = scrapy.Field()
    tajolas = scrapy.Field()
    kilatas = scrapy.Field()
    kert = scrapy.Field()
    tetoter = scrapy.Field()
    parkolas = scrapy.Field()

    cimsor = scrapy.Field()