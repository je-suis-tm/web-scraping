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

1. Wall Street Journal WSJ

2. Financial Times FT

3. Bloomberg

4. Thompson Reuters

5. Al Jazeera AJ

6. British Broadcasting Corporation BBC

7. Fortune

8. Cable News Network CNN

9. The Economist

10. London Metal Exchange LME

11. Chicago Merchantile Exchange CME

12. Shanghai Future Exchange SHFE

13. Certificate in Quantitative Finance CQF


