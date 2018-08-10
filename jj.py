import requests
import re
import time
from bs4 import BeautifulSoup
# 晋江爬虫判断逻辑：
# 	1.入v前：url为普通，host为www 标题和正文用正则匹配，作者有话要说放在readsmall
# 	2.入v后：url多个vip，host为my 
# 		（1）未防盗：和入v前保持一致
# 		（2）防盗版：正文放在readsmall里面
# 	注：1.标题可以用正则也可以用bueautifulsoup抓取
# 			2.bueautifulsoup解析用html5lib，lxml（出现丢失）和html.parser(标签错误)
# 				解析速度：lxml>html.parser>html5lib 兼容性则反之


def get_html(url):
	context=requests.get(url)
	return context.text


def login(url):
	header={
	'Host': 'www.jjwxc.net',
	'Proxy-Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en-US;q=0.7,en;q=0.6',
	'Cookie': "timeOffset_o=675.60009765625; UM_distinctid=1651227a422417-0d77e3bfcdf165-2711938-144000-1651227a423e48; testcookie=yes; Hm_lvt_bc3b748c21fe5cf393d26c12b2c38d99=1533534066; token=MjEwMDg0NDR8ZjZmNTg0MDU0MzhhN2NjNzQ3YjkxZThhMjQ2ZjBkMDd8fGNnYyoqKkAxNjMuY29tfHwyNTkyMDAwfDF8fHzmrKLov47mgqjvvIzmmYvmsZ%2FnlKjmiLd8MXxtb2JpbGU%3D; JJEVER=%7B%22ispayuser%22%3A%2221008444-1%22%2C%22foreverreader%22%3A%2221008444%22%2C%22sms_total%22%3A%220%22%7D; nicknameAndsign=2%7E%29%2524; isnickname=2%7E%29%2524; clicktype=; CNZZDATA30075907=cnzz_eid%3D2042898215-1533531241-http%253A%252F%252Fwww.jjwxc.net%252F%26ntime%3D1533698641; Hm_lpvt_bc3b748c21fe5cf393d26c12b2c38d99=1533702791",
	}
	session=requests.session()
	cur_page=66
	file=open('女配悲痛欲绝.txt','a+')
	while(cur_page<=102):         
		if cur_page<=23:            #入v前
			_url='http://www.jjwxc.net/onebook.php?novelid=2875770&chapterid='+str(cur_page)
			header['Host']="www.jjwxc.net"
			s=session.get(_url,headers=header)
			s.encoding='gbk'
			pattern=re.compile('<h2>(.*?)</h2></div>.*?<div style="clear:both;"></div>(.*?)<div id="favoriteshow_3"',re.S)
			item=re.findall(pattern,s.text)
			file.write('<h2>第'+str(cur_page)+'章 '+item[0][0]+'</h2>\n')
			file.write(item[0][1]+'\n')

		else:                      #入v后
			_url='http://my.jjwxc.net/onebook_vip.php?novelid=2875770&chapterid='+str(cur_page)
			header['Host']="my.jjwxc.net"		
			s=session.get(_url,headers=header)
			s.encoding='gbk'
			pattern=re.compile('<h2>(.*?)</h2></div>.*?<div style="clear:both;"></div>(.*?)<div id="favoriteshow_3"',re.S)
			soup=BeautifulSoup(s.content,'html5lib')
			item=re.findall(pattern,s.text)
			file.write('<h2>第'+str(cur_page)+'章 '+item[0][0]+'</h2>\n')
			if (cur_page<=65 or cur_page>=99):		#没有防盗
				file.write(item[0][1]+'\n')
			else:
				file.write(str(soup.find_all(attrs={'class':'readsmall'})[0])+'\n')
		cur_page+=1
	file.close()
	
#s='2018-07-25 17:10:13'
#t=time.strptime(s,"%Y-%m-%d %H:%M:%S")
#If-Modified-Since=time.strftime("%a, %d %b %Y %H:%M:%S ", t)
url='http://www.jjwxc.net/onebook.php?novelid=2875770'
login(url)