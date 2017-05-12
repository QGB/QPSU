import BaseHTTPServer
import logging
import os
from urlparse import urlparse,parse_qs
from mimetypes import types_map

register_route = {"GET":{},"POST":{}}
def route(path="/", method=["GET"],h=True):
	def decorator(f):
		for m in method:
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
handler_method = {}
def override(method=None):
	def decorator(f):
		handler_method[method] = f
		return f
	return decorator

class extended_BaseHTTPServer(BaseHTTPServer.BaseHTTPRequestHandler):
	def log_message(self, format, *args):
		return ""
		
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()

	def do_POST(s):
		o = urlparse(s.path)
		length = int(s.headers['Content-Length'])
		arguments = parse_qs(s.rfile.read(length).decode('utf-8'))
		s.do_routing(o, arguments, "POST")

	def do_GET(s):
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
					if "404" not in handler_method:
						build_response(s, "404 - Not Found", 404)
					else:
						retour = handler_method['404'](o, arguments, action)
						build_response(s, retour, 404)
		except Exception as eh:
			# Gestion des erreurs
			if "500" not in handler_method:
				s.send_response(500)
				s.send_header("Content-type", "text/plain")
				s.end_headers()
				import traceback
				s.wfile.write("Internal Server Error \n%s"%traceback.format_exc())
				# build_response(s, , 500)
			else:
				retour = handler_method['500'](o, arguments, action)
				build_response(s, retour, 500)


def build_response(output, retour, code=200):
	if type(retour) is dict:
		output.send_response(retour.get("code",code))
		for header in retour:
			if header not in ["code","content"]:
				output.send_header(header, retour[header])
		output.end_headers()
		output.wfile.write(retour['content'])
	else:
		output.send_response(code)
		output.send_header("Content-type", "text/html")
		output.end_headers()
		output.wfile.write(retour)


def redirect(location=""):
	return {"content":"","code":301,"Location":location}

def serve(ip="0.0.0.0", port=80):
	httpd = BaseHTTPServer.HTTPServer((ip, port), extended_BaseHTTPServer)
	try:
		from threading import Thread
		Thread(target=httpd.serve_forever).start()
		input('{0}:{1}'.format(ip,port))
	except:
		pass
	httpd.server_close()
server=serve

if __name__=='__main__':
	serve()