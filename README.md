# Web Scraping

*The readme is still under renovation. Please be patient as I am quite busy (lazy) at the moment. Merci beaucoup!*

<br>

## Intro

My understanding of web scraping is patience and attention to details. Scraping is not rocket science (deep learning is). When I do scraping, I typically spend 50% of my time in analyzing the source (navigate through HTML parse tree or inspect element to find the post form) and the rest 50% in ETL. The process does not require much brain power but it is quite time-consuming. Again, patience and attention to details matter. 

This repository contains a couple of python web scrapers. These scrapers mainly target at different commodity future exchanges and influential media websites (or so-called fake news, lol). Most scripts were written during my early days of Python learning. Since this repository gained unexpected popularity, I have restructure everything to make it more user-friendly. All the scripts featured in this repository are ready for use. Each script is designed to feature a unique technique that I found useful throughout my experience of data engineering. 

Scripts inside this repository are classified into two groups, beginner and advanced. At the beginning, the script is merely about some technique to extract the data. As you progress, the script leans more towards data architect and other functions to improve the end product. If you are experienced or simply come to get scrapers for free, you may want to skip the content and just look at <a href= https://github.com/je-suis-tm/web-scraping#available-scrapers>available scrapers</a>. If you are here to learn, you may look at <a href= https://github.com/je-suis-tm/web-scraping#table-of-contents>table of contents</a> to determine which suits you best. In addition, there are some <a href= https://github.com/je-suis-tm/web-scraping#notes>notes</a> on the annoying issues such as proxy authentication (usually corporate or university network) and legality (hopefully you won’t come to that).

<br>

## Table of Contents

#### Beginner

<a href=https://github.com/je-suis-tm/web-scraping#1-html-parse-tree-search-cme1>1. HTML Parse Tree Search (CME1)</a>

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

## Beginner

#### 1. HTML Parse Tree Search (CME1)

Tree is an abstract data type in computer science. Now that you are a programmer, Binary Tree and AVL Tree must feel like primary school math (haha, I am joking, tree is my worst nightmare when it comes to interview). For a webpage, if you right click and select view source (CTRL+U in both IE & Chrome), you will end up with a bunch of codes like this.

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme1%20html.PNG)

The codes are written in HTML. The whole HTML script is a tree structure as well. The HTML parse tree looks like this. 

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme1%20tree.png)

There is something interesting about HTML parse tree. The first word after the left bracket is HTML tag (in tree structure we call it node). In most cases, tags come in pairs. Of course, there are some exceptions such as line break tag `<br>` or doc type tag ` <!DOCTYPE>`. Usually the opening tag is just tag name but the closing tag has a slash before the name. Different tag names represent different functionalities. In most cases, there are only a few tags that contain information we need, e.g., tag `<div>` usually defines a table, tag `<a>` creates a hyperlink (the link is at attribute `href` and it may skip prefix if the prefix is the same as current URL), tag `<img>` comes up with a pic (the link is hidden in attribute `src`), tag `<p>` or `<h1>`-`<h6>` normally contains text. For more details of tagging, please refer to <a href= https://www.w3schools.com/tags/default.asp>w3schools</a>.

It is vital to understand the basics of HTML parse tree because most websites with simple layout can easily be traversed via a library called BeautifulSoup. When we use urllib or other packages to request a specific website via python, we end up with HTML parse tree in bytes. When the bytes are parsed to BeautifulSoup, it makes life easier. It allows us to search the tag name and other attributes to get the content we need. The link to the documentation of BeautifulSoup is <a href= https://www.crummy.com/software/BeautifulSoup/bs4/doc>here</a>.

For instance, we would love to get the link to quiz on Dragon Ball, we can do

`result.find(‘div’,class_=’article article__list old__article-square’).find(‘a’).get(‘href’)`

Here, result is a BeautifulSoup object. The attribute `find` returns the first matched tag. The attribute `get` enables us to seek for attributes inside a tag.

Or we are interested in all the titles of the articles, we do

`temp=result.find(‘div’,class_=’article article__list old__article-square’).find_all(‘a’)` 

`output=[i.text for i in temp]`

The attribute `find_all` returns all the matched results. Note that the second article has a subtitle ‘subscriber only’, we will have a rather longer title for the second article. 

You can refer to <a href= https://github.com/je-suis-tm/web-scraping/blob/master/CME1.py>CME1</a> for more details. Please note that CME1 is an outdated script for Chicago Mercantile Exchange. Due to the change of the website, you cannot go through HTML parse tree to extract data any more. Yet, the concept of HTML parse tree is still applicable to other cases.
