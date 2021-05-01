#coding=utf-8
import sys
if __name__.endswith('qgb.N'):from qgb import py
else:
	from pathlib import Path
	gsqp=Path(__file__).absolute().parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
	# import py  #'py': <module 'py' from '..\\py.py'>,
U,T,N,F=None,None,None,None
# __all__=['N','HTTPServer']

gError=[]
def setErr(ae):
	U=py.importU()
	global gError
	if U.gbLogErr:# U.
		if type(gError) is list:gError.append(ae)
		elif gError:gError=[gError,ae]
		else:gError=[ae]
	else:
		gError=ae
	if U.gbPrintErr:U.pln('#Error ',ae) # U.

try:
	if __name__.endswith('qgb.N'):
		from . import HTTP
		from . import HTTPServer
		from . import HTML
	else:
		import HTTP
		import HTTPServer
		import HTML
except Exception as ei:
	py.traceback(ei)

	
if py.is3():
	from http.server import SimpleHTTPRequestHandler,HTTPServer as _HTTPServer
else:
	from SimpleHTTPServer import SimpleHTTPRequestHandler
	from BaseHTTPServer import HTTPServer as _HTTPServer

def rpc_fifo_put_cmd(s,name='cmd',path=None):
	''' Linux has os.mkfifo(fn)  
Windows:AttributeError: module 'os' has no attribute 'mkfifo' 
	'''
	U,T,N,F=py.importUTNF()
	if not path:path=U.gst+'fifo/'
	if F.isabs(name):
		fn=name
	else:
		path=F.mkdir(path)
		fn=path+name
	import os
	try:
		os.mkfifo(fn)
	except FileExistsError as e:
		print(fn,e)
	t=U.itime()
	with os.fdopen(os.open(fn, os.O_SYNC | os.O_CREAT | os.O_RDWR)) as f:
		# os.write(f, s)
		f.write(s)
	return s,U.itime()-t
def rpc_fifo_eval(cmd='cmd',result='result',path=None,**ka):
	U,T,N,F=py.importUTNF()
	if not path:path=U.gst+'fifo/'
	def get_fn(name):
		if F.isabs(name):
			fn=name
		else:
			path=F.mkdir(path)
			fn=path+name
		try:
			os.mkfifo(fn)
		except FileExistsError as e:
			print(fn,e)
		return fn
	t=[U.itime()]		
	with os.fdopen(os.open(get_fn(cmd), os.O_RDONLY)) as rf:
		s=os.read(rf, -1)
	t.append(U.itime()-t[-1])	
	r=U.execResult(s,**ka)
	t.append(U.itime()-t[-1])	
	with os.fdopen(os.open(fn, os.O_SYNC | os.O_CREAT | os.O_RDWR)) as f:
		os.write(f, r)
	t.append(U.itime()-t[-1])	
	return r,t
	
def pppoe():
	'''
506 192.168.2.1+192.168.1.1 073198799737 777124	

'''
	
def copy_request(a,p=True):
	import requests
	U,T,N,F=py.importUTNF()
	if py.istr(a):a=F.dill_load(a)
	req=py.getattr(a,'request',0)
	if req:a=req
		# params=request.args, # ?a=b  in a.url
		
	if p:print(
U.v.requests.request(method=a.method,url=a.url,headers=a.headers,)
	)
		
	return requests.request(method=a.method, 
		url=a.url, 
		headers=a.headers, )
copy_req=req_copy=rebuild_request=request_copy=copy_request
	

def download_http_everthing(url,save_path=py.No('auto using pwd ?'),r=1,p=1):
	'''   '''
	global U,T,N,F
	U,T,N,F=py.importUTNF()
	from six.moves.urllib.parse import urlsplit

	h=N.get(url)
	if py.istr(h) and '''<a href="/"><img class="logo" src="/Everything.gif" alt="Everything"></a>''' in h:
		pass
			# url+='/'
	else:
		return h
	url=N.auto_url(url)
	# if not url.endswith('/'):url+='/'
	up=urlsplit(url=url)  # obj
	
	netloc=up.netloc
	url_base='http://'+netloc
	
	ups=[s for s in up.path.split('/') if s]	
	if not ups:cu='es-'+U.stime()
	else     :cu=ups[-1]
	
	# icu=url.rindex('/',0,-1)
	# if icu<=6:cu=''#'download_http_everthing'
	# else:
		# cu=url[icu+1 : -1] # 'C%3A'	
		# if ':' in cu:cu=T.url_encode(cu)
	
	#索引 /   indexof">索引 C:</p>     ">索引 C:\test</p>
	# c_folder=T.sub(h,'<tr><td colspan="3"><p class="indexof">','</p></td></tr>')
	# c_folder=F.get_filename(c_folder) # ''      '索引 C:'     'test'
	# save_path=F.mkdir(save_path)
	if not save_path.endswith('/') and not save_path.endswith('\\'):
		save_path+='/'
	save_path_cu=F.mkdir(save_path+cu)
	rfs=[]
	for r4 in parse_everthing_html(h):
		fn=save_path_cu + [s for s in r4[0].split('/') if s] [-1]
		if r4[-1]:
			fn+='/'
			if r:
				rfs.append( 
	{fn:download_http_everthing(url_base+r4[0],save_path=save_path_cu,r=r,p=p) } 
				)
				
			# continue  # skip folder
		else:
			fn=N.HTTP.get(url_base+r4[0],file=fn)	
			rfs.append(fn)
		if p:print(fn)	
	return rfs	
des=down_es=esdl=dl_es=dles=download_es=download_everthing_http=download_http_everthing

	
def parse_everthing_html(html):
	''' 名称	大小	修改日期    isd
	'''
	global T
	if not T:T=py.importT()
	b=T.BeautifulSoup(html)
	r=[]
	for n,e in enumerate(b.select('tr[class*=trdata]')     ):
		p=T.sub(e,'<a href="','"><img alt="')
		size=T.sub(e,'<td class="sizedata"><span class="nobr"><nobr>','</nobr></span>')
		time=T.sub(e,'<td class="modifieddata"><span class="nobr"><nobr><span class="nobr"><nobr>','</nobr></span></nobr></span></td>')
		isd=T.sub(e,'<img alt="" class="icon" src="/','.gif"/') == 'folder'
		# print('%-3s %-80s %-6s %-22s %-5s'%(n,p,size,time,isd)  )
		r.append([p,size,time,isd])
	return r	
parse_es=parse_everthing=parse_everthing_http=parse_http_everthing=parse_everthing_html
	
def zhihu_question(url,response=None):
	import qgb.tests.zhihu_scrapy_single_QA
	if not( py.istr(url) or py.isint(url) ):
		url=py.getattr(url,'url')
		
	r= qgb.tests.zhihu_scrapy_single_QA.zhihu(url)
	if response:
		response.set_data(r)
	return r
zhihu=zhihu_question	

