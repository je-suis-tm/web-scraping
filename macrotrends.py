# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 16:49:09 2021

@author: Administrator
"""


#this website is called macrotrends
#this script is designed to scrape its financial statements
#yahoo finance only contains the recent 5 year
#macrotrends can trace back to 2005 if applicable
import re
import json
import pandas as pd
import requests
import os
os.chdir('k:/')


#simply scrape
def scrape(url,**kwargs):
    
    session=requests.Session()
    session.headers.update(
            {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})
    
    response=session.get(url,**kwargs)

    return response


#create dataframe
def etl(response):

    #regex to find the data
    num=re.findall('(?<=div\>\"\,)[0-9\.\"\:\-\, ]*',response.text)
    text=re.findall('(?<=s\: \')\S+(?=\'\, freq)',response.text)

    #convert text to dict via json
    dicts=[json.loads('{'+i+'}') for i in num]

    #create dataframe
    df=pd.DataFrame()
    for ind,val in enumerate(text):
        df[val]=dicts[ind].values()
    df.index=dicts[ind].keys()
    
    return df


def main():
    
    url='https://www.macrotrends.net/stocks/charts/AAPL/apple/financial-statements'
    response=scrape(url)
    df=etl(response)
    df.to_csv('aapl financial statements.csv')
    
    return


if __name__ == "__main__":
    main()