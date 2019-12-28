#coding=utf-8
import os,sys
if __name__.endswith('qgb.N.HTTPServer'):from .. import py
else:
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
U=py.importU()

	
if py.is2():
	from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
	from urlparse import urlparse,parse_qs
else:
	from http.server import BaseHTTPRequestHandler,HTTPServer
	from urllib.parse import urlparse,parse_qs
import logging
# from qgb import *#循环import
def forwardReq(a):
	url_path = urlparse(a.path).path
	if url_path == '/0':
		import webControl
		webControl.forwardReq(a)
	
	return a.send_not_found()

register_route = {"GET":{},"POST":{}}
def route(path="/", method=["GET"],h=True,args=True):
	if not args:h=False
	if py.istr(method):
		method=method.upper()
		if method in register_route:
			method=[method]
		else:raise Exception('unsupported method:'+method)
	
	
	def decorator(f):
		for m in method:
			m=m.upper()
			try:
				if h:
					register_route[m][path] = f
				else:
					def wrap(handler,*a,**ka):return f(*a,**ka)
					register_route[m][path]=wrap#lambda handler:f()		
			except:
				logging.error("{0} method is not available.".format(m))
		return f
	return decorator
router=route
handler_method = {}#404,500,static
def override(method=None):
	def decorator(f):
		handler_method[method] = f
		return f
	return decorator

class Handler(BaseHTTPRequestHandler):
	server_version = __name__#'qgb.N.HTTPServer'
	# def log_message(self, format, *args):
		# return ""
		
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()

	def do_POST(s):
		o = urlparse(s.path)
		arguments = parse_qs(o.query)
		length = int(s.headers['Content-Length'])
		s.postData = s.rfile.read(length)
		
		# parse_qs(s.rfile.read(length).decode('utf-8'))
		s.do_routing(o, arguments, "POST")

	def do_GET(s):
		# raise Exception(233333)             
		o = urlparse(s.path)
		arguments = parse_qs(o.query)
		s.do_routing(o, arguments, "GET")
	
	def do_routing(s, o, arguments, action):
		try:
			if o.path in register_route[action]:
				retour = register_route[action][o.path](s,**arguments)
				build_response(s, retour, 200)
			else:
				# Fichier static ?
				try:
					if "static" in handler_method:
						retour = handler_method['static'](o, arguments, action)
						build_response(s, retour, 200)
					else:
						with open(os.path.join("."+o.path)) as f:
							fname,ext = os.path.splitext(o.path)
							ctype = "text/plain"
							if ext in types_map:
								ctype = types_map[ext]
							build_response(s, {'Content-type':ctype,"content":f.read()}, 200)
				except Exception as e:
					# Url introuvale et fichier static introuvable ==> 404
					if 404 not in handler_method:
						build_error(s,e, 404)
					else:
						retour = handler_method[404](o, arguments, action)
						build_response(s, retour, 404)
		except Exception as eh:
			# Gestion des erreurs
			py.traceback(eh)
			if "500" not in handler_method:
				build_error(s,eh,500,'500 [not in handler_method,use @override("500") ]')

				
				# build_response(s, , 500)
			else:
				retour = handler_method[500](o, arguments, action)
				build_response(s, retour, 500)

def build_error(s,e,code,msg=''):
	# if not U.count():U.repl()
	s.send_response(code)
	s.send_header("Content-type", "text/plain")
	s.end_headers()
	if not msg:
		msg="HTTP Status:{2}\n{0} \n{1}".format(e,'traceback.format_exc()',code)  	
	if py.is3():#\lib\socketserver.py", line 775, in write  TypeError: a bytes-like object is required, not 'str'
		msg=msg.encode(U.encoding)
	s.wfile.write(msg)
	return s.finish()	
		
	s.send_response(code,msg)
	# try:raise e
	# except:# 只追踪到raise的地方，弃用
	# import traceback
	# s.wfile.write("{0} \n{1}".format(msg,traceback.format_exc())  )
		
