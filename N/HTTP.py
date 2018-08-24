
#coding=utf-8
from __future__ import absolute_import
if __name__.endswith('HTTP'):from . import py
else:import py

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

	return

def get(url):
	# return method(url,'get')#<http.client.HTTPResponse at 0x203a16a74a8>
	url=autoUrl(url)
	try:
		return grequest.urlopen(url).read()
	except Exception as e:
		return url,e
	
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