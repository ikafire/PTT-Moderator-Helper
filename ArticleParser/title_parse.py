# -*- coding: utf-8 -*-
# users_dict = {} # key = user id; value = [總發文數, [新聞]數, [問卦]數, 轉錄文章數, 退文數]
# self.moderator_list = ["meowmeowgo", "seabox", "APPLEin5566", "XXXXGAY"]
# self.prev_date = "" # Post date of previous article
import article

def check_date(article, prev_date, users_dict):
    # Check date
    # If the date has changed, clear the user data.
    if not article.date == prev_date:
        users_dict.clear()
        prev_date = article.date

def check_author(article, users_dict):
    # Check the author
    author = article.author
    if author.find("(") > 0:
        author = author[0 : author.find(")")]
    if author in users_dict:
        users_dict[author][0] += 1 # total_count increases by 1
    else:
        # Initialize user data
        users_dict[author] = [1, 0, 0, 0, 0]

def check_tag(article, users_dict):
    moderator_list = ["meowmeowgo", "seabox", "APPLEin5566", "XXXXGAY"]
    tag = article.get_tag()
    author = article.author
    if tag == "新聞":
        users_dict[author][1] += 1
        return 0
    elif tag == "問卦":
        users_dict[author][2] += 1
        return 0
    elif tag == "爆卦":
        return 0
    elif tag == "公告":
        if not article.author in moderator_list:
            return 1
        else:
            return 0
    elif tag == u"轉錄":
         users_dict[author][3] += 1
         return 0
    else:
       return -1
