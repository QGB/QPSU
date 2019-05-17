#coding=utf-8
import sys
if __name__.endswith('qgb.N'):from qgb import py
else:
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
	# import py  #'py': <module 'py' from '..\\py.py'>,

# __all__=['N','HTTPServer']

gError=[]
def setErr(ae):
	py.importU()
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
	else:
		import HTTP
		import HTTPServer
except Exception as ei:
	py.traceback(ei)

	
if py.is3():
	from http.server import SimpleHTTPRequestHandler,HTTPServer as _HTTPServer
else:
	from SimpleHTTPServer import SimpleHTTPRequestHandler
	from BaseHTTPServer import HTTPServer as _HTTPServer
	
def uploadServer(port=1122,host='0.0.0.0',dir='./',url='/up'):
	'''curl  http://127.0.0.1:1122/up -F file=@./U.py
	'''
	U=py.importU()	
	
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
		
def rpcServer(port=23571,thread=True,ip='0.0.0.0',currentThread=False,
	execLocals=None,qpsu=True,importMods='sys,os',request=True):
	
	from threading import Thread
	from http.server import BaseHTTPRequestHandler as h
	import ast
	U=py.importU()
	T=py.importT()
	
	if not execLocals:execLocals={}
		
	for modName in importMods.split(','):
		execLocals[modName]=U.getMod(modName)
	if qpsu:
		for modName in 'py,U,T,N,F'.split(','):
			execLocals[modName]=U.getMod('qgb.'+modName)	
	
	
	def execResult(source, globals=None, locals=None):
		'''exec('r=xx') ;return r # this has been tested in 2&3
		当没有定义 r 变量时，自动使用 最后一次 出现的值 作为r
		当定义了 r ，但不是最后一行，这可能是因为 还有一些收尾工作
		'''
		if globals==None:
			globals={}
		if locals==None:#因为参数不是 不可变对象，且在接下来会改变
			locals ={}
		# U.log(locals)
		# body=ast.parse(code).body
		# r_lineno=0
		# for i,b in py.reversed(py.list( enumerate(body) )  ): # 从最后一条语句开始解析，序号还是原来的
			# if isinstance(b, ast.Assign):
				# if b.targets[0].id=='r':
					# r_lineno=i
					# break# r之前的就不管了
			# ''' [ 可能在r 之后 还有表达式 或者 根本没有出现 r ，Expr 都看成 r '''
			# if isinstance(b, ast.Expr):
				# Assign
				
		try:
			exec(source, globals, locals)
		except Exception as e:
			return py.repr(e)
			
		if 'r' in locals:
			try:return U.pformat(locals['r'] )
			except:return py.repr(  locals['r']  )
		else:
			return 'can not found "r" variable after exec locals'+T.pformat(locals)
	
	from flask import Flask,make_response
	from flask import request as _request
	
	app=Flask('rpcServer'+U.stime_()   )
	@app.errorhandler(404)
	def flaskEval(e):
		code=T.urlDecode(_request.url)
		code=T.sub(code,':{}/'.format(port) )
		U.log( ('\n'+code) if '\n' in code else code	)
		# U.ipyEmbed()()
		if request:
			execLocals['request']=_request
		r=make_response( execResult(code,locals=execLocals) )
		r.headers['Access-Control-Allow-Origin'] = '*'
		r.headers['Content-Type'] = 'text/plain;charset=utf-8'
		return r
	
	flaskArgs=py.dict(host=ip,port=port,debug=0,threaded=True)
	if currentThread or not thread:
		return app.run(**flaskArgs)
	else:
		t= Thread(target=app.run,name='qgb thread '+app.name,kwargs=flaskArgs)
		t.start()
		return (t,app)
		
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
	
	
def get(url,protocol='http',file=''):
	py.importU()
	T=U.T
	if '://' in url:
		p=T.sub(url,'',':')
		if p:protocol=p
		else:raise U.ArgsErr(url)
	else:url=protocol+'://'+url
	if url.startswith('http'):
		# import HTTP
		return HTTP.get(url,file=file)	
	raise U.NotImplementedError
	return U.getAllMods()

def http(url,method='get',*args):
	return HTTP.method(url,method,*args)


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

#setip 192.168  ,  2.2	
def setIP(ip='',adapter='',gateway='',source='dhcp',mask='',ip2=192.168,dns=py.No('gateway') ):
	'''配置的 DNS 服务器不正确或不存在。   # 其实已经设置好了，可以正常使用'''
	U=py.importU()
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
		if type(ip) is py.int:
			ip='{0}.2.{1}'.format(ip2,ip)
		if type(ip) is py.float:
			ip='{0}.{1}'.format(ip2,ip)		
		
		if not mask:mask='255.255.255.0'
		if not mask.startswith('mask'):mask='mask='+mask
		
		if not gateway:
			T=py.importT()
			gateway=T.subLast(ip,'','.')+'.1'
		if not gateway.startswith('gateway'):
			if not dns:
				dns=gateway
			dns='address={}  register=primary'.format(dns)
			gateway='gateway='+gateway
			
		if not ip.startswith('addr'):ip='address='+ip
	else:
		ip=''
	r=[ 'netsh interface ip set address name={0} source={1} {2} {3} {4} '.format(adapter,source,ip,mask,gateway),
		'netsh interface ip set dnsservers name={0} source={1} {2}'.format(adapter,source,dns)
		]
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
	py.importU()
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
			U.pln( 'Scanning  %.0f%%' % (percent*100), len(threads)     )
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
	
	
	rpcServer()
	exit()
	U.pln( getLAN_IP())
	exit()
	gsurlip=['http://ip.chinaz.com/getip.aspx'][0]
	
	
	s=http(gsurlip)#.encode('utf8').decode('mbcs')
		 
		 
	U.pln( s.decode('utf8').encode('mbcs'))
	# import chardet
	# U.pln( chardet.detect(s)
	
