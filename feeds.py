# -*- coding: utf-8 -*-

"""

Created on Thu Jun 21 14:28:55 2018



"""

import pandas as pd
from bs4 import BeautifulSoup as bs 
import urllib.request as u
import datetime as dt
import win32com.client as win32 
import sqlite3
import getpass
import os
os.chdir('H:\database')



    

#keep outlook open

def send(ult):

    print(ult)

    outlook = win32.Dispatch('outlook.application')  

    mail = outlook.CreateItem(0)

    

    #these emails are fabricated, PLZ DO NOT HARASS OUR GODDESS

    receivers = ['lana.rhodes@brazzers.com','tori.black@brazzers.com','rachel.woods@brazzers.com']  

    mail.To = ';'.join(receivers) 

    mail.Subject ='New Feeds %s'%(dt.datetime.now())  

    mail.Body = '\r\n'.join(ult)

    mail.Attachments.Add('new.db') 

    

    condition=str(input('0/1 for no/yes:'))

    if condition=='1':

        mail.Send()

        print('\nSENT')

    

    return



    

def media_etl(page,name):

    temp=[]

    df=pd.DataFrame()

    

    if name=='xvideos':

        prefix='https://www.xvideos.com'

    else:

        prefix=''

        

        

    for i in page:

        try:                

            temp.append(i.find('a').get_text())

            temp.append(prefix+i.find('a').get('href'))

        except:

            pass

    

    df['title']=temp[0::2]

    df['link']=temp[1::2]

    

        

    return df





#

def database(df,name):

    

    #c.execute("""CREATE TABLE new (title TEXT PRIMARY KEY, link TEXT);""")

    #db=pd.read_sql("""SELECT * FROM new""",conn)

    

    

    conn = sqlite3.connect('new.db')

    c = conn.cursor()

    out=['','%s'%name,'','']

    for i in range(len(df)):

        try:

            c.execute("""INSERT INTO new VALUES (?,?)""",df.iloc[i,:])

            conn.commit()

            out.append(df.iloc[i,:]['title']+'                 '+df.iloc[i,:]['link'])

        except Exception as e:

            print(e)

    

    conn.close()

    

    if len(out)==4:

        out.append('No updates yet, wankers.')

    

    return out





#

def scrape(url,what,method,name):

    

    response=soup1(url)

    page=response.find_all(what)

    df=method(page,name)

    out=database(df,name)

    return out        





#

def soup1(url):

    

    try:

        username='Dr Surname'

        password=getpass.getpass('input password:')

        proxy='www.someproxyaddress.com:8080'

        

        proxy_handler = u.ProxyHandler({'http':'%s'%(proxy)})

        password_mgr = u.HTTPPasswordMgrWithDefaultRealm()

        proxy_auth_handler = u.ProxyBasicAuthHandler(password_mgr)

        proxy_auth_handler.add_password(None, 'http://%s'%(proxy),'%s'%(username), '%s'%(password))

        

        opener = u.build_opener(proxy_handler,proxy_auth_handler)

        req = u.Request(url,headers={'User-Agent': 'Mozilla/5.0'})

        r = opener.open(req)

        result = r.read()

        

        soup=bs(result,'html.parser')

        

        print(url)

        return soup

    

    except Exception as e:

        print(e)

        

        

pornhub=scrape('https://www.pornhub.com','h4',media_etl,'pornhub')

xvideos=scrape('https://www.xvideos.com','h4',media_etl,'xvideos')

youporn=scrape('https://www.youporn.com','h3',media_etl,'youporn')

    

ult=[]

for i in [pornhub,xvideos,youporn]:

    ult+=['']+i+['']

        

send(ult)