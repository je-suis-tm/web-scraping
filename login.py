#this is a script to scrape website that requires login
#make sure you understand the basics of a webpage
#u should go through other simple scrapers in this repo before moving to this one
# https://github.com/je-suis-tm/web-scraping

#in the following context
#the script is trying to get some articles from a website
#this website called cqf only allows pdf download for registered users

import requests
from bs4 import BeautifulSoup as bs
import re
import os
os.chdir('d:/')

def main():
          
    #input your username and password
    #ideally we should not store password
    #we should use getpass as followed
    """
    import getpass
    getpass.getpass('input password:')
    """
    session=requests.Session()
    username=''
    password=''
    prefix='https://www.cqfinstitute.org/cqf-access/nojs/'
    login_url='https://www.cqfinstitute.org/user/login?destination=cqf-access/nojs/'

    
    #the first stage is to get a list of what you want
    response=session.get('https://www.cqfinstitute.org/articles')
    page=bs(response.content,'html.parser')
    
    #in this case, we just need to find a list of all the articles
    #each article is assigned with a code
    #we only need (prefix+code) to visit the article download website
    articlelist=page.find_all('a',class_='use-ajax ctools-modal-cqf-popup')
    
    d={}
    for i in articlelist:
        if i.text:
            d[i.text]=re.search('(?<=nojs\/)\d*',
                                i.get('href')).group()
    
    #d is a dictionary that contains all the articles and codes
    #for simplicity, we only wanna get the first article
    target=d[list(d.keys())[0]]
          
          
    #the second stage is authentication
    #for websites without captcha or other methods to detect bots
    #it will be as simple as followed
    #if we need to go through captcha or other human verification
    #we can use neural network to recognize stuff
    #or download the image and let human identify it
    #this script will not cover that part (cuz i am lazy)
    
    #u may wonder where i get the headers and data from
    #before writing any script at all
    #we should use browser to login and go through the process
    #while typing username and password in browser
    #we can right click and inspect element
    #in chrome, simply ctrl+shift+i
    #the top columns in a popup window are elements, console, sources, network...
    #we select network monitor before we login
    #next, we click sign in button
    #and we should see a lot of traffic in network monitor
    #usually there is something called login or sign-in or auth
    #when we click it, we can see our username and password in form data
    #voila, that is everything we need to post
    #an easy way is to copy as powershell and paste it in our ide
    #we just need to restructure headers and form data in a pythonic way
    #normally we dont include cookies as they may expire after a few weeks
    #and we can find login url in request url section 
    auth=session.post(login_url+target,
                 headers={"Cache-Control":"max-age=0",
                          "Origin":"https://www.cqfinstitute.org",
                          "Upgrade-Insecure-Requests":"1",
                          "DNT":"1",
                          "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
                          "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                          "Referer":"https://www.cqfinstitute.org/user/login?destination=cqf-access/nojs/"+target,
                          "Accept-Encoding":"gzip, deflate, br",
                          "Accept-Language":"en-US,en;q=0.9"},
                 data={'name': username,
                       'pass': password,
                       'form_id': 'user_login',
                       'device_authentication_operating_system': 'Windows 10 64-bit',
                       'device_authentication_browser': 'Chrome',
                       'op': 'Log in'})
    
          
    #normally when we finish login
    #we should take a look at the response
    #in most cases, login response is a json
    #we need to find something like token or auth
    #and update the session header as followed
    """
    token=auth.json()["token"]
    session.headers.update({"Authorization": 'Token %s'%token})
    """
    

    #once we officially sign in as a user
    #the third stage is to download the pdf
    response=session.get(prefix+target)
    page=bs(response.content,'html.parser')
    
    pdf_link=(page.find('div',class_='file file-ext').find('a').get('href'))
    
    pdf=session.get(pdf_link)
    
    f=open('a.pdf','wb')
    f.write(pdf.content)
    f.close()
        
    
    return

    
    
if __name__ == "__main__":
    main()
