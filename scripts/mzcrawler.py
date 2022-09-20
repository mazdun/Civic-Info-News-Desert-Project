#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#import sys
#import subprocess

#subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#'newspaper3k'])
#subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#'storysniffer'])
#subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#'dill'])
#subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#'scikit-learn==1.0.2'])


import requests
from urllib.parse import urlparse, urljoin
import sys
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json
import urllib.parse
import hashlib
from storysniffer import StorySniffer
import ast
from newspaper import Article
import nltk

#Whole Script

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_news_urls(url):
    # all URLs of `url`
    domain_name = urlparse(url).netloc
    urls = set()
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                external_urls.add(href)
            continue
        urls.add(href)
        internal_urls.add(href)

def crawl(news_url):
    print('get link ==> ', news_url)
    resp = requests.get(news_url)
    return resp.text

def get_host(url: str):
    token = url.split('://')[1]
    token = token.split('.')
    if token[0] == 'www':
        return token[1]
    return token[0]

if __name__ == "__main__":
    
    print(sys.argv)

    if len(sys.argv) < 2:
        print('Need more arguments \n example: python crawler.py url')
        exit(1)
        
    internal_urls = set()
    external_urls = set()
    
    url = sys.argv[1]

    urls = get_news_urls(url)

    valid_urls = []
    
    sniffer = StorySniffer()

    for u in internal_urls:
        try:
            if sniffer.guess(u) == True:
                valid_urls.append(u)

        except BaseException as e:
            pass

    news_data = []
    # print(valid_urls)
    for u in valid_urls:
        hash = hashlib.sha256(u.encode())
        news_data.append({
            'id': hash.hexdigest(),
            'url': u,
            'crawl_date': str(datetime.now()),
            'text': crawl(u),
            'host': urllib.parse.urlsplit(u).hostname
        })
print(news_data[0])

    #with open('{}_{}.json'.format(get_host(url), str(datetime.now())), 'w') as f:
        #json.dump(news_data, f, indent=4, ensure_ascii=True)

