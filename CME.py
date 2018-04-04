# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 16:23:53 2018


"""

#scraping CME is soooo effortless
#how i love Chicago
import urllib.request as u
import pandas as pd
from bs4 import BeautifulSoup as bs
import re
import os

os.chdir('H:/')
os.getcwd()

#this function is basically standard procedure of webscraping

def soup1(t1,t2):
    #i use proxy handler cuz my company network runs on its proxy
    #and it forbids python to run on its proxy, so i use empty proxy to bypass it
    proxy_handler = u.ProxyHandler({})
    opener = u.build_opener(proxy_handler)
    #cme officially forbids scraping
    #so a header must be used to disguise as an internet browser
    #technically speaking, they should be able to block that
    #they just officially say no and then leave a backdoor for us, thx CME
    #i need different types of commodity, so i need to format the website for each commodity
    #t1 is the category, t2 is the commodity
    req = u.Request('http://www.cmegroup.com/trading/metals/%s/%s.html'%(t1,t2),headers={'User-Agent': 'Mozilla/5.0'})
    r = opener.open(req)
    result = r.read()
    soup=bs(result,'lxml')
    return soup

#beautiful soup
def soup2(t1,t2):
    
    try:
        p=soup1(t1,t2)
        print(t2)

 
    except Exception as e:
        print(e)
#after scraping, i need date, prior settle price and volume
#it is essential to view source of the website first
#then use beautiful soup to search specific class
 
    p1=p.find_all('span',class_='cmeNoWrap')
    p2=p.find_all('td',class_=['statusOK','statusNull','statusAlert'])
    p3=p.find_all('td',class_="cmeTableRight")

    a=[]
    b=[]
    c=[]
    for i in p1:
        a.append(i.text)

#somehow prior settle is hard to get, so i searched for change instead
#i use find next to get to prior settle from change
    for j in p2:
        z=j.find_next()
        b.append(z.text)

#the volume contains comma, thats why i implement regular expression 
#alternatively i can use replace, i am not sure about the time complexity of both
    for k in p3:
        k1=re.findall('\d',k.text)
        k2=''.join(k1)
        c.append(int(k2))
        
    df=pd.DataFrame(a)
    df['%s prior settle'%(t2)]=b
    df['%s vol'%(t2)]=c
    # i wanna highlight the pior settlement of front month.
    #The front month is the month where the majority of the trading volume and liquidity occurs.
    z=df['%s prior settle'%(t2)][df['%s vol'%(t2)]==max(df['%s vol'%(t2)])]
    df['%s target'%(t2)]=z
    
    return df

#scraping
df1=soup2('precious','silver')
df2=soup2('precious','gold')
df3=soup2('precious','palladium')
df4=soup2('base','copper')

#concatenate then export
dd=pd.concat([df1,df2,df3,df4],axis=1)
dd.to_csv('cme.csv',encoding='utf_8_sig')
