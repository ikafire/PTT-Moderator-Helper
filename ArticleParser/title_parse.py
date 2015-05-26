# -*- coding: utf-8 -*-

# import json
import article
'''
# Parsing JSON format (Test data)
articles = json.loads('[{"2_作者":"liveforhappy(a)","3_標題":"[問卦]有沒有","4_日期":"Thu May 13 21:56:01 2015"},\
                        {"2_作者":"liveforhappy(a)","3_標題":"[問卦]有沒有","4_日期":"Thu May 13 21:56:01 2015"},\
                        {"2_作者":"liveforhappy(a)","3_標題":"[問卦]有沒有","4_日期":"Thu May 13 21:56:01 2015"},\
                        {"2_作者":"liveforhappy(a)","3_標題":"[新聞]有沒有","4_日期":"Thu May 13 21:56:01 2015"},\
                        {"2_作者":"liveforhappy(a)","3_標題":"[新聞]有沒有","4_日期":"Thu May 13 21:56:01 2015"},\
                        {"2_作者":"liveforhappy(a)","3_標題":"有沒有","4_日期":"Thu May 13 21:56:01 2015"},\
                        {"2_作者":"liveforhappy(a)","3_標題":"[公告]有沒有","4_日期":"Thu May 13 21:56:01 2015"}]')
'''

class TitleParser:
    def __init__(self):
        self.users_dict = {} # key = user id; value = [總發文數, [新聞]數, [問卦]數, 轉錄文章數, 退文數]
        self.violations = {} # key = article id; value = [article_title, article_link, [violated_rules]]
        self.moderator_list = ['meowmeowgo', 'seabox', 'APPLEin5566', 'XXXXGAY']
        self.prev_date = '' # Post date of previous article

    def add_violation(self, article, violated_rule):
        if article.id in self.violations:
            self.violations[article.id][2].append(violated_rule)
        else:
            self.violations[article.id] = [article.title, article.link, [violated_rule]]

    def check_date(self, article):
        # Check date
        # If the date has changed, clear the user data.
        if not article.date[0:9] == self.prev_date[0:9]:
            self.users_dict.clear()
            prev_date = article.date

    def get_author_data(self,article):
        # Check the author
        author = article.author
        if author in self.users_dict:
            self.users_dict[author][0] += 1 # total_count increases by 1
        else:
            # Initialize user data
            self.users_dict[author] = [1, 0, 0, 0, 0]

    def check_tag(self, article):
        tag = article.get_tag()
        author = article.author
        print tag
        if tag == u'新聞':
            self.users_dict[author][1] += 1
            self.check_news_num(article)
        elif tag == u'問卦':
            self.users_dict[author][2] += 1
            self.check_ask_num(article)
        elif tag == u'爆卦':
            pass
        elif tag == u'公告':
            if not article.author in self.moderator_list:
                self.add_violation(article, u'1-9-2 5. 任意使用公告、回應公告。')
        elif tag == u'轉錄':
            self.users_dict[author][3] += 1
            self.check_transfer_num(article)
        else:
           self.add_violation(article, u'1-1-4 文章請使用本看板所提供之分類，自訂分類或無分類之文章一律刪除。')

    def check_news_num(self, article):
        author = article.author
        # check news number
        if self.users_dict[author][1] == 2:
            if self.users_dict[author][4] < 1:
                self.add_violation(article, u'1-1-1 新聞額度超貼 1 篇。以退文處理。')
                self.users_dict[author][4] += 1
            else:
                self.add_violation(article, u'1-1-1 新聞額度超貼', self.users_dict[author][1]-1 , u'篇。')
        elif self.users_dict[author][1] > 2:
            self.add_violation(article, u'1-1-1 新聞額度超貼', self.users_dict[author][1]-1 , u'篇。')
    def check_ask_num(self, article):
        author = article.author
        # Check ask posts
        if self.users_dict[author][2] == 3:
            if self.users_dict[author][4] < 1:
                self.add_violation(article, u'1-1-1 問卦額度超貼 1 篇。以退文處理。')
                self.users_dict[author][4] += 1
            else:
                self.add_violation(article, u'1-1-1 問卦額度超貼', self.users_dict[author][2]-2 , u'篇。')
        elif self.users_dict[author][2] > 3:
            self.add_violation(article, u'1-1-1 問卦額度超貼', self.users_dict[author][2]-2 , u'篇。')
    def check_transfer_num(self, article):
        author = article.author
        # Check transfer posts
        if self.users_dict[author][3]>1:
            self.add_violation(article, u'1-1-5 轉錄文章限制一人一天一篇，超貼轉錄', self.users_dict[author][3]-1 ,u'篇, 水桶', (self.users_dict[author][3]-1)*2 , u'週。')
    def check_total_num(self, article):
        author = article.author
        # Check total posts
        if self.users_dict[author][0] > 5:
            self.add_violation(article, u'1-1-1 每日發文額度超貼', self.users_dict[author][0]-5 , u'篇。')

    def parse(self, article):
        self.check_date(article)
        self.get_author_data(article);
        self.check_tag(article)
        self.check_total_num(article)

def main():
    articles = article.create_articles_from_file('data.json')
    title_parser = TitleParser();
    for a in articles:
        title_parser.parse(a)
    for v in title_parser.violations.values():
        print v[0]
        print v[1]
        for rule in v[2]:
            print rule



if __name__ == '__main__':
    main()
