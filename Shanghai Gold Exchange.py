# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 14:46:58 2018


"""

#scraping shanghai gold exchange requires two step
#there are two layers, the first layer store links to daily summary report
#the second layer is the daily summary report that i need
#thus, i scrape the first layer to find the hyperlink to yesterday's report
#i use regular expression to get hyperlink ID
#i scrape again to get the report
#my assumption is that the hyperlink ID should be hash encrypted

import urllib.request as u
import pandas as pd
from bs4 import BeautifulSoup as bs
import re
import datetime as dt
import os

os.chdir('H:/')
os.getcwd()

a=dt.datetime.now().year
b=dt.datetime.now().month
# i wanna scrape t-1, thats why there is a minus one expression
c=dt.datetime.now().day-1
#k is the class of html structures, its vital to view the source of website first
k=['xl63','xl64','xl65','xl66','xl68']
url='http://www.sge.com.cn/sjzx/mrhqsj'
q=[]

#this function is basically standard procedure of webscraping

def soup1(url):
    try:
        #i use proxy handler cuz my uni network runs on its proxy
        #and it forbids python to run on its proxy, so i use empty proxy to bypass it
        proxy_handler = u.ProxyHandler({})
        opener = u.build_opener(proxy_handler)
        req = u.Request(url)
        r = opener.open(req)
        result = r.read()
        soup=bs(result,'lxml')
        return soup
    except Exception as e:
        print(e)

#i am using beautiful soup to find the title of yesterday's daily summary report
p1=soup1(url).find(text=r'上海黄金交易所%d年%d月%d日交易行情' %(a,b,c))
#i go to the parent level of parent level of the text
#i use regular expression to get the hyperlink ID
x=re.findall('\d*',str(p1.parent.parent))
y=[]
for i in x:
    if len(i)>6:
        y.append(i)

print(y)
#formatting the link
url='http://www.sge.com.cn/sjzx/mrhqsj/%s?top=%s'%(y[0],y[1])


#second layer scraping
p1=soup1(url).find_all('td',class_=k)


#replace the space symbols
for i in p1:
    s=i.text.replace('\r\n\t\t\t\t\t','').replace('\r\n\t\t\t\t','')
    q.append(s)


df=pd.DataFrame()
#using slicing to turn the list into a structured table
for k in range(13):
    df[q[k]]=q[(k+13)::13]
#the encoding of utf 8 sig is important, otherwise the chinese characters wont show correctly
df.to_csv('SGE.csv',encoding='utf_8_sig')
