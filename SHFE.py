# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 10:48:35 2018

"""

#Shanghai Future Exchange's daily price is stored in a dat file
#when you make a query on the website
#the page runs jquery to get the json file
#then convert json to dat file and put it on the website table
#the process can be tracked by inspect element
#the logic of getting dat file is pretty much the same as cme2
# https://github.com/je-suis-tm/web-scraping/blob/master/CME2.py
#theoretically speaking, we can use the same trick as json
#here, we apply a more general way to process it
#regular expression a.k.a. regex

#regex can work on any sort of text extraction
#when we cannot extract text from html parse tree 
#or maybe we just need a part of the text
#regex is the most efficient way
#even for a simple html parse tree
#we can still convert response.content to string first
#and apply regex to extract what we need later
#regex in python is the same as regex in any other languages
#the rules of regex is basically universal
#check the link below to see more details of regex
# https://www.w3schools.com/python/python_regex.asp
import requests
import pandas as pd
import re
import datetime as dt
import os
os.chdir('H:/')


#this funtion is to format the date
#the date format of SHFE is yyyymmdd
def format_date():
    
    year=str(dt.datetime.now().year)
    month=(dt.datetime.now().month)
    
    #i normally get t-1 prices
    day=(dt.datetime.now().day)-1
    
    datetime=str(pd.to_datetime(f'{year}-{month}-{day}'))
    date=datetime[:10].replace('-','')
    
    return date


#
def scrape(date):
    
    session=requests.Session()
    response = session.get('http://www.shfe.com.cn/data/dailydata/kx/kx%s.dat'%(date))
        
    return response.content


#
def etl(content):
    
    #if we look closely at dat file, it is just json in another format
    #all we need to do is to discover the pattern of where the data is stored
    #all the price data i care about are behind colon :
    #regex lookahead will do the trick
    numbers=re.findall('(?<=:)-?\d*\.?\d*',content.decode('utf_8-sig'))

    #i only need the close price, which is the expression of slicing 9::16
    #and i only need certain types of commodity
    temp=numbers[9::16]
    cu=temp[0:12]
    al=temp[13:25]
    zn=temp[26:38]
    pb=temp[39:51]
    ni=temp[52:64]
    au=temp[78:86]
    ag=temp[87:99]
    frb=temp[100:112]

    #customize the format based on my requirement
    group=al+['','']+cu+['','']+zn+['','']+pb+['','']+ni
    upload=[al[0]]+cu[0:3]+zn[0:3]+pb[0:3]+frb[0:2]+[ag[2]]+['']+[au[2]]+ni[0:2]+[ni[3]]+[0]*50
    df=pd.DataFrame(upload)
    df['upload']=group
    df['al extra']=al[1]

    return df
    
    #this is the regex to get date of each contract
    #even though price and date are both stored in the same file
    #date has quotation marks, price doesnt
    #i dont need date, if u need it, just use the regex below
    
    """
    temp=re.findall('(?<=")\d*(?=")',content.decode('utf_8-sig'))
    date=temp[0:12]
    """

#
def main():
    
    date=format_date()
    
    content=scrape(date)
    
    df=etl(content)
    
    df.to_csv('murex update.csv')
    
    
if __name__ == "__main__":
    main()
