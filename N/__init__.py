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

def getAllAdapter():
	
	return r
	
def setIP(ip='',source='dhcp',adapter='',mask=''):
	if not adapter:adapter=u'"\u672c\u5730\u8fde\u63a5 2"'.encode('gb2312')
	if ip:
		source='static'
		if not ip.startswith('addr='):
			ip='addr='+ip
		if not mask:mask='mask='+'255.255.255.0'
		elif not mask.startswith('mask'):mask='mask='+mask
		
	import os
	os.system('netsh interface ip  set address name={0} source={1} {2} {3}'.format(adapter,source,ip,mask))
setip=setIP
		
if __name__=='__main__':
	print getIP()
	exit()
	gsurlip=['http://ip.chinaz.com/getip.aspx'][0]
	
	
	s=http(gsurlip)#.encode('utf8').decode('mbcs')
		 
		 
	print s.decode('utf8').encode('mbcs')
	# import chardet
	# print chardet.detect(s)
	
