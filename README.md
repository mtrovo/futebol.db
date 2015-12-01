# futebol.db

database and scraping tool for Brazil's Campeonato Brasileiro soccer championship.

How many games are in each year?
```
scrapy runspider --nolog scraper/spiders/__init__.py -o - -t json | grep -o /20dd  | sort | uniq -c
 552 /2003
 552 /2004
 473 /2005
 380 /2006
 380 /2007
 380 /2008
 380 /2009
 380 /2010
 380 /2011
 380 /2012
 380 /2014
```
Note: On 2005 there's more than the official reported games (462) because some
games were subsequently annulled due to a bribering scandal.
Following is the list of games that were played two times:
```
Internacional x Coritiba
Ponte Preta x São Paulo
Fluminense x Brasiliense
Paysandu x Cruzeiro
Juventude x Figueirense
Santos x Corinthians
Juventude x Fluminense
Vasco x Botafogo
Vasco x Figueirense
Cruzeiro x Botafogo
São Paulo x Corinthians
```

