import urllib2


def autoUrl(a):
	if type(a)==type(''):
		if a.startswith('http') and '://' in a:return a
		if a[0] in T.alphanumeric:return 'http://'+a

def http(aurl):
	aurl=autoUrl(aurl)
	return urllib2.urlopen(aurl).read()
	print 233
	
def findFunc(name,root=9,depth=3,case=False):
	print dir(root)
	print '='*44
	print globals().keys()
	print '='*44
	print locals().keys()
	print '='*44
	print vars().keys()
	exit()
# findFunc('set*')		
	


def getIP(type='local'):
	import inspect
	a = inspect.getargspec(getIP)
	print a.defaults
	# for i 
if __name__=='__main__':
	print getIP()
	exit()
	gsurlip=['http://ip.chinaz.com/getip.aspx'][0]
	
	
	s=http(gsurlip)#.encode('utf8').decode('mbcs')
		 
		 
	print s.decode('utf8').encode('mbcs')
	# import chardet
	# print chardet.detect(s)
	
