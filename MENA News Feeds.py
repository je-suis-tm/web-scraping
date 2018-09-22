# coding: utf-8

#this file is to scrape news title, article link and image link from some major news websites initially
#next, insert scraped content into database and only keep the latest information
#after that, use home made graph structure traversal algorithm to extract key info and remove similar contents
#finally, send html emails including titles, links and images
#for details of scraping, database and outlook manipulation, plz take the following link as a reference
# https://github.com/tattooday/web-scraping/blob/master/Feeds%20from%20Database.py

import pandas as pd
from bs4 import BeautifulSoup as bs 
import marketanalysis as ma
import datetime as dt
import win32com.client as win32 
import sqlite3
import os
import re
import copy
import time
os.chdir('d:/')

#this is a home made special package for text mining
#it is designed to extract key information and remove similar contents
#for details of this graph traversal algorithm plz refer to the following link
# https://github.com/tattooday/graph-theory/blob/master/Text%20Mining%20project/alternative%20bfs.py
import graph

#main stuff
def main():
    
    ec=scrape('https://www.economist.com/middle-east-and-africa/',economist)
    aj=scrape('https://www.aljazeera.com/topics/regions/middleeast.html',aljazeera)
    tr=scrape('https://www.reuters.com/news/archive/middle-east',reuters)    
    bc=scrape('https://www.bbc.co.uk/news/world/middle_east',bbc)
    ws=scrape('https://www.wsj.com/news/types/middle-east-news',wsj)
    ft=scrape('https://www.ft.com/world/mideast',financialtimes)
    bb=scrape('https://www.bloomberg.com/view/topics/middle-east',bloomberg)
    cn=scrape('https://edition.cnn.com/middle-east',cnn)
    fo=scrape('https://fortune.com/tag/middle-east/',fortune)
    
    #concat scraped data via append, can use pd.concat as an alternative
    #unlike the previous version, current version does not sort information by source
    df=ft
    for i in [aj,tr,bc,ws,cn,fo,ec,bb]:
        df=df.append(i)
    
    #CRUCIAL!!!
    #as we append dataframe together, we need to reset the index
    #otherwise, we would not be able to use reindex in database function call
    df.reset_index(inplace=True,drop=True)
    
    #first round, insert into database and remove outdated information
    df=database(df)
    
    #second round, use home made package to remove similar contents
    output=graph.remove_similar(df,graph.stopword)
    
    print(output)
    
    html='<br><b><font color="Black">Mid East<font></b><br><br>'
    
    #there are a few ways for embed image in html email
    #here, we use the link of the image
    #it may be a lil bit slow to load the image but its the most efficient way
    #alternatively, we can use mail.Attachments.add()
    #we attach all images, and set <img src='cid: imagename.jpg'>
    #the issue with this method is that we have to scrape the website repeatedly to get images
    #or we can use < img src='data:image/jpg; base64, [remove the brackets and paste base64]'/>
    #but this is blocked by most email clients including outlook 2016
    for i in range(len(output)):
        
        html+="""<br><a href="%s"><font color="#6F6F6F">%s<font><a><br>
        <img src="%s" width="200" height="150"/>
        <br><br>"""%(output['link'][i],output['title'][i],output['image'][i])
        html+='<br>'
    
    send(html)


    
#send html email via outlook
def send(html):
    
    outlook = win32.Dispatch('outlook.application')  
    mail = outlook.CreateItem(0)  
    receivers = ['naomi.woods@brazzers.com']  
    mail.To = ';'.join(receivers) 
    mail.Subject ='Mid East News Feeds %s'%(dt.datetime.now())
    mail.BodyFormat=2
    mail.HTMLBody=html
    
    condition=str(input('0/1 for no/yes:'))
    if condition=='1':
        mail.Send()
        print('\nSENT')
    
    return


#the economist etl
def economist(page):
    
    title,link,image=[],[],[]
    df=pd.DataFrame()
    prefix='https://www.economist.com'
    
    a=page.find_all('div',class_="topic-item-container")
    
    for i in a:
    
        link.append(prefix+i.find('a').get('href'))
        title.append(i.find('a').text)
        image.append(i.parent.find('img').get('src'))

    df['title']=title
    df['link']=link
    df['image']=image
    
    return df



#fortune etl
def fortune(page):
    
    title,link,image=[],[],[]
    df=pd.DataFrame()
    prefix='https://fortune.com'
    
    a=page.find_all('article')
    
    for i in a:
    
        link.append(prefix+i.find('a').get('href'))
    
        if 'http' in i.find('img').get('src'):
            image.append(i.find('img').get('src'))
        else:
            image.append('')
    
        temp=re.split('\s*',i.find_all('a')[1].text)
        temp.pop()
        temp.pop(0)
        title.append(' '.join(temp))

    df['title']=title
    df['link']=link
    df['image']=image
    
    return df



#cnn etl
def cnn(page):
    
    title,link,image=[],[],[]
    df=pd.DataFrame()
    
    prefix='https://edition.cnn.com'
    
    a=page.find_all('div', class_='cd__wrapper')
    for i in a:
        title.append(i.text)
        link.append(prefix+i.find('a').get('href'))
        try:
            image.append('https:'+i.find('img').get('data-src-medium'))
        except:
            image.append('')
        
    df['title']=title
    df['link']=link
    df['image']=image
    
    return df


