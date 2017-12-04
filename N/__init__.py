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
	if not adapter:
		#adapter=u'"\u672c\u5730\u8fde\u63a5"'.encode('gb2312')#本地连接
		adapter='1'
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
		
def scanPorts(host,from_port=1,to_port=65535,threadsMax=33,callback=None):
	'''return [opens,closes,errors]
	callback(*scanReturns)
	if callback and ports> threadsMax: 剩下结果将异步执行完成
	'''
	from threading import Thread
	import socket
	# host = raw_input('host > ')
	# from_port = input('start scan from port > ')
	# to_port = input('finish scan to port > ')   
	counting_open = []
	counting_close = []
	errors=[]
	threads = []

	def scan(port):
		try:
			s = socket.socket()
			result = s.connect_ex((host,port))
			# print('working on port > '+(str(port)))      
			if result == 0:
				counting_open.append(port)
				#print((str(port))+' -> open') 
				s.close()
			else:
				counting_close.append(port)
				#print((str(port))+' -> close') 
				s.close()
		except Exception as e:
			errors.append({port:e})
	def newThread(port):
		t = Thread(target=scan, args=(i,))		
		threads.append(t)
		t.start()
			
	for i in range(from_port, to_port+1):
		if len(threads)<=threadsMax:
			newThread(i)
		else:
			for x in threads:
				if x.isAlive():
					x.join()
					newThread(i)
					break
	# if callback:
		# return callback
	[x.join() for x in threads]
	return [counting_open,counting_close,errors]
	
if __name__=='__main__':
	print getLAN_IP()
	exit()
	gsurlip=['http://ip.chinaz.com/getip.aspx'][0]
	
	
	s=http(gsurlip)#.encode('utf8').decode('mbcs')
		 
		 
	print s.decode('utf8').encode('mbcs')
	# import chardet
	# print chardet.detect(s)
	
