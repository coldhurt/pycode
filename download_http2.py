# -*- coding:utf-8 -*-
"""
    This program is designed to download all images of a page of https://www.mzitu.com/zipai/comment-page-1/#comments
"""

from bs4 import BeautifulSoup
from hyper.contrib import HTTP20Adapter
import requests
import re
import os

folder = './imgs'  # Folder to save images
s = requests.Session()


def getHeaders(url):
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': url,
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0'
    }


def downloadFile(url):
    name = os.path.basename(url)
    if not os.path.exists(folder):
        os.mkdir(folder)
    path = os.path.join(folder, name)
    f = open(path, 'wb')
    f.write(s.get(url, headers=getHeaders(url)).content)
    f.close


def getImgUrls(url):
    s.mount(url, HTTP20Adapter())
    html_content = s.get(url, headers=getHeaders(url)).text
    soup = BeautifulSoup(html_content, "html.parser")
    img_urls = soup.findAll('img', class_='lazy')
    for i in img_urls:
        downloadFile(i['data-original'])


def analysis(t):
    s = re.findall('http[s]?://', t)
    if len(s) == 1:
        getImgUrls(t)
    else:
        print('Invalid url')


def main():
    u = input('Please input target url')
    s = re.findall('http[s]?://', u)
    if len(s) == 1:
        analysis(u)
    else:
        print('Invalid url')


if __name__ == '__main__':
    main()
