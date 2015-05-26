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

class CommonVar:
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

def check_date(comm_var, article):
    # Check date
    # If the date has changed, clear the user data.
    if not article.date[0:9] == comm_var.prev_date[0:9]:
        comm_var.users_dict.clear()
        comm_var.prev_date = article.date

def get_author_data(comm_var,article):
    # Check the author
    author = article.author
    if author in comm_var.users_dict:
        comm_var.users_dict[author][0] += 1 # total_count increases by 1
    else:
        # Initialize user data
        comm_var.users_dict[author] = [1, 0, 0, 0, 0]

def check_tag(comm_var, article):
    tag = article.get_tag()
    author = article.author
    if tag == u'新聞':
        comm_var.users_dict[author][1] += 1
        check_news_num(comm_var, article)
    elif tag == u'問卦':
        comm_var.users_dict[author][2] += 1
        check_ask_num(comm_var, article)
    elif tag == u'爆卦':
        pass
    elif tag == u'公告':
        if not article.author in comm_var.moderator_list:
            comm_var.add_violation(article, u'1-9-2 5. 任意使用公告、回應公告。')
    elif tag == u'轉錄':
        comm_var.users_dict[author][3] += 1
        check_transfer_num(comm_var, article)
    else:
        comm_var.add_violation(article, u'1-1-4 文章請使用本看板所提供之分類，自訂分類或無分類之文章一律刪除。')

def check_news_num(comm_var, article):
    author = article.author
    # check news number
    if comm_var.users_dict[author][1] == 2:
        if comm_var.users_dict[author][4] < 1:
            comm_var.add_violation(article, u'1-1-1 新聞額度超貼 1 篇。以退文處理。')
            comm_var.users_dict[author][4] += 1
        else:
            comm_var.add_violation(article, u'1-1-1 新聞額度超貼', comm_var.users_dict[author][1]-1 , u'篇。')
    elif comm_var.users_dict[author][1] > 2:
        comm_var.add_violation(article, u'1-1-1 新聞額度超貼', comm_var.users_dict[author][1]-1 , u'篇。')
def check_ask_num(comm_var, article):
    author = article.author
    # Check ask posts
    if comm_var.users_dict[author][2] == 3:
        if comm_var.users_dict[author][4] < 1:
            comm_var.add_violation(article, u'1-1-1 問卦額度超貼 1 篇。以退文處理。')
            comm_var.users_dict[author][4] += 1
        else:
            comm_var.add_violation(article, u'1-1-1 問卦額度超貼', comm_var.users_dict[author][2]-2 , u'篇。')
    elif comm_var.users_dict[author][2] > 3:
        comm_var.add_violation(article, u'1-1-1 問卦額度超貼', comm_var.users_dict[author][2]-2 , u'篇。')
def check_transfer_num(comm_var, article):
    author = article.author
    # Check transfer posts
    if comm_var.users_dict[author][3]>1:
        comm_var.add_violation(article, u'1-1-5 轉錄文章限制一人一天一篇，超貼轉錄', comm_var.users_dict[author][3]-1 ,u'篇, 水桶', (comm_var.users_dict[author][3]-1)*2 , u'週。')
def check_total_num(comm_var, article):
    author = article.author
    # Check total posts
    if comm_var.users_dict[author][0] > 5:
        comm_var.add_violation(article, u'1-1-1 每日發文額度超貼', comm_var.users_dict[author][0]-5 , u'篇。')

def parse(comm_var, article):
    check_date(comm_var,article)
    get_author_data(comm_var,article);
    check_tag(comm_var,article)
    check_total_num(comm_var,article)

def main():
    articles = article.create_articles_from_file('data.json')
    comm_var = CommonVar();
    for a in articles:
        parse(comm_var, a)
    for v in comm_var.violations.values():
        print v[0]
        print v[1]
        for rule in v[2]:
            print rule



if __name__ == '__main__':
    main()
