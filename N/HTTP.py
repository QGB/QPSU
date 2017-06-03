#coding=utf-8
import urllib2

def autoUrl(a):
	if type(a)==type(''):
		if  '://' in a[1:10]:return a
		else:return 'http://'+a

def get(aurl):
	aurl=autoUrl(aurl)
	return urllib2.urlopen(aurl).read()
	
def head(aurl):
	return method(aurl,'head').info().items()
	
'''not return String
HTTP«Î«Û∑Ω∑®
OPTIONS GET HEAD POST PUT DELETE TRACE CONNECT PATCH
https://zh.wikipedia.org/wiki/%E8%B6%85%E6%96%87%E6%9C%AC%E4%BC%A0%E8%BE%93%E5%8D%8F%E8%AE%AE#.E8.AF.B7.E6.B1.82.E6.96.B9.E6.B3.95
'''
def method(aurl,amethod='get'):
	aurl=autoUrl(aurl)
	request = urllib2.Request(aurl)
	request.get_method = lambda : amethod.upper()

	response = urllib2.urlopen(request)
	return response