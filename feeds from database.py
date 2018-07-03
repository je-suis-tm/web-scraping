# -*- coding: utf-8 -*-

"""
Created on Thu Jun 21 14:28:55 2018

"""

#this is something i have been working for the past few days
#i intended to create a local database to store everything i scrape from different websites
#this way, i would be able to compare scraped data with the database
#it would be easy to find out what has been updated
#i only need to send those updates via email

#the following codes are a demonstration
#do not expect it to scrape porn websites

import pandas as pd
from bs4 import BeautifulSoup as bs 
import urllib.request as u
import datetime as dt
import win32com.client as win32 
import sqlite3
import getpass
import os
os.chdir('H:\database')


#i use win32 to launch outlook and send email
#when running on corporate network, it is the easiest way to do
#otherwise, there is a library called smtp for pop3/imap server
#supposedly authentication of corporate email would kill u
#i definitely recommend to use win32 library
#note that to use win32.email
#outlook has to be kept open
#for work, it should be easily managed

def send(ult):

    #before sending emails, gotta double check what we are sending
    print(ult)
    
    #create an email with recipient, subject, context and attachment
    outlook = win32.Dispatch('outlook.application')  
    mail = outlook.CreateItem(0)

    #these email addresses are fabricated, PLZ DO NOT HARASS OUR GODDESS
    #just some random pornstar i love
    receivers = ['lana.rhodes@brazzers.com','tori.black@brazzers.com','rachel.woods@brazzers.com']  

    #use ';' to separate receipients
    #this is a requirement of outlook
    mail.To = ';'.join(receivers) 
    mail.Subject ='New Feeds %s'%(dt.datetime.now())  

    #remember to use '\r\n' to go to the next line
    mail.Body = '\r\n'.join(ult)
    mail.Attachments.Add('new.db') 

    #check carefully before sending emails
    condition=str(input('0/1 for no/yes:'))
    if condition=='1':
        mail.Send()
        print('\nSENT')

    return


#this is a function for data etl
def media_etl(page,name):

    temp=[]
    df=pd.DataFrame()
  
    #some scraped links do not contain prefix 'www'
    if name=='xvideos':
        prefix='https://www.xvideos.com'
    else:
        prefix=''

    
    #getting the title and link for ...
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
