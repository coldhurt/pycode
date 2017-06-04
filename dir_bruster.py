#!/usr/bin/python
#coding=utf-8

import urllib2
import threading
import Queue
import os
import urllib
import argparse

resume = None
mutex = threading.Lock()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'

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
                if ext.startswith('.'):
                    paths.append('/%s%s' % (path, ext))
                else:
                    paths.append('/%s.%s' % (path, ext))
        
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

def main():
    parse = argparse.ArgumentParser(description='A dir scanner')
    parse.add_argument('url', action='store', help='target url')
    parse.add_argument('-w', required=True, dest='wordlist', action='store', help='wordlist path')
    parse.add_argument('-t', dest='threads', action='store', help='thread count', type=int, default=10)
    parse.add_argument('-e', dest='extensions', action='store', help='extensions, eg: "php,asp"', default='')
    args = vars(parse.parse_args())
    global target,wordlist,threads,extensions
    target, wordlist, threads, ext = args['url'], args['wordlist'], args['threads'], \
    args['extensions'].split(',')
    if not target.startswith("http://"):
        target = 'http://%s' % target
    if os.path.exists(wordlist):
        word_queue = build_wordlist(wordlist)
        for i in range(threads):
            t = threading.Thread(target=dir_bruster, args=(target, word_queue, ext))
            t.start()

if __name__ == '__main__':
    main()
