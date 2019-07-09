# Web Scraping

*The readme is still under renovation. Please be patient as I am quite busy (lazy) at the moment. Veuillez patienter. Merci beaucoup!*

<br>

## Intro

My understanding of web scraping is patience and attention to details. Scraping is not rocket science (deep learning is). When I do scraping, I typically spend 50% of my time in analyzing the source (navigate through HTML parse tree or inspect element to find the post form) and the rest 50% in ETL. The most useful tools for me are `requests`, `bs4` and `re`. Some people may recommend `selenium` for non-static website. To be honest, I have never used `selenium` throughout my career, but dynamic websites like Facebook and Twitter are still within my grasp. You see? patience and attention to details matter. 

This repository contains a couple of python web scrapers. These scrapers mainly target at different commodity future exchanges and influential media websites (or so-called fake news, lol). Most scripts were written during my early days of Python learning. Since this repository gained unexpected popularity, I have restructured everything to make it more user-friendly. All the scripts featured in this repository are ready for use. Each script is designed to feature a unique technique that I found useful throughout my experience of data engineering. 

Scripts inside this repository are classified into two groups, beginner and advanced. At the beginning, the script is merely about some technique to extract the data. As you progress, the script leans more towards data architect and other functions to improve the end product. If you are experienced or simply come to get scrapers for free, you may want to skip the content and just look at <a href= https://github.com/je-suis-tm/web-scraping#available-scrapers>available scrapers</a>. If you are here to learn, you may look at <a href= https://github.com/je-suis-tm/web-scraping#table-of-contents>table of contents</a> to determine which suits you best. In addition, there are some <a href= https://github.com/je-suis-tm/web-scraping#notes>notes</a> on the annoying issues such as proxy authentication (usually corporate or university network) and legality (hopefully you won’t come to that).

<br>

## Table of Contents

#### Beginner

<a href=https://github.com/je-suis-tm/web-scraping#1-html-parse-tree-search-cme1>1. HTML Parse Tree Search (CME1)</a>

<a href=https://github.com/je-suis-tm/web-scraping#2-json-cme2>2. JSON (CME2)</a>

<a href=https://github.com/je-suis-tm/web-scraping#3-regular-expression-shfe>3. Regular Expression (SHFE)</a>

#### Advanced

<a href=https://github.com/je-suis-tm/web-scraping#1-sign-in-cqf>1. Sign-in (CQF)</a>

<a href=https://github.com/je-suis-tm/web-scraping#2-database-lme>2. Database (LME)</a>

<a href=https://github.com/je-suis-tm/web-scraping#3-newsletter-mena>3. Newsletter (MENA)</a>

#### Notes

<a href=https://github.com/je-suis-tm/web-scraping#1-proxy-authentication>1. Proxy Authentication</a>

<a href=https://github.com/je-suis-tm/web-scraping#2-ethics>2. Ethics</a>

<br>

## Available Scrapers

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsletter.py>1. Wall Street Journal WSJ</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsletter.py>2. Financial Times FT</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsletter.py>3. Bloomberg</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsletter.py>4. Thompson Reuters</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsletter.py>5. Al Jazeera AJ</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsletter.py>6. British Broadcasting Corporation BBC</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsletter.py>7. Fortune</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsletter.py>8. Cable News Network CNN</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/MENA%20Newsletter.py>9. The Economist</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/LME.py>10. London Metal Exchange LME</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/CME2.py>11. Chicago Mercantile Exchange CME</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/SHFE.py>12. Shanghai Future Exchange SHFE</a>

<a href=https://github.com/je-suis-tm/web-scraping/blob/master/CQF.py>13. Certificate in Quantitative Finance CQF</a>

<br>

## Beginner

#### 1. HTML Parse Tree Search (CME1)

Tree is an abstract data type in computer science. Now that you are a programmer, Binary Tree and AVL Tree must feel like primary school math (haha, I am joking, tree is my worst nightmare when it comes to interview). For a webpage, if you right click and select view source (CTRL+U in both IE & Chrome), you will end up with a bunch of codes like this.

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme1%20html.PNG)

