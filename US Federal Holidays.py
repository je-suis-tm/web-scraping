#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: filetype=python


# In[1]:


#this script computes cme holidays
#based upon federal holidays for the next two years
#if you just want the current year holiday calendar
# https://www.cmegroup.com/tools-information/holiday-calendar.html

import datetime as dt
import pandas as pd
import random as rd
import time
import requests
import os
os.chdir('d:/')


# In[2]:


#scraping function
def scrape(url):
    
    session=requests.Session()
    
    session.headers.update(
            {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})
    
    time.sleep(rd.randint(0,10))
   
    response=session.get(url,verify=False)
    
    return response
    

# In[3]:


#get exchange holidays
def get_cme_holidays():
    
    weekdays=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    federal_holidays=["New Year's Day",
                     'M L King Day',
                     "Presidents' Day",
                     'Good Friday',
                     'Memorial Day',
                     'Thanksgiving Day',
                     'Christmas']
    
    currentyear=dt.datetime.now().year
    allholidays=pd.DataFrame(columns=['DAY', 'DATE', 'HOLIDAY'])
    
    #get this year plus the next two years
    for year in range(currentyear,currentyear+3):
        
        url=f'https://www.calendarlabs.com/holidays/us/{year}'
        response=scrape(url)
        response.raise_for_status()
        
        #get tables from html
        dataframes=pd.read_html(response.text)
        
        #cleansing
        holidays=dataframes[1]        
        holidays['DATE']=holidays['DATE'].apply(lambda x:x[:-6])        
        holidays['DAY']=holidays['DAY'].apply(lambda x:x[-3:])
        
        #datetime conversion
        holidays['DATE']=pd.to_datetime(holidays['DATE'])
        
        #only select federal holiday + good friday
        cme_holidays=holidays[holidays['HOLIDAY'].isin(federal_holidays)]
        cme_holidays.reset_index(inplace=True,drop=True)
        
        #create cme holidays based upon +-1 day on the official holiday
        for i in cme_holidays.index:
            
            temp=pd.DataFrame(columns=cme_holidays.columns)
            
            if cme_holidays.at[i,'DAY']=='Mon':
                temp['DAY']=['Fri','Tue']
                temp['DATE']=[cme_holidays.at[i,'DATE']-dt.timedelta(days=3),
                             cme_holidays.at[i,'DATE']+dt.timedelta(days=1)]
                temp['HOLIDAY']=[cme_holidays.at[i,'HOLIDAY']]*2
                
            elif cme_holidays.at[i,'DAY']=='Fri':
                temp['DAY']=['Thu','Mon']
                temp['DATE']=[cme_holidays.at[i,'DATE']-dt.timedelta(days=1),
                             cme_holidays.at[i,'DATE']+dt.timedelta(days=3)]
                temp['HOLIDAY']=[cme_holidays.at[i,'HOLIDAY']]*2
                
            elif cme_holidays.at[i,'DAY']=='Sat':
                temp['DAY']=['Fri','Mon']
                temp['DATE']=[cme_holidays.at[i,'DATE']-dt.timedelta(days=1),
                             cme_holidays.at[i,'DATE']+dt.timedelta(days=2)]
                temp['HOLIDAY']=[cme_holidays.at[i,'HOLIDAY']]*2
                
            elif cme_holidays.at[i,'DAY']=='Sun':
                temp['DAY']=['Fri','Mon']
                temp['DATE']=[cme_holidays.at[i,'DATE']-dt.timedelta(days=2),
                             cme_holidays.at[i,'DATE']+dt.timedelta(days=1)]
                temp['HOLIDAY']=[cme_holidays.at[i,'HOLIDAY']]*2
                
            else:
                temp['DAY']=[weekdays[dt.datetime.weekday(cme_holidays.at[i,'DATE'])-1],
                            weekdays[dt.datetime.weekday(cme_holidays.at[i,'DATE'])+1]]
                temp['DATE']=[cme_holidays.at[i,'DATE']-dt.timedelta(days=1),
                             cme_holidays.at[i,'DATE']+dt.timedelta(days=1)]
                temp['HOLIDAY']=[cme_holidays.at[i,'HOLIDAY']]*2 
                
            cme_holidays=cme_holidays.append(temp)
            cme_holidays.reset_index(inplace=True,drop=True)
            
        allholidays=allholidays.append(cme_holidays)
        allholidays.reset_index(inplace=True,drop=True)
    
    return allholidays


# In[4]:


def main():    
    
    allholidays=get_cme_holidays()
    allholidays.to_csv('cme holidays.csv',index=False)
    
if __name__ == "__main__":
    main()
