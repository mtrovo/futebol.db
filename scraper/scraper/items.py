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

class Player(scrapy.Item):
    name = scrapy.Field()
    position = scrapy.Field()

class Goal(scrapy.Item):
    team =scrapy.Field()
    player =scrapy.Field()
    minutes =scrapy.Field()
    own_goal =scrapy.Field()

class MatchDetails(scrapy.Item):
    home = scrapy.Field()
    visitor = scrapy.Field()
    summary = scrapy.Field()
    date = scrapy.Field()
    home_players = scrapy.Field()
    visit_players = scrapy.Field()
    goals = scrapy.Field()
    cards = scrapy.Field()

