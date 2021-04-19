# coding: utf-8

#this script is about the latest news of MENA region
#we scrape different influential media websites, or so-called fake news, lol
#and send only updates to the mailbox for daily newsletter
#in order to do that, we need a db to store all the historical content of websites
#and all the scraping techniques from html parse tree to regular expression
#over time, i also discovered the issue of information overload in daily newsletter
#hence, i invented a graph theory based algorithm to extract key information
#a part of this algo will also be featured in this script to solve info redundancy
#as u can see, this is the most advanced script in web scraping repository
#it contains almost every technique we have introduced so far
#make sure you have gone through all the other scripts before moving onto this one

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
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
# https://github.com/je-suis-tm/graph-theory/blob/master/Text%20Mining%20project/text_mining.py
import text_mining


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
    #the purpose of blending data together is to go through text mining pipeline
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
    output=text_mining.remove_similar(df,text_mining.stopword)
    
    #if the link is not correctly captured
    #remove anything before www and add https://
    for i in range(len(output)):
        if 'https://' not in output['link'][i]:
            temp=re.search('www',output['link'][i]).start()
            output.at[i,'link']='http://'+output['link'][i][temp:]
    
    print(output)
    
    
    #using html email template
    #check stripo for different templates
    # https://stripo.email/templates/
    html="""
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html>

    <head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta name="x-apple-disable-message-reformatting">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="telephone=no" name="format-detection">
    <title></title>
    <!--[if (mso 16)]>
    <style type="text/css">
    a {text-decoration: none;}
    </style>
    <![endif]-->
    <!--[if gte mso 9]><style>sup 
    { font-size: 100% !important; }</style><![endif]-->
    </head>

    <body>
    <div class="es-wrapper-color">
        <!--[if gte mso 9]>
                <v:background xmlns:v="urn:schemas-microsoft-com:vml" 
                fill="t">
                    <v:fill type="tile" color="#333333"></v:fill>
                </v:background>
            <![endif]-->
        <table class="es-content-body" width="600" 
        cellspacing="15" cellpadding="15" bgcolor="#ffffff" 
        align="center">
         <tr>
            <td class="esd-block-text" align="center">
            <h2>Middle East</h2></td>
         </tr></table>
         <div><br></div>
        
    """
    
    
    #there are a few ways for embed image in html email
    #here, we use the link of the image
    #it may be a lil bit slow to load the image, its the most efficient way
    #alternatively, we can use mail.Attachments.add()
    #we attach all images, and set <img src='cid: imagename.jpg'>
    #the downside is that we have to scrape the website repeatedly to get images
    #or we can use < img src='data:image/jpg; base64, [remove the brackets and paste base64]'/>
    #base64 can be generated via the following code
    # from io import BytesIO
    # import base64
    # def create_image_in_html(fig):
    #     tmpfile = BytesIO()
    #     fig.savefig(tmpfile, format='png')
    #     encoded = base64.b64encode(
    #         tmpfile.getvalue()).decode('utf-8')
    #     return encoded
    #but this approach is blocked by most email clients including outlook 2016
    for i in range(len(output)):
        html+="""<table class="es-content-body" width="600" 
        cellspacing="10" cellpadding="5" bgcolor="#ffffff"
        align="center">"""
        html+="""<tr><td class="esd-block-text es-p10t es-p10b"
        align="center"><p><a href="%s">
        <font color="#6F6F6F">%s<font><a></p></td></tr>
        <tr><td align="center">
        <img src="%s" width="200" height="150"/></td></tr>
        <tr>"""%(output['link'][i],output['title'][i],output['image'][i])
        html+="""</tr></table><div><br></div>"""
        
    html+="""
    </div>
    </body>
    </html>
    """
    
    
    send(html)

   