def get_github_raw(q):
	''' 
https://github.com/nobodywasishere/SGH-I537_NA_LL_Opensource/blob/d731152178585788b45d6fd9c0168412ced4bfd8/Platform/vendor/samsung/common/packages/apps/SBrowser/src/chrome/test/data/extensions/api_test/webrequest_sendmessage/background.html

https://github.com/nobodywasishere/SGH-I537_NA_LL_Opensource/blob/master/Platform/vendor/samsung/common/packages/apps/SBrowser/src/chrome/test/data/extensions/api_test/webrequest_sendmessage/background.html

https://github.com/Banou26/chromium-issue-1178811/raw/main/content-script.js

https://raw.githubusercontent.com/Banou26/chromium-issue-1178811/main/content-script.js
'''	
	a=get_flask_request_a(q)
	sa=a.split('/')
	if '://github.com/' in a:
		n0=-1
		for n,i in py.enumerate(sa):
			if i=='github.com':
				n0=n
				
	
	
graw=getraw=github_raw=raw_github=get_github_raw	

def ping(addr,sum=5,sleep=0,timeout= 4,ttl=None,seq=0,size=56,interface=None,p=False,r=True,**ka):
	''' ping3.ping(
    dest_addr: str,
    timeout: int = 4,
    unit: str = 's', ##unit: The unit of returned value. "s" for seconds, "ms" for milliseconds. (default "s")
    src_addr: str = None,
    ttl: int = None,
    seq: int = 0,
    size: int = 56,
    interface: str = None,
) -> float 
Returns:
    The delay in seconds/milliseconds or None on timeout. # qgb return ms
	
C:\QGB\Anaconda3\lib\site-packages\ping3.py in send_one_ping(sock, dest_addr, icmp_id, seq, size)
    189     _debug("Sent ICMP Payload:", icmp_payload)
    190     packet = icmp_header + icmp_payload
--> 191     sock.sendto(packet, (dest_addr, 0))  # addr = (ip, port). Port is 0 respectively the OS default behavior will be used.
    192
    193

OSError: [WinError 10051] 向一个无法连接的网络尝试了一个套接字操作。	
OSError(10065, '套接字操作尝试一个无法连接的主机。', None, 10065, None),'192.168.2.1',56

'''
	import ping3
	U,T,N,F=py.importUTNF()
	addr=auto_ip(addr,**ka)
	sum=U.get_duplicated_kargs(ka,'times','n',default=sum)
	def _return(msg,*a):
		Win.set_title(title=_title)
		if py.islist(msg):return msg
		else:
			return py.No(msg,*a)
	lr=[];re=[]
	if p:
		sv=U.v(dest_addr=addr,timeout=timeout,unit='ms',ttl=ttl,seq=seq,size=size,interface=interface)[1:-2]
		time=U.stime()
		if U.isWin():
			Win=py.from_qgb_import('Win')
			_title=U.set('window_title',Win.get_title())
			Win.set_title(title='ping '+sv+' '+time)
		print(time,'%54s'%addr)
		print(sv, )
		print('-'*80)
	for i in py.range(sum):
		try:
			if i and sleep and ms!=None:U.sleep(sleep)
			ms=ping3.ping(dest_addr=addr,timeout=timeout,unit='ms',ttl=ttl,seq=seq,size=size,interface=interface)
		except OSError as e:
			ms=py.No(e)
		except (SystemExit,KeyboardInterrupt,Exception) as e:#必须加括号，否则语法错误
			return _return(e,addr,size,)
		if not py.isnumber(ms):
			re.append(i)
		if p:
			print('%-5s'%i,'%-15s'%U.stime()[12:],'ms=%r'%ms,)
		if r:lr.append([i,ms])
		else:ms #TODO count timeout rate, avg ms
	if py.len(re)==sum:
		return _return('ping %s %s times all faild!'%(addr,sum),addr,timeout,ttl,seq,size,interface)
	else:
		if r:return _return(lr)

def range_http_server(port=2233,**ka):
	'''
#TODO 标准库test 不支持https 

['C:/QGB/npp/notepad++.exe',
 'C:\\QGB\\Anaconda3\\lib\\http\\server.py',
 '-n 1219']
 
def test(HandlerClass=BaseHTTPRequestHandler,
		 ServerClass=ThreadingHTTPServer,
		 protocol="HTTP/1.0", port=8000, bind=""):	
	
	'''
	try				  :import http.server as SimpleHTTPServer	# Python3
	except ImportError:import SimpleHTTPServer					# Python 2
	from RangeHTTPServer import RangeRequestHandler
	U,T,N,F=py.importUTNF()

	ip=U.get_duplicated_kargs(ka,'ip','bind','addr','address','listen','IP',default='0.0.0.0')
	# import RangeHTTPServer

	a=U.parse_args(port=port,ip=ip)
 
	return SimpleHTTPServer.test(HandlerClass=RangeRequestHandler,port=a.port,bind=a.ip)
RangeRequestHandler=RangeHTTPServer=rangeHTTPServer=range_server=range_http_server
	
	
def uploadServer(port=1122,host='0.0.0.0',dir='./',url='/up'):
	'''curl  http://127.0.0.1:1122/up -F file=@./U.py
	'''
	U,T,N,F=py.importUTNF()
	
	from flask import Flask,request,make_response, send_from_directory
	app= Flask('uploadServer'+U.stime_() )
	@app.route(url,methods=['POST','GET'])
	def upload_file():
		file = request.files['file']
		if file:
			filename = U.path.join(dir, file.filename)
			file.save(filename)			
			r= make_response(filename)
			r.headers['Content-Type'] = 'text/plain;charset=utf-8'
			return r
	app.run(host=host,port=port,debug=0,threaded=True)	

def get_or_set_rpc_base(base):
	if not base:
		base=U.get_or_set('N.rpc.base','http://127.0.0.1:23571/')
	if not py.istr(base):
		if py.isfloat(base):
			base='http://192.168.{}:23571/'.format(base)
		else:
			raise py.ArgumentUnsupported('rpc base_url:',base)

	if not base.endswith('/'):
		if ':' not in base:
			base=base+':23571'
		base+='/'
	return U.set('N.rpc.base',base)	
	
def rpcGetVariable(varname,base=py.No('auto history e.g. [http://]127.0.0.1:23571[/../] '),
		timeout=9,):
	U,T,N,F=py.importUTNF()	
	if not base:
		base=U.get_or_set('N.rpc.base','http://127.0.0.1:23571/')
	if not base.endswith('/'):base+='/'
	U.set('N.rpc.base',base)
	
	url='{0}response.set_data(F.dill_dump({1}))'.format(base,varname)
	# import requests,dill
	# dill_loads=dill.loads
	# get=requests.get
	dill_loads=py.importF().dill_loads
	get=HTTP.get_bytes

	b=get(url,verify=False,timeout=timeout)
	if not b:return b
	if not py.isbytes(b):
		b=b.content
	return dill_loads(b)
rpc_get=rpc_get_var=rpcGetVariable