def build_response(s, retour, code=200):
	if type(retour) is dict:
		s.send_response(retour.get("code",code))
		for header in retour:
			if header not in ["code","content"]:
				s.send_header(header, retour[header])
		s.end_headers()
		r=retour['content']
	else:
		s.send_response(code)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		r=retour
	if py.is3():r=r.encode(U.encoding)
	s.wfile.write(r)
	s.finish()
	# U.repl(	)
	# finish_request(s, s,s.client_address)

def redirect(location=""):
	return {"content":"","code":301,"Location":location}
#error: [Errno 10053]  浏览器关闭 了这个连接
def http(ip="0.0.0.0", port=80,log=True,onMainThread=False):
	httpd = HTTPServer((ip, port), Handler)
	try:
		if onMainThread:
			print('{0}:{1}\n'.format(ip,port))
			httpd.serve_forever()
		else:
			from threading import Thread
			Thread(target=httpd.serve_forever).start()
			input('{0}:{1}\n'.format(ip,port))
	except:
		pass
	httpd.server_close()#TODO: muti thread
serve=httpd=server=http

def https(ip="0.0.0.0", port=443,key='',log=True,onMainThread=False):
	try:
		httpd = HTTPServer((ip, port), Handler)
	except Exception as e:
		return (ip,port,e)
	if not key:
		U=py.importU()
		key=U.getModPath()+'N/.tmall.com.crt'#lk.lk.crt'
	import ssl
	httpd.socket=ssl.wrap_socket( httpd.socket, keyfile=key,  certfile=key)
	
	try:
		if onMainThread:
			print('{0}:{1}\n'.format(ip,port))
			httpd.serve_forever()
		else:
			from threading import Thread
			Thread(target=httpd.serve_forever).start()
			input('{0}:{1}\n'.format(ip,port))
	except BaseException as e:
		py.traceback(e)
		# py.pdb()
	httpd.server_close()
httpsd=https

def main(port=443,crt='N/CA.crt' ,onMainThread=True):
	import sys
	
	# try:U=sys.modules['qgb.U']
	# except:
		# sys.path[0]=sys.path[0][:-5]
		# U.pln( sys.path)
		# from qgb import U
	U=py.importU()	
	@route('/',['get','post'])
	def data(h,**ka):
		h.send_response(200)
		h.send_header("Content-type", "text/plain")
		h.send_header('Access-Control-Allow-Origin', '*')
		h.end_headers()
		
		if 'postData' in dir(h):
			ka=h.postData
		else:
			# U.pln(ka,file=h.wfile) #>>h.wfile,ka
			# ka=list(ka)
			ka['h.wfile']=h.wfile
		U.set(ka)
			
		h.finish()
		U.set('h',h)
		return  ka
	ca=U.getModPath()+crt
	return https(key=ca,port=port,onMainThread=onMainThread)
__doc__='''
@route()
def h(h):
    U.set(h)

'user-agent' in h.headers.dict 


'''
if __name__=='__main__':
	main()
	
'''127.0.0.1 - - [11/May/2018 03:56:40] "GET /323 HTTP/1.1" 404 -
127.0.0.1 - - [11/May/2018 03:56:40] "GET /323 HTTP/1.1" 500 -
----------------------------------------
Exception happened during processing of request from ('127.0.0.1', 55009)
Traceback (most recent call last):
  File "G:\QGB\Anaconda2\lib\SocketServer.py", line 290, in _handle_request_noblock
    self.process_request(request, client_address)
  File "G:\QGB\Anaconda2\lib\SocketServer.py", line 318, in process_request
    self.finish_request(request, client_address)
  File "G:\QGB\Anaconda2\lib\SocketServer.py", line 331, in finish_request
    self.RequestHandlerClass(request, client_address, self)
  File "G:\QGB\Anaconda2\lib\SocketServer.py", line 654, in __init__
    self.finish()
  File "G:\QGB\Anaconda2\lib\SocketServer.py", line 713, in finish
    self.wfile.close()
  File "G:\QGB\Anaconda2\lib\socket.py", line 286, in close
    self._sock.close()
AttributeError: 'NoneType' object has no attribute 'close'


'''