The codes are written in HTML. The whole HTML script is a tree structure as well. The HTML parse tree looks like this. 

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme1%20tree.png)

There is something interesting about HTML parse tree. The first word after the left bracket is HTML tag (in tree structure we call it node). In most cases, tags come in pairs. Of course, there are some exceptions such as line break tag `<br>` or doc type tag ` <!DOCTYPE>`. Usually the opening tag is just tag name but the closing tag has a slash before the name. Different tag names represent different functionalities. In most cases, there are only a few tags that contain information we need, e.g., tag `<div>` usually defines a table, tag `<a>` creates a hyperlink (the link is at attribute `href` and it may skip prefix if the prefix is the same as current URL), tag `<img>` comes up with a pic (the link is hidden in attribute `src`), tag `<p>` or `<h1>`-`<h6>` normally contains text. For more details of tagging, please refer to <a href= https://www.w3schools.com/tags/default.asp>w3schools</a>.

It is vital to understand the basics of HTML parse tree because most websites with simple layout can easily be traversed via a library called BeautifulSoup. When we use urllib or other packages to request a specific website via python, we end up with HTML parse tree in bytes. When the bytes are parsed to BeautifulSoup, it makes life easier. It allows us to search the tag name and other attributes to get the content we need. The link to the documentation of BeautifulSoup is <a href= https://www.crummy.com/software/BeautifulSoup/bs4/doc>here</a>.

For instance, we would love to get the link to the quiz on Dragon Ball, we can do

`result.find(‘div’,class_=’article article__list old__article-square’).find(‘a’).get(‘href’)`

Here, result is a BeautifulSoup object. The attribute `find` returns the first matched tag. The attribute `get` enables us to seek for attributes inside a tag.

Or we are interested in all the titles of the articles, we do

`temp=result.find(‘div’,class_=’article article__list old__article-square’).find_all(‘a’)` 

`output=[i.text for i in temp]`

The attribute `find_all` returns all the matched results. `.text` attribute automatically gets all `str` values inside the current tag. The second article has a subtitle ‘subscriber only’. So we will have a rather longer title for the second article compared to the rest. 

You can refer to <a href= https://github.com/je-suis-tm/web-scraping/blob/master/CME1.py>CME1</a> for more details. Please note that CME1 is an outdated script for Chicago Mercantile Exchange. Due to the change of the website, you cannot go through HTML parse tree to extract data any more. Yet, the concept of HTML parse tree is still applicable to other cases.

#### 2. JSON (CME2)

JSON, is the initial for JavaScript Object Notation. Like csv, it is another format to store data. According to the <a href=https://www.json.org>official website</a> of JSON, it is easy for humans to read and write. Pfff, are you fxxking with me? If you open JSON with notepad, you will see something like this.

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20json.PNG)

Gosh, the structure is messy and I will have a panic attack very soon. Duh! Just kidding. If you are familiar with adjacency list in graph theory, you will find it very easy to understand JSON. If not, do not worry, JSON is merely dictionaries inside dictionaries (with some lists as well). To navigate through the data structure, all you need to know is the key of the value.

Reading a JSON file in Python is straight forward. There are two ways.

There is a default package just called json, you can do

`import json`

`with open('data.json') as f:`

`	data = json.load(f)`

`print(data)`

Nevertheless, I propose a much easier way. We can parse the content to pandas and treat it like a dataframe. You can do

`import pandas as pd`

`df=pd.read_json('data.json')`

`print(df)`

Reading JSON is not really the main purpose of this chapter. What really made me rewrite the scraper for CME is the change of website structure. In April 2018, I could not extract data from searching for HTML tags any more. I came to realize that CME created a dynamic website by JavaScript. The great era of BeautifulSoup was water under the bridge. At this critical point of either adapt or die, I had to find out where the data came from and develop a new script. Guess where?

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20url.PNG)

The URL is still in page source! The HTML tag for the hidden link is `<script>`. As I have mentioned at the beginning of this README file, scraping is about patience and attention to details. If you try to search all `<script>` tags, you will end up with more than 100 results. It took me a while for me to sniff the data source. My friends, patience is a virtue. 

