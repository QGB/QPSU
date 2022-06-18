import sys;'qgb.U' in sys.modules or sys.path.append('C:/QGB/babun/cygwin/bin/');from qgb import *

ga='[XIUREN-p+--°] 2019.04.28 NO.1423 +_++-úSandy'

def get_c(url):
	t=N.HTTP.get(url,proxies='127.0.0.1:21080'[:0])   
	sd='{'+T.sub(t,'var _c = {','};\nvar CodeMirror =')+'}'
	
	
	return t,sd,T.json_loads(sd)
def iter(dc):
	global ga
	
	if 'dirs' in dc:
		lk=py.list(dc['dirs'])
		if py.len(lk)!=2 and '' not in lk:raise py.EnvironmentError(lk)
		lk.remove('')
		ga=kd=lk[0]
		dcfs=dc['dirs'][kd]
	elif 'files' in dc:
		kd=dc['basename']
		dcfs=dc
	U.set_gst('E:/test/www.xiezhen.xyz/'+kd,cd=1)
	
	
	
	for f,v in dcfs['files'].items():
		# f='22164I2-B-1Z2.jpg'
		u= v['url_path']
		# fn=T.sub_last(u,'/')
		up=T.sub_last(u,'','/')[5:]
		# if up!=ga:
			# print('#err ',f)
		url=T.url_encode('https://www.xiezhen.xyz/index.php?file={}/{}'.format(up,f) ,safe=':/?=')	
		if F.size(f):continue
		rb=N.HTTP.get_byte(url,file=f)
		print(U.stime(),rb)
	return kd,up,f
	
'''

import requests

headers = {
    'pragma': 'no-cache',
    'origin': 'https://www.xiezhen.xyz',
    # 'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 YaBrowser/19.3.1.779 Yowser/2.5 Safari/537.36',
    'accept': 'application/json',
    'cache-control': 'no-cache',
    'authority': 'www.xiezhen.xyz',
    'x-requested-with': 'XMLHttpRequest',
    'referer': 'https://www.xiezhen.xyz/?%5BXIUREN-p+--%C2%B0%5D%202019.09.20%20NO.1688%20Cris_++%C2%B5%C2%BD8%CB%9C',
}

data = {
    'action': 'files',
    'dir': '[XIUREN-p+--°] 2019.09.19 NO.1687 +_++-úSandy',
    'post_hash': 'c7b8a378f97cd17af899527b6287c463',
}

response = requests.post('https://www.xiezhen.xyz/index.php', headers=headers, data=data)

	
'''
	