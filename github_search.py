#!/usr/bin/env python

import sys
import requests

# curl -H 'Accept: application/vnd.github.v3.text-match+json'
# https://api.github.com/search/code\?q\=password+in:file+language:python+user:tyrchen
def query(keyword, lang, username):
    url = 'https://api.github.com/search/code?q=%s+in:file+language:%s+user:%s' % (keyword, lang, username)
    headers = {'Accept': 'application/vnd.github.v3.text-match+json'}
    print("Using url: %s" % url)
    r = requests.get(url, headers=headers)

    data = r.json()
    total = data['total_count']
    items = data['items']

    print("Total %s matches." % total)
    for item in items:
        path = item['path']
        if 'migration' in path:
            continue

        code_url = item['html_url']
        repo_desc = item['repository']['description']
        fragments = map(lambda x: x['fragment'], item['text_matches'])
        print("In file: %s:" % path)
        #print("\tURL: %s" % code_url)
        #print("\tDesc: %s" % repo_desc)
        #print("\tMatches:")
        for frag in fragments:
            print("\t%s" % frag.replace('\r', ' ').replace('\n', ' '))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: %s <keyword> <language> <user>" % sys.argv[0])
        exit(-1)

    query(sys.argv[1], sys.argv[2], sys.argv[3])

 
