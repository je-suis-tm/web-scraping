# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 16:23:53 2018

"""

#scraping CME is soooo effortless
#just simple html parse tree
#how i love Chicago
import urllib.request as u
import pandas as pd
from bs4 import BeautifulSoup as bs
import os
os.chdir('H:/')


#
def scrape(category_name,commodity_name):
    
    #i use proxy handler cuz my uni network runs on its proxy
    #and i cannot authenticate python through the proxy
    #so i use empty proxy to bypass the authentication
    proxy_handler = u.ProxyHandler({})
    opener = u.build_opener(proxy_handler)
    
    #cme officially forbids scraping
    #so a header must be used for disguise as an internet browser
    #the developers say no to scraping, it appears to be so
    #but actually they turn a blind eye to us, thx
    #i need different types of commodity
    #so i need to format the website for each commodity
    req=u.Request('http://www.cmegroup.com/trading/metals/%s/%s.html'%(
            category_name,commodity_name),headers={'User-Agent': 'Mozilla/5.0'})
    response=opener.open(req)
    result=response.read()
    soup=bs(result,'html.parser')
    
    return soup


#
def etl(category_name,commodity_name):
    
    try:
        page=scrape(category_name,commodity_name)
        print(commodity_name)
 
    except Exception as e:
        print(e)
        
        
    #i need date, prior settle price and volume
    #it is essential to view source of the website first
    #then use beautiful soup to search specific class
    p1=page.find_all('span',class_='cmeNoWrap')
    p2=page.find_all('td',class_=['statusOK','statusNull','statusAlert'])
    p3=page.find_all('td',class_="cmeTableRight")

    a=[]
    b=[]
    c=[]
    
    for i in p1:
        a.append(i.text)

    #somehow prior settle is hard to get
    #we cannot find that specific tag
    #we can search for the previous tag instead
    #the find_next function of beautifulsoup allows us to get the next tag
    #the previous tag of prior settle is change
    for j in p2:
        temp=j.find_next()
        b.append(temp.text)

    #the volume contains comma
    for k in p3:
        c.append(float(str(k).replace(',','')))
        
        
    df=pd.DataFrame()    
    df['expiration date']=a
    df['prior settle']=b
    df['volume']=c
    df['name']=commodity_name
    
    #for me, i wanna highlight the front month
    #The front month is the month where the majority of volume and liquidity occurs
    df['front month']=df['volume']==max(df['volume'])


#
def main():
    
    #scraping and etl
    df1=etl('precious','silver')
    df2=etl('precious','gold')
    df3=etl('precious','palladium')
    df4=etl('base','copper')

    #concatenate then export
    dd=pd.concat([df1,df2,df3,df4])
    dd.to_csv('cme.csv',encoding='utf_8_sig')
    
    
if __name__ == "__main__":
    main()
