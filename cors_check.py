#!/usr/bin/python
#coding=utf-8

import requests
import argparse
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    parse = argparse.ArgumentParser(description='Detect whether the target has cors vulnerability')
    parse.add_argument('target', action='store', help='target')
    args = vars(parse.parse_args())
    if args['target']:
        headers = {'Origin': 'http://test.com'}
        r = requests.get(args['target'], headers=headers)
        cors = r.headers.get('Access-Control-Allow-Origin', '')
        if cors == '*' or cors == headers['Origin']:
            print(bcolors.OKGREEN + 'Has cors vulnerability')
        else:
            print(bcolors.FAIL + 'Not vulnerable')
        if cors:
            print('Response Access-Control-Allow-Origin is ' + cors)
    

if __name__ == '__main__':
    main()