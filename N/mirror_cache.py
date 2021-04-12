#coding=utf-8
import sys
if __name__.endswith('qgb.N.mirror_cache'):from .. import py
else:
	from pathlib import Path
	gsqp=Path(__file__).absolute().parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	# print(sys.path,gsqp)
	# print(Path(__file__).parent.parent.parent)
	from qgb import py
U,T,N,F=py.importUTNF()
from requests import request as send_request
from flask import Flask,request,make_response

use_cache=True	
ips=F.dill_load('ips') or []


app=Flask(__name__)
N.rpcServer(locals=globals(),globals=globals(),app=app,key='-')

def target_to_response(target):
	response=make_response()
	response.status_code=target.status_code
	response.headers._list=list(target.headers.items())
	response.headers['Content-Security-Policy']=''
	response.headers['Content-Encoding']='utf-8'
	response.set_data(target.content)
	return response

@app.errorhandler(404)
def mirror_cache(*a,**ka):
	''' 
# 'Content-Length': '',  pythonAnywhere 这一句 请求头， 会导致绝大数网站返回 400  错误
'''	
	# us=request.path.split('/')
	ip=request.headers.get('X-Real-Ip',request.remote_addr) 
	if ip not in ips:
		return ip+'\nNot allowed! ips'
		
	path=request.path[1:]
	method=request.method
	# fn=cache_path+method[:1]+T.url2fn(path+request.environ.get('HTTP_COOKIE','')[:99] )
	url=T.sub(request.url,request.url_root ) 
	fn=cache_path+method[:1]+T.url2fn(url)
	
	if use_cache:
		target=F.dill_load(fn)
		if target:
			# print()
			# U.p('##',fn,file=sys.stderr,flush=True)
			return target_to_response(target)
	print(U.stime(),path)	
	send_headers={}
	for k,v in request.headers.items():
		v=v.replace(request.host,target_host)
		if k=='Content-Length':
			if v:print('### Content-Length',U.stime(),request.url,request.headers)
			continue
		send_headers[k]=v
	
	target=send_request(method=method, 
		url=target_base_url+path, 
		params=request.args, headers=send_headers, )
	response= target_to_response(target)
	F.dill_dump(protocol=4,obj=target,file=fn)
	return response
	
def run(target,port=1122,currentThread=True):
	global app,thread
	U.log(config(target))
	
	flaskArgs=py.dict(port=port,host='0.0.0.0',debug=True,threaded=True)
	if currentThread:
		thread=None
		return app.run(**flaskArgs)
	else:
		thread=U.Thread(target=app.run,name='qgb thread '+app.name,kwargs=flaskArgs)
		thread.start()
		return (thread,app)

def config(target):
	global cache_path,target_base_url,target_host
	from six.moves.urllib.parse import urlsplit
	up=urlsplit(url=target)
	target_host=up.netloc
	target_base_url='{}://{}/'.format(up.scheme,target_host)
	cache_path=F.mkdir(target_host) # in gst	
	return cache_path,target_base_url,target_host

if __name__=='__main__':
	a=U.parseArgs(str=r'https://www.dulwich.io',int=1122)
	run(target=a.str,port=a.int)

