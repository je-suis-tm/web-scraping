# Intro

This folder contains some python web scrapers. I mainly use them to scrape the price on different global future exchanges and major news websites (or so-called fake news lol). The key thing for scraping is to figure out the structure of html parse tree of the website and to do ETL. So far the most efficient way of ETL I found is regular expression. It is much more powerful than beautiful soup (beautiful soup is very good tho). Of course, writing regular expression is a pain in the ass for any human being. 

I used to scrape a lot of websites when I was working in a commodity trading house (not gonna tell you which, but it's pretty famous and awful), including Shanghai Metals Market (this one is shitty af), London Metal Exchange, but there isn't too much technique to do scraping. If you can't get anything from html parse tree, you should inspect element and monitor the network to see if you can track the source (sometimes you could encounter awful hash functions, omg). If this doesn't work, okay, it's javascript. Gotta try selenium then.

# Websites

1. Chicago Merchantile Exchange CME

2. Shanghai Future Exchange SHFE

3. Shanghai Gold Exchange SGE

4. Reuters

5. Al Jazeera

# Updates

2018/4/9

I had said scraping CME was effortless in CME1.py file. It freaking backfired, lol. CME websites changed its table structure from XML to JSON query. So I had to use a different approach to scrape CME data. The update is called CME2.py.

2018/7/3

I uploaded a new py file called Scrape, ETL, HTML Email from Database.py (okay, this is a shittyname, I admit it). It is designed to scrape several websites and store the information in a local database. And it would automatically sends updates of the information via HTML structured email.
