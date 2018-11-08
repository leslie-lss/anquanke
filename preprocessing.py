# -*- coding: utf-8 -*-
#www.anquanke.com
#处理获取到的文章内容
#过滤掉英文及特殊字符，保留中文字符
#利用jieba进行中文分词
from pymongo import MongoClient
import jieba
import re


def import_stopword_dict():
    stopwords = []
    with open('stopword.txt', 'r') as f:
        for line in f.readlines():
            line = line.decode('utf-8')
            stopwords.append(line[:-1])
    return stopwords

def get_dict_from_mongo():
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.anquanke
    my_set = db.news_article_1102_1335
    for x in my_set.find():
        print(x['url'])
        dict = filter_url(x)
        dict = remain_chinese_english(dict)
        print('remain_chinese_english:')
        print(dict['article_chi'])
        print(dict['article_eng'])
        dict = jieba_text(dict)
        print('stop_word:')
        print(dict['article_chi_final'])
        print(dict['article_eng_final'])
        save_mongo(dict)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

#过滤掉文本中的网址url
def filter_url(dict):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = re.findall(pattern, dict['article'])
    dict['article_no_url'] = re.sub(pattern, ' ', dict['article'])
    print('all urls:')
    for url in urls:
        print(url)
    return dict

#保留中英文字符
def remain_chinese_english(dict):
    # 处理帖子正文，保留中英文字符，其余均替换为space
    post_text = dict['article_no_url']
    article_chi = ''
    article_eng = ''
    for uchar in post_text:
        if is_chinese(uchar):
            article_chi = article_chi + uchar
        elif is_english(uchar):
            article_eng = article_eng + uchar.lower()
        else:
            article_chi = article_chi + ' '
            article_eng = article_eng + ' '

    dict['article_chi'] = article_chi.encode('utf-8')
    dict['article_eng'] = article_eng.encode('utf-8')
    return dict

#判断一个unicode是否为汉字
def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

#判断一个unicode是否为英文字符
def is_english(uchar):
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


#利用jiaba进行分词
def jieba_text(dict):
    article_chi = dict['article_chi']
    seg_chi = jieba.cut(article_chi)
    dict['article_chi_final'] = stop_word(seg_chi).encode('utf-8')

    article_eng = dict['article_eng']
    seg_eng = jieba.cut(article_eng)
    dict['article_eng_final'] = stop_word(seg_eng).encode('utf-8')
    return dict

#去除掉无意义的停用词
def stop_word(seg_list):
    final_text = ''
    for word in seg_list:
        if word not in stopwords:
            final_text = final_text + ' ' + word
    return final_text

def save_mongo(dict):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.anquanke
    my_set = db.news_fenci_1102_1441
    try:
        my_set.insert(dict)
        print('******************insert database success!*************************')
    except:
        print('###################insert database fail!!#######################')

if __name__ == '__main__':
    stopwords = import_stopword_dict()
    get_dict_from_mongo()
