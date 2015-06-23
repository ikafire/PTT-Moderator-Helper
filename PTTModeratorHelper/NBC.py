# -*-coding:utf-8-*-
import article
import jieba
import jieba.analyse

from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier

class NaiveBayesClassifier:
    def __init__(self):
        jieba.set_dictionary('dict.big.txt')
        self.articleTrainer = Trainer(tokenizer)

    def train(self):
        # Training
        articles = article.create_articles_from_file("data/HatePoliticsdata.json")
        p_train = articles[0:3001]
        p_test = articles[3001:3031]

        for a in p_train:
            doc = a.body
            #seg_list = jieba.lcut(doc, cut_all=False)
            seg_list = jieba.analyse.extract_tags(doc)
            doc = " ".join(seg_list)
            self.articleTrainer.train(doc, 'politics')

        articles = article.create_articles_from_file("data/Gossipingdata.json")
        g_train = articles[0:3000]
        g_test = articles[3001:3301]

        for a in g_train:
            doc = a.body
            #seg_list = jieba.lcut(doc, cut_all=False)
            seg_list = jieba.analyse.extract_tags(doc)
            doc = " ".join(seg_list)
            self.articleTrainer.train(doc, 'gossiping')

    def classify(self, article):
        #Testing
        self.articleClassifier = Classifier(articleTrainer.data, tokenizer)
        doc = a.body
        #seg_list = jieba.lcut(doc, cut_all=False)
        seg_list = jieba.analyse.extract_tags(doc)
        doc = " ".join(seg_list)
        classification = articleClassifier.classify(doc)
        return classification[0][0]
