# -*- coding: utf-8 -*-

class Article:
    def __init__(self):
        pass

    def get_tag(self):
        start = self.title.find(u'[')
        end = self.title.find(u']', start)
        if start >= 0 and end >= 0:
            tag = self.title[(start + 1):end]
        else:
            tag = ''
        return tag


def create_articles_from_file(filename):
    f = open(filename, 'r', -1, 'utf-8')
    import json
    j = json.load(f)
    articles = []
    for entry in j:
        article = Article()
        article.id = entry[u'ID']
        article.author = entry[u'作者']
        if article.author.find('(') > 0:
            article.author = article.author[0 : article.author.find('(')]
        article.title = entry[u'標題']
        article.date = entry[u'日期']
        article.ip = entry[u'ip']
        article.body = entry[u'內文']
        article.link = entry[u'文章網址']
        article.type = entry[u'發文/回文']
        article.timestamp = entry[u'TimeStamp']
        article.signature = entry[u'簽名檔']
        articles.append(article)
    return articles

def main():
    articles = create_articles_from_file('data.json')
    for a in articles:
        print(u'ID: {0}'.format(a.id))
        print(u'作者: {0}'.format(a.author))
        print(u'標題: {0}'.format(a.title))
        print(u'日期: {0}'.format(a.date))
        print(u'IP: {0}'.format(a.ip))
        print(u'內文: {0}'.format(a.body))
        print(u'網址: {0}'.format(a.link))
        print(u'發回文: {0}'.format(a.type))
        print(u'Timestamp: {0}'.format(a.timestamp))
        print(u'簽名檔: {0}'.format(a.signature))


if __name__ == '__main__':
    main()
