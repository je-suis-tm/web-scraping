# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:19:57 2021

@author: Administrator
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: filetype=python

#if wallstreetbets can move the market
#why not join em? 
#fuck investment banks and hedge funds
#they only make the rich richer
#this script scrapes the topics under different flairs
#we only care about the hottest within the past 24 hours
#im not willing to use any stemmer or lemmatizer here
#simply becuz i dont want any ticker code gets fucked over
#if u want any nlp cleansing, check the link below
# https://github.com/je-suis-tm/machine-learning/blob/master/naive%20bayes.ipynb
import logging
import time
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import win32com.client as win32 
import requests
import traceback

global stopword_dict
global punctuations
global commodities_of_interests

punctuations= ['!', '(', ')', '[', ']', '{', '}', ';', ':', "'", '"',
               '\\', ',', '<', '>', '.', '/', '?', '@', '#', '%', '^',
               '&', '*', '_', '~',]

#remove swearing words
stopword_dict=punctuations+['i','yolo', 'fuck', 'fucking', 'shit',
                            'take', 'still', 'new', 'say', 'get',
                            'add', 'update', 'me', 'my', 'myself',
                            'we', 'our', 'ours', 'ourselves', 'be',
                            'you', "you're", "you've", "you'll",
                            "you'd", 'your', 'yours', 'yourself',
                            'yourselves', 'he', 'him', 'his', 'were',
                            'himself', 'she', "she's", 'her', 'been',
                            'hers', 'herself', 'it', "it's", 'being',
                            'its', 'itself', 'they', 'them', 'their',
                            'theirs', 'themselves', 'what', 'which',
                            'who', 'whom', 'this', 'that', "that'll",
                            'these', 'those', 'am', 'is', 'are', 'was',
                            'have', 'has', 'had', 'having', 'do',
                            'does', 'did', 'doing', 'a', 'an', 'the',
                            'and', 'but', 'if', 'or', 'because', 'as',
                            'until', 'while', 'of', 'at', 'by', 'for',
                            'with', 'about', 'against', 'between',
                            'into', 'through', 'during', 'before',
                            'after', 'above', 'below', 'to', 'from',
                            'up', 'down', 'in', 'out', 'on', 'off',
                            'over', 'under', 'again', 'further',
                            'then', 'once', 'here', 'there', 'when',
                            'where', 'why', 'how', 'all', 'any',
                            'both', 'each', 'few', 'more', 'most',
                            'other', 'some', 'such', 'no', 'nor',
                            'not', 'only', 'own', 'same', 'so', 'than',
                            'too', 'very', 's', 't', 'can', 'will',
                            'just', 'don', "don't", 'should', 
                            "should've", 'now', 'd', 'll', 'm', 'o',
                            're', 've', 'y', 'ain', 'aren', "aren't",
                            'couldn', "couldn't", 'didn', "didn't",
                            'doesn', "doesn't", 'hadn', "hadn't",
                            'hasn', "hasn't", 'haven', "haven't",
                            'isn', "isn't", 'ma', 'mightn', "mightn't",
                            'mustn', "mustn't", 'needn', "needn't",
                            'shan', "shan't", 'shouldn', "shouldn't",
                             'wasn', "wasn't", 'weren', "weren't",
                             'won','other','others', "won't",'guys',
                             'another','many','much', 'wouldn','guy',
                             'go', "wouldn't",'retard','retards',
                             'dick','dickhead','bitch','porn',
                             'asshole','pussy','cock']

commodities_of_interests=['wheat','soybean','corn','milk','cheese',
                          'butter','whey','lean hog','live cattle',
                          'lumber','pork','cocoa','sugar','coffee',
                          'cotton','diesel','ethanol','natural gas',
                          'coal','gasoline','gasoil','methanol',
                          'urea','rough rice','oats','palm oil',
                          'lead','carbon','greenhouse gas','freight',
                          'baltic','iron ore','steel','aluminium',
                          'aluminum','copper','gold','silver','brent',
                          'wti','henry hub','uranium','cobalt',
                          'nickel','zinc','palladium','platinum',
                          'propane','naphtha','fuel oil']



def scraping_data(session):
    """scraping"""
    
    logger = logging.getLogger('scraping starts')
    
    flairs=['DD','Discussion',
            'Chart','YOLO',
            '"Earnings%20Thread"',
           'Gain','Loss','News']

    threads=[]
    pages={}

    for flair in flairs:
        url=f'https://new.reddit.com/r/wallstreetbets/search?sort=hot&restrict_sr=on&q=flair%3A{flair}&t=day'
        
        logger.debug(f'scraping {flair}')
        time.sleep(5)
        response=session.get(url,verify=False)

        page=bs(response.content,'html.parser')

        pages[url]=page
        threads+=[i.text for i in page.find_all('span', attrs={'style':"font-weight:normal"})]

    return threads


