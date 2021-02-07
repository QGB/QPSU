#coding=utf-8
import sys #endswith 是为了适配qgb处于另外一个包内的情况
if __name__.endswith('qgb.N.HTTP'):from .. import py
else:
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py

if py.is2():
	import urllib2 as urllib
	grequest = urllib.Request
	grequest.urlopen=urllib.urlopen
else:
	import urllib
	from urllib import request#  加了这句才不会 AttributeError: module 'urllib' has no attribute 'request
	try:
		grequest = urllib.request.Request
		grequest.urlopen=urllib.request.urlopen		
	except Exception as ei:
		print(urllib,ei)
		py.importU().repl()

def post(url,**ka):
	'''
Signature: requests.post(url, data=None, json=None, **kwargs)
Docstring:
Sends a POST request.

:param url: URL for the new :class:`Request` object.
:param data: (optional) Dictionary (will be form-encoded), bytes, or file-like object to send in the body of the :class:`Request`.
:param json: (optional) json data to send in the body of the :class:`Request`.
:param \*\*kwargs: Optional arguments that ``request`` takes.
:return: :class:`Response <Response>` object
:rtype: requests.Response
File:      e:\qgb\anaconda3\lib\site-packages\requests\api.py
Type:      function
'''	
	U,T,N,F=py.importUTNF()

	url=N.auto_url(url)
	proxies=U.get_duplicated_kargs(ka,'proxies','proxy')
	if proxies:
		proxies=N.set_proxy(proxy)
	else:
		proxies=N.get_proxy()
	ka['proxies']=proxies
	
	import requests
	return requests.post(url,**ka)

def get_str(url,**ka ,):
	T=py.importT()
	return T.auto_decode(  get_bytes(url,**ka)  )
gets=getStr=get_str

def get_bytes(url,	**ka ,):
	U,T,N,F=py.importUTNF()

	url=N.auto_url(url)
	proxies=U.get_duplicated_kargs(ka,'proxies','proxy')
	if proxies:
		proxies=N.set_proxy(proxy)
	else:
		proxies=N.get_proxy()
	ka['proxies']=proxies

	import requests
	try:
		return requests.get(url,**ka).content
	except Exception as e:
		return py.No(e)
getb=getByte=getBytes=get_byte=get_bytes

gheaders=headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.2171.95 Safari/537.36'}

def random_headers():
	import fake_headers
	return fake_headers.Headers( headers=fake_headers.make_header() ).generate()
	
def get(url,file='',
		headers = gheaders,
		timeout=9,
		**ka ,
	):
	U,T,N,F=py.importUTNF()
	url=N.auto_url(url)

	proxies=U.get_duplicated_kargs(ka,'proxies','proxys','proxyes','proxy')
	if proxies:
		proxies=N.set_proxy(proxies)
	else:
		proxies=N.get_proxy()


	def writeFile():
		if file:
			U=py.importU()
			content=r.content
			if content:
				return U.F.write(file,content)
			else:
				return py.No('response.content is Null!')
			
	b=b''
	try:
		import requests
		r=requests.get(url,verify=False,timeout=timeout,headers=headers,proxies=proxies)
		if 'text' in U.getDictV(r.headers,'Content-Type').lower():
			return T.autoDecode(r.content)
			# try:return r.content.decode('gb18030')
			# except:pass
			# return r.text
		else:
			b= r.content
			
	except ModuleNotFoundError:
		try:
			b=grequest.urlopen(url).read()
		except Exception as e:
			return py.No(url,e)
		#####################
	except Exception as e:
		return py.No(e)

	try:
		s= T.auto_decode(b)
		if not s and b:raise Exception('decode error')
		return s
	except:
		return b
	

def head(url):
	return method(url,'head').info().items()
	
def options(url):
	return dict(method(url,'options').info().items() )['allow']

		
def method(url,amethod='get',*args):
	r'''#TODO: post etc need args'''
	U,T,N,F=py.importUTNF()
	try:
		url=N.auto_url(url)
		request = grequest(url)
		request.get_method = lambda : amethod.upper()
		response = grequest.urlopen(request)
		return response
	# except urllib2.HTTPError as eh:
		# setError(eh)
	except Exception as e:
		setErr(e)
gError=None
def setErr(a):
	global gError
	gError=a
	raise a#[eh.msg,eh.headers.items(),eh]