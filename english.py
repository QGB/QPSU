#coding=utf-8
import sys,pathlib				 # .py/qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)
from qgb import py
U,T,N,F=py.importUTNF()

def get_lemma(a):
	''' 单词 原型 
词形还原 (Lemmatisation)	

An auxiliary verb 助动词 (abbreviated aux) 
	'''
	import lemminflect
	r=[]
	for t in lemminflect.core.Inflections.Inflections.DICT_UPOS_TYPES:
		w=lemminflect.getLemma(a, upos=t)
		# assert py.len(w)==1
		# if py.len(w)!=1:
			# print(t,w)
		if not w:continue
		w=w[0]
		if w==a:continue
		r.append([w,t])
	return r
getLemma=get_lemma	


def get_lemma_online(a):
	import requests

	cookies = {
		'PHPSESSID': '2aeaaqpqc308tc89r7gpjel6k0',
		'_pk_id.3.76c1': '90d1198aa8bc0666.1669974379.',
		'_pk_ses.3.76c1': '1',
		'googtrans': '/auto/zh-CN',
		'googtrans': '/auto/zh-CN',
	}

	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ru;q=0.5,ja;q=0.4,zh-TW;q=0.3,it;q=0.2,de;q=0.1',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryZXuC4Jc1YZng6box',
		# 'Cookie': 'PHPSESSID=2aeaaqpqc308tc89r7gpjel6k0; _pk_id.3.76c1=90d1198aa8bc0666.1669974379.; _pk_ses.3.76c1=1; googtrans=/auto/zh-CN; googtrans=/auto/zh-CN',
		'Origin': 'https://cst.dk',
		'Referer': 'https://cst.dk/tools/index.php',
		'Sec-Fetch-Dest': 'document',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-Site': 'same-origin',
		'Sec-Fetch-User': '?1',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24',
		'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
	}

	data = '------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="MAX_FILE_SIZE"\r\n\r\n8000000\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="inputform"\r\n\r\nj\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="language"\r\n\r\nen\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="password"\r\n\r\n\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="inputText"\r\n\r\nas\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="inputFile"; filename=""\r\nContent-Type: application/octet-stream\r\n\r\n\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="token"\r\n\r\nj\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="pos"\r\n\r\nj\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="lemma"\r\n\r\nj\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="anonym"\r\n\r\nn\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="abbr"\r\n\r\nj\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="mwu"\r\n\r\nj\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="what"\r\n\r\nb\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="sorting"\r\n\r\nnosort\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="ambi"\r\n\r\nn\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box\r\nContent-Disposition: form-data; name="dict"\r\n\r\nj\r\n------WebKitFormBoundaryZXuC4Jc1YZng6box--\r\n'

	print(U.stime(),)
	response = requests.post('https://cst.dk/tools/index.php', cookies=cookies, headers=headers, data=data)
	print(U.stime(),response)
	bs=T.beautifulSoup(response)
	t=bs.select('body > div > table.fullpagewidth > tbody > tr > td > p[dir=auto]')[0].text
	assert t[-1]=='\n'
	
	return t[:-1]