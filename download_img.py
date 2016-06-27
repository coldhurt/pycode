#-*- coding:utf-8 -*-
"""
    This program is designed to download all images of a post of tieba.baidu.com
"""

from bs4 import BeautifulSoup
import requests
import re
import os

folder = 'H:/imgs' #Folder to save images

def downloadFile(url):
    name = os.path.basename(url)
    if not os.path.exists(folder):
        os.mkdir(folder)
    path = os.path.join(folder,name)
    f = open(path,'wb')
    f.write(requests.get(url).content)
    f.close


def getImgUrls(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': url,
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0'
    }
    soup = BeautifulSoup(requests.get(url).text,"html.parser")
    img_urls = soup.findAll('img',class_='BDE_Image');
    for i in img_urls:
        if len(re.findall('jpg$',i['src'])) != 0:
            print i['src']
            downloadFile(i['src'])

def analysis(t):
    s = re.findall('http[s]?://',t)
    if len(s) == 1:
        getImgUrls(t)
    else:
        print 'Invalid url'

def main():
    u = raw_input('Please input target url')
    s = re.findall('http[s]?://',u)
    if len(s) == 1:
        soup = BeautifulSoup(requests.get(u).text,"html.parser")
        pages = len(soup.findAll('a',href=re.compile('pn=\d$')))/2
        print pages
        for i in range(1,pages,1):
            t = u + '?pn=' + str(i)
            print '[*]Target url:' + t
            analysis(t)
    else:
        print 'Invalid url'


if __name__ == '__main__':
    main()
