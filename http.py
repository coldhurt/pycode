#!/usr/bin/python
#coding=utf-8

import requests
import os
import threading
import argparse

mutex = threading.Lock()
def getHeaders(target, header):
    if not str(target).startswith('http'):
        target = 'http://' + target
    res = requests.head(target)
    if res.headers and mutex.acquire(1):
        print('\n[+]Target: ' + target)
        if header != 'all':
            print(header + ' : ' + res.headers[header])
        else:
            for n in res.headers:
                print(n + ' : ' + res.headers[n])
    mutex.release()

def getTargets(file, header):
    if os.path.exists(file):
        f = open(file, 'r')
        for l in f.readlines():
            t = threading.Thread(target=getHeaders, args=(l.replace('\n',''), header))
            t.start()

def main():
    parse = argparse.ArgumentParser(description='Show HTTP Headers')
    parse.add_argument('-t', dest='target', action='store', help='target url')
    parse.add_argument('-f', dest='file', action='store', help='file includes targets')
    parse.add_argument('-H', dest='header', action='store', default='all', help='target header')
    args = vars(parse.parse_args())
    if args['file']:
        getTargets(args['file'], args['header'])
    else:
        getHeaders(args['target'], args['header'])

if __name__ == '__main__':
    main()