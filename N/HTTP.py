#coding=utf-8
import urllib2

def post(url,data):

	return

def get(url):
	url=autoUrl(url)
	return urllib2.urlopen(url).read()
	
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
'''not return String
HTTP«Î«Û∑Ω∑®
OPTIONS GET HEAD POST PUT DELETE TRACE CONNECT PATCH
https://zh.wikipedia.org/wiki/%E8%B6%85%E6%96%87%E6%9C%AC%E4%BC%A0%E8%BE%93%E5%8D%8F%E8%AE%AE#.E8.AF.B7.E6.B1.82.E6.96.B9.E6.B3.95
'''
def method(url,amethod='get'):
	try:
		url=autoUrl(url)
		request = urllib2.Request(url)
		request.get_method = lambda : amethod.upper()
		response = urllib2.urlopen(request)
		return response
	# except urllib2.HTTPError as eh:
		# setError(eh)
	except Exception as e:
		setError(e)
gError=None
def setError(a):
	global gError
	gError=a
	raise a#[eh.msg,eh.headers.items(),eh]