As for other websites, we may not be that lucky. Take <a href= https://www.euronext.com/en/products/indices/FR0003502079-XPAR>Euronext</a> for example, you won’t find any data in page source. We have to right click and select inspect element (CTRL+SHIFT+I in Chrome, F12 in IE).

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20inspect%20element.png)

The next step is to select Network Monitor in a pop-up window. Now let’s view data.

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20network.PNG)

There is a lot of traffic. Each one contains some information. Currently what truly matters to us is the request URL. Other information such as header or post form data will be featured in a later chapter. We must go through all the traffic to find out which URL leads to a JSON file. Once we hit the jackpot, we right click the request and copy link address.

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20request%20url.PNG)

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20link%20address.png)

Voila!

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cme2%20euronext.PNG)

Euronext is still considered an easy one. Sometimes you have to post a form with valid header to get the JSON file. You will see that in the first chapter of advanced level. For more details of JSON, feel free to take a look at <a href= https://github.com/je-suis-tm/web-scraping/blob/master/CME2.py>CME2</a>. Please note that CME2 has replaced CME1 to be the available scraper for Chicago Mercantile Exchange.

#### 3. Regular Expression (SHFE)

Sometimes, navigate through HTML parse tree may not get you what you need. For instance, you have some information inside a javascript function. You don't really want the whole bloc. All you care about is API key. 

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/shfe%20javascript.png)

Or you got multiple titles. You only care about the numbers inside these titles. You are unable to use array slicing with indices because numbers don't appear in fixed positions. Those numbers can even be negative.

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/shfe%20regex.png)

Helpless, right? Not if you know regular expression! We will call it regex in the following context. Think of regex as another simple language as HTML. In Python, there is a built-in library called `re`. There are a couple of functions inside this module. But for web scraping, `re.findall` and `re.search` are commonly used. `re.findall` returns a list of all the matched words and `re.search` returns a regex object. We simply apply attribute `re.search('','').group()` to concatenate the text together.

As for the regex itself, there are a few useful tips. `(?<=)` and `(?=)` are my favorite pair. They are called look-ahead and look-behind. If the content you are looking for is always behind a comma and before a question mark. You can simply do

`(?<=\,)\S*(?=\?)`

Punctuation marks have special meanings in regex. If you need to specify comma instead of special meanings, you always remember to put a slash before it. `\S*` refer to all the non-whitespace characters. Characters have no special meanings in regex. But when you put a slash before characters, all of sudden they have special meanings, quite the opposite to punctuation marks. 

The full table of my useful tips is here.

Syntax | Meaning
------------ | -------
`\d*` | All the numbers. If we remove asterisk mark, we will only match one digit. Asterisk mark refers to zero or multiple occurrence.
`\w*` | All the characters, numbers and underscore marks
`\S*` | All the non-whitespace characters
`-?\d*\,?\d*` | All the numbers, potential negative signs and potential commas. Question mark means the character can be zero or one occurrence.
`\d{4}` | 4 digits
`^Tori` | Anything starts with Tori
`Black$` | Anything ends with Black
`[a-z0-9]` | Anything involves lower case characters or digits
`[^A-Z]` | Anything except upper case characters
`(?<=\,)\S*(?=\?)` | Anything behind a comma and before a question mark

You can check <a href=https://www.w3schools.com/python/python_regex.asp>w3schools</a> for more details on regex syntax. 

In this chapter, the example is to navigate through a JSON file by regex (way faster than parsed as a pandas dataframe). Recalled from the previous chapter, JSON file is sort of dictionaries inside dictionaries. Normally we access the value by multiple keys. If you think of JSON file as a tree ADT, we need to know every node (key) from root to parent to go to the child node (value). Now we convert the whole structure to string and search for certain patterns via regex. With look-ahead and look-behind pair, knowing a parent node is fairly sufficient to get the value. Don't believe me? Feel free to take a look at <a href=https://github.com/je-suis-tm/web-scraping/blob/master/SHFE.py>SHFE</a> for coding details.