#bloomberg etl
def bloomberg(page):
    c=[]
    title,link,image=[],[],[]
    df=pd.DataFrame()
    prefix='https://www.bloomberg.com'
    
    a=page.find_all('h1')
    for i in a:
        try:
            link.append(prefix+i.find('a').get('href'))
            title.append(i.find('a').text.replace('â€™','\''))
        except:
            pass
    

    b=page.find_all('li')
    for j in b:
        try:
            temp=j.find('article').get('style')
            
            image.append( \
                         re.search('(?<=url\()\S*(?=\))', \
                                   temp).group() \
                        )
        except:
            temp=j.find('article')
            
            try:
                temp2=temp.get('id')
                if not temp2:
                    image.append('')
            except:
                pass


    df['title']=title
    df['link']=link
    df['image']=image
    
    return df



#financial times etl
def financialtimes(page):
    
    title,link,image=[],[],[]
    df=pd.DataFrame()
    prefix='https://www.ft.com'

    a=page.find_all('a',class_='js-teaser-heading-link')
    for i in a:
        link.append(prefix+i.get('href'))
        temp=i.text.replace('â€™','\'').replace('â€˜','\'')
        title.append(temp.replace('\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t',''))

    for j in a:
        temp=j.parent.parent.parent
        try:
            text=re.search('(?<=")\S*(?=next)',str(temp)).group()
            image.append(text+'next&fit=scale-down&compression=best&width=210')
        except:
            image.append('')
    
    df['title']=title
    df['link']=link
    df['image']=image
    
    return df



#wall street journal etl
def wsj(page):
    
    df=pd.DataFrame()
    
    text=str(page)

    link=re.findall('(?<=headline"> <a href=")\S*(?=">)',text)

    image=re.findall('(?<=img data-src=")\S*(?=")',text)

    title=[]
    for i in link:
        try:
            temp=re.search('(?<={}")>(.*?)<'.format(i),text).group()
            title.append(temp)
        except:
            pass

    for i in range(len(title)):
        title[i]=title[i].replace('â€™',"'").replace('<','').replace('>','')
        
    df['title']=title
    df['link']=link[:len(title)]
    df['image']=image
        
    return df


#bbc etl
def bbc(page):
    
    title,link,image=[],[],[]
    df=pd.DataFrame()
    
    prefix='https://www.bbc.co.uk'
    
    a=page.find_all('span',class_='title-link__title-text')
    
    for i in a:
        temp=i.parent.parent.parent.parent
        b=(re.findall('(?<=src=")\S*(?=jpg)',str(temp)))
        
        if len(b)>0:
            b=copy.deepcopy(b[0])+'jpg'
        else:
            b=''
            
        image.append(b)
    
    for j in a:
        title.append(j.text)
    
    for k in a:
        temp=k.parent.parent
        c=re.findall('(?<=href=")\S*(?=">)',str(temp))
        link.append(prefix+c[0])
        
    df['title']=title
    df['link']=link
    df['image']=image
    
    return df



#thompson reuters etl
def reuters(page):
    title,link,image=[],[],[]
    df=pd.DataFrame()
    
    prefix='https://www.reuters.com'
        
    for i in page.find('div', class_='news-headline-list').find_all('h3'):
        temp=i.text.replace('								','')
        title.append(temp.replace('\n',''))
    
    for j in page.find('div', class_='news-headline-list').find_all('a'):
        link.append(prefix+j.get('href'))
    link=link[0::2]
        
    for k in page.find('div', class_='news-headline-list').find_all('img'):
        if k.get('org-src'):
            image.append(k.get('org-src'))
        else:
            image.append('')

    
    df['title']=title
    df['link']=link
    df['image']=image
    
    return df



#al jazeera etl
def aljazeera(page):
    title,link,image=[],[],[]
    df=pd.DataFrame()
    
    prefix='https://www.aljazeera.com'
    
    a=page.find_all('div',class_='frame-container')
    for i in a:
        title.append(i.find('img').get('title'))
        image.append(prefix+i.find('img').get('src'))
        temp=i.find('a').get('href')
        link.append(temp if 'www' in temp else (prefix+temp))
    
    b=page.find_all('div',class_='col-sm-7 topics-sec-item-cont')
    c=page.find_all('div',class_='col-sm-5 topics-sec-item-img')
    
    limit=max(len(b),len(c))
    j,k=0,0
    while j<limit:
        
        title.append(b[j].find('h2').text)
        temp=b[j].find_all('a')[1].get('href')
        link.append(temp if 'www' in temp else (prefix+temp))
        
        #when there is an opinion article
        #the image tag would change
        #terrible website
        if 'opinion' in b[j].find('a').get('href'):
            image.append(' ')

        else:
            image.append(prefix+c[k].find_all('img')[1].get('data-src'))
            k+=1
            
        j+=1
    
    df['title']=title
    df['link']=link
    df['image']=image
        
    return df




#database insertion and output the latest feeds
def database(df):
    
    temp=[]
    conn = sqlite3.connect('mideast_news.db')
    c = conn.cursor()
    
    
    for i in range(len(df)):
        try:
            c.execute("""INSERT INTO news VALUES (?,?,?)""",df.iloc[i,:])
            conn.commit()
            print('Updating...')
            temp.append(i)
        except Exception as e:
            print(e)
    
    conn.close()
    
    output=df.loc[[i for i in temp]]
    output.reset_index(inplace=True,drop=True)
    
    return output



#scraping webpages
def scrape(url,method):
    
    
    print('scraping webpage effortlessly')
    time.sleep(5)
    
    http = u.PoolManager()
    response = http.request('GET',url,headers={'User-Agent': 'Mozilla/5.0'})      
    page=bs(response.data,'html.parser')
    
    df=method(page) 
    out=database(df)
    
    return out        



if __name__ == "__main__":
    main()
