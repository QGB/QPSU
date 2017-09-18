#coding=utf-8
# __all__=['N','HTTPServer']
import sys
if 'qgb.U' in sys.modules:U=sys.modules['qgb.U']
elif 'U' in sys.modules:  U=sys.modules['U']
else:
	from sys import path as _p
	_p.insert(-1,_p[0][:-1-1-3-1]) # python2.7\\qgb\\N
	from qgb import U
	if U.iswin():from qgb import Win
gError=[]
def setErr(ae):
	global gError
	if U.gbLogErr:# U.
		if type(gError) is list:gError.append(ae)
		elif gError:gError=[gError,ae]
		else:gError=[ae]
	else:
		gError=ae
	if U.gbPrintErr:print '#Error ',ae# U.
	
	
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
	


def getLAN_IP():
	r=getAllAdapter()
	return r

def getAllAdapter():
	if U.iswin():
		from qgb import Win
		return Win.getAllNetworkInterfaces()
	
def setIP(ip='',source='dhcp',adapter='',mask=''):
	if not adapter:adapter=u'"\u672c\u5730\u8fde\u63a5"'.encode('gb2312')#本地连接
	if ip:
		source='static'
		if not ip.startswith('addr='):
			ip='addr='+ip
		if not mask:mask='mask='+'255.255.255.0'
		
		if not mask.startswith('mask'):mask='mask='+mask
	r='netsh interface ip  set address name={0} source={1} {2} {3}'.format(adapter,source,ip,mask)
	import os
	os.system(r)
	return r
setip=setIP
		
if __name__=='__main__':
	print getLAN_IP()
	exit()
	gsurlip=['http://ip.chinaz.com/getip.aspx'][0]
	
	
	s=http(gsurlip)#.encode('utf8').decode('mbcs')
		 
		 
	print s.decode('utf8').encode('mbcs')
	# import chardet
	# print chardet.detect(s)
	
