#coding=utf-8
import sys
if __name__.endswith('qgb.N.HTTP'):from qgb import py
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

def post(url,data):
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
	import requests
	return requests.post(url,data=data)
	
def getBytes(url):
	url=autoUrl(url)
	import requests
	try:
		return requests.get(url).content
	except Exception as e:
		return py.No(e)
	
def get(url,file='',
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.2171.95 Safari/537.36'},
		timeout=9
	):
	# return method(url,'get')#<http.client.HTTPResponse at 0x203a16a74a8>
	url=autoUrl(url)
	U=py.importU()
	def writeFile():
		if file:
			U=py.importU()
			content=r.content
			if content:
				return U.F.write(file,content)
			else:
				return py.No('response.content is Null!')
			
	
	try:
		import requests
		r=requests.get(url,headers=headers,verify=False,timeout=timeout)
		if 'text' in U.getDictV(r.headers,'Content-Type'):
			try:return r.content.decode('gb18030')
			except:pass
			return r.text
		else:
			return r.content
	except ModuleNotFoundError:
		try:
			r=grequest.urlopen(url).read()
		except Exception as e:
			return py.No(url,e)
		#####################
	except Exception as e:
		return py.No(e)


def head(url):
	return method(url,'head').info().items()
	
def options(url):
	return dict(method(url,'options').info().items() )['allow']

def autoUrl(a):
	if type(a)==type(''):
		if  '://' in a[1:10]:return a
		else:return 'http://'+a
	else:
		raise Exception('url need string')

def method(url,amethod='get',*args):
	r'''#TODO: post etc need args'''
	try:
		url=autoUrl(url)
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