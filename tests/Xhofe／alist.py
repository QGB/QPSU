import requests
import sys;'qgb.U' in sys.modules or sys.path.append('C:/QGB/babun/cygwin/bin/');from qgb import *

cp=['1-100','1001-1100','101-200','201-300','301-400','401-500','501-600','601-700','701-800','801-900','901-1000']
for cpi in cp:
	path='/asmr/中文音声/小苮儿/长篇/%s/'%cpi
	domain='https://one.asmr.gay/'
	U.set_gst('c:/test/'+T.sub(domain,'://','/'),cd=1,p=1)
	dsp=U.get_or_set(path,{})
	if not dsp:
		rp=requests.post(domain+'api/public/path',json={'path': path}, verify=False,proxies=proxies)
		f100=rp.json()['data']['files']
	for n,i in enumerate(f100):
		sp=i['name']
		if sp not in dsp:
			pi=requests.post(domain+'api/public/path',json={'path': path+sp}, verify=False,proxies=proxies)
			dsp[sp]=pi
			print(U.stime(),n,sp,pi)
		pi=dsp[sp]
		fts=[js['name'] for js in pi.json()['data']['files'] if js['name'].endswith('.txt')]
		if not fts:
			print('##Error txt',n,sp,pi,fts)
		for ft in fts:
			url=domain+'p'+path+sp+'/'+ft
			udir=T.file_legalized(path)+'/'
			F.mkdir(U.gst+udir)
			f=udir+sp+'_'+ft
			if F.size(f):continue
			b=N.HTTP.get_byte(url,file=f,proxies=proxies)
			print(U.stime(),n,pi,b)
		