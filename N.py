import urllib2


def autoUrl(a):
	if type(a)==type(''):
		if a.startswith('http') and '://' in a:return a
		if a[0] in T.alphanumeric:return 'http://'+a

def http(aurl):
	aurl=autoUrl(aurl)
	return urllib2.urlopen(aurl).read()
	print 233