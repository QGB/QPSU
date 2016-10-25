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
	
def backLocals(f=None,i=0,r=[]):
	print i+1,'='*(20+i*2)
	
	if f is None and i==0:f=__import__('sys')._getframe()
	try:print f.f_locals.keys();r.append(f.f_locals)
	except:return r

	return backLocals(f.f_back,i+1,r)	
	
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
	
