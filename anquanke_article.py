# -*- coding: utf-8 -*-
#www.anquanke.com
#获取文章正文内容

import sys
import requests
import random
import time
from lxml import etree
from pymongo import MongoClient

my_headers = [    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
                  "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                  'Opera/9.25 (Windows NT 5.1; U; en)',
                  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                  'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                  'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                  "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                  "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36']
headers = {
    'user-agent': random.choice(my_headers),
    'Connection': 'keep-alive',
    'host': 'www.anquanke.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Enocding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def get_article(id):
    url = 'https://www.anquanke.com/post/id/{0}'.format(str(id))
    print(url)
    try:
        page_source = requests.get(url, headers=headers).content
    except:
        time.sleep(60)
        try:
            page_source = requests.get(url, headers=headers).content
        except:
            sys.exit(0)

    html = etree.HTML(page_source)
    article = html.xpath("//div[@class='article-content']")
    article_text = ''
    for x in article:
        for eve_text in x.itertext():
            article_text = article_text + ' ' + eve_text

    dict = {
        '_id': id,
        'url': url,
        'article': article_text.encode('utf-8')
    }
    return dict

def save_mongo(dict):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.anquanke
    my_set = db.test_1102_1311
    try:
        my_set.insert(dict)
        print('******************insert database success!*************************')
    except:
        print('###################insert database fail!!#######################')

def get_id_from_mongo():
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.anquanke
    my_set = db.test_1102_1125
    all_article = my_set.find()
    for article in all_article:
        print('----------------------------------------------------------------------------------------------------')
        dict = get_article(article['id'])
        save_mongo(dict)

if __name__ == '__main__':
    get_id_from_mongo()