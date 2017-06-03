#coding=utf-8
# __all__=['N','HTTPServer']

import HTTPServer
import HTTP
	
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
	
