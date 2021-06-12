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
dump=True
replace_domain=True
skip_response_headers={
	'Transfer-Encoding': 'chunked',
	'transfer-encoding': 'chunked',
}
gdreplace={}
gencoding='utf-8'
base_host=b'' # bytes flask_request.host
app=Flask(__name__)
N.rpcServer(locals=globals(),globals=globals(),app=app,**dict(T.split_to_2d_list(''.join(chr(z%311) for z in U.prime_factorization(1126670844869212339)),chr(58),)),)
def config(target):
	global cache_path,target_base_url,target_host,btarget_host
	from six.moves.urllib.parse import urlsplit
	up=urlsplit(url=target)
	target_host=up.netloc
	btarget_host=target_host.encode(gencoding)
	
	target_base_url='{}://{}/'.format(up.scheme,target_host)
	cache_path=F.mkdir(target_host) # in gst	
	F.dill_dump(file='target_base_url',obj=target_base_url)
	return cache_path,target_base_url,target_host
	
target_base_url=F.dill_load('target_base_url') or ''
if target_base_url:print( config(target_base_url) )

ips=F.dill_load('ips') or []
ipsn=F.dill_load('ipsn') or []

def target_to_flask_response(target,response=None,flask_request=None):
	global base_host
	if not response:response=make_response()
	response.status_code=target.status_code
	for k,v in target.headers.items():
		if k in skip_response_headers:
			continue
		response.headers[k]=v
	# response.headers._list=list(target.headers.items())
	response.headers['Content-Security-Policy']=''
	response.headers['Content-Encoding']=gencoding
	b=target.content
	if replace_domain and flask_request:
		if not base_host:base_host=flask_request.host.encode(gencoding)
		b=b.replace(btarget_host,base_host)
		
	response.set_data(b)
	return response

@app.errorhandler(404)
def mirror_cache(*a,**ka):
	''' 
# 'Content-Length': '',  pythonAnywhere 这一句 请求头， 会导致绝大数网站返回 400  错误

'''	
	# us=request.path.split('/')
	ip=request.headers.get('X-Real-Ip',request.remote_addr) 
	if ip not in ips:
		ipsn.append(ip)
		F.dill_dump(obj=ipsn,file='ipsn')
		return ip+'\nNot allowed!\n'+U.stime()
		
	path=request.path[1:]
	method=request.method
	# fn=cache_path+method[:1]+T.url2fn(path+request.environ.get('HTTP_COOKIE','')[:99] )
	url=T.sub(request.url,request.url_root ) 
	# if 
	fn=cache_path+method[:1]+T.url2fn(url)[:255-1-5]  
#Linux OSError: [Errno 36] File name too long  path 不算长度内。filename+ext 长度<= 255 OK
	
	if use_cache:
		target=F.dill_load(fn)
		if target:
			# print()
			# U.p('##',fn,file=sys.stderr,flush=True)
			return target_to_flask_response(target,flask_request=request)
	print(U.stime(),path)	
	send_headers={}
	for k,v in request.headers.items():
		v=v.replace(request.host,target_host)
		if k in {'Content-Length','Content-Type'}:
			if not v:continue
			U.println('###',k,v,U.stime(),request.url,request.headers,file=sys.stderr)
		send_headers[k]=v
	
	target=send_request(method=method, 
		url=target_base_url+path, 
		params=request.args, headers=send_headers, )
		
	flask_response= target_to_flask_response(target,flask_request=request)
	if dump:F.dill_dump(protocol=4,obj=target,file=fn)
	return flask_response
	
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


if __name__=='__main__':
	a=U.parseArgs(str=r'https://www.dulwich.io',int=1122)
	run(target=a.str,port=a.int)

