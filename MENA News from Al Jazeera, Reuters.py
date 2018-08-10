# coding: utf-8

#this file is to scrape news title, article link and image link from some media stream websites
#next, insert latest feeds into database and send html emails including titles, links and images
#for details of scraping, database and outlook manipulation, plz take my previous file as a reference
# https://github.com/tattooday/web-scraping/blob/master/Feeds%20from%20Database.py

import pandas as pd
from bs4 import BeautifulSoup as bs 
import datetime as dt
import win32com.client as win32 
import sqlite3
import os
import urllib3 as u
import time
os.chdir('d:/')


#main stuff
def main():
    
    aj=scrape('https://www.aljazeera.com/topics/regions/middleeast.html',aljazeera)
    return
    tr=scrape('https://www.reuters.com/news/archive/middle-east',reuters)
    
    
    html=''
    
    #there are a few ways for embed image in html email
    #here, we use the link of the image
    #it may be a lil bit slow to load the image but its the most efficient way
    #alternatively, we can use mail.Attachments.add()
    #we attach all images, and set <img src='cid: imagename.jpg'>
    #the issue with this method is that we have to scrape the website for images repeatedly
    #or we can use < img src='data:image/jpg; base64, [remove the brackets and paste base64]'/>
    #but this is blocked by most email clients including outlook 2016
    for i in [('Al Jazeera',aj),('Reuters',tr)]:
        html+='<br><b><font color="Black">%s<font></b><br><br>'%i[0]
        for j in range(1,len(i[1]),3):
            html+="""<br><a href="%s"><font color="#6F6F6F">%s<font><a><br>
            <img src="%s" width="200" height="150"/><br><br>"""%(i[1][j],i[1][j-1],i[1][j-2])
            html+='<br>'
        
    send(html)

    
#send html email via outlook
def send(html):
    
    outlook = win32.Dispatch('outlook.application')  
    mail = outlook.CreateItem(0)  
    receivers = ['anyone@companyname.com']  
    mail.To = ';'.join(receivers) 
    mail.Subject ='Mid East News Feeds %s'%(dt.datetime.now())
    mail.BodyFormat=2
    mail.HTMLBody=html
    
    condition=str(input('0/1 for no/yes:'))
    if condition=='1':
        mail.Send()
        print('\nSENT')
    
    return


#reuters data etl
def reuters(page):
    
    print('reuters data etl')
    
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



#al jazeera data etl
def aljazeera(page):
    
    print('al jazeera data etl')
    
    title,link,image=[],[],[]
    df=pd.DataFrame()
    
    prefix='https://www.aljazeera.com'
    
    a=page.find_all('div',class_='frame-container')
    for i in a:
        title.append(i.find('img').get('title'))
        image.append(prefix+i.find('img').get('src'))
        link.append(prefix+i.find('a').get('href'))
    
    b=page.find_all('div',class_='col-sm-7 topics-sec-item-cont')
    for j in b:
        title.append(j.find('h2').text)
        link.append(prefix+j.find_all('a')[1].get('href'))
        
        #sometimes they replace pic with stupid avatar
        try:
            image.append(prefix+j.find('img').get('src'))
        except AttributeError:
            pass
    
    c=page.find_all('div',class_='col-sm-5 topics-sec-item-img')
    for k in c:
        temp=(prefix+k.find_all('img')[1].get('data-src'))
        image.append(temp)
    
    
    
    df['title']=title
    df['link']=link
    df['image']=image
    
        
    return df



#database insertion and output the latest feeds
def database(df):
    
    conn = sqlite3.connect('mideast_news.db')
    c = conn.cursor()
    out=[]
    for i in range(len(df)):
        try:
            c.execute("""INSERT INTO news VALUES (?,?,?)""",df.iloc[i,:])
            conn.commit()
            out.append(df.iloc[i,:]['title'])
            out.append(df.iloc[i,:]['link'])
            out.append(df.iloc[i,:]['image'])
            print('Updating...')
        except Exception as e:
            print(e)
    
    conn.close()
    
    if not out:
        out.append('No updates yet.')
        out.append('')
    
    return out


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
