#!/usr/bin/python
#coding=utf-8

import urllib2
import threading
import Queue
import urllib

def build_wordlist(wordlist):
    '''Create Queue of file wordlist

    Args:
        wordlist: file path of the wordlist
    '''
    fd = open(wordlist, 'rb')
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words = Queue.Queue()

    for word in raw_words:
        word = word.rstrip()
        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print('Resuming wordlist from : %s' % resume)
        else:
            words.put(word)
    return words

def dir_bruster(target, word_queue, extensions=None):
    '''Scan target use wordlist queue and extendsions

    Args:
        target: target url
        word_queue: a Queue obj created by build_wordlist function
        extensions: some extension, a list or tuple
    '''
    while not word_queue.empty():
        path = word_queue.get()
        paths = []

        if '.' not in path:
            paths.append('/%s/' % path)
        else:
            paths.append('/%s' % path)

        if extensions:
            for ext in extensions:
                paths.append('/%s%s' % (path, ext))
        
        for brust in paths:
            url = '%s%s' % (target, urllib.quote(brust)) #urllib.quote can encode request path to support Chinese or other language
            try:
                headers = {}
                headers['user-agent'] = user_agent
                r = urllib2.Request(url, headers=headers) # create request through url and headers
                res = urllib2.urlopen(r) #urlopen send request
                if len(res.read()) and mutex.acquire(1):
                    print('[%d] => %s' % (res.code, url))
                    mutex.release()
            except urllib2.HTTPError as e:
                if hasattr(e, 'code') and e.code != 404:
                    print('!!! %d => %s' % (e.code, url))
                pass

threads = 10 # thread count
target_url = 'http://testphp.vulnweb.com' #target url to scan, there is a test site provided by OWASP
wordlist = './dir.txt' #wordlist path
resume = None
mutex = threading.Lock()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
word_queue = build_wordlist(wordlist)
extensions = ['.php','.html']
for i in range(threads):
    t = threading.Thread(target=dir_bruster, args=(target_url, word_queue, extensions))
    t.start()
