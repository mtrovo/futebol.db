from __future__ import absolute_import
import scrapy
from datetime import date
import re
from scraper.items import Match

FIRST_ROUND_ROBIN = 2003
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
            match_info = SUMMARY_RE.match(summary)
            if not match_info:
                self.log.error("match not found %s", summary)
                return
            self.logger.info('processing match %s', summary)
            home, home_score, visitor_score, visitor = match_info.groups()
            match_date = match.xpath('../time/@datetime')[0].extract()
            round_num = match.xpath('../../@data-rodada')[0].extract()
            location = ''.join(match.xpath('..') \
                               .css('.data-local span[itemprop="name"]::text')\
                               .extract())
            time = match.xpath('..').css('.data-local span.horario::text')[0].extract()

            yield Match(home=home,
                        home_score=home_score,
                        visitor=visitor,
                        visitor_score=visitor_score,
                        championship_round=round_num,
                        location=location,
                        time=time,
                        date=match_date)

