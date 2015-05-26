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

users_dict = {} # key = user id; value = [總發文數, [新聞]數, [問卦]數, 轉錄文章數, 退文數]
moderator_list = ["meowmeowgo", "seabox", "APPLEin5566", "XXXXGAY"]
prev_date = "" # Post date of previous article

for article in articles:
  # Check date
  post_date = article[u"4_日期"][0:10]
  # If the date has changed, clear the user data.
  if not post_date == prev_date:
    users_dict.clear()
    prev_date = post_date

  # Check the author
  author = article[u"2_作者"]
  if author.find('(') > 0:
    author = author[0 : author.find('(')]
  if author in users_dict:
    total_count = users_dict[author][0]+1 # total_count increases by 1
    news_count = users_dict[author][1]
    ask_count = users_dict[author][2]
    transfer_count = users_dict[author][3]
    return_count = users_dict[author][4]
  else:
    # Initialize user data
    users_dict[author] = [1, 0, 0, 0, 0]
    total_count = 1 # total_count increases by 1
    news_count = 0
    ask_count = 0
    transfer_count = 0
    return_count = 0

  # Check tag
  title = article[u"3_標題"]
  tag_start = title.find('[')
  tag_end = title.find(']', tag_start)
  if tag_start >= 0 and tag_end >= 0:
    tag = title[tag_start+1:tag_end]
    print author, " ", tag, " ", title
    if tag == u"新聞":
      news_count = news_count + 1;
      if news_count == 2:
        if return_count < 1:
          print u"1-1-1 新聞額度超貼 1 篇。以退文處理。"
          return_count = return_count + 1
        else:
          print u"1-1-1 新聞額度超貼", news_count-1 , u"篇。"
      elif news_count > 2:
        print u"1-1-1 新聞額度超貼", news_count-1 , u"篇。"
    elif tag == u"問卦":
      ask_count = ask_count + 1;
      if ask_count == 3:
        if return_count < 1:
          print u"1-1-1 問卦額度超貼 1 篇。以退文處理。"
          return_count = return_count + 1
        else:
          print u"1-1-1 問卦額度超貼", ask_count-2 , u"篇。"
      elif ask_count > 3:
        print u"1-1-1 問卦額度超貼", ask_count-2 , u"篇。"
    elif tag == u"爆卦":
      pass
    elif tag == u"公告":
      if not author in moderator_list:
        print u"1-9-2 5. 任意使用公告、回應公告。"
    elif tag == u"轉錄":
      transfer_count = transfer_count + 1
      if transfer_count>1:
        print u"1-1-5 轉錄文章限制一人一天一篇，超貼轉錄", transfer_count-1 ,u"篇水桶", (transfer_count-1)*2 , u"週。"
    else:
      print u"1-1-4 文章請使用本看板所提供之分類，自訂分類或無分類之文章一律刪除。"
  else:
    print author, " unknown ", title
    print u"1-1-4 文章請使用本看板所提供之分類，自訂分類或無分類之文章一律刪除。"

  # Check total posts
  if total_count > 5:
    print u"1-1-1 每日發文額度超貼", total_count-5 , u"篇。"

  # Update user data
  users_dict[author][0] = total_count
  users_dict[author][1] = news_count
  users_dict[author][2] = ask_count
  users_dict[author][3] = transfer_count
  users_dict[author][4] = return_count
