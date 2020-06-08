#!/usr/bin/env python
# coding: utf-8



#scrape cftc trader commitment report


# In[1]:


import requests
import pandas as pd
import re
import os
os.chdir('H:/')


# In[2]:


#scraping function
def scrape(url):
    
    session=requests.Session()
    
    session.headers.update(
            {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})
    
    response=session.get(url)    

    return response


# In[3]:


#get data
def etl(response):
    
    #create a list
    text=response.content.decode('utf-8').split('\r')    
    
    
    #create index for each block
    assets=[i for i in text if 'CHICAGO MERCANTILE EXCHANGE' in i]
    ind=[text.index(i) for i in assets]
    
            
    overall=[]
    
    #etl
    for i in ind:
        
        commodity=text[i].split(' - CHICAGO MERCANTILE EXCHANGE')[0].replace('\n','')
        commodity_code=text[i].split('Code-')[-1].replace('\n','')
        date=re.search('\d{2}\/\d{2}\/\d{2}',text[i+1]).group()
        contractunit=re.search('(?<=\().*(?=OPEN INTEREST)',text[i+7]).group().replace(')','')
        open_interest=re.search('(?<=OPEN INTEREST\:).*',text[i+7]).group()
        non_commercial_long_commitment,non_commercial_short_commitment, \
        non_commercial_spread_commitment,commercial_long_commitment, \
        commercial_short_commitment,total_long_commitment,total_short_commitment, \
        non_reportable_long_commitment,non_reportable_short_commitment=re.findall('\S+',text[i+9])
        changedate=re.search('\d{2}\/\d{2}\/\d{2}',text[i+11]).group()
        change_open_interest=text[i+11].split(' ')[-1].replace(')','')
        non_commercial_long_change,non_commercial_short_change, \
        non_commercial_spread_change,commercial_long_change, \
        commercial_short_change,total_long_change,total_short_change, \
        non_reportable_long_change,non_reportable_short_change=re.findall('\S+',text[i+12])
        non_commercial_long_percent,non_commercial_short_percent, \
        non_commercial_spread_percent,commercial_long_percent, \
        commercial_short_percent,total_long_percent,total_short_percent, \
        non_reportable_long_percent,non_reportable_short_percent=re.findall('\S+',text[i+15])
        totaltraders=text[i+17].split(' ')[-1].replace(')','')
        non_commercial_long_traders,non_commercial_short_traders, \
        non_commercial_spread_traders,commercial_long_traders, \
        commercial_short_traders,total_long_traders,total_short_traders=re.findall('\S+',text[i+18])
        
        temp=[commodity,commodity_code,date,contractunit,open_interest,
              non_commercial_long_commitment,non_commercial_short_commitment,
              non_commercial_spread_commitment,commercial_long_commitment,
              commercial_short_commitment,total_long_commitment,
              total_short_commitment,non_reportable_long_commitment,
              non_reportable_short_commitment,changedate,change_open_interest,
              non_commercial_long_change,non_commercial_short_change,
              non_commercial_spread_change,commercial_long_change,
              commercial_short_change,total_long_change,total_short_change,
              non_reportable_long_change,non_reportable_short_change,
              non_commercial_long_percent,non_commercial_short_percent,
              non_commercial_spread_percent,commercial_long_percent,
              commercial_short_percent,total_long_percent,
              total_short_percent,non_reportable_long_percent,
              non_reportable_short_percent,totaltraders,
              non_commercial_long_traders,non_commercial_short_traders,
              non_commercial_spread_traders,commercial_long_traders,
              commercial_short_traders,total_long_traders,total_short_traders]
        
        overall+=temp
    
    
    colnames=['commodity',
     'commodity_code',
     'date',
     'contract_unit',
     'open_interest',
     'non_commercial_long_commitment',
     'non_commercial_short_commitment',
     'non_commercial_spread_commitment',
     'commercial_long_commitment',
     'commercial_short_commitment',
     'total_long_commitment',
     'total_short_commitment',
     'non_reportable_long_commitment',
     'non_reportable_short_commitment',
     'change_date',
     'change_open_interest',
     'non_commercial_long_change',
     'non_commercial_short_change',
     'non_commercial_spread_change',
     'commercial_long_change',
     'commercial_short_change',
     'total_long_change',
     'total_short_change',
     'non_reportable_long_change',
     'non_reportable_short_change',
     'non_commercial_long_percent',
     'non_commercial_short_percent',
     'non_commercial_spread_percent',
     'commercial_long_percent',
     'commercial_short_percent',
     'total_long_percent',
     'total_short_percent',
     'non_reportable_long_percent',
     'non_reportable_short_percent',
     'total_traders',
     'non_commercial_long_traders',
     'non_commercial_short_traders',
     'non_commercial_spread_traders',
     'commercial_long_traders',
     'commercial_short_traders',
     'total_long_traders',
     'total_short_traders']
    
    
    #create dataframe
    df=pd.DataFrame(columns=colnames)
    
    
    for i in range(len(colnames)):
        df[colnames[i]]=overall[i::len(colnames)]
        
    
    #transform
    ind=['commodity', 'commodity_code','change_date',
         'date', 'contract_unit', 'open_interest',
         'change_open_interest','total_traders']

    df=df.melt(id_vars=ind,value_vars=[i for i in df.columns if i not in ind])

    #isolate position
    df['position']=''

    ind_long=df.loc[df['variable'].apply(lambda x: 'long' in x )].index
    ind_short=df.loc[df['variable'].apply(lambda x: 'short' in x )].index
    ind_spread=df.loc[df['variable'].apply(lambda x: 'spread' in x )].index

    for i in ind_spread:
        df.at[i,'position']='spread'
    for i in ind_short:
        df.at[i,'position']='short'
    for i in ind_long:
        df.at[i,'position']='long'

    df['variable']=df['variable'].str.replace('long_','').str.replace('short_','').str.replace('spread_','')

    #isolate type
    df['type']=df['variable'].apply(lambda x:'_'.join(x.split('_')[:-1]))

    #clean variable name
    df['variable']=df['variable'].apply(lambda x:x.split('_')[-1])

    df['variable']=df['variable'].str.replace('percent',
                               'percent_of_open_interest_for_each_type_of_traders')

    df['variable']=df['variable'].str.replace('traders',
                               'number_of_traders_in_each_type')

    #change col order
    df=df[['commodity', 'commodity_code', 'change_date',
        'date', 'contract_unit','open_interest', 
           'change_open_interest', 'total_traders', 
           'type','position','variable','value', ]]
    
    return df
    
    
# In[4]:

def main():

    url='https://www.cftc.gov/dea/futures/deacmesf.htm'
    
    #scrape
    response=scrape(url)

    #get data
    df=etl(option_url)

    df.to_csv('trader commitment report.csv',index=False)
    

if __name__ == "__main__":
    main()

