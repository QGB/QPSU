# coding=utf-8
from ctypes import windll, Structure, c_ulong, byref
u=windll.user32
msgbox=windll.user32.MessageBoxA
import  os,sys,socket
from pprint import pprint
from threading import *


gsImport='''
from qgb import U,T
'''

def sortDictV(ad,des=True):
	'''des True,,, python dict key auto sort ?'''
	if type(ad)!=type({}):return {}
	return sorted(ad.iteritems(),key=lambda ad:ad[1],reverse=True)
# d={}
# for i in range(7):
	# d[i]=i*i-5*i
	
# d={'ok':1,'no':2}
# d={0: 0, 5: 0, 6: 6, 1: -4, 2: -6, 3: -6, 4: -4}
# print d
# d=sortDictV(d)
# print d ,type(d)
# exit()

def read(a,mod='r'):
	f=open(a,mod)
	s=f.read()
	f.close()
	return s

def write(a,data,mod='wb'):
	f=open(a,mod)
	f.write(data)
	f.close()


def mkdir(afn):
	if sys.platform == "win32":
		os.system('md '+afn)
md=mkdir

def eval(s):
	exec(s)

def calltimes(): 
	ff=calltimes
	if ff.__dict__.has_key("count"): 
		ff.count += 1 
	else: 
		ff.count = 0 #Do Not Modify
	# print ff.count 
	return ff.count 
ct=calltimes

if(calltimes()<1):BDEBUG=True;__stdout=None
debug=BDEBUG

def setOut(afileName):
	global __stdout
	if(__stdout != None):
		resetOut()
	__stdout,sys.stdout=sys.stdout,open(afileName,'w+')
	

def resetOut():
	global __stdout
	if(__stdout != None and __stdout != sys.stdout):
		sys.stdout.close()
		sys.stdout=__stdout


def browser(url):
	os.system('''start '''+str(url))
txthtml=('<textarea style="width:100%; height:100%;">','</textarea>')		
def shtml(file,txt,browser=True):
	f=open(file,'a')
	txt=txt.replace(txthtml[1],txthtml[1][:1]+'!!!qgb-padding!!!'+txthtml[1][1:])	
	f.write(txthtml[0])
	f.write(txt)
	f.write(txthtml[1])
	f.close()
	if(browser==True):globals()['browser'](f.name)
	
def helphtml(obj,file=None):
	if(file==None):
		try:file=obj.__name__+'.html'
		except Exception:file='obj.html'
	elif(file.lower()[-1]!='l'):file=file+'.html'
	setOut(file)
	print txthtml[0]
	help(obj)
	print txthtml[1]
	sf=sys.stdout.name
	resetOut()
	globals()['browser'](sf)
	
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
	if(browser==True):globals()['browser'](f.name)
	# print vars()
	# vars()['browser'](f.name)

def phtml(file):
	if(file.lower()[-1]!='l'):file=file+'.html'
	setOut(file)
	print txthtml[0]
def phtmlend():
	print txthtml[1]
	sf=sys.stdout.name
	resetOut()
	globals()['browser'](sf)
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
def getAllMod():
	fp=os.path.dirname(__file__)
	ls=[]
	for i in os.listdir(fp):
		if(len(i)<3):continue
		if(i.find('__')!=-1):continue
		if(i.lower()[-3:]!='.py'):continue
		ls.append(i[:-3])
	return ls
if __name__ == '__main__':
	import Clipboard
	gsImport=gsImport.replace('\n','')
	for i in getAllMod():
		if gsImport.find(i)==-1:gsImport+=(','+i)
	###get coding line
	for i in read(__file__).splitlines():
		if i.startswith('#') and i.find('cod')!=-1:
			gsImport=i+'\n'+gsImport
	
	print gsImport
	Clipboard.set(gsImport)