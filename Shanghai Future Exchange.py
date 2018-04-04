# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 10:48:35 2018

@author: terry.mai
"""

import urllib.request as u
import pandas as pd
import re

import datetime as dt
import os

#Shanghai Future Exchange's daily price is stored in a dat file
#and when you do query on the website
#it runs jquery then format the dat file into the website
#it can be tracked by pressing f12 to inspect element on network
os.chdir('H:/')
os.getcwd()

y=str(dt.datetime.now().year)
m=(dt.datetime.now().month)
# i normally scraped t-1 prices
d=(dt.datetime.now().day)-1


#this funtion is used to format the date, the date that SHFE uses is yyyymmdd
#for instance january, if we use datetime now, we only get 1
#so for digits smaller than 10, add 0 before it

def f(x):
    if int(x)<10:
        return '0'+str(x)
    else:
        return str(x)
    
#this function is basically standard procedure of webscraping

def soup1(date):
    try:
        #i use proxy handler cuz my company network runs on its proxy
        #and it forbids python to run on its proxy, so i use empty proxy to bypass it
        proxy_handler = u.ProxyHandler({})
        opener = u.build_opener(proxy_handler)
        #there is no need to disguise as an internet browser for SHFE
        req = u.Request('http://www.shfe.com.cn/data/dailydata/kx/kx%s.dat'%(date))
        r = opener.open(req)
        result = r.read()
        
        return result
    except Exception as e:
        print(e)


#this is the procedure of formatting yyyymmdd
m=f(m)
d=f(d)
date=y+m+d

#scraping...
a=(soup1(date))
#if we look closely at the dat file, it is well structured
#i dont know much about java though, i assume it is some kinda dictionary
#for every value, it has key
#hence, i only need to use regular expression to get the numbers behind colon :
b=re.findall('(?<=:)-?\d*\.?\d*',a.decode('utf-8'))
#i only need the close price, which is the expression of slicing 9::16
#and i only need certain types of commodity
#for general use, you can use a function to do slicing 
c=b[9::16]
cu=c[0:12]
al=c[13:25]
zn=c[26:38]
pb=c[39:51]
ni=c[52:64]
au=c[78:86]
ag=c[87:99]
frb=c[100:112]
#this is just formatting, and export csv file
#you can customize based on your requirement
group=al+['','']+cu+['','']+zn+['','']+pb+['','']+ni
upload=[al[0]]+cu[0:3]+zn[0:3]+pb[0:3]+frb[0:2]+[ag[2]]+['']+[au[2]]+ni[0:2]+[ni[3]]+[0]*50
df=pd.DataFrame(upload)
df['upload']=group
df['al extra']=al[1]
df.to_csv('murex update.csv')


#this is the regular expression to get date of each contract
#even though price and date are both stored in values of dictionary
#date has quotation marks
#i dont need date for my work, if u need it, just use this regular expression
d=re.findall('(?<=")\d*(?=")',a.decode('utf-8'))
e=d[0:12]
#


