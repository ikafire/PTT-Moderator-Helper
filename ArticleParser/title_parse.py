# -*- coding: utf-8 -*-
import json

# Parsing JSON format (Test data)
articles = json.loads('[{"2_作者":"liveforhappy(a)","3_標題":"[問卦]有沒有","4_日期":"Thu May 13 21:56:01 2015"},\
                        {"2_作者":"liveforhappy(a)","3_標題":"[問卦]有沒有","4_日期":"Thu May 13 21:56:01 2015"},\
                        {"2_作者":"liveforhappy(a)","3_標題":"[問卦]有沒有","4_日期":"Thu May 13 21:56:01 2015"},\
                        {"2_作者":"liveforhappy(a)","3_標題":"[新聞]有沒有","4_日期":"Thu May 13 21:56:01 2015"},\
                        {"2_作者":"liveforhappy(a)","3_標題":"[新聞]有沒有","4_日期":"Thu May 13 21:56:01 2015"},\
                        {"2_作者":"liveforhappy(a)","3_標題":"有沒有","4_日期":"Thu May 13 21:56:01 2015"},\
                        {"2_作者":"liveforhappy(a)","3_標題":"[公告]有沒有","4_日期":"Thu May 13 21:56:01 2015"}]')

class TitleParser:
    def __init__(self):
        self.users_dict = {} # key = user id; value = [總發文數, [新聞]數, [問卦]數, 轉錄文章數, 退文數]
        self.violations = {} # key = article id; value = [article_title, article_link, [violated_rules]]
        self.moderator_list = ['meowmeowgo', 'seabox', 'APPLEin5566', 'XXXXGAY']
        self.prev_date = '' # Post date of previous article

    def add_violation(self, article, violated_rule):
        if article.id in violations:
            violations[article.id][2].append(violated_rule)
        else:
            violations[article.id] = [article.title, article.link, [violated_rule]]

    def check_date(self, article):
        # Check date
        # If the date has changed, clear the user data.
        if not article.date == prev_date:
            users_dict.clear()
            prev_date = article.date

    def get_author_data(self,article):
        # Check the author
        author = article.author
        if author.find('(') > 0:
            author = author[0 : author.find('(')]
        if author in users_dict:
            users_dict[author][0] += 1 # total_count increases by 1
        else:
            # Initialize user data
            users_dict[author] = [1, 0, 0, 0, 0]

    def check_tag(self, article):
        tag = article.tag
        if tag == u'新聞':
            users_dict[author][1] += 1
        elif tag == u'問卦':
            users_dict[author][2] += 1
        elif tag == u'爆卦':
            pass
        elif tag == u'公告':
            if not article.author in moderator_list:
                add_violation(article, u'1-9-2 5. 任意使用公告、回應公告。')
        elif tag == u'轉錄':
             users_dict[author][3] += 1
        else:
           add_violation(article, u'1-1-4 文章請使用本看板所提供之分類，自訂分類或無分類之文章一律刪除。')

    def check_post_num(self, article):
        author = article.author
        # check news number
        if users_dict[author][1] == 2:
            if users_dict[author][4] < 1:
                add_violation(article, u'1-1-1 新聞額度超貼 1 篇。以退文處理。')
                users_dict[author][4] += 1
            else:
                add_violation(article, u'1-1-1 新聞額度超貼', users_dict[author][1]-1 , u'篇。')
        elif users_dict[author][1] > 2:
            add_violation(article, u'1-1-1 新聞額度超貼', users_dict[author][1]-1 , u'篇。')
        # Check ask posts
        if users_dict[author][2] == 3:
            if users_dict[author][4] < 1:
                add_violation(article, u'1-1-1 問卦額度超貼 1 篇。以退文處理。')
                users_dict[author][4] += 1
            else:
                add_violation(article, u'1-1-1 問卦額度超貼', users_dict[author][2]-2 , u'篇。')
            elif users_dict[author][2] > 3:
                add_violation(article, u'1-1-1 問卦額度超貼', users_dict[author][2]-2 , u'篇。')
        # Check transfer posts
        if users_dict[author][3]>1:
            add_violation(article, u'1-1-5 轉錄文章限制一人一天一篇，超貼轉錄', users_dict[author][3]-1 ,u'篇, 水桶', (users_dict[author][3]-1)*2 , u'週。')
        # Check total posts
        if users_dict[author][0] > 5:
            add_violation(article, u'1-1-1 每日發文額度超貼', users_dict[author][0]-5 , u'篇。')
