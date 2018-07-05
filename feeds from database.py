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

def send(html):

    
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

    #html email is used here
    #for simple structure, we can use string instead
    #remember to use '\r\n' to go to the next line
    #the code should be mail.Body = '\r\n'.join(html)
    mail.BodyFormat=2
    mail.HTMLBody=html
    ail.Attachments.Add('new.db')

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

#this function is to insert data into sqlite3 database
#im not gonna go into details for sql
#for pythoners, sql is a piece of cake
#go check out the following link for sql
# https://www.w3schools.com/sql/
def database(df,name):
    
    #plz make sure u have created the database and the table
    #to create a table in database, first two lines are the same as below
    #just add a few more lines
    #c.execute("""CREATE TABLE new (title TEXT PRIMARY KEY, link TEXT);""")
    #conn.commit()
    #conn.close()
    #to see what its like in the database
    #use microsoft access or other visualization tools or just pandas
    #db=pd.read_sql("""SELECT * FROM new""",conn)

    conn = sqlite3.connect('new.db')
    c = conn.cursor()
    
    #add a title for output
    out=['','%s'%name,'','']

    #the idea is very simple
    #insert each line from dataframe to database
    #as the primary key has been set up
    #and primary key doesnt allow duplicates
    #insert what has already been in database would raise an error
    #ignore the error and continue the iteration
    #every successful insertion also guarantees insertion into the output
    #at the end, output only contains updates of the website
    for i in range(len(df)):
        try:
            c.execute("""INSERT INTO new VALUES (?,?)""",df.iloc[i,:])
            conn.commit()
            out.append(df.iloc[i,:]['title'])
            out.append(df.iloc[i,:]['link'])
            print('Updating...')
        except Exception as e:
            print(e)

    conn.close()

    #check if the output contains no updates
    if not out:
        out.append('No updates yet.')
        out.append('')

    return out


#scraping a concatenation of functions
#scrape the website, do data etl, insert into database
def scrape(url,what,method,name):
  
    response=soup1(url)
    page=response.find_all(what)
    df=method(page,name)
    out=database(df,name)

    return out        

#scraping is just like the rest scrapers in this repo
#except we add some extra authentication for corporate proxy
#note that getpass doesnt work in spyder
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
        
#
pornhub=scrape('https://www.pornhub.com','h4',media_etl,'pornhub')
xvideos=scrape('https://www.xvideos.com','h4',media_etl,'xvideos')
youporn=scrape('https://www.youporn.com','h3',media_etl,'youporn')


#concatenate all these infamous websites:P
#and use html to make email looks more elegant
#html is very simple
#check the website below to see more html tutorials
# https://www.w3schools.com/html/
html=''
for i in [('pornhub',pornhub),('xvideos',xvideos),('youporn',youporn)]:
    html+='<br><b><font color="Black">%s<font></b><br><br>'%i[0]
    for j in range(1,len(i[1]),2):
        html+='<br><a href="%s"><font color="#6F6F6F">%s<font><a><br>'%(i[1][j],i[1][j-1])
    html+='<br>'

#take a look at what we are gonna send before sending
#alternatively, we can add one more line to send function
#use mail.Display() to see the draft
print(pornhub,xvideos,youporn)
send(html)
