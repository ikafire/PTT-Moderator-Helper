# -*- coding: utf-8 -*-

class Article:
    def __init__(self):
        pass

    def get_tag(self):
        start = self.title.find(u'[')
        end = self.title.find(u'[', start)
        if start >= 0 and end >= 0:
            tag = self.title[(start + 1):end]
        else:
            tag = ''
        return tag

def create_articles_from_file(filename):
    f = open(filename, 'r')
    import json
    j = json.load(f)
    articles = []
    for entry in j:
        article = Article()
        article.id = entry[u'1_ID']
        article.author = entry[u'2_作者']
        article.title = entry[u'3_標題']
        article.date = entry[u'4_日期']
        article.ip = entry[u'5_ip']
        article.body = entry[u'6_內文']
        article.link = entry[u'7_文章網址']
        article.type = entry[u'8_發文/回文']
        article.timestamp = entry[u'9_TimeStamp']
        articles.append(article)
    return articles

def main():
    articles = create_articles_from_file('data.json')
    for a in articles:
        print(a.title)

if __name__ == '__main__':
    main()