<br>

## Advanced

#### 1. Sign-in (CQF)

Congrats! I assume you have mastered entry-level web scraping. Since we come to more advanced level, we will have to deal with more complex issues. In this chapter, we will talk about how to sign into a website in Python. Please bear in mind that we will only discuss login without any captcha or other Turing Test (google’s reCAPTCHA is one of the worst). It doesn’t mean captcha is the dead end for scraping. There are two ways to bypass captcha, manually downloading image for human recognition or using external package to do image recognition. You will find something <a href=https://www.tutorialspoint.com/python_web_scraping/python_web_scraping_processing_captcha.htm>here</a>.

Well, login is no magic. Traditionally it is posting a form consists of critical information to a certain address. When each piece of information matches the record in website backend database, the website will assign a token to you. Token is like security clearance. It enables you to visit the content that requires login. Always remember to insert a token into the header when you got one after authentication.

Big companies like Facebook or Twitter use a slightly different approach called CSRF token. The website sends a token to you before sign-in. It goes without saying that CSRF token must be presented at login. There will be no more token assigned to you after authentication because the cookies will take care of everything. Think of CSRF as buying TTP in Madrid, once you tap it on the card reader to pass the gate, you do not need it to visit any station or exit the metro system. 

Let’s look at a simple case, a website called CQF. This great website features many free reports and videos on quantitative finance. But, there is always a but, the annoying part is resources are exclusive to registered users. Thus, we will be forced to include the login part in our python scraper. As usual, we always take a quick look at the website before coding. When we log in, we need to inspect element to seek for the login activity (if you forget how to do this, please refer to chapter 2 in the beginner level). There are quite a few activities when we log in, right? The quickest way to distinguish the login from the rest is to search your username and password. Because username and password are normally unhashed. 

Now that we have located the login activity, there are three key things we need to keep an eye on. The first one is Request URL. It will be the URL we post our form to. Pay attention to Request Method. The login is often POST method, rather than GET method.

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cqf%20login%20link.PNG)

The second one will be Request Headers. Headers are great tools to disguise your scraping as an internet browser. They are called headers because you would spend most of your time scratching your head to get them right. We can observe tons of information in the headers. Only a small bit of them are genuinely useful to the login. An effective way is to exclude cookies and anything contains hashed information. Nonetheless, this is not always the case. Some websites filter out machines by valid cookies with hashed information for login. If you accidentally exclude those headers, you may trigger the alarm of the website and end up with some form of captcha.

*My apologies for the redaction in these headers. The redaction plays a vital role here to protect my privacy. It turns my headers into some confidential documents from MI6.*

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cqf%20request%20header.PNG)

The last but not least one will be Form Data. It contains the critical information for authentication, such as username and password. 

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cqf%20post%20form.PNG)

There is another part called Query String Parameters. We do not encounter it very often at login. It is more frequently seen in data query though.

