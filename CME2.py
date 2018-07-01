# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 11:33:03 2018


"""
#previously i said scraping CME is soooo effortless
#i guess CME has found out what i said
#now they totally changed the website from xml structure to json query
#i used inspect element to see where json files are stored
#so i only need to remember the code for each commodity
#the most reliable way would be scrape the website first
#use regular expression to find the json query 
#then scrape the json file
import urllib.request as u
import pandas as pd
from bs4 import BeautifulSoup as bs
import re
import os

os.chdir('H:/')
os.getcwd()

#this function is basically standard procedure of webscraping


#
def soup1(t1):
    
    #i use proxy handler cuz my network runs on its proxy
    #and it forbids python to run on its proxy, so i use empty proxy to bypass it
    proxy_handler = u.ProxyHandler({})
    opener = u.build_opener(proxy_handler)
    
    #cme officially forbids scraping
    #so a header must be used to disguise as an internet browser
    #technically speaking, they should be able to block that
    #they just officially say no and then leave a backdoor for us, thx CME
    #i need different types of commodity, so i need to format the website for each commodity
    #t1 is the commodity code
    req = u.Request('http://www.cmegroup.com/CmeWS/mvc/Quotes/Future/%s/G'%(t1),headers={'User-Agent': 'Mozilla/5.0'})
    r = opener.open(req)
    result = r.read()
    soup=bs(result,'lxml')
    return soup

#
def soup2(t1,t2):
    
    try:
        a=soup1(t1).decode('utf-8')
        print(t2)

 
    except Exception as e:
        print(e)
        
        
#after scraping, i need date, prior settle price and volume
#i use regular expression to get what i need
#alternatively we can save json on local disks
#read it as a dictionary
#the trouble is that we have to be familiar with the dictionary structure of this json
#the slicing is kinda exhausting, i'd rather not
 
    b=re.findall('(?<=priorSettle\":")\S*(?=\","open)',a)
    c=re.findall('(?<=volume\":")\S*(?=\","mdKey)',a)
    d=re.findall('(?<=expirationDate\":")\S*(?=\","productName)',a)
    e=[]
    
    #this loop is to convert the string to float and replace the comma
    #cuz i wanna find out the front month
    #The front month is the month where the majority of the trading volume and liquidity occurs
    #using string would cause errors
    for i in c:
        e.append(float(i.replace(',','')))

  
#t2 is just for the formatting purpose
#otherwise i will get lost in the datasets        
    df=pd.DataFrame(d)
    df['%s prior settle'%(t2)]=b
    df['%s vol'%(t2)]=e
    
    # i wanna highlight the pior settlement of front month.
    #prior to the convertion, i wanna use max function on the volume list
    z=df['%s prior settle'%(t2)][df['%s vol'%(t2)]==max(df['%s vol'%(t2)])]
    df['%s target'%(t2)]=z
    
    return df

#scraping
df1=soup2('458','silver')
df2=soup2('437','gold')
df3=soup2('445','palladium')
df4=soup2('438','copper')

#concatenate then export
dd=pd.concat([df1,df2,df3,df4],axis=1)
dd.to_csv('cme.csv',encoding='utf_8_sig')

