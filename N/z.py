import sys;'qgb.U' in sys.modules or sys.path.append('C:/QGB/babun/cygwin/bin/')
from qgb import *
from qgb import py
N.rpcServer(port=2345,execLocals=globals())

c=item=html=0
next_url=[]
answers=[]
next_url=[]
def zhihu_question(id):
	global c,next_url,answers,html,next_url
	if py.istr(id):
		id=T.filterInt(id,range(8,11))[0]
	start_url = 'https://www.zhihu.com/api/v4/questions/'+str(id)+'/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=0&sort_by=default'
	
	import requests
	from bs4 import BeautifulSoup
	import json

	headers = {
		'accept-language': 'zh-CN,zh;q=0.9',
		'origin': 'https://www.zhihu.com',
		'referer': 'https://www.zhihu.com/question/290268306',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
	}
	
	next_url = [start_url]
	answers = []
	for url in next_url:
		try:
			html = requests.get(url, headers=headers,verify=False)
			html.encoding = html.apparent_encoding
			soup = BeautifulSoup(html.text, "lxml")
			content = str(soup.p).split("<p>")[1].split("</p>")[0]
			c = json.loads(content)
			answers+=pq(c)
			next_url.append(c["paging"]["next"])
			if c["paging"]["is_end"]:
				break
		except Exception as e:
			globals()['err']=e
			continue
	# for item in answers:
		# print(item)
	title=''
	try:title=c['data'][0]['question']['title']+f' | {len(answers)}'
	except:pass
	U.log(title)

	r=''
	for i,v in enumerate(answers):
		r+=f'\n[第{i+1}] {T.filterZh(v[0],11)} {v[1]}'
	return title+r
zhihu=zhihu_question
	
def extract_answer(s):
	import re
	REG = re.compile('<[^>]*>')
	temp_list = REG.sub("", s).replace("\n", "").replace(" ","")
	return temp_list

def pq(c):		
	return [ 
[extract_answer(item["content"]),
U.stime(item['created_time'])[:-4-3].replace('_',' ')
] for item in c["data"] if extract_answer(item["content"]) != ""]

def spq(c):
	answers=pq(c)
	title=''
	try:title=c['data'][0]['question']['title']
	except:pass
	U.log([title,len(answers)])
	
	r=''
	for i,v in enumerate(answers):
		r+=f'\n[第{i+1}] {v[0]} {v[1]}'
	return title+r
