# -*- coding: utf-8 -*-
import scrapy


class Match(scrapy.Item):
    home = scrapy.Field()
    visitor = scrapy.Field()
    home_score = scrapy.Field()
    visitor_score = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    championship_round = scrapy.Field()
