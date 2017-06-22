#!/usr/bin/python
#coding=utf-8

import requests
import Queue
import threading
import sys
import argparse
from pyquery import PyQuery as pq

mutex = threading.Lock()
class search_bing(object):
    def __init__(self, q, page=1, file=''):
        self.wd = q #inurl search string
        self.page = page # page count
        self.file = None # save file
        if file:
            self.file = open(file,'a')
        self.url = 'http://cn.bing.com/search?q=' + q

    def search(self, pageNo):
        res = requests.get('%s&first=%d' % (self.url, pageNo*10+1))
        pageNo = pageNo + 1    
        p = pq(res.content) #use pyquery to resolve every page content
        cite = p.find('cite') #find all urls
        mutex.acquire(1)
        print('pageNo:' + str(pageNo))
        for n in cite:
            text = pq(n).text().replace(' ','')
            if self.wd.replace('inurl:','') in text: #check target inurl string exists in result url
                if self.file is not None:
                    self.file.write(text + '\n') #write to file
                print(text)
        mutex.release()

    def run(self):
        threads = []
        for i in range(int(self.page)):
            t = threading.Thread(target=self.search, args=[i])
            threads.append(t)
        for n in threads:
            n.start()
        for n in threads:
            n.join()
        if self.file is not None:
            self.file.close()
def main():
    parse = argparse.ArgumentParser(description='This program is to print urls in bing search result about inurl syntax search.')
    parse.add_argument('string', action='store', help='search string')
    parse.add_argument('-p', default=1, dest='page', action='store', help='page count')
    parse.add_argument('-o', dest='file', action='store', help='output file', type=str)
    args = vars(parse.parse_args())
    sea = search_bing(args['string'], args['page'], args['file'])
    sea.run()

if __name__ == '__main__':
    main()