def rpcSetVariable(*obj,base=py.No('auto history e.g. [http://]127.0.0.1:23571[/../] '),timeout=9,varname='v',**ka):
	U,T,N,F=py.importUTNF()
	ext_cmd=U.get_duplicated_kargs(ka,'ext_cmd','cmd','extCmd','other_cmd')
	
	if len(obj)==1 and ',' not in varname:
		obj=obj[0]

	if not base:
		base=U.get_or_input('rpc_base',default='http://127.0.0.1:23571/')
	else:
		base=U.set('rpc_base',base)
	url='{0}{1}=F.dill_loads(request.get_data());r=U.id({1});{2}'.format(base, varname,ext_cmd	)
	# import requests,dill
	# dill_loads=dill.loads
	# post=requests.post
	post=HTTP.post
	# dill_dump=F.dill_dump
	print(url)
	b=post(url,verify=False,timeout=timeout,data=F.dill_dump(obj)) # data=list:TypeError: cannot unpack non-iterable int object
	if not b:return b
	if not py.isbytes(b):
		b=b.content
	if py.isbytes(b):
		b= b.decode('utf-8')
	# if py.istr:
	return url,b

set_rpc=set_rpc_var=rpc_set=rpc_set_var=rpcSetVariable


def rpcServer(port=23571,thread=True,ip='0.0.0.0',ssl_context=(),currentThread=False,app=None,key=None,
execLocals=None,locals=None,globals=None,
qpsu='py,U,T,N,F',importMods='sys,os',request=True,
flaskArgs=None,
	):
	'''
	locals : execLocals
	if app : port useless
	key char must in T.alphanumeric
key compatibility :  key='#rpc\n'==chr(35)+'rpc'+chr(10)	
	ssl_context default use https port=443 
	
	'''
	from threading import Thread
	U=py.importU()
	T=py.importT()
	if not U.get('pformat_kw'):
		U.set('pformat_kw',{'width':144})
	
	if not flaskArgs:
		flaskArgs=py.dict(debug=0,threaded=True)
	
	if execLocals:
		warnning='### deprecated args execLocals {ip}:{port}'.format(ip=ip,port=port)
		U.log(warnning)
		globals=execLocals
		locals={'warnning':warnning} #同时模仿以前可以保存变量的效果
		
	if not globals:globals={}
	
	for modName in importMods.split(','):
		globals[modName]=U.getMod(modName)
	if qpsu:
		for modName in qpsu.split(','):
			globals[modName]=U.getMod('qgb.'+modName)	
		
	from flask import Flask,make_response
	from flask import request as _request
	
	app=app or Flask('rpcServer'+U.stime_()   )
	
	def _flaskEval(code=None):
		nonlocal globals,locals 
		if not code:code=T.urlDecode(_request.url)
		code=T.sub(code,_request.url_root )
		if key and code.startswith(key):code=code[py.len(key):]
		# U.log( (('\n'+code) if '\n' in code else code)[:99]	)
		# U.ipyEmbed()()
		_response=make_response()
		_response.headers['X-XSS-Protection']=0
		_response.headers['Access-Control-Allow-Origin'] = '*'
		_response.headers['Content-Type'] = 'text/plain;charset=utf-8'
		
		if request:#rpcServer config
			globals['request']=_request
			globals['response']=_response
			globals['q']=_request
			globals['p']=_response
		if not globals:globals=None # 如果globals 为空dict，防止闭包保存变量，保持globals在每个请求重新为空这一特性
		r=U.execResult(code,globals=globals,locals=locals) #因为在这里一般指定了 不为None的 globals，所以在每个请求中可以共享 
		if (not _response.response) and (not _response.get_data()):
			_response.set_data(r)
		return _response
	
	if py.istr(key):
		if py.len(key)<1:return py.No('key length < 1',key)
		# for i in key:
			# if i not in T.alphanumeric:
				# return py.No('key char must in T.alphanumeric',key)
		
		@app.route('/'+key+'<path:text>',
			methods=['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE', 'HEAD', 'PATCH'])
		def flaskEval(*a,**ka):return _flaskEval()
	else:
		@app.errorhandler(404)
		def flaskEval(*a,**ka):return _flaskEval()
		
	if not app.name.startswith('rpcServer'):
		return (py.No('caller provide app,so no thread start'),app)
	
	flaskArgs.update(py.dict(host=ip,port=port) ) #可变dict，不能用flaskArgs=
	
	if ssl_context:
		flaskArgs['ssl_context']=ssl_context
		if port==23571:
			port=443
			flaskArgs['port']=port
	# U.log(flaskArgs)
	if currentThread or not thread:
		return app.run(**flaskArgs)
	else:
		t= Thread(target=app.run,name='qgb thread '+app.name,kwargs=flaskArgs)
		t.start()
		return (t,app)
########### flaskEval end ###########	
	if py.is3():from http.server import BaseHTTPRequestHandler as h
	class H(SimpleHTTPRequestHandler):
		def do_GET(s):
			code=s.path[1:]
			try:
				r=execResult(code)
				s.send_response(200)
			except Exception as e:
				s.send_response(500)
				
			s.send_header("Content-type", "text/plain")
			s.end_headers()		
			
			if not py.istr(r):
				r=repr(r)
			if py.is3():
				r=r.encode('utf8')
			s.wfile.write(r)
	

		
	# with _HTTPServer((ip,port), H) as httpd:
		# sa = httpd.socket.getsockname()
		# serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
		# print(serve_message.format(host=sa[0], port=sa[1]))
		# try:
			# if currentThread or not thread:httpd.serve_forever()
			# else:
				# t= Thread(target=httpd.serve_forever,name='qgb.rpcServer '+U.stime() )
				# t.start()
				# return t
				
		# except KeyboardInterrupt:
			# print("\nKeyboard interrupt received, exiting.")
	
# class rpcServer(HTTPHandler):
	# def __init__
		# super()
		
	
def rpcClient(url_or_port='http://127.0.0.1:23571',code=''):
	if py.isint(url_or_port):
		url='http://127.0.0.1:'+py.str(url_or_port)
	else:
		url=py.str(url_or_port)
	if not url.endswith('/'):url+='/'
	T=py.importT()
	code=T.urlEncode(code)
	return get(url+code)
	# if py.is3():
		# from xmlrpc.client import ServerProxy,MultiCall
	# server = ServerProxy(url)
	# return server

def parse_pem(pem_str_or_bytes):
	if py.istr(pem_str_or_bytes):
		pem_bytes=pem_str_or_bytes.encode('utf-8')
	elif py.isbytes(pem_str_or_bytes):
		pem_bytes=pem_str_or_bytes
	else:
		raise py.ArgumentError()
	import pem
	list= pem.parse(pem_bytes)
	if py.len(list)==1:
		return list[0]
	else:
		return list
	# with open('cert.pem', 'rb') as f:
	# 	certs = pem.parse(f.read())

def get_all_socket_obj():
	import socket
	return U.get_objects(socket.socket) 
get_socket_all_obj=get_all_socket_obj

def get_socket_req(PORT = 65432,HOST = '127.7.7.7'):
	import socket
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		req, addr = s.accept()
		return req, addr

