##############################################
#                                            #
# PTT Crawler                       Lion Kuo #
# ------------------------------------------ #
# Before you use ...                         #
#   1). Python3                              #
#   2). BeautifulSoup 4                      #
#   3). requests                             #
#                                            #
# Usage ...                                  #
# ------------------------------------------ #
#                                            #
#   python3 PTTCrawler.py                    #
#                                            #
#                                            #
#   Check the LastPage file, if not exists   #
#   Do the first fetch from the newest page  #
#   to the old page in 10.                   #
#   If it exists, fetch the range from       #
#   LastPage to newestPage.                  #
#                                            #
##############################################

from bs4 import BeautifulSoup
from time import sleep,time
import os.path
import re
import json
import requests
import sys
import datetime

URL = 'http://www.ptt.cc/bbs/Gossiping/index'
COOKIE = {'over18': '1'}


def getPageNum():
    fetchURL = URL + '.html'
    res = requests.get(url=fetchURL, cookies=COOKIE)
    indexPage = BeautifulSoup(res.text)
    pageNum = int(re.sub(r'[^0-9]+', '', indexPage.find_all("a", class_="btn wide")[1].get('href')))

    return pageNum

def crawler(start, end):
    
    page = start
    n = end-start+1
    article_id = 0;
    k = 0;
    for i in range(n):
        print('Page(Index): ' + str(page))
        fetchURL = URL + str(page) + '.html'

        res = requests.get(url=fetchURL, cookies=COOKIE)
        soup = BeautifulSoup(res.text)
        for tag in soup.find_all('div','r-ent'):
            if k==1: break

            try:
                link = str(tag.find_all('a'))
                link = link.split("\"")
                link = 'http://www.ptt.cc' + link[1]
                parseArticle(link, article_id)
                article_id += 1
                sleep(0.5)
                #k = 1
            except:
                print("Fetch Error at Page " + str(page) + ' with Article ' + str(article_id))
                pass
        sleep(0.3)
        page +=1


def parseArticle(link, id):
    res = requests.get(url=str(link), cookies=COOKIE)
    soup = BeautifulSoup(res.text)
    

    # 抓取時間
    st = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 作者、標題、日期
    author = soup.find(id='main-container').contents[1].contents[0].contents[1].string.replace(' ','')
    title = soup.find(id='main-container').contents[1].contents[2].contents[1].string.replace(' ','')
    date = soup.find(id='main-container').contents[1].contents[3].contents[1].string

    # 換日期 
    # date = 'Thu May 14 21:56:01 2015'
    #          0   1   2     3      4
    a = [t(s) for t,s in zip((str,str,int,str,int),date.split())]
    monthDic = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9,
                'Oct':10, 'Nov':11, 'Dec':12}
    date = str(a[4]) + '-' + str(monthDic[a[1]]) + '-' + str(a[2]) + ' ' + str(a[3])



    # 判斷發文/回文
    if str(title).startswith('Re:'):
        reply = 'R'
    else:
        reply = 'P'

    # 抓 ip 位置
    try:
        ip = soup.find(text=re.compile('※ 發信站:'))
        ip = re.search("[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*",str(ip)).group()
    except:
        ip = "Not Found"


    # 文章內容
    a = str(soup.find(id='main-container').contents[1])
    a = a.split('</div>')
    a = a[4].split("<span class=\"f2\">※ 發信站: 批踢踢實業坊(ptt.cc),")
    content = BeautifulSoup(a[0])
    content = content.text

    # 簽名檔
    t = content.split("--")
    if len(t) >= 3:
        signature = str(t[1])
    else:
        signature = 'No'


    # 文章網址
    try:
        articleSite = soup.find_all(class_='fb-like')
        articleSite = re.search('http://www.ptt.cc/bbs/Gossiping/.+.html', str(articleSite)).group()
        articleID = re.search('M.+.html', str(articleSite)).group()
    except:
        articleSite = "Not Found"

    '''
    num, g, b, n, message = 0,0,0,0,{}
    for tag in soup.find_all("div","push"):
        num += 1
        push_tag = tag.find("span","push-tag").string.replace(' ', '')
        push_userid = tag.find("span","push-userid").string.replace(' ', '')
        push_content = tag.find("span","push-content").string.replace(' ', '').replace('\n', '').replace('\t', '')
        push_ipdatetime = tag.find("span","push-ipdatetime").string.replace('\n', '')

        message[num]={"狀態":push_tag,"留言者":push_userid,"留言內容":push_content,"留言時間":push_ipdatetime}
        if push_tag == '推 ':
            g += 1
        elif push_tag == '噓 ':
            b += 1
        else:
            n += 1          
    messageNum = {"2_推":g,"3_噓":b,"4_箭頭":n,"1_全部":num}
    '''

    d = { "ID":id ,"作者":author ,"標題":title ,"日期":date ,"ip":ip ,"內文":content ,"文章網址":articleSite, "發文/回文":reply, "TimeStamp":st, "簽名檔":signature, "文章ID":articleID}
    json_data = json.dumps(d,ensure_ascii=False,indent=4,sort_keys=True)+','
    print("Fetch " + str(articleID) + " Finish ...")
    store(json_data) 
    
def store(data):
    with open('data.json', 'a',encoding='utf-8') as f:
        f.write(data)

def writePageNum(nowPageNum):
    with open('LastPage','w+') as f:
        f.write(str(nowPageNum))

def readPageNum():
    with open('LastPage','r') as f:
        k = int(f.read())
    return k

def executeCrawl():
    # 回傳現在有幾頁，越新數字越大 7560 -> 7561, 該數字+1為最新之頁數
    nowPageNum = getPageNum()
    
    if os.path.exists("./LastPage") is True :   
        last = readPageNum()
        if last != (nowPageNum+1):
            store('[') 
            crawler(last,nowPageNum+1)
            store(']') 
            with open('data.json', 'r', encoding="utf-8") as f:
                p = f.read()
            with open('data.json', 'w', encoding="utf-8") as f:
                f.write(p.replace(',]',']'))
            writePageNum(nowPageNum+1)
    else:
        store('[') 
        crawler(nowPageNum-1,nowPageNum+1)
        store(']') 
        with open('data.json', 'r', encoding="utf-8") as f:
            p = f.read()
        with open('data.json', 'w', encoding="utf-8") as f:
            f.write(p.replace(',]',']'))
        writePageNum(nowPageNum+1)



