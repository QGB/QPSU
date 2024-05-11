#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()


#第一个请求就卡住用不了
headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ru;q=0.5,ja;q=0.4,zh-TW;q=0.3,it;q=0.2,de;q=0.1',
 'Cache-Control': 'max-age=0',
 'Connection': 'keep-alive',
 'Content-Length': '197',
 'Content-Type': 'application/x-www-form-urlencoded',
 'Cookie': '_TESTCOOKIEHTTP=1',
 'Host': '192.168.1.1',
 'Origin': 'http://192.168.1.1',
 'Referer': 'http://192.168.1.1/',
 'Upgrade-Insecure-Requests': '1',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'}

headers={'Content-Type': 'application/x-www-form-urlencoded',}

def login(u='http://192.168.1.1'):
	print(U.stime(),u)
	rg = requests.get(u, headers=headers)
	print(U.stime(),rg)
	h=rg.text
	# h=N.HTTP.get(u)
	hs=h.splitlines()
	ms='Frm_Logintoken,Frm_Loginchecktoken'.split(',')
	dr={'Username':'CMCCAdmin',
	'UserRandomNum':98993771,
	'Password':'f598f8372e117766616f2f5942d415cae14633c9c190001f92864f4dabce0515',
	'action':'login',
	'Right':'',}
	# U.sha256(b'98993771')
	for s in hs:
		for m in ms:
			ma=f'getObj("{m}").value = "'
			mr=T.sub(s,ma,'"')
			if mr:dr[m]=mr
	if ms[0] not in dr:return py.No('dr',dr,rg)
	print(dr)

	response = requests.post(u, headers=headers, data=dr, cookies=rg.cookies)
	print(U.stime(),response)
	if "initMenu()" in response.text:
		print("登录成功!")
	else:print('登录失败:')
	
	return response
	# raise Exception('登录失败: {}'.format(response.text))
