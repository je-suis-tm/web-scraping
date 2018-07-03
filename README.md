# Web-scraping

This folder contains some python web scrapers. I mainly use them to scrape the price on different future exchanges around the world. The key thing for scraping is to understand the html parse tree of the website and doing ETL. So far the most efficient way of ETL I found is regular expression. It is much more powerful than beautiful soup. Of course, writing regular expression is a pain in the ass. 

I used to scrape a lot of websites, including Shanghai Metals Market, London Metal Exchange, but there is not too much technique to do these. I only keep these three as they are very typical.

1. Chicago Merchantile Exchange CME

2. Shanghai Future Exchange SHFE

3. Shanghai Gold Exchange SGE

# Updates

2018/4/9

Previously I had said scraping CME was effortless. It freaking backfired. CME websites changed its website structure from XML to JSON query. So I had to update the new method to scrape CME which is called CME2.

2018/7/3

Uploaded a new py file called feeds. It is designed to scrape several websites and store the information in a local database. And it only sends updates of the information via email.
