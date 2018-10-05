# Intro

This folder contains some python web scrapers. I mainly use them to scrape the price on different global future exchanges and major news websites (or so-called fake news lol). The key thing for scraping is to figure out the structure of html parse tree of the website and to do data ETL (brainless but exhausting). So far the most efficient way of ETL I found is regular expression. It is much more powerful than beautiful soup (beautiful soup is very good for a clear parsing tree structure tho). When html parsing tree is so fucked up, I personally recommend to convert html content to string and use regular expression instead of buried in multi-layer tree structures. Of course, writing regular expression is a pain in the ass for any human being. 

I used to scrape a lot of websites when I was working in a commodity trading house (not gonna tell you which, but it's pretty famous and the work culture is fucking awful). If you can't get anything from html parse tree, you should inspect element and monitor the network to see if you can track the source (sometimes you could encounter awful hash functions, omg). If this doesn't work, okay, it's javascript. Gotta try selenium then.

# Websites

1. Wall Street Journal WSJ

2. Financial Times FT

3. Bloomberg

4. Reuters

5. Al Jazeera AJ

6. BBC

7. Fortune

8. CNN

9. Chicago Merchantile Exchange CME

10. London Metal Exchange LME

11. Shanghai Future Exchange SHFE

12. Shanghai Gold Exchange SGE

13. The Economist

# Updates

2018/4/9

I had said scraping CME was effortless in CME1.py file. It freaking backfired, lol. CME websites changed its table structure from XML to JSON query. So I had to use a different approach to scrape CME data. The update is called CME2.py.

2018/7/3

I uploaded a new py file called Scrape, ETL, HTML Email from Database.py (okay, this is a shitty name, I admit it). It is designed to scrape several websites and store the information in a local database. And it would automatically sends updates of the information via HTML structured email.

2018/9/21

There is a major change on MENA news feeds.py. Instead of sending an email sorted by sources, I decided to concatnate them together and use graphy theory to extract key information and remove similar contents. This is a cross repo project called Text Mining Project. Please refer to the following link for the details of text mining after scraping.

https://github.com/tattooday/graph-theory/blob/master/Text%20Mining%20project/README.md