def get_rpc_request_a(request=None):
	''' 
a=T.subr(u,T.u23)#'%23-'	

pythonAnywhere : multi[ // or  %2F%2F%2F%2F%2F ] in url will auto convert to one / ,it can't bypass
	'''
	if py.istr(request):return request
	if not request:
		from flask import request
	U,T,N,F=py.importUTNF()
	u=request.url
	if '%23=' in u:
		a=T.sub_tail(u,'%23=')
	elif '%23-' in u:
		a=T.sub_tail(u,'%23-')
	elif '#-' in u: # pythonAnywhere
		a=T.sub_tail(u,'#-')
	else:
		if '%23' not in u:
			raise py.ArgumentError('%23 not in request.url')
		a=T.sub_tail(u,'%23')
	return T.url_decode(a)
geta=get_a=get_request_a=get_flask_request_a=get_rpc_request_a


def get_flask_request_file(q):
	''' dir(f)  
[__...,'_parse_content_type', '_parsed_content_type', 'close', 'content_length', 'content_type', 'filename', 'headers', 'mimetype', 'mimetype_params', 'name', 'save', 'stream']
'''	
	f=q.files['file']
	r=f.save(dp+f.filename)  # None
	return f,r

def pdf2html(url,response=None,zoom=None,path=None,pw=None):
	U,T,N,F=py.importUTNF()
	if not zoom:
		zoom=U.get('pdf2html_zoom',1)
	if not path:
		path=U.get('pdf2html_path','/root/pdf/')
	U.cd(path)
	fn=T.url2fn(url[-200:])
	if not fn.lower().endswith('.pdf'):fn+='.pdf'

	def do_resp(a):
		if not response:return a
		if not (py.istr(a) or py.isbytes(a)):
			a=T.pformat(a)
			response.set_data(a)	
		else:
			response.headers['Content-Type']='text/html;charset=utf-8';
			response.set_data(a)	
		return a
	
	if not F.exists(path+fn):
		U.cmd('wget','-O',fn, url,timeout=30)
		# b=N.HTTP.getBytes(url)
		# if not b:return do_resp(b)
		# U.pln(F.write(path+fn,b))
	html_file=path+fn[:-4]+'.html'
	if not F.exists(html_file):
		if not pw:
			pw=U.get('sudo_pw')
		if not pw:
			return do_resp('wocao,no pw')
	# -it : the input device is not a TTY
		cmd='docker run --rm -v {path}:/pdf bwits/pdf2htmlex pdf2htmlEX --no-drm 1 --zoom {zoom} {fn}'
		cmd=cmd.format(path=path,fn=fn,zoom=zoom)
		U.sudo(password=pw,cmd=cmd)
	if not F.exists(html_file):
		fs=F.ls(path,f=1)
		return do_resp(['not found html of pdf : ',fn,
		U.v.U.sudo(password=pw,cmd=cmd),fs])
	else:
		return do_resp(F.read(html_file))

def flask_html_response(response,html='',file='',remove_tag=(
		['<script','</script>'],
['<SCRIPT','</SCRIPT>'],'ondragstart=','oncopy=','oncut=','oncontextmenu=','"return false;"',
	),encoding='utf-8',splitor='<hr>',content_type='text/html;charset=utf-8',**ka):
	'''
Resource interpreted as Stylesheet but transferred with MIME type text/html:
不正确设置 type可能导致页面无法正常显示
'''	
	U,T,N,F=py.importUTNF()
	if U.get_duplicated_kargs(ka,'remove_script','del_script','no_script'):
		remove_tag=(
['<script','</script>'], ['<SCRIPT','</SCRIPT>'],
		)
		
	if not html and file:
		import mimetypes
		content_type = (
             mimetypes.guess_type(file)[0] or content_type #"application/octet-stream"
                )
		# ext= T.subLast(file,'.').lower()
		if 'text' in content_type:
			fencoding=F.detect_encoding(file,print_detect_encoding=False)
			if not fencoding:fencoding=encoding
			content_type+=';charset=%s'%(fencoding,)
		html=F.read_bytes(file)
	if py.istr(html):
		pass
	elif py.isbyte(html):#TODO byte remove tag,no convert
		if remove_tag:html=html.decode(encoding)
		pass
	elif U.iterable(html):#TODO byte remove tag,no convert
		html=splitor.join( py.str(i) for i in html )
	else:#if not py.istr(html):
		html=py.str(html)
	
	for itag in remove_tag:
		if py.istr(itag):
			html=html.replace(itag,'')
			continue
		if py.len(itag)==2:
			start,end=itag
		s=True
		while s:
			s=T.sub(html,start,end)
			if not s:break
			html=html.replace(start+s+end,'')
	response.headers['Content-Type']=content_type;
	response.set_data(html)
html=htmlp=response_html=html_response=flask_html_response

def get_chunk(full_path,byte1, byte2=None,):
	 # = "try2.mp4"
	file_size = os.stat(full_path).st_size
	start = 0
	length = 102400

	if byte1 < file_size:
		start = byte1
	if byte2:
		length = byte2 + 1 - byte1
	else:
		length = file_size - start

	with open(full_path, 'rb') as f:
		f.seek(start)
		chunk = f.read(length)
	return chunk, start, length, file_size

def flask_media_stream_response(request,response,file=None,):		
	from flask import stream_with_context
	U,T,N,F=py.importUTNF()
	if not file:
		file=get_flask_request_a(request)					
	import re
	range_header = request.headers.get('Range', None)
	byte1, byte2 = 0, None
	if  range_header:
		match = re.search(r'(\d+)-(\d*)', range_header)
		groups = match.groups()

		if groups[0]:
			byte1 = int(groups[0])
		if groups[1]:
			byte2 = int(groups[1])
			
	gen=F.read_as_stream(file,start=byte1) # 这里不会出错，iter generator 才 服务器内部错误
	try:
		py.next(gen)
		response.response=stream_with_context(gen)
		response.headers['Content-Type'] = 'video/mp4'
		response.headers['mimetype'] = 'video/mp4'
		if range_header:
			response.headers.add('Content-Range', 'bytes {0}-'.format(byte1
		#, byte1 + length - 1, file_size
			))
			if byte1>0:
				response.status_code = 206

	except Exception as e:
		# r=T.pformat([e,U.get_tb_stack()],**U.get('pformat_kw',{}))
		r=py.repr(e)
		response.set_data(r)
	return	

	chunk, start, length, file_size = get_chunk(byte1, byte2)
	resp = Response(chunk, 206, mimetype='video/mp4',
					  content_type='video/mp4', direct_passthrough=True)
	resp.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
	return resp	
	
mp4_response=media_response=flask_media_stream_response
	
def flask_file_stream_response(response,file,):
	from flask import stream_with_context,request
	U,T,N,F=py.importUTNF()
	# try:
	range=get_request_range(request)
	# request.headers.get('Range','')
	# if range:
		
	gen=F.read_as_stream(file) # 这里不会出错，iter generator 才 服务器内部错误
	try:
		py.next(gen)
		response.response=stream_with_context(gen)
		# 不获取filename, 保存文件名是 D__test_7C_荣耀7C-LND-B202_8.0.zip
		# 不进行url_encode,chrome ERR_RESPONSE_HEADERS_TRUNCATED
		# response.headers['Content-Disposition'] = "inline; filename=" + T.url_encode(file)
		response.headers['Content-Disposition'] ="inline; filename=" + T.url_encode(F.get_filename_from_full_path(file))
		response.headers['Content-Length'] =F.size(file)
		
	except Exception as e:
		# r=T.pformat([e,U.get_tb_stack()],**U.get('pformat_kw',{}))
		r=py.repr(e)
		response.set_data(r)

