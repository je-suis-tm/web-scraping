# Web-scraping

This folder contains some python web scrapers. I mainly use them to scrape the price on different future exchanges around the world. The key thing for scraping is to understand the html parse tree of the website and doing ETL. So far the most efficient way of ETL I found is regular expression. It is much more powerful than beautiful soup.

1. Chicago Merchantile Exchange

2. Shanghai Future Exchange

3. Shanghai Gold Exchange

# Updates

2018/4/9

Previously I had said scraping CME was effortless. Now it backfired. CME websites changed its website structure from XML to JSON query. So I updated the new method to scrape CME which is called CME2.
