# nouvelle

Proxy, it has always been associated with censorship. It is commonly used to access the websites blocked by some parties (e.g. governments) or it is enforced by some parties (e.g. corporates) for the purpose of surveillance. Either way, it is against liberté. Yet, it’s not my place to make a moral judgement. For whatever reason to use proxy, the authentication can become a huge pain in the ass. I have literally spent hours scratching my head to figure out why my code doesn’t work. Here are a few key points to make our life easier.

###### URL Protocol, Domain and Port

It goes without saying how important proxy URL is. Protocol is usually `http` but occasionally `https`. Domain could be a bunch of number (e.g. 192.168.1.1) or a normal one (e.g. myproxy.com). As for the port, it can only be numbers (e.g. 8080).
If you don’t have URL information, you can always try to check Local Area Network Settings. Assuming you are using Windows, you can go to internet options in IE (in windows 10, you can find it in Windows Settings - Network & Internet - Proxy)

Click connections on the top panel then click LAN settings

You could find the proxy setup here

If not, you have to contact your local IT administrator. Sometimes python may be going through proxy by default. We could pass empty dictionary to `session.proxies` to get things working. 

Once we obtain the proxy URL, we can do
```Python
session.proxies={'http':'http://domain:port'}
```
###### Username and Password

Proxy commonly requires authentication. The package we are using offers three types of authentication, HTTPBasicAuth, HTTPDigestAuth and HTTPProxyAuth. For simplicity, we just do
```Python
session.auth=requests.auth.HTTPProxyAuth('username',
                                         'password')
```

###### Certificates

Given correct username and password, you still get `TimeoutError` thrown to your face? Or what exactly is this `SSLError`? You are not alone! I have been hung out to dry for days simply because I neglect the role of certificates. The library `requests` provide two types of certificates, SSL and client side. They are both handy to use. For client side certificates, we can do
```Python
session.cert='path/proxy.cer'
```

For SSL certificates, we can do
```Python
session.verify='path/proxy.cer'
```

If you don't know where to find certificates or your IT administrator does not cooperate, additionally, there is a dangerous shortcut. We simply disable SSL verification at the risk of man in the middle attack (by raising this issue, your IT admin shall comply, it works every time :smirk: ).
```Python
session.verify=False
```

Now we can harness the power of web-scraping!
```Python
session.get('https://www.lepoint.fr/gastronomie/')
```