file=stream_file=file_stream=read_as_stream=flask_file_stream_response

def flask_image_response(response,image,format='png',**ka):
	from io import BytesIO
	img_io = BytesIO()
	image.save(img_io, format)
	img_io.seek(0)
	# response.response=stream_with_context(gen)
	ctype='image/'+format
	response.headers['Content-Type'] = ctype
	response.headers['mimetype'] = ctype
	bytes=img_io.read(-1)
	response.set_data(bytes)
	return U.v  # huawei Android 旧版 系统浏览器，如果url 不是 .png等 结尾。不会显示图像
	# return response,image,bytes

def flask_screenshot_response(response,rect=py.No('rect=[x,y,x1,y1] or auto get clipboard or full_screen '),**ka):
	''' rect (crop)  defining the left, upper, right, and lower pixel
	
Image.open(fp)	
:param fp: A filename (string), pathlib.Path object or a file object.
   The file object must implement `~file.read`,
   `~file.seek`, and `~file.tell` methods,
   and be opened in binary mode.	
	'''
	from PIL import Image
	U,T,N,F=py.importUTNF()
	if U.isWin() or U.isMac():
		from PIL import ImageGrab
	if rect:
		if py.istr(rect) or py.isfile(rect):
			# if F.exist(rect):
			im=Image.open(rect)
		elif py.isinstance(rect,Image.Image):
			im=rect
		elif U.len(rect)!=4:
			raise py.ArgumentError('rect must be PIL Image or [ x0,y0,x1,y1 ]')
		else:
			im = ImageGrab.grab(rect)
	else:	
		im = ImageGrab.grabclipboard()
		if not im:
			im=ImageGrab.grab()
	return flask_image_response(response,im)
img= screenshot_response=flask_screenshot_response
	
def is_flask_request(q):
	from werkzeug.local import LocalProxy
	return isinstance(q,LocalProxy)

def set_proxy(host='',port='',protocol='socks5',target_protocol=('http','https'),**ka):
	''' no args provide,proxy will clean
'proxies','proxy','ip'  =py.No('duplicated arg:host')	
	'''
	U,T,N,F=py.importUTNF()
	d={}
	proxies=U.get_duplicated_kargs(ka,'proxies','proxy','ip')
	if not host and proxies:
		host=proxies
	if py.isdict(host):
		for k,v in host.items():
			d.update( set_proxy(v,target_protocol=k) ) # 递归
		return d
	
	host=host.strip()
	if '://' in host:
		protocol=T.sub(host,'','://')
		host=T.sub(host,'://','')
	if ':' in host:
		port=T.subLast(host,':','')
		host=T.subLast(host,'',':')

	if py.istr(target_protocol):
		target_protocol=[target_protocol]
	for t in target_protocol:
		# if not ip:
		host=U.set('{}.proxy.host'.format(t),host)
		port=U.set('{}.proxy.port'.format(t),port)
		protocol=U.set('{}.proxy.protocol'.format(t),protocol)
		if not host or not port or not protocol:
			# 跳过格式不对的代理
			continue
		d[t]="{}://{}:{}".format(protocol,host,port)
	return d
	# {'http': "socks5://myproxy:9191"}
setProxy=set_proxy

def get_proxy(target_protocol=('http','https'), ):
	U,T,N,F=py.importUTNF()
	d={}
	for t in target_protocol:
		host=U.get('{}.proxy.host'.format(t),)
		port=U.get('{}.proxy.port'.format(t),)
		protocol=U.get('{}.proxy.protocol'.format(t),)
		if not host or not port or not protocol:continue
		d[t]="{}://{}:{}".format(protocol,host,port)
	return d
getProxy=get_proxy

def get(url,protocol='http',**ka):
	U,T,N,F=py.importUTNF()
	if F.exist(url):
		return F.read(url)
	if '://' in url:
		p=T.sub(url,'',':')
		if p:protocol=p
		else:raise U.ArgsErr(url)
	else:url=protocol+'://'+url
	if url.startswith('http'):
		# import HTTP
		return HTTP.get(url,**ka)	

def http(url,method='get',*args):
	return HTTP.method(url,method,*args)

def ipToInt(ip):
	ips=ip.split('.')
	if py.len(ips)!=4:return py.No('ip format err',ip)
	r=0
	for n,s in py.enumerate(ips):
		i=py.int(s)
		r+=i*256**(3-n)
	return r
ip_int=ip2int=ipToInt

def ipLocation(ip,reverse_ip=False,
junk=['本机地址  CZ88.NET','IANA 保留地址','局域网 IP','局域网 对方和您在同一内部网'] ):
	location=' '.join(ip_location_qqwry(ip))
	location=location.replace('CZ88.NET','').strip() #去除包含的
	
	if location in junk:
		return ip
		location=py.No(location)	
	if reverse_ip:
		return '%-15s [%s] '%(ip,location)
		# return '{0} [{1}] '.format(ip,location)
	else:
		return location		
sip_location=sipLocation=ip_location=ipLocation

