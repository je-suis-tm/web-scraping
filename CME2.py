# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 11:33:03 2018

"""
#previously in CME1
#i said scraping CME is soooo effortless
#CME technical guys must have heard my voice
#they changed the website from xml structure to json query
#holy crap!! well, it would not scare off people like us!!

#here is the trick
#before we actually go to the website of CME quotes
#we press ctrl+shift+i in chrome or f12 in ie
#we can inspect element of the website
#we just go to the network monitor
#we will be able to see all the network activity
#including where the data of CME is coming from
#this is how we gon do it baby
import pandas as pd
import requests
import os
os.chdir('H:/')


#
def scrape(commodity_code):    
    
    session=requests.Session()
    
    
    #cme officially forbids scraping
    #so a header must be used to disguise as a browser
    #technically speaking, the website should be able to detect that too
    #those tech guys just turn a blind eye, thx fellas
    session.headers.update(
            {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})
    
    
    #now that we have found out where the data is coming from
    #we need to do a lil analysis on the url
    #e.g. http://www.cmegroup.com/CmeWS/mvc/Quotes/Future/437/G
    #it is quite obvious that 437 is a code name for commodity gold
    #but how do we know the code for each commodity
    #this is an issue raised by maysam19
    # https://github.com/je-suis-tm/web-scraping/issues/1
    #might as well as mention the solution here
    #there are two ways to solve it
    
    #if you only need very few types of commodity
    #you can go to websites one by one
    #e.g. https://www.cmegroup.com/trading/metals/precious/gold.html
    #you can right click and select view page source
    #search for /CmeWS/mvc/Quotes/Future/
    #you should find the commodity code easily
    
    #if you got so many types of commodity to scrape
    #you should seek for the link that contains such information from inspect element
    #here is the hack that i have done for you, voila
    # https://www.cmegroup.com/CmeWS/mvc/ProductSlate/V2/List
    #it is a json file that contains codes of each commodity in cme
    #if you are visiting this script to understand json file
    #dont worry, we will talk about how to read it very soon
    response=session.get(
            'http://www.cmegroup.com/CmeWS/mvc/Quotes/Future/%s/G'%(commodity_code))

    return response


#
def etl(commodity_code,commodity_name):
    
    try:
        response=scrape(commodity_code)
        print(response)
 
    except Exception as e:
        print(e)
        
        
    #think of json file as dictionaries inside dictionaries
    #the simplest way to handle json files is pandas
    #remember, the solution is pandas package, not json package!
    #dataframe is a default way of reading json
    #if you dont like the structure
    #you can use pd.read_json with orient as a key argument
    #you can choose from index, columns, values, split, records
    df=pd.DataFrame(response.json())
    
    #pandas turns json into a dataframe
    #still, for df['quotes']
    #we end up with a bunch of dictionaries
    #we just treat things as normal dictionaries
    #we use the key to get value for each dictionary
    #and we form a new dataframe as output
    #for me, i only need prior settle price and expiration date
    #volume is used to detect the front month contract
    output=pd.DataFrame()
    output['prior settle']=[i['priorSettle'] for i in df['quotes']]
    output['expiration date']=[i['expirationDate'] for i in df['quotes']]
    output['volume']=[i['volume'] for i in df['quotes']]
    output['name']=commodity_name
    output['front month']=output['volume']==max(output['volume'])
    
    return output


#
def main():

    df1=etl('458','silver')
    df2=etl('437','gold')
    df3=etl('445','palladium')
    df4=etl('438','copper')


    #concatenate then export
    output=pd.concat([df1,df2,df3,df4])
    output.to_csv('cme.csv',encoding='utf_8_sig')
    

if __name__ == "__main__":
    main()
