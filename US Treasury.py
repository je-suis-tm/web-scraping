#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: filetype=python


# In[1]:


#this script scrapes us treasury website
#for constant maturity treasury rate
#the treasury rate will be used as risk free interest rate
#which is crucial to the vix calculator
# https://github.com/je-suis-tm/quant-trading/blob/master/VIX%20Calculator.py


import pandas as pd
import requests
import os
os.chdir('d:/')


# In[2]:


#scraping function
def scrape(url):
    
    session=requests.Session()
    
    session.headers.update(
            {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})
       
    response=session.get(url,verify=False)
    
    return response
    

# In[3]:


def main():    
    
    url='https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'
    response=scrape(url)

    #the second table is yield curve rate
    data=pd.read_html(response.text)[1]
    
    #cleanse
    data=data.melt(id_vars='Date',var_name='maturity')
    
    #convert to datetime
    data['Date']=pd.to_datetime(data['Date'])
    
    data.to_csv('treasury yield curve rates.csv',index=False)
    
if __name__ == "__main__":
    main()
