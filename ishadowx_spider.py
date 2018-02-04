#!/usr/bin/python

import requests
from bs4 import BeautifulSoup, element

url = 'https://global.ishadowx.net/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': url,
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'
}

def parse():
    req = requests.get(url, headers=headers)
    bso = BeautifulSoup(req.content,"html.parser")
    freess = bso.findAll('div', attrs={'class':'hover-text'})
    for item in freess:
        cld = list(item.children);
        hostname = list(cld[1].children)[1]
        port = list(cld[3].children)[1]
        password = list(cld[5].children)[1]
        method = cld[7]
        print('"server" : "%s"' % hostname.text)
        print('"server_port" : %s' % port.text.strip())
        print('"password" : "%s"' % password.text.strip())
        print('"method" : "%s"\n' % method.text.replace('Method:',''))
            
if __name__ == '__main__':
    parse()