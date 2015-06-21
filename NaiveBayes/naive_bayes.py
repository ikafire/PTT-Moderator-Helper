# -*-coding:utf-8-*-
import article
import jieba
import jieba.analyse

jieba.set_dictionary('dict.big.txt')

from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier

# Training
articleTrainer = Trainer(tokenizer)

articles = article.create_articles_from_file("data/HatePoliticsdata.json")
p_train = articles[0:3001]
p_test = articles[3001:3031]

for a in p_train:
    doc = a.body
    #seg_list = jieba.lcut(doc, cut_all=False)
    seg_list = jieba.analyse.extract_tags(doc)
    doc = " ".join(seg_list)
    articleTrainer.train(doc, 'politics')

articles = article.create_articles_from_file("data/Gossipingdata.json")
g_train = articles[0:3000]
g_test = articles[3001:3301]

for a in g_train:
    doc = a.body
    #seg_list = jieba.lcut(doc, cut_all=False)
    seg_list = jieba.analyse.extract_tags(doc)
    doc = " ".join(seg_list)
    articleTrainer.train(doc, 'gossiping')

#Testing
articleClassifier = Classifier(articleTrainer.data, tokenizer)
p_gossiping = 0
p_politics = 0
g_gossiping = 0
g_politics = 0

for a in p_test:
    doc = a.body
    #seg_list = jieba.lcut(doc, cut_all=False)
    seg_list = jieba.analyse.extract_tags(doc)
    doc = " ".join(seg_list)
    classification = articleClassifier.classify(doc)
    if classification[0][0] == 'gossiping':
        p_gossiping += 1
    else:
        p_politics += 1

for a in g_test:
    doc = a.body
    #seg_list = jieba.lcut(doc, cut_all=False)
    seg_list = jieba.analyse.extract_tags(doc)
    doc = " ".join(seg_list)
    classification = articleClassifier.classify(doc)
    if classification[0][0] == 'gossiping':
        g_gossiping += 1
    else:
        g_politics += 1

print(p_gossiping, ' ', p_politics, ' ', g_gossiping, ' ', g_politics)
