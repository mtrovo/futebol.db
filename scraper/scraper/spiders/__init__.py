from __future__ import absolute_import
import scrapy
from datetime import date
import re
from scraper.items import *

FIRST_ROUND_ROBIN = 2014
CURRENT_YEAR = date.today().year
SUMMARY_RE = summary_re = re.compile(r"^(.*?) (\d+) x\s+(\d+)\s*(.*)$", re.MULTILINE)


class FutpediaSpider(scrapy.Spider):
    name = 'futpedia.globo.com'
    allowed_domains = ['futpedia.globo.com']
    start_urls = ["http://futpedia.globo.com/campeonato/campeonato-brasileiro/%i" % y
                  for y in range(FIRST_ROUND_ROBIN, CURRENT_YEAR)]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        matches = response.css('.lista-classificacao-jogo > a > meta[itemprop="name"]')
        for match in matches:
            summary = match.xpath("@content").extract()[0]
            home, home_score, visitor_score, visitor = self.extract_info_from_summary(summary)
            match_date = match.xpath('../time/@datetime')[0].extract()
            round_num = match.xpath('../../@data-rodada')[0].extract()
            location = ''.join(match.xpath('..') \
                               .css('.data-local span[itemprop="name"]::text')\
                               .extract())
            time = match.xpath('..').css('.data-local span.horario::text')[0].extract()
            match_url = match.xpath('../link[@itemprop="url"]/@href')[0].extract()

            yield scrapy.Request(match_url, callback=self.parse_details)
            yield Match(home=home,
                        home_score=home_score,
                        visitor=visitor,
                        visitor_score=visitor_score,
                        championship_round=round_num,
                        location=location,
                        time=time,
                        date=match_date)

    def extract_info_from_summary(self, summary):
        match_info = SUMMARY_RE.match(summary)
        if not match_info:
            self.log.error("match not found %s", summary)
            return
        self.logger.info('processing match %s', summary)
        return match_info.groups()

    def extract_players(self, players):
        ret = []
        for player in players:
            name = player.css('.jogador::text')[0].extract()
            pos = player.css('.posicao::text')[0].extract()
            ret.append(Player(name=name, position=pos))
        return ret

    def normalize_minutes(self, mins):
        minute, half = mins.split('\'/')
        base = 45 if half[0] == '2' else 0
        return base + min(int(minute), 45)

    def extract_goals(self, game_stats):
        if not game_stats:
            return []

        ret = []
        for goal in game_stats.css('.gol'):
            team = goal.css('.escudo img::attr("alt")')[0].extract()
            player = goal.css('.autor-lance span::text')[0].extract().strip()
            minutes = ''.join(s.strip() for s in goal.xpath('li[@class="tempo-lance"]//text()').extract())
            minutes = self.normalize_minutes(minutes)
            own_goal = len(goal.css('.autor-lance span.contra')) > 0
            ret.append(Goal(team=team,
                            player=player,
                            minutes=minutes,
                            own_goal=own_goal))
        return ret

    def extract_cards(self, game_stats):
        return []

    def parse_details(self, response):
        summary = response.css('h1.placar > meta::attr("content")')[0].extract()
        home, home_score, visitor_score, visitor = self.extract_info_from_summary(summary)
        match_date = response.css('.dados-localizacao > time::attr("datetime")')[0].extract()
        home_players = response.css('#escalacao-mandante > ul.jogadores > li')
        visit_players = response.css('#escalacao-visitante > ul.jogadores > li')
        yield MatchDetails(home=home,
                           visitor=visitor,
                           summary=summary,
                           home_players=self.extract_players(home_players),
                           visit_players=self.extract_players(visit_players),
                           goals=self.extract_goals(response.css('#ficha-jogo .gols')),
                           cards=self.extract_cards(response.css('#ficha-jogo .cartoes')))
