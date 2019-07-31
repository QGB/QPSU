import sys
if sys.platform=='win32':
	'qgb.U' in sys.modules or sys.path.append('E:/QGB/babun/cygwin/bin/');
if sys.platform=='linux':
	'qgb.U' in sys.modules or sys.path.append('/home/qgb/');
import qgb.N.DjangoMiddleware

from qgb import U,T,N,F,py

from django.shortcuts import HttpResponse   
		
class Log:
	def __init__(self, get_response):
		self.get_response = get_response
		# One-time configuration and initialization.
		self.g={'sys':sys,
				'py':py, 'U':U, 'T':T, 'N':N, 'F':F}
	def __call__(self, request):
		q=request.META['QUERY_STRING']
		q=('?'+q) if q else ''
		url=request.path+q
		try:
			# if not U.DEBUG:raise Exception(request._stream.stream)
			if U.isWin():
				ip,port=request._stream.stream.raw._sock.getpeername()
			if U.isLinux():
				ip,port=request._stream.stream.stream.raw._sock.getpeername()
				
			ip=N.ip_location(ip,reverse_ip=True)
			
			log_obj={
			'url': url,
			'ua': request.environ['HTTP_USER_AGENT'],
			'data':request.body,
			'ip':ip,
			'port':port,
			
			}
			self.s=log_obj
			F.write('log/8000/'+U.stime(),U.pformat(log_obj))
		except Exception as e:
			self.e=e
			F.write('log/8000/e'+U.stime(),U.pformat(e))
			
		if url.startswith('/#rpc\n'):
			self.g['self']=self #test?
			
			request.url=url
			self.g['q']=request
			
			response = HttpResponse()
			response['content-type'] = 'text/plain; charset=utf-8'
			response['X-XSS-Protection']='0'
			response['Access-Control-Allow-Origin'] = '*'
			self.g['p']=response
			
			r=U.execStrResult(url[1:],globals=self.g)
			if not response.content:
				response.content=r
			return response

		# Code to be executed for each request before
		# the view (and later middleware) are called.
		response = self.get_response(request)
		# Code to be executed for each request/response after
		# the view is called.
		return response