![Alt Text](https://github.com/je-suis-tm/web-scraping/blob/master/preview/cqf%20query.PNG)

Once we have gathered everything we need, we can simply do

`session.post(url,headers={'iamnotarobot':True},data={'username':'lanarhodes4avn','password':'i<3ellahughes'},params={'id':'jia.lissa'})`

The session will automatically update its cookie after posting a form. Generally speaking, the website gives a token in return (CQF does not). And the response is likely to be in JSON format, then we do 

`session.headers.update({'token':response.json()['token']})`

We have obtained the security clearance now. We can snoop around every corner as we please. Quite simple, isn't it? For more details, feel free to click <a href=https://github.com/je-suis-tm/web-scraping/blob/master/CQF.py>CQF</a>. If you crave for a bigger challenge, why don't you start with scraping a private instagram account?


#### 2. Database (LME)

Why do we need database?

There are many reasons for a big organization. For an individual user like us, the biggest advantage is, EFFICIENCY. Assume a website publishes data every day and you need consistent time series to run some models. For economic reasons, we only need to scrape the latest report each day in theory. What if one report gets delayed by some ‘technical issues’ (usually this is a lame excuse)? We have to scrape two reports next day. But we cannot keep track of everything every day and machines are supposed to do the grunt work for us. If we scrape the entire historical dataset as an alternative, it will take too much time and computing capacity. Additionally, we are running a risk of being blacklisted by the website. Some of those APIs even implement daily limit for each user. This is when database kicks in and keep tracks of everything. With records in the database, we can always start from where we left off last time. Of course, there are many other benefits of database, e.g. Data Integrity, Data Management.
Enough of sales pitch, let’s get into the technical details of database. The package we installed is called sqlite3, referring to SQLite database. The setup of SQLite database is hassle-free, in contrast to other relational database such as MySQL or PostgreSQL. Other benefits of SQLite include rapide execution, petit size. Since we are not running a big organization, we shouldn’t be bothered with things like Azure SQL server or Mongo DB.

To create a database, we simply do

`conn = sqlite3.connect('database.db')`
<br>
`c = conn.cursor()`

The above command would create a database if it does not exist in a given directory. If it exists, it will automatically connect to the database instead. 

Next step is to create a table in the database, we can do

`c.execute("""CREATE TABLE table_name ([column1] DATATYPE, [column2] DATATYPE, [column3] DATATYPE, PRIMARY KEY ([column1], [column2], [column3]));""")`
<br>
`conn.commit()`

Some key notes
* An interesting feature of SQL is its case insensitivity. Still, the upper case letters make things more distinguishable. The brackets `[]` serve the same purpose.
* For some reason, sqlite3 requests `;` at the end of each SQL command.
* Always remember to commit changes to database. Think of it as a pop up window to ask you if you want to save all the changes and you click HELL YEAH.
* The data types in SQL are very sophisticated and precise. Unless your duty is to maintain the efficiency of the database, I'd suggest you go with python data types such as 'FLOAT','DATE','TEXT'.
* Primary key is crucial to your data integrity. Primary key guarantees the uniqueness of the datasets. For instance, if the website modifies one historical data point, without the primary key constraint, we could end up with two values for the same period. With the primary key constraint, we can update the old value to skip any data corruption. 
* Only one primary key is allowed in each table (or no primary key at all). Even though, primary key can involve multiple columns, like the above statement.

Now that tables are set up, let's insert some scraped data into the database, we can do

`c.execute("""INSERT INTO table_name VALUES (?,?,?,?)""",[data1,data2,data3,data4])`
<br>
`conn.commit()`
<br>
`conn.close()`

We should not forget the last statement. SQLite3 database does not allow multiple modification at the same time. Other users cannot make changes inside the table if we don't close the database, similar to Excel in a way.

To make query directly from database, we do

`c=conn.cursor()`
<br>
`c.execute(“““SELECT * FROM table_name WHERE [column1]=value1;”””)`
<br>
`rows=c.fetchall()`
<br>
`conn.commit()`

The above is a conventional query method in sqlite3. However, pandas provide a much more convenient way. The output goes straight into dataframe instead of tuples within a list. Easy peasy lemon squeezy! 

`df=pd.read_sql(“““SELECT * FROM table_name WHERE [column1]=value1”””,conn)`

One of the very common issues from query is encoding. Unfortunately, I haven’t managed to solve it so far. Though there is a way to get around like this

`'C\'était des loques qui se traînaient'.encode('latin-1').decode('ISO-8859-1')`

There are other useful SQL sentences as well. For more details, you can check <a href=https://www.w3schools.com/sql>w3schools</a>. I personally believe fluency in `SELECT`, `DELETE`, `UPDATE` and `INSERT` is enough to cover most of your daily tasks, unless you aim to be a data architect dealing with numerous schemas.

Some other useful statements including

`UPDATE table_name SET [column1]=value1`
<br>
`DELETE FROM table_name WHERE [column1]=value1`

Feel free to take a look at <a href= https://github.com/je-suis-tm/web-scraping/blob/master/LME.py>LME</a> for more coding details.


#### 3. Newsletter (MENA)

<br>

## Notes

#### 1. Proxy Authentication

#### 2. Ethics