######################  qqwry   ###########################
gw_qqwry=['CoreLink骨干网', '不丹', '东帝汶', '中非', '丹麦', '乌克兰', '乌兹别克斯坦', '乌干达', '乌拉圭', '乍得', '也门', '亚太地区', '亚洲', '亚美尼亚', '以色列', '伊拉克', '伊朗', '伯利兹', '佛得角', '俄罗斯', '保加利亚', '克罗地亚', '关岛', '冈比亚', '冰岛', '几内亚', '几内亚比绍', '列支敦士登', '刚果共和国', '刚果民主共和国', '利比亚', '利比里亚', '加勒比海地区', '加拿大', '加纳', '加蓬', '匈牙利', '北美地区', '北马其顿', '北马里亚纳群岛', '南极洲', '南苏丹', '南非', '博茨瓦纳', '卡塔尔', '卢旺达', '卢森堡', '印尼', '印度', '印度尼西亚', '危地马拉', '厄瓜多尔', '厄立特里亚', '叙利亚', '古巴', 
'台湾省', '台湾省云林县', '台湾省南投县', '台湾省南投县南投市', '台湾省台东县', '台湾省台中市', '台湾省台北市', '台湾省台南市', '台湾省嘉义县', '台湾省嘉义市', '台湾省基隆市', '台湾省宜兰县', '台湾省屏东县', '台湾省彰化县', '台湾省新北市', '台湾省新竹县', '台湾省新竹市', '台湾省桃园市', '台湾省澎湖县', '台湾省花莲县', '台湾省苗栗县', '台湾省金门县', '台湾省高雄市', 
'吉尔吉斯斯坦', '吉布提', '哈萨克斯坦', '哥伦比亚', '哥斯达黎加', '喀麦隆', '图瓦卢', '土库曼斯坦', '土耳其', '圣卢西亚', '圣基茨和尼维斯', '圣多美和普林西比', '圣巴泰勒米', '圣文森特和格林纳丁斯', '圣皮埃尔和密克隆群岛', '圣诞岛', '圣马力诺', '圭亚那', '坦桑尼亚', '埃及', '埃塞俄比亚', '基里巴斯', '塔吉克斯坦', '塞内加尔', '塞尔维亚', '塞拉利昂', '塞浦路斯', '塞舌尔', '墨西哥', '多哥', '多米尼克', '多米尼加', '奥兰群岛', '奥地利', '委内瑞拉', '孟加拉', '孟加拉国', '安哥拉', '安圭拉', '安提瓜和巴布达', '安道尔', '密克罗尼西亚联邦', '尼加拉瓜', '尼日利亚', '尼日尔', '尼泊尔', '巴勒斯坦', '巴哈马', '巴基斯坦', '巴巴多斯', '巴布亚新几内亚', '巴拉圭', '巴拿马', '巴林', '巴西', '布基纳法索', '布隆迪', '希腊', '帕劳', '库克群岛', '库拉索', '开曼群岛', '德国', '意大利', '所罗门群岛', '托克劳', '拉美地区', '拉脱维亚', '挪威', '捷克', '摩尔多瓦', '摩洛哥', '摩纳哥', '文莱', '斐济', '斯威士兰', '斯洛伐克', '斯洛文尼亚', '斯里兰卡', '新加坡', '新喀里多尼亚', '新西兰', '日本', '智利', '朝鲜', '柬埔寨', '根西岛', '格林纳达', '格陵兰', '格鲁吉亚', '梵蒂冈', '欧洲', '欧洲地区', '欧盟', '欧美地区', '比利时', '毛里塔尼亚', '毛里求斯', '汤加', '沙特阿拉伯', '法国', '法属圣马丁', '法属圭亚那', '法属波利尼西亚', '法罗群岛', '波兰', '波多黎各', '波斯尼亚和黑塞哥维那', '泰国', '泽西岛', '津巴布韦', '洪都拉斯', '海地', '澳大利亚', '澳洲', '澳门', '爱尔兰', '爱沙尼亚', '牙买加', '特克斯和凯科斯群岛', '特立尼达和多巴哥', '玻利维亚', '瑙鲁', '瑞典', '瑞士', '瓜德罗普', '瓦利斯和富图纳群岛', '瓦努阿图', '留尼汪岛', '白俄罗斯', '百慕大', '直布罗陀', '福克兰群岛', '科威特', '科摩罗', '科特迪瓦', '科索沃', '秘鲁', '突尼斯', '立陶宛', '索马里', '约旦', '纳米比亚', '纽埃', '缅甸', '罗马尼亚', '美国', '美属维尔京群岛', '美属萨摩亚', '美洲地区', '老挝', '肯尼亚', '芬兰', '苏丹', '苏里南', '英国', '英属印度洋领地', '英属维尔京群岛', '荷兰', '荷兰加勒比', '荷兰省', '荷属圣马丁', '莫桑比克', '莱索托', '菲律宾', '萨尔瓦多', '萨摩亚', '葡萄牙', '蒙古 ', '蒙特塞拉特岛', '西班牙', '诺福克岛', '贝宁', '赞比亚', '赤道几内亚', '越南', '阿塞拜疆', '阿富汗', '阿尔及利亚', '阿尔巴尼亚', '阿曼', '阿根廷', '阿联酋', '阿鲁巴', '非洲地区', '韩国', '韩国首尔', '香港', '马尔代夫', '马恩岛', '马拉维', '马提尼克', '马来西亚', '马约特', '马绍尔群岛', '马耳他', '马达加斯加', '马里', '黎巴嫩', '黑山'] 
#278

g_reserved_qqwry=[ 'IANA机构', 'IANA保留地址', '运营商级NAT','本机地址', '本地', 'IANA', '局域网']
# 7
	
gn_qqwry=['上海', '云南', '内蒙古', '北京', '南京', '吉林', '四川', '天津', '宁夏', '安徽', '山东', '山西', '广东', '广西', '新疆', '江苏', '江西', '河北', '河南', '浙江', '海南', '湖北', '湖南', '甘肃', '福建', '西藏', '贵州', '辽宁', '重庆', '陕西', '青海', '黑龙江', '东北三省', '广州市清', '长春工业', '西安石油', '北方工业', '首都经贸', '首都师范', '宁波大学', '华中农业', '中国人民', '华东师范', '中南大学', '长江大学', '东北农业', '对外经济', '东华大学', '华南理工', '华中科技', '武汉大学', '大连理工', '南开大学', '中国', '中国青岛嘉华网络BGP', '中国农业科学院', '雅虎中国', '雅虎中国公司', '中国CEI(中国经济信息网)骨干网', '中国国际电子商务中心', '中国电信', '南昌理工学院', '电信'] 
#63
# 203.14.187.0-255 ('电信', ' CZ88.NET')

	
def ip_location_qqwry(ip,dat_path=py.importU().gst+'qqwry.dat'):
	'''return ('地区' , '运营商')
if want update qqwry.dat , reloa N module,and call this with dat_path !!!
warnning: NOT thread safe !!!

pip install qqwry-py3

pip install qqwry  # Not have cz88update
	'''	
	if ('q' not in ip_location_qqwry.__dict__):
		U=py.importU()
		F=py.importF()
		import qqwry
		
		if not dat_path:
			if U.isWin():
				qqwry_path=r'C:\Program Files (x86)\cz88.net\ip\qqwry.dat'
				if F.exist(qqwry_path):
					dat_path=qqwry_path
			if not dat_path:
				dat_path=U.gst+'qqwry.dat'
				
		if not F.exist(dat_path):
			U.log(['updateQQwry length:', qqwry.updateQQwry(dat_path)] )
			
		ip_location_qqwry.q = qqwry.QQwry()
		ip_location_qqwry.q.load_file(dat_path,loadindex=True)
	
	return ip_location_qqwry.q.lookup(ip)  #('北京市', '联通')

###################  qqwry end ###########################
def address_coordinate(address,raw_response=True):
	import requests
	cookies = {
		'BAIDUID': '7240C1BD73BF5509083867D8372AA3C8:FG=1',
		'PSTM': '1547906786',
		'BDUSS': 'dnamEzZk5OT3N6R3J2QnJVckMtdjdIMm54ZjY3VWNsTGQ5SmtodjVOS2JaOE5jQVFBQUFBJCQAAAAAAAAAAAEAAACYT6sRUUdCQ1MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJvam1yb2ptcaV',
		'MCITY': '-%3A',
		'H_WISE_SIDS': '131410_126124_128701_129321_114744_128142_120764_120189_131601_118886_118868_131402_118843_118833_118797_130762_131650_131577_131535_131534_131529_130222_131390_129565_107320_131394_130123_131518_131240_131195_117327_130347_117436_130075_129647_124635_130690_131435_131687_131036_131047_129981_130989_129901_129479_129646_124802_131467_131424_110085_127969_131506_123290_131094_131297_128200_131550_131264_131262_128600',
		'BIDUPSID': '2DD44AA3F0CF69531B5E310CF80AEBD8',
		'pgv_pvi': '6249972736',
		'pgv_si': 's660814848',
		'ZD_ENTRY': 'google',
		'H_PS_PSSID': '1453_21112_18560_29523_29521_29720_29568_29220_22159',
	}
	headers = {
		'Pragma': 'no-cache',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 YaBrowser/19.3.1.779 Yowser/2.5 Safari/537.36',
		'Accept': '*/*',
		'Referer': 'https://maplocation.sjfkai.com/',
		'Connection': 'keep-alive',
		'Cache-Control': 'no-cache',
	}
	# '湖南省长沙市长沙县长沙经济技术开发区开元东路华润置地广场一期12幢'
	params=(('address', address),
	('output', 'json'),
	('ak', 'gQsCAgCrWsuN99ggSIjGn5nO'),
	('callback', 'showLocation0'))

	response = requests.get('https://api.map.baidu.com/geocoder/v2/', headers=headers, params=params, cookies=cookies)
	s=response.content.decode('utf-8')
	s=s.replace('showLocation0&&showLocation0(','')
	s=s.replace('}})','}}')
	T=py.importT()
	try:
		json=T.json_loads(s)
	except Exception as e:
		json={'err_s':s,
			  'err':e}
	response.close()
	if raw_response:
		json['raw_response']=response
	return json
	
