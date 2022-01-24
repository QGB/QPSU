#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

# rsignin=None
def sign_in(email,pw,dill_file=py.No('auto use email'),set_app_id=False):
	# global rsignin
	if '@' not in email and not dill_file:
		raise py.ArgumentError('email',email)
	if not dill_file:
		dill_file=T.filename(email)
	dill_file=F.auto_path(dill_file,ext='.dill')
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

	#<Response [400]> {"code":107,"error":"Malformed json object. A json dictionary is expected."}
	# data = r'''{'email':%r,'password':%r}'''%(email,pw) # 400
	
	data='{"email":"%s","password":"%s"}'%(email,pw)

	print(U.v.requests.post('https://us-w1-console-api.leancloud.app/1.1/signin', headers=headers, data=data))
	rsignin = requests.post('https://us-w1-console-api.leancloud.app/1.1/signin', headers=headers, data=data)
	print(rsignin,rsignin.text[:99])
	if 'XSRF-TOKEN' not in rsignin.cookies or not rsignin.cookies['XSRF-TOKEN']:
		return py.No(rsignin,rsignin.text,)
	if set_app_id:
		rsignin.app_id=get_app_id(rsignin)
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
	def login(s,**ka):
		s.rsignin,s.dill_file=sign_in(**ka)
		return s.rsignin,s.dill_file
	
def get_app_id(rsignin):
	if not rsignin:return rsignin
	if py.getattr(rsignin,'app_id',''):
		return rsignin.app_id
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
	try:
		return ra.json()[0]['app_id']
	except Exception as e:
		return py.No(ra,rsignin,msg=ra.text,)
	 
get_apps=get_app_id	

def get_all_traffic(*rs):
	''' resp.app_id=lc.get_app_id(resp) '''
	import datetime
	now=datetime.datetime.now()+datetime.timedelta(seconds=120)
	params = (
		('start', (now-datetime.timedelta(days=1)).isoformat()+'+08'),
		('end'  , now.isoformat()+'+08'),
		('groupName', 'web'),
	)
	m=py.len(rs)
	# r=[[],] * m  # [[('sum', 0],#to...#), ..m..  ### [[,],] SyntaxError###
	r=[py.list() for n in py.range(m) ]  #  [[],] * m 初始化会造成 r[0],r[1]...都是同一个 list
	for n,rsignin in py.enumerate(rs):
		email=rsignin.json()['email']
		app_id=get_app_id(rsignin)
		headers_t = {'x-xsrf-token': rsignin.cookies['XSRF-TOKEN'],
			'x-lc-id': get_app_id(rsignin),
			}
		rt = requests.get('https://us-w1-console-api.leancloud.app/1.1/engine/stats/outbound-traffic', headers=headers_t, params=params,cookies=rsignin.cookies)
		for k,v in rt.json()[0]['dps'].items():
			s=U.stime(int(k))
			s=s.replace('.00__.000','')
			r[n].append( [s,F.IntSize(v)] )
		size_len=F.IntSize(py.sum(U.get_col(r[n],1)),size=13-1),py.len(r[n])
		r[n].insert(0,size_len)
		r[n].insert(0,'%-17s:%-17s'%(email,app_id ))
	return r
def flat_traffic(r):
	m=py.len(r)
	rm=[]
	
	for i,_row in py.enumerate(r[0]):
		skip=False
		row=[  r[0][i][0]  ]
		for n in py.range(m):
			if i<2:
				row[0]=U.len(*r)
				if i==0:
					n=r[n][i]
				if i==1:
					n=py.repr(  r[n][i][0] )
			else:
				if r[n][i][0] != row[0]:
					print(n,i)
					NOT_Equal
				n=py.repr( r[n][i][1] )
				# n=U.StrRepr( T.justify(py.repr(n),size=19)  )
			row.append(n )
		row=[U.StrRepr( T.justify(j,size=18,cut=1) )	for j in row]
		rm.append(row)
	return rm		
	# for n,rn in py.enumerate(r):
		# for 
	
def get_net_traffic(rsignin,app_id=''):
	if not app_id:
		app_id=get_app_id(rsignin)
	import datetime
	now=datetime.datetime.now()+datetime.timedelta(seconds=120)
	params = (
		('start', (now-datetime.timedelta(days=1)).isoformat()+'+08'),
		('end'  , now.isoformat()+'+08'),
		('groupName', 'web'),
	)
	
	headers_t = {
		 # 'authority': 'us-w1-console-api.leancloud.app',
		 # 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
		 # 'accept': 'application/json',
		 'x-xsrf-token': rsignin.cookies['XSRF-TOKEN'], #必须{"code":401,"error":"unauthorized"}
		 # 'accept-language': 'zh',
		 'x-lc-id': app_id,
		 # 'sec-ch-ua-mobile': '?0',
		 # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62',
		 # 'origin': 'https://console.leancloud.app',
		 # 'sec-fetch-site': 'same-site',
		 # 'sec-fetch-mode': 'cors',
		 # 'sec-fetch-dest': 'empty',
		 # 'referer': 'https://console.leancloud.app/',
		 # 'if-none-match': 'W/"2ab3-EqExlKR8YKEmkR34IjJep2jOREc"',
	 }
	print(U.v.requests.get('https://us-w1-console-api.leancloud.app/1.1/engine/stats/outbound-traffic', headers=headers_t, params=params,cookies=rsignin.cookies))
	rt = requests.get('https://us-w1-console-api.leancloud.app/1.1/engine/stats/outbound-traffic', headers=headers_t, params=params,cookies=rsignin.cookies)
	print(rt,rt.text[:122])
	sl=[]
	for k,v in rt.json()[0]['dps'].items():
		s=U.stime(int(k))
		s=s.replace('.00__.000','')
		sl.append( [s,F.IntSize(v)] )
 
	return sl
	
def load(s):
	if py.istr(s):
		ls=[i.strip() for i in s.split(',')]
	if py.islist(s):
		ls=s
	print(ls)
	r=[]
	dlogin=U.get_or_set('lc.login',{})
	for i in ls:
		if not i:continue
		f=r'C:/test/{}@qgbcs.uu.me.dill'.format(i)
		q=F.dill_load(f)
		if not q:
			print('#Err',f,repr(q))
			raise q
		dlogin[i]=q	
		r.append(q)
	return r	
	
async def set_cookies(rsignin):
	from qgb.tests import taobao_trade,lc;tb=taobao_trade  	
	cks=await tb.get_all_cookies()  
	for k,v in rsignin.cookies.items():
		d={'name': k,
		  'value': v,
		  'domain': '.leancloud.app',
		  'path': '/',
		  'expires': U.itime()+3600*24*22,
		  'size': 24,
		  'httpOnly': False,
		  'secure': False,
		  'session': False,
		  'priority': 'Medium'}
		if d not in cks: 
			cks.append(d) 
			
	await tb.set_cookies(cks) 		
	U.search_iterable(cks,'lean')	