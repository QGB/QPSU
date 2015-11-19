# coding=utf-8
from ctypes import windll, Structure, c_ulong, byref
u=windll.user32
msgbox=windll.user32.MessageBoxA
import  os,sys,socket

from threading import *

#m(0, 'rtegwf', 'hi', 0)
#print 
'''
from qgb import U,T
# '''
# if __calltimes=0
BDEBUG=True
__stdout=None



def setOut(afileName):
	__stdout,sys.stdout=sys.stdout,open(afileName,'w+')


def resetOut():
	# msgbox(__stdout)
	if(__stdout != None and __stdout != sys.stdout):
		sys.stdout.close()
		# sys.stdout=__stdout
txthtml=('<textarea style="width:100%; height:100%;">','</textarea>')	

def browser(url):
	os.system('''start "" '''+str(url))
def shtml(file,txt,browser=True):
	f=open(file,'w+')
	txt=txt.replace(txthtml[1],txthtml[1][:1]+'!!!qgb-padding!!!'+txthtml[1][1:])	
	f.write(txthtml[0]+txt+txthtml[1])
	f.close()
	globals()['browser'](f.name)
def dicthtml(file,dict,aikeylength=10,browser=True):
	for i in dict.keys():
		if(len(i)>aikeylength):aikeylength=len(i)+1
	sformat='%-'+str(aikeylength)+'s:'
	txt=''
	for i in dict.keys():
		txt+= (sformat%i)+str(dict[i])+'\n'
	txt=txt.replace(txthtml[1],txthtml[1][:1]+'!!!qgb-padding!!!'+txthtml[1][1:])	
	f=open(file,'w+')
	f.write(txthtml[0]+txt+txthtml[1])
	f.close()
	globals()['browser'](f.name)
	# print vars()
	# vars()['browser'](f.name)

# dicthtml('uvars.html',vars())
	

	
def getThreads():
	r=()
	for threadId, stack in sys._current_frames().items():
		r+=(threadId,)
	return r
	

def getCursorPos():
	class POINT(Structure):
		_fields_ = [("x", c_ulong), ("y", c_ulong)]
	pt = POINT()
	windll.user32.GetCursorPos(byref(pt))
	return pt.x,pt.y



SG_EXIT='exit'
SG_ASK='ask'
__bsg=False
def __single(port,callback,reply):
	__bsg=True
	sock=None
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	sock.bind(('0.0.0.0', port))
	sock.listen(5) 
	while True:	
		if(not __bsg):break
		connection,address = sock.accept()	
		try:	
			connection.settimeout(50)
			buf=''
			while buf!=None:
				
				buf = connection.recv(4096) 
				if(reply!=None):connection.send(reply+buf)
				Thread(target=callback,args=[buf]).start()
				# msgbox(buf)
		except Exception as e:  #如果建立连接后，该连接在设定的时间内无数据发来，则time out  
			# if(str(e)!='[Errno 10053] '):
			if(BDEBUG):print e ,'#%s#'%str(e) 
			continue
	connection.close()   

def notsingle(port,ip='127.0.0.1'):
	try: 
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
		sock.connect((ip, port))
		sock.send(SG_ASK)	
		sock.close()
		return True
	except Exception:
		return False 
def single(port,callback,reply='\naccepted:'):
	'''singleton'''
	Thread(target=__single,args=[port,callback,reply]).start()
	
def singlexit():
	pass
	
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
	if(len(a)<1):
		sys.stdout.flush()
		return
	for i in a:
		sys.stdout.write(str(i)+' ')
	sys.stdout.flush()

	
def x(msg=None):
	if(msg!=None):print msg
	exit(235)
	
def exit(i=2357):
	os._exit(i)