map_location=address_coordinate	
	
	
	
def whois(domain,raw_response=False):
	'''
In [59]: [i for i in dw if 'admin_name' not in dw[i] ] #58643
['csfangyi.com', 'xn--xuw24ggz9aile.cn', '06jd.com', 'yzy88.com', 'cshelong.com']

''' 
	T=py.importT()
	import requests
	cookies = {	'st': '95f5609d7aaadb13806df43e2ca1961c',	}
	headers = {
		'Pragma': 'no-cache',
		'Origin': 'http://whois.4.cn',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
	'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 YaBrowser/19.3.1.779 Yowser/2.5 Safari/537.36',

		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Cache-Control': 'no-cache',
		'X-Requested-With': 'XMLHttpRequest',
		'Connection': 'keep-alive',
		'Referer': 'http://whois.4.cn/batch',
	}

	data = {'domain': domain,  'isRefresh': '1'}
	response=requests.post('http://whois.4.cn/api/main',headers=headers,cookies=cookies,data=data)
	json=T.json_loads(response.content.decode('utf-8'))
	response.close()
	if raw_response:
		json['raw_response']=response
	return json
	
	
def bulk_whois(domain_list,args):
	import requests,json,logging
	bulkwhois_base_url = 'https://www.whoisxmlapi.com/BulkWhoisLookup/bulkServices/'
	session = requests.session()
	data = {
		"domains": domain_list,
		"password": args.password,
		"username": args.username,
		"outputFormat": 'json'
	}
	header = {'Content-Type': 'application/json'}
	# Posting task to API
	response = session.post(bulkwhois_base_url + 'bulkWhois',
							 data=json.dumps(data),
							 headers=header,
							 timeout=5)
	if response.status_code != 200:
		logging.error("wrong response code: %i" % response.status_code)
		return response
	response_data = json.loads(response.text)
	if response_data['messageCode'] == 200:
		logging.debug('Response: ' + response.text)
		del data['domains']
		data.update({
			'requestId': response_data['requestId'],
			'searchType': 'all',
			'maxRecords': 1,
			'startIndex': 1
		})
	else:
		logging.error('Response: ' + response.text)
		return response

	# waiting for job complete
	logging.debug("data:" + str(data))
	recordsLeft = len(domain_list)
	while recordsLeft > 0:
		time.sleep(args.interval)
		response = session.post(bulkwhois_base_url + 'getRecords',
								headers=header,
								data=json.dumps(data))
		if response.status_code != 200:
			logging.error("wrong response code: %i" % response.status_code)
			exit(1)
		recordsLeft = json.loads(response.text)['recordsLeft']
		logging.debug('Response: ' + response.text)

	data.update({'maxRecords': len(args.domains)})
	# dump json data
	time.sleep(args.interval)
	response = session.post(bulkwhois_base_url + 'getRecords',
							headers=header,
							data=json.dumps(data))
	with open(args.output + '.json','w') as json_file:
		json.dump(json.loads(response.text),json_file)

	# download csv data
	time.sleep(args.interval)
	with open(args.output + '.csv', 'wt') as csv_file:
		response = session.post(bulkwhois_base_url + 'download',
								headers=header,
								data=json.dumps(data))
		for line in response.text.split('\n'):
			clear_line = line.strip()
			# remove blank lines
			if clear_line != '':
				csv_file.write(clear_line + '\n')
################### whois end #####################


def netplan_add_routes(ip,gateway=py.No('auto use first'),
	adapter=py.No('auto use first who has routes'),
	yamlFile=r'/etc/netplan/50-cloud-init.yaml' ):
	''' '''
	U=py.importU()
	F=U.F
	n=F.readYaml(yamlFile)
	for adapterName,v in n['network']['ethernets'].items():
		if ( (not gateway) or (not adapter) ) and 'routes' in v:
			for dipg in v['routes']:
				gateway=dipg['via'] if not gateway else gateway
				adapter=adapterName if not adapter else adapter
				break
	if ('.' not in ip ) or (not gateway) or (not adapter):
		raise py.ArgumentError('please specify ip gateway adapter',ip,gateway,adapter)
	adapterV=n['network']['ethernets'][adapter]
	if 'routes' not in adapterV:
		adapterV['routes']=[]
	routes= adapterV['routes']
			
	for i in routes:
		if ip==i['to']:
			i['via']=gateway
			break
	else:
		routes.insert(0,{'to':ip,'via':gateway } )
		
	# import os;os.system('sudo netplan apply')
	
	return (ip,gateway,adapter,F.writeYaml(yamlFile,n) )
	

def get_ip_from_mac(mac):
	'''mac=='' return all ip
	'''
	U=py.importU()
	T=U.T
	r=U.cmd('arp','-a').splitlines() 
	r=[T.sub(i,'  ', '   ') for i in r if mac in i]
	r=[i for i in r if i]
	if py.len(r)==0:
		return py.No('no ip match mac:{} in arp table!'.format(mac))
	if py.len(r)>1:
		return py.No('more then 1 ip matched mac:{} in arp table!'.format(mac),r)
	if py.len(r)==1:
		return r[0]

def getLAN_IP_HOSTS(ip='192.168.1.{}',count=256):
	import socket
	for i in range(count):
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			s.connect((ip.format(i), 9))
			my_ip = s.getsockname()[0]
			print(my_ip, flush=True)	
	r=getAllAdapter()
	return r

def getAllAdapter():
	U=py.importU()
	if U.iswin():
		from qgb import Win
		return Win.getAllNetworkInterfaces()
getIP=getip=get_ip=getAllAdapter

