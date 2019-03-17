# Web Scraping

*Since this repository gained unexpected popularity, I would restructure everything slowly to make it more user-friendly. After all, most scripts were written in a very immature way during my early days of Python learning. Meanwhile, please be patient and see if anything that may help you along the way to being a data engineer. Merci beaucoup!*

<br>

## Intro

This folder contains some python web scrapers. I mainly use them to scrape the price on different global future exchanges and major news websites (or so-called fake news lol). The key thing for scraping is to figure out the structure of html parse tree of the website and to do data ETL (brainless but exhausting). So far the most efficient way of ETL I found is regular expression. It is much more powerful than beautiful soup (beautiful soup is very good for a clear parsing tree structure tho). When html parsing tree is so fucked up, I personally recommend to convert html content to string and use regular expression instead of buried in multi-layer tree structures. Of course, writing regular expression is a pain in the ass for any human being. 

I used to scrape a lot of websites when I was working in a commodity trading house (not gonna tell you which, but it's pretty famous and the work culture is fucking awful). If you can't get anything from html parse tree, you should inspect element and monitor the network to see if you can track the source (sometimes you could encounter awful hash functions, omg). If this doesn't work, okay, it's javascript. Gotta try selenium then.

<br>

## Table of Contents

#### Beginner

1. HTML Parse Tree Search (CME1)

2. JSON (CME2)

3. Regular Expression (SHFE)

#### Advanced

1. Sign-in (CQF)

2. Database (LME)

3. Newsfeed (MENA)

#### Notes

1. Proxy Authentication

2. Ethics

<br>

## Available Scrapers

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>1. Wall Street Journal WSJ</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>2. Financial Times FT</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>3. Bloomberg</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>4. Thompson Reuters</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>5. Al Jazeera AJ</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>6. British Broadcasting Corporation BBC</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>7. Fortune</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>8. Cable News Network CNN</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsfeed.py>9. The Economist</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/LME.py>10. London Metal Exchange LME</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/CME2.py>11. Chicago Merchantile Exchange CME</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/SHFE.py>12. Shanghai Future Exchange SHFE</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/CQF.py>13. Certificate in Quantitative Finance CQF</a>


