# coding=utf-8
from ctypes import windll#.user32.MessageBoxA as m
u=windll.user32
msgbox=windll.user32.MessageBoxA
import  os,sys,socket

from threading import *
#m(0, 'rtegwf', 'hi', 0)
#print 
'''
from qgb import U,T
'''
BDEBUG=True

SG_EXIT='exit'
SG_ASK='ask'

def __single(port,callback,reply):
	sock=None
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
	sock.bind(('0.0.0.0', port))
	sock.listen(5) 
	while True:    
		connection,address = sock.accept()    
		try:    
			connection.settimeout(50)
			buf=''
			while buf!=None:  
				buf = connection.recv(4096) 
				if(reply!=None):connection.send(reply+buf)
				Thread(target=callback,args=[buf]).start()
		except Exception as e:  #如果建立连接后，该连接在设定的时间内无数据发来，则time out  
			 if(BDEBUG):print e  
			 continue
	connection.close()   

def isingle(port,ip='127.0.0.1'):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
		sock.connect((ip, port))
		sock.send(SG_ASK)    
		sock.close()
		return False
	except Exception:
		return True
def single(port,callback,reply='\naccepted:'):
	Thread(target=__single,args=[port,callback,reply]).start()

import inspect
def fields(obj):
	return inspect.getmembers(obj)

def methods(obj):
	return dir(obj)

def msgbox(s='',st='title',*a):
	if(a!=()):s=str(s)+ ','+str(a)[1:-2]
	u.MessageBoxA(0, str(s), str(st), 0)

def pln(*a):
	print a
	sys.stdout.flush()

	
def p(*a):
	if(len(a)<1):return
	for i in a:
		sys.stdout.write(str(i)+' ')
	sys.stdout.flush()

	
def x(msg=None):
	if(msg!=None):print msg
	exit(235)
	
def exit(i=2357):
	os._exit(i)