URL_SCHEME_CHARS=py.No('call N.auto_url will auto set')
def auto_url(a,default_protocol='http',p=0):
	'''According to RFC 2396, Appendix A:
scheme = alpha *( alpha | digit | "+" | "-" | "." )

Scheme names consist(组成) of a sequence of characters beginning with a lower case letter(小写字母开头) and followed by any combination of lower case letters, digits, plus ("+"), period句号 ("."), or hyphen ("-").
'''
	global URL_SCHEME_CHARS
	T=py.importT()
	URL_SCHEME_CHARS=T.alphanumeric+'+.-'
	# r=''
	
	if not py.istr(a):
		raise py.ArgumentError('url need string')
	a=a.strip()
	if  '://' in a:
		 # 放宽一点要求 ?，不检查首位，有时出现全部大写的URL
		for i,c in py.enumerate(a):
			if c not in URL_SCHEME_CHARS:
				if a[i:i+3]=='://':
					break
				else:
					return py.No('url SCHEME invalid',a,i)
					# raise py.ArgumentError('url SCHEME invalid',a,i)
					
		r=a
	elif a.startswith('//'):
		# if 
		r=default_protocol+':'+a
	else:
		r=default_protocol+'://'+a
	if p:print(r)	
	return r

autourl=autoUrl=autoURL=auto_url


#setip 192.168  ,  2.2	
def auto_ip(ip,ip2=py.No('192.168',no_raise=1),ip1=py.No('2',no_raise=1),**ka):
	global U
	U=py.importU()
	ip1=U.get_duplicated_kargs(ka,'ip_1','c','C',default=ip1)
	ip2=U.get_duplicated_kargs(ka,'ip_2','ab','AB','a_b',default=ip2)
	if py.isint(ip2):
		if ip1 or py.isint(ip1):raise py.ArgumentError('ip2 should be a.b format')
		ip1=ip2
		ip2=U.SET_NO_VALUE
	
	
	ip1=U.set_or_get('auto_ip.1',ip1,default=2)
	ip2=U.set_or_get('auto_ip.2',ip2,default='192.168')
	
	if py.istr(ip):
		try:ip=py.float(ip)
		except:			
			try:ip=py.float(ip)
			except:pass
	if py.isint(ip):#TODO check ip_int < 256 ?
		ip='{0}.{1}.{2}'.format(ip2,ip1,ip)
	if py.isfloat(ip):
		ip='{0}.{1}'.format(ip2,ip)		
		
	return ip

def setIP(ip='',adapter='',gateway='',source='dhcp',mask='',ip2=192.168,dns=py.No('auto use gateway') ):
	'''配置的 DNS 服务器不正确或不存在。   # 其实已经设置好了，可以正常使用'''
	U,T,N,F=py.importUTNF()
	if U.islinux():
		import socket,struct,fcntl
		if not py.isbytes(adapter):adapter=adapter.encode('ascii')
		if not py.isbytes(gateway):gateway=gateway.encode('ascii')
		if not py.isbytes(mask)   :mask=mask.encode('ascii')
			
		SIOCSIFADDR = 0x8916
		SIOCSIFNETMASK = 0x891C
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if mask:
			ifreq = struct.pack('16sH2s4s8s', adapter, socket.AF_INET, b'\x00' * 2, 
			socket.inet_aton(mask), b'\x00' * 8)
			fcntl.ioctl(sock, SIOCSIFNETMASK, ifreq)
			
		bin_ip = socket.inet_aton(ip)
		ifreq = struct.pack('16sH2s4s8s', adapter, socket.AF_INET, b'\x00' * 2, bin_ip, b'\x00' * 8)
		return fcntl.ioctl(sock, SIOCSIFADDR, ifreq)
	
	if not adapter:
		#adapter=u'"\u672c\u5730\u8fde\u63a5"'.encode('gb2312')#本地连接
		try:
			adapter=getAllAdapter()[0][0]	#   ( [11,'192.168.1.111',..] , [..] , ..]
		except:	
			if py.is2():adapter="\xb1\xbe\xb5\xd8\xc1\xac\xbd\xd3"
			else:		adapter="本地连接"
		# from qgb import Win
		# if Win.isxp():
			
	if ip:
		source='static'
		ip=N.auto_ip(ip,ip2)	
		
		if not mask:mask='255.255.255.0'
		if not mask.startswith('mask'):mask='mask='+mask
		
		if gateway:
			gateway=N.auto_ip(gateway,ip2)	
		else:
			gateway=T.subLast(ip,'','.')+'.1'
		if not gateway.startswith('gateway'):
			if py.isNo(dns) and 'auto' in dns.msg:
				dns=gateway
			if dns:
				dns=N.auto_ip(dns,ip2)	
				dns='address={}  register=primary'.format(dns)
			gateway='gateway='+gateway
			
		if not ip.startswith('addr'):ip='address='+ip
	else:
		ip=''
	r=[ 'netsh interface ip set address name={0} source={1} {2} {3} {4} '.format(adapter,source,ip,mask,gateway),
		]
	if dns:
		dns='netsh interface ip set dnsservers name={0} source={1} {2}'.format(adapter,source,dns)
		r.append(dns)
	import os
	for i in r:
		os.system(i)
	return r
setip=setIP
def getComputerName():
	import socket
	return socket.gethostname()
gethostname=getHostName=getComputerName

def getArpTable():
	U=py.importU()
	return U.cmd('arp -a')
		
def scanPorts(host,threadsMax=33,from_port=1,to_port=65535,callback=None,ip2=192.168):
	'''return [opens,closes,errors]
	callback(*scanReturns)
	if callback and ports> threadsMax: 剩下结果将异步执行完成
	'''
	U=py.importU()
	from threading import Thread
	import socket
	# host = raw_input('host > ')
	# from_port = input('start scan from port > ')
	# to_port = input('finish scan to port > ')   
	counting_open = []
	counting_close = []
	errors=[]
	threads = []
	if isinstance(host,py.float):host='{0}.{1}'.format(ip2,host)
	
	def scan(port):
		# U.count(1)
		try:
			s = socket.socket()
			result = s.connect_ex((host,port))
			# U.pln('working on port > '+(str(port)))	  
			if result == 0:
				counting_open.append(port)
				#U.pln((str(port))+' -> open') 
				s.close()
			else:
				counting_close.append(port)
				#U.pln((str(port))+' -> close') 
				s.close()
		except Exception as e:
			errors.append({port:e})
	def newThread(port):
		t = Thread(target=scan, args=(i,))		
		threads.append(t)
		try:
			t.start()
		except:
			"can't start new thread"
	im=py.float(to_port-from_port+1)
	percent=0.0
	for i in range(from_port, to_port+1):
		if (i/im>percent):
			U.pln( 'Scanning  %.0f%%' % (percent*100), len(threads)	 )
			percent+=0.01
			
		if len(threads)<=threadsMax:
			newThread(i)
		else:
			for x in threads:
				if x.isAlive():
					x.join()
					newThread(i)
				else:
					threads.remove(x)
				break
	# if callback:
		# return callback
	[x.join() for x in threads]
	return [counting_open,counting_close,errors]
	

if __name__=='__main__':
	rpcServer(currentThread=True)
	exit()
	U.pln( getLAN_IP() )
	exit()
	gsurlip=['http://ip.chinaz.com/getip.aspx'][0]

	s=http(gsurlip)#.encode('utf8').decode('mbcs')

	U.pln( s.decode('utf8').encode('mbcs'))
	# import chardet
	# U.pln( chardet.detect(s)
	
