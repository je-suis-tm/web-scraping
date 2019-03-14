# -*- coding: utf-8 -*-






import requests
import pandas as pd
from io import BytesIO
import re


#say if we wanna get the trader commitment report of lme from the link below
# https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders#tabIndex=1
#when we select aluminum and we will be redirected to a new link
# https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Aluminium
#if we try to view page source, we will find nothing in html parse tree
#what do we do?
#here is a very common scenario in web scraping
#we simply right click and select inspect element
#we will have to monitor the traffic one by one to identify where the report comes from
#as usual, i have done it for you
def get_download_link():
    
    download_link='https://www.lme.com/api/Lists/DownloadLinks/%7B02E29CA4-5597-42E7-9A22-59BB73AE8F6B%7D'
        
    
    #there are quite a few pages of reports
    #for simplicity, we only care about the latest report
    #note that the page counting starts from 0
    session=requests.Session()
    response = session.get(download_link, 
                           params={"currentPage": 0})
    
    
    #the response is a json file
    #i assume you should be familiar with json now
    #if not, plz check the link below
    # https://github.com/je-suis-tm/web-scraping/blob/master/CME2.py
    url_list=response.json()['content_items']
    
    
    return url_list



#once we find out where the download link is
#we can get the actual report
def get_report(url_list):
    
    prefix='https://www.lme.com'    
    url=url_list[0]['Url']
    
    
    session=requests.Session()
    response = session.get(prefix+url)
    
    
    #we also get the date of the data from url
    date=pd.to_datetime(re.search(r"\d{4}/\d{2}/\d{2}",url).group())
    
    return response.content,date


#
def etl(content,date):
    
    #the first seven rows are annoying headers
    #we simply skip them
    df = pd.ExcelFile(BytesIO(content)).parse('AH', skiprows=7)
    
    #assume we only want positions of investment funds 
    #lets do some etl
    df['Unnamed: 0'].fillna(method='ffill',
                            inplace=True)
    
    col=list(df.columns)
    for i in range(1,len(col)):
        if 'Unnamed' in col[i]:
            col[i]=col[i-1]
    
    df.columns=col
    del df['Notation of the position quantity']
    df.dropna(inplace=True)
    
    output=df['Investment Funds'][df['Unnamed: 0']=='Number of Positions']    
    output.columns=['long','short']
    
    output=output.melt(value_vars=['long','short'], 
                       var_name='position', 
                       value_name='value')
    
    output['type']=df['LOTS'].drop_duplicates().tolist()*2
    output['date']=date
    
    return output



def main():
    
    url_list=get_download_link()
    
    content,date=get_report(url_list)
    
    output=etl(content,date)
    

if __name__ == "__main__":
    main()