def create_wordcloud(text):
    """draw wordcloud"""
    
    #use shape    
    mask=np.array(Image.open('silhouette.jpg'))

    wordcloud=WordCloud(mask=mask,
                        #to draw the boundary
                        #contour_width=3,contour_color='grey',
                        background_color='white',
                        #color_func=image_colors,
                        colormap='gist_heat',
                        stopwords=stopword_dict,
                        height=900,
                        width=1200,
                         ).generate(text)

    ax=plt.figure(figsize=(12,9)).add_subplot(111)

    #display the image of word cloud
    plt.imshow(wordcloud)

    #remove axis
    plt.axis("off")
    plt.savefig('output.png')
    
    
def create_df_from_dict(potential):
    """create df from dict"""
    
    if len(potential)==0:
        return pd.DataFrame()
    
    #make sure each value has the same length
    maxlen=max([len(potential[i]) for i in potential])

    for i in potential:
        if len(potential[i])!=maxlen:
            potential[i]+=['']*(maxlen-len(potential[i]))

    return pd.DataFrame().from_dict(potential)



def main():
    """ main  """
    
    logger = logging.getLogger()
    
    session=requests.Session()
    threads=scraping_data(session)
    
    logger.debug("prepare for wordcloud")
    
    #etl
    rawtext=''.join(threads)
    cleantext=[i for i in rawtext.split(' ') if i.lower() not in stopword_dict]
    
    #cleanse
    potential_tickers={}
    potential_commodities={}
    
    for ind,val in enumerate(cleantext):
        
        #remove punctuations
        for j in punctuations:
            if j in val:
                cleantext[ind]=val.replace(j,'')
                
        #remove stopword
        if cleantext[ind].lower() in stopword_dict:
            cleantext[ind]=''
        
        #ticker starts with $
        if val[0]=='$' and not val[1].isdigit():
            potential_tickers[val]=[]
        
        #find commodities of interests
        for ii in commodities_of_interests:
            if ii in val.lower():
                potential_commodities[ii]=[]
    
    #find the context
    for ind,val in enumerate(threads):
        
        for j in potential_commodities:
            if j in val.lower():
                potential_commodities[j].append(val)
            
        for j in potential_tickers:
            if j in val:
                potential_tickers[j].append(val)
    
    
    logger.debug("create output")
    
    #count freq
    lexicons=set([i for i in cleantext])
    D={}
    for word in lexicons:
        D[word]=cleantext.count(word)
    
    #create wordcount
    df=pd.DataFrame()
    df['word']=D.keys()
    df['count']=D.values()
    df.sort_values('count',inplace=True,ascending=False)
    
    #create context finder
    df_commodities=create_df_from_dict(potential_commodities)
    df_tickers=create_df_from_dict(potential_tickers)
    
    #concatenate
    writer=pd.ExcelWriter('output.xlsx')    
    df_commodities.to_excel(writer,
                            sheet_name='potential commodities',
                            index=False)    
    df_tickers.to_excel(writer,sheet_name='potential tickers',
                        index=False)   
    df.to_excel(writer,sheet_name='word count',
                            index=False)    
    writer.save()
    
    
    logger.debug("wordcloud")    
    processed=' '.join(cleantext)
    create_wordcloud(processed)
    
    #cleanse text
    text_commodities=', '.join([i.title() for i in potential_commodities])
    text_tickers=', '.join([i.upper() for i in potential_tickers])
    
    #create html
    row1=f"""*Commodities Mentioned: <font color="red">{text_commodities}</font>"""
    row2=f"""*Tickers Mentioned: <font color="red">{text_tickers}</font>"""
    disclaimer='*Please check the spreadsheet attached for the exact context of the mentioning.'
    image="""<img width=800 height=600 id="1" src="cid:output.png">"""
    html=f"""<p>{row1}</p><p>{row2}</p><br>{image}<br><p>{disclaimer}</p>"""
    
    
    files=['output.png','output.xlsx']
    
    #send email
    try:
        title = dt.datetime.today()

        outlook = win32.Dispatch('outlook.application')  
        mail = outlook.CreateItem(0)      
        receivers = ['lana.rhodes@brazzers.com',
                     'tori.black@brazzers.com',
                     'naomi.woods@brazzers.com']  
        mail.To = ';'.join(receivers)   
        mail.Attachments.Add(Source=files)
        mail.Subject ='What was Reddit talking about %s'%(title)
        mail.BodyFormat=2    
        mail.HTMLBody=html
        mail.Send()
        
    except Exception:
        print(traceback.format_exc())
            

if __name__ == "__main__":
    main()
