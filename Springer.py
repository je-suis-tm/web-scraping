#!/usr/bin/env python
# coding: utf-8

# In[9]:


import requests
import os
import pandas as pd
import time
os.chdir('d:/python')


# In[4]:


def scrape(url):
    
    session=requests.Session()

    page=session.get(url,verify=False)

    return page.content


# In[5]:
def main():
    
    #get textbook list
    content=scrape('https://resource-cms.springernature.com/springer-cms/rest/v1/content/17858272/data/v4')
        
    f=open('textbook.xlsx','wb')
    f.write(content)
    f.close
        
    df=pd.ExcelFile('textbook.xlsx').parse('eBook list')
    
    
    #iterate through all books but it will take a long ass time
    for i in range(len(df)):
        
        
        name=df['Book Title'][i]
        url=df['OpenURL'][i]
        print(name)
        
        prefix='https://rd.springer.com/content/pdf/'
        postfix=df['DOI URL'][i].split('http://doi.org/')[-1].replace('/','%2F')        
        url=prefix+postfix+'.pdf'
        
        time.sleep(5)
        content=scrape(url)
        f=open(f'{name}.pdf','wb')
        f.write(content)
        f.close


if __name__ == "__main__":
    main()



