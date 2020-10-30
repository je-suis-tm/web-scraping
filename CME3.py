#!/usr/bin/env python
# coding: utf-8



#without the help of my intern, this option data scraper would never exist
#thank you, Olivia, much appreciated for the data etl

# In[1]:


import requests
import pandas as pd
import time
import random as rd
import os
os.chdir('H:/')


# In[2]:


#scraping function
def scrape(url):
    
    session=requests.Session()
    
    session.headers.update(
            {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})
    
    time.sleep(rd.randint(0,10))
    
    response=session.get(url,params={"_": int(time.time()*1000)})    

    return response


# In[3]:


#get options expiration id
def get_expiration_data(expiration_json,options_id):

    expiration_dict=expiration_json[str(options_id)]['expirations']

    return [(expiration_dict[i]['expiration'],expiration_dict[i]['label']) for i in expiration_dict]


# In[4]:


#get group id
def get_groupid(jsondata):
    
    commoditygroup=pd.DataFrame.from_dict(jsondata['filters']['group'])

    var=locals()
    for i in range(len(commoditygroup)):
        var['a'+str(i)]=pd.DataFrame.from_dict(commoditygroup['children'].iloc[i])
        var['a'+str(i)]['group']=commoditygroup['name'].iloc[i]

    groupid=pd.concat([var['a'+str(i)] for i in range(len(commoditygroup))])
    groupid.reset_index(inplace=True,drop=True)
    
    return groupid

#get product id
def get_productid(jsondata):
    
    return pd.DataFrame.from_dict(jsondata['products'])


# In[5]:


#get option quote
def get_data(jsondata):
    
    table=pd.DataFrame.from_dict(jsondata,orient='index').T
    
    #unpack option related data    
    optionContractQuotes=table['optionContractQuotes'].iloc[0]
        
    var=locals()
    for i in range(len(optionContractQuotes)):        
        var['a'+str(i)]=pd.DataFrame.from_dict(optionContractQuotes[i]).T
        
        var['a'+str(i)]['strikePrice']=var['a'+str(i)]['change'].loc['strikePrice']
        var['a'+str(i)]['strikeRank']=var['a'+str(i)]['change'].loc['strikePrice']
        var['a'+str(i)]['underlyingFutureContract']=var['a'+str(i)]['change'].loc['underlyingFutureContract']
        var['a'+str(i)].drop(['strikePrice','strikeRank','underlyingFutureContract'],
                             inplace=True)
        var['a'+str(i)].reset_index(inplace=True)
        var['a'+str(i)].columns=var['a'+str(i)].columns.str.replace('index','optiontype')    
    
    options=pd.concat([var['a'+str(i)] for i in range(len(optionContractQuotes))])
    options.columns=['options-'+i for i in options.columns]

    #unpack underlying future contract
    assert len(table)==1,"table length mismatch"
    underlyingFutureContractQuotes=pd.DataFrame.from_dict(table['underlyingFutureContractQuotes'].iloc[0])
    
    assert len(underlyingFutureContractQuotes)==1,"underlyingFutureContractQuotes length mismatch"
    lastTradeDate_dict=underlyingFutureContractQuotes['lastTradeDate'].iloc[0]
    lastTradeDate=pd.DataFrame()
    for i in lastTradeDate_dict:
        lastTradeDate[i]=[lastTradeDate_dict[i]]
    
    priceChart_dict=underlyingFutureContractQuotes['priceChart'].iloc[0]
    priceChart=pd.DataFrame()
    for i in priceChart_dict:
        priceChart[i]=[priceChart_dict[i]]
    del underlyingFutureContractQuotes['lastTradeDate']
    del underlyingFutureContractQuotes['priceChart']
    priceChart.columns=priceChart.columns.str.replace('code','pricechartcode')
    
    futures=pd.concat([underlyingFutureContractQuotes,lastTradeDate,priceChart],axis=1)
    futures.columns=['futures-'+i for i in futures.columns]
    
    #concatenate options and futures
    output=options.copy(deep=True)
    
    assert len(futures)==1,"futures length mismatch"
    for i in futures:
        output[i]=futures[i].iloc[0]
        
    del table['optionContractQuotes']
    del table['underlyingFutureContractQuotes']
    for i in table:
        output[i]=table[i].iloc[0]
        
    return output



# In[6]:

def main():

    id_url='https://www.cmegroup.com/CmeWS/mvc/ProductSlate/V2/List'
    
    #get group and product id to find the future contract
    response_id=scrape(id_url)
    groupid=get_groupid(response_id.json())
    productid=get_productid(response_id.json())
        
    #301 denotes corn option
    option_id=301

    #get expiration code from futures
    expiration_url=f'https://www.cmegroup.com/CmeWS/mvc/Options/Categories/List/{option_id}/G?optionTypeFilter='
    response_expiration=scrape(expiration_url)
    target_exp_id=get_expiration_data(response_expiration.json())
    
    #get option data
    for expiration_id,expiration_date in target_exp_id:
        
        option_url=f'https://www.cmegroup.com/CmeWS/mvc/Quotes/Option/{option_id}/G/{expiration_id}/ALL?optionProductId={option_id}&strikeRange=ALL'
        response_option=scrape(option_url)
        
        #not every expiration_id leads to concrete data
        try:
            df=get_data(response_option.json())

            target=['options-optiontype',
             'options-change',
             'options-close',
             'options-high',
             'options-highLimit',
             'options-last',
             'options-low',
             'options-lowLimit',
             'options-mdKey',
             'options-open',
             'options-percentageChange',
             'options-priorSettle',
             'options-updated',
             'options-volume',
             'options-strikePrice',
             'options-strikeRank',
             'futures-change',
             'futures-close',
             'futures-expirationDate',
             'futures-high',
             'futures-highLimit',
             'futures-last',
             'futures-low',
             'futures-lowLimit',
             'futures-mdKey',
             'futures-open',
             'futures-optionUri',
             'futures-percentageChange',
             'futures-priorSettle',
             'futures-productId',
             'futures-productName',
             'futures-updated',
             'futures-volume',
             'futures-default24',
             'tradeDate']
        
            df=df[target]
            
            #fix the expiration mismatch between futures and options
            #or you can use cme rule based month coding system
            # https://www.cmegroup.com/month-codes.html
            df['futures-expirationDate']=pd.to_datetime(expiration_date)
            
            df.to_csv(f'corn option {expiration_id}.csv',index=False)
        
        except ValueError:
            pass

if __name__ == "__main__":
    main()


