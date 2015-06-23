# -*- coding: UTF-8 -*-
# coding=UTF-8
__author__ = 'g2525_000'

import sys
import re
import io
import jieba.analyse

from optparse import OptionParser
reload(sys)
sys.setdefaultencoding("utf-8")

def TFIDF(topK = 10, train = False):

    file_name = "trainingdata.txt"

    content = open(file_name, 'rb').read()
    jieba.set_dictionary('dict.txt.big')
    jieba.analyse.set_idf_path("idf.txt.big")
    jieba.analyse.set_stop_words("stop_words.txt")
    tags = jieba.analyse.extract_tags(content, topK=topK,withWeight=True)
    f = open("keywords.txt", "w")
    #for tag in tags:
    #    print("tag: %s\t\t weight: %f" % (tag[0],tag[1]))


    return tags

def isPoltics(body = ""):
    tags = TFIDF(14)
    f = io.open('data.txt', 'r', encoding='UTF-8')
    data = f.read()
    data = data.split("\"內文\":")
    print(data[3])

    weight = 0
    count = 0
    for tag in tags:
        temp = tag[0]
        times = body.count(temp)
        if times > 0:
            count = count + 1
        weight += times * tag[1]
    if count !=0 :
        weight = weight / count
    else:
        weight = 0.0
    print(weight)
    if weight > 0.28:
        return True
    else:
        return False

