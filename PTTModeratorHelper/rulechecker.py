# -*- coding: utf-8 -*-
import article
import count
import title_parse as title

def rule_1(article, users_dict):
    sentence = "版規一: \n"
    violated = False

    tag = title.check_tag(article, users_dict)
    if tag < 0:
        sentence += "文章請使用本看板所提供之分類，自訂分類或無分類之文章一律刪除。\n"
        violated = True

    author = article.author
    # check news number
    if users_dict[author][1] > 1:
        if users_dict[author][4] < 1:
            sentence += "新聞額度超貼 1 篇。以退文處理。\n"
            violated = True
            users_dict[author][4] += 1
        else:
            sentence += "新聞額度超貼 " + users_dict[author][1]-1 + " 篇, 給予水桶 " + users_dict[author][1]-1 + " 個月。\n"
            violated = True

    # Check ask posts
    if users_dict[author][2] > 2:
        if users_dict[author][4] < 1:
            sentence += "問卦額度超貼 1 篇。以退文處理。\n"
            violated = True
            users_dict[author][4] += 1
        else:
            sentence += "問卦額度超貼 " + users_dict[author][2]-2 + " 篇, 給予水桶 " + users_dict[author][2]-2 + " 個月。\n"
            violated = True

    # Check transfer posts
    if users_dict[author][3] > 1:
        sentence += "轉錄文章限制一人一天一篇，超貼轉錄 " + users_dict[author][3]-1 + " 篇, 給予水桶 " + (users_dict[author][3]-1)*2 + " 週。"
        violated = True
    # Check total posts
    if users_dict[author][0] > 5:
        if users_dict[author][4] < 1:
            sentence += "每日發文額度超貼 1 篇。以退文處理。\n"
            violated = True
            users_dict[author][4] += 1
        else:
            sentence += "每日發文額度超貼 " + users_dict[author][0]-5 + " 篇, 給予水桶 " + users_dict[author][0]-5 + " 個月。\n"
            violated = True
    return violated, sentence

def rule_6(article):
    sentence = "版規六: \n"
    violated = False

    if count.number_of_lines(article.signature) > 6:
        sentence += "文章簽名檔過長。刪除\n"
        violated = True

    artCharsCount = count.art_chars(article.body)
    tradCharsCount = count.traditional_chinese_chars(article.body)
    if artCharsCount > tradCharsCount:
        sentence += "內容含過多色碼、亂碼。刪除\n"
        violated = True

    simpCharsCount = count.simplified_chinese_chars(article.body)
    if simpCharsCount > tradCharsCount:
        sentence += "內容含過多非正體中文。退回並水桶三個月\n"
        violated = True

    return violated, sentence


def rule_9(article, users_dict):
    sentence = "版規九: \n"
    violated = False

    if len(article.body) == 0:
        sentence += "空白文，退回並水桶六個月\n"
        violated = True

    tradCharsCount = count.traditional_chinese_chars(article.body)
    if tradCharsCount < 20:
        sentence += "發表內容之繁體中文字未滿二十個字，退回並水桶六個月\n"
        violated = True
    elif count.number_of_lines(article.body) <= 1:
        sentence += "滿二十個字，但使用電腦觀看為一行文，退回並水桶六個月\n"
        violated = True

    if title.check_tag(article,users_dict) > 0:
        sentence += "任意使用公告\n"
        violated = True


    return violated, sentence

def checkRules():
    articles = article.create_articles_from_file('data.json')
    users_dict = {}
    prev_date = ""
    result = ""
    for a in articles:
        title.check_date(a, prev_date, users_dict)
        title.check_author(a, users_dict)
        violated1, sentence1 = rule_1(a, users_dict)
        violated6, sentence6 = rule_6(a)
        violated9, sentence9 = rule_9(a, users_dict)
        violated = violated1 or violated6 or violated9
        subResult = ""
        if violated:
            subResult += a.title + "\n"
        if violated1:
            subResult += sentence1 +"\n"
        if violated6:
            subResult += sentence6 + "\n"
        if violated9:
            subResult += sentence9 + "\n"
        if violated:
            subResult += "==========\n"
            try:
                print("Detect violation -->", subResult)
            except:
                pass
        result += subResult
    return result

if __name__ == '__main__':
    checkRules()
