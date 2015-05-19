##############################################
#                                            #
# PTT Crawler             		    Lion Kuo #
# ------------------------------------------ #
# Before you use ...                         #
#   1). Python2 or Python3                   #
#   2). BeautifulSoup 4                      #
#   3). requests                             #
#                                            #
# Usage ...                                  #
# ------------------------------------------ #
#                                            #
#                                            #
#                                            #
#                                            #
#                                            #
#                                            #
#                                            #

from bs4 import BeautifulSoup
from time import sleep,time
import re
import json
import requests
import sys
import datetime

URL = 'http://www.ptt.cc/bbs/Gossiping/index'
COOKIE = {'over18': '1'}

def crawler(start, end):
	
	page = start
	n = end-start+1
	article_id = 0;

	for i in range(n):
		print('Page(Index): ' + str(i))
		fetchURL = URL + str(page) + '.html'

		res = requests.get(url=fetchURL,cookies=COOKIE)
		soup = BeautifulSoup(res.text)
		for tag in soup.find_all('div','r-ent'):
			try:
				link = str(tag.find_all('a'))
				link = link.split("\"")
				link = 'http://www.ptt.cc' + link[1]
				parseArticle(link, article_id)
				article_id += 1
				sleep(0.5)
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
	content = a[0].replace(' ', '').replace('\n', '').replace('\t', '')
	content = BeautifulSoup(content)
	content = content.text

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
	d={ "1_ID":id ,"2_作者":author ,"3_標題":title ,"4_日期":date ,"5_ip":ip ,"6_內文":content ,"7_文章網址":articleSite, "8_發文/回文":reply, "9_TimeStamp":st}
	json_data = json.dumps(d,ensure_ascii=False,indent=4,sort_keys=True)+','
	print("Fetch " + str(articleID) + " Finish ...")
	store(json_data) 
	
def store(data):
    with open('data.json', 'a') as f:
        f.write(data)

if __name__ == '__main__':
	store('[') 
	crawler(int(sys.argv[1]),int(sys.argv[2]))
	store(']') 
	with open('data.json', 'r') as f:
		p = f.read()
	with open('data.json', 'w') as f:
		f.write(p.replace(',]',']'))