#i use win32 to control outlook and send emails
#when you have a win 10 pro, it is the easiest way to do it
#cuz windows pro automatically launches outlook at startup
#otherwise, there is a library called smtp for pop3/imap server
#supposedly authentication of corporate email would kill u
#i definitely recommend folks to use win32 library
#note that using win32.email requires outlook to stay active
#do not close the app until u actually send out the email

#win32 library uses COM api to control windows
#go to microsoft developer network 
#check mailitem object model to learn how to manipulate outlook emails
#the website below is the home page of outlook vba reference
# https://msdn.microsoft.com/en-us/vba/vba-outlook
def send(html):
        
    #create an email with recipient, subject, context and attachment
    outlook = win32.Dispatch('outlook.application')  
    mail = outlook.CreateItem(0)  
    
    #these email addresses are fabricated, PLZ DO NOT HARASS OUR GODDESS
    #just some random pornstar i love
    receivers = ['lana.rhodes@brazzers.com',
                 'tori.black@brazzers.com',
                 'naomi.woods@brazzers.com']  

    #use ';' to separate receipients
    #this is a requirement of outlook
    mail.To = ';'.join(receivers) 
    
    mail.Subject ='Mid East Newsletter %s'%(dt.datetime.now())
    mail.BodyFormat=2
    
    #use html to make email looks more elegant
    #html is very simple
    #use br for line break, b for bold fonts
    #font for color and size, a href for hyperlink
    #check the website below to see more html tutorials
    # https://www.w3schools.com/html/
    
    #Alternatively, we can use plain text email
    #remember to use '\r\n' to jump line
    #assuming html is a list of str
    #the code should be mail.Body = '\r\n'.join(html)
    mail.HTMLBody=html
    
    #i usually print out everything
    #need to check carefully before sending to stakeholders
    #we can use mail.Display() to see the draft instead
    condition=str(input('0/1 for no/yes:'))
    if condition=='1':
        mail.Send()
        print('\nSENT')
    else:
        print('\nABORT')
    
    return


#database insertion and output the latest feeds
#i assume you are familiar with sqlite3
#if not, plz check the following link
# https://github.com/je-suis-tm/web-scraping/blob/master/LME.py
def database(df):
    
    temp=[]
    conn = sqlite3.connect('mideast_news.db')
    c = conn.cursor()
    
    #the table structure is simple
    #the table name is new
    #there are three columns, title, link and image
    #the data types of all of them are TEXT
    #title is the primary key which forbids duplicates
    for i in range(len(df)):
        try:
            c.execute("""INSERT INTO news VALUES (?,?,?)""",df.iloc[i,:])
            conn.commit()
            
            print('Updating...')
            
            #the idea is very simple
            #insert each line from our scraped result into database
            #as the primary key has been set up
            #we have non-duplicate title constraint
            #insert what has already been in database would raise an error
            #if so, just ignore the error and pass to the next iteration
            #we can utilize the nature of database to pick out the latest information
            #every successful insertion into the database also goes to the output
            #at the end, output contains nothing but latest updates of websites
            #that is what we call newsletter
            temp.append(i)
            
        except Exception as e:
            print(e)
    
    conn.close()
    
    #check if the output contains no updates
    if temp:
        output=df.loc[[i for i in temp]]
        output.reset_index(inplace=True,drop=True)
    else:
        output=pd.DataFrame()
        output['title']=['No updates yet.']
        output['link']=output['image']=['']
    
    return output


#scraping webpages and do some etl
def scrape(url,method):
    
    print('scraping webpage effortlessly')
    time.sleep(5)
    
    session=requests.Session()
    response = session.get(url,headers={'User-Agent': 'Mozilla/5.0'})      
    page=bs(response.content,'html.parser',from_encoding='utf_8_sig')
    
    df=method(page) 
    out=database(df)
    
    return out        


"""
the functions below are data etl of different media sources
"""
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
        title.append(i.find('span').text)
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
    df['image']=image+[''] if (len(image)!=len(title)) else image
        
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


if __name__ == "__main__":
    main()
