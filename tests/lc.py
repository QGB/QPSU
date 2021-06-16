#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

# rsignin=None
def sign_in(email,pw,dill_file=py.No('auto use email')):
	# global rsignin
	if '@' not in email:
		raise py.ArgumentError('email',email)
	if not dill_file:
		dill_file=T.filename(email)
	if F.exist(dill_file):
		r=F.dill_load(dill_file)
		if check_login(r):
			return r,dill_file
		else:
			print('can not load',F.ll(dill_file),'skip')
			
	headers = {
		'authority': 'us-w1-console-api.leancloud.app',
		'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
		'accept': 'application/json',
		'accept-language': 'zh',
		'sec-ch-ua-mobile': '?0',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safa',
		'content-type': 'application/json; charset=utf-8',
		'origin': 'https://console.leancloud.app',
		'sec-fetch-site': 'same-site',
		'sec-fetch-mode': 'cors',
		'sec-fetch-dest': 'empty',
		'referer': 'https://console.leancloud.app/',
	#    'cookie': '_ga=GA1.2.1912224529.1620372988; _gid=GA1.2.855550602.1623739540',
	}

	data = '{"email":%r,"password":%r}'%(email,pw)

	rsignin = requests.post('https://us-w1-console-api.leancloud.app/1.1/signin', headers=headers, data=data)
	print(rsignin,rsignin.text[:99])
	if 'XSRF-TOKEN' not in rsignin.cookies or not rsignin.cookies['XSRF-TOKEN']:
		return py.No(rsignin,rsignin.text,)
	f=F.dill_dump(obj=rsignin,file=dill_file)
	return rsignin,f
login=signin=sign_in

def check_login(resp):
	if not resp or not py.getattr(resp,'cookies',0):
		return py.No(resp)
	if 'XSRF-TOKEN' not in resp.cookies:
		return py.No(resp.cookies)		
	return get_apps(resp)

class LC:
	def login(s,**ka)
		s.rsignin,s.dill_file=sign_in(**ka)
		return s.rsignin,s.dill_file
	
def get_apps(rsignin):
	if not rsignin:return rsignin
    # 'cookie': rsignin.cookies,
	headers_apps = {
    'authority': 'us-w1-console-api.leancloud.app',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
    'accept': 'application/json',
    'x-xsrf-token': rsignin.cookies['XSRF-TOKEN'],
    'accept-language': 'zh',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62',
    'origin': 'https://console.leancloud.app',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://console.leancloud.app/',
	}

	ra = requests.get('https://us-w1-console-api.leancloud.app/1.1/clients/self/apps', headers=headers_apps,cookies=rsignin.cookies)
	app_id=ra.json()[0]['app_id']
	

def get_net_traffic():

	headers_t = {
		 # 'authority': 'us-w1-console-api.leancloud.app',
		 # 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
		 # 'accept': 'application/json',
		 'x-xsrf-token': rsignin.cookies['XSRF-TOKEN'], #必须{"code":401,"error":"unauthorized"}
		 # 'accept-language': 'zh',
		 'x-lc-id': ra.json()[0]['app_id'],
		 # 'sec-ch-ua-mobile': '?0',
		 # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62',
		 # 'origin': 'https://console.leancloud.app',
		 # 'sec-fetch-site': 'same-site',
		 # 'sec-fetch-mode': 'cors',
		 # 'sec-fetch-dest': 'empty',
		 # 'referer': 'https://console.leancloud.app/',
		 # 'if-none-match': 'W/"2ab3-EqExlKR8YKEmkR34IjJep2jOREc"',
	 }

	rt = requests.get('https://us-w1-console-api.leancloud.app/1.1/engine/stats/outbound-traffic', headers=headers_t, params=params,cookies=rsignin.cookies)
	print(rt,rt.text[:122])
	sl=[[U.stime(int(k)),F.IntSize(v)] for k,v in rt.json()[0]['dps'].items()]