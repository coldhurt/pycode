#!/usr/bin/python

import requests
from bs4 import BeautifulSoup

url = 'https://www.socks-proxy.net/'
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
    table = bso.findAll('table', attrs={'id':'proxylisttable'})
    trs = list(list(table[0].children)[1].children)
    for tr in trs:
        tds = list(tr.children)
        # print('ip:%s,port:%s,type:%s'%(tds[0].text,tds[1].text,tds[4].text))
        print('%s %s %s'%(tds[4].text.lower(), tds[0].text, tds[1].text))


if __name__ == '__main__':
    parse()