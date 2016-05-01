# coding=utf-8
gsImport='''
from qgb import U,T
'''

imax=2147483647
imin=-2147483648

import  os,sys,socket;stdin=sys.stdin;pid=os.getpid();path=os.path
from threading import *;thread=Thread
from multiprocessing import *;process=Process

# import T
# print T.string;exit()
import platform
def iswin():
	if platform.system().startswith('Windows'):return True
	else:return False
def isnix():
	if 'nix' in platform.system().lower():return True
	else:return False
########################
if iswin():
	from ctypes import windll, Structure, c_ulong, byref
	msgbox=windll.user32.MessageBoxA
########################

def msgbox(s='',st='title',*a):
	if(a!=()):s=str(s)+ ','+str(a)[1:-2]
	if iswin():windll.user32.MessageBoxA(0, str(s), str(st), 0)

def pln(*a):
	print a 
	sys.stdout.flush()

	
def p(*a,**ka):
	# print len(a)
	# print a,ka
	# return
	if len(a)==1:
		sys.stdout.write(str(a[0]))
	elif len(a)>1:
		if 'sep' in ka.keys():sep=ka['sep']
		else:sep=' '
		
		for i in a:
			sys.stdout.write(str(i)+str(sep))
	sys.stdout.flush()
# p(4,2,sep='9')
# exit()

def inMuti(a,*la,**func):
	la=flap(la)

	if len(func)!=1:func=None
	else:
		if not func.keys()[0].startswith('f'):func=None
		
		func=func.values()[0]
		if type(func)==type(''):
			func=a.__getattribute__(func)
		# if callable(func):			
			
	# print a,func,la
	for i in la:
		if not callable(func):
			if i in a:return True
		try:
			if a.__getattribute__(func.__name__)==func:
				return func(i)
		except:continue
	return False
# print inMuti(gsImport,'g9','77',)
# exit()	

def iterable(a):
	try:
		for i in a:pass
		return True
	except:return False

def flat(*a):
	'''Breadth-First Traversal'''
	a=list(a);r=[];i=0
	while -1<i<len(a):
		if hasattr(a[i], '__iter__'):a.extend(a[i])
		else:r.append(a[i])
		i+=1
	return tuple(r)
	
# print flat([[1,2,3], [5, 2, 8], [7,8,9]])
##(1, 2, 3, 5, 2, 8, 7, 8, 9)
# print flat([1,2,3,[4,5,[1,2],6]],['aaa'])
##  (1, 2, 3, 'aaa', 4, 5, 6, 1, 2)

	
def cmd(*a):
	import T
	s=''
	if iswin():quot='"'
	if len(a)==0:return -1
	if len(a)==1:
		if type(a[0])==type(''):s=a[0]
		elif len(a[0])==1:s=T.string(a[0])
		elif len(a[0])>1:a=a[0]
	if len(a)>1:
		a=list(a)
		s=T.string(a.pop(0))+' '
		for i in a:
			if type(i)==type([]):
				for j in i:	
					s+=quot+T.string(i)+quot+' '
			else:
				s+=quot+T.string(i)+quot+' '
			
	# pys()
	# pln(s)
	# exit()
	try:
		return os.system(s)
	except:return -2
	# exit()
# cmd('echo 23456|sub','3','')	
def sleep(aisecond):
	__import__('time').sleep(aisecond)
	
def pause(a='Press Enter to continue...'):
	'''a=msg'''
	if iswin():
		# cmd('pause');return
		try:
			raw_input(a)
		except:exit()
	return True	
def run(a,*args):
	if type(a)==type(''):a=[a]
	if type(a)!=type([]):a=list(a)
	if len(args)>0:a.extend(args)
	if type(a)==type([]):
		return __import__('subprocess').Popen(a)
	
	
	
def curl(a):
	if type(a)!=type(''):return
	if a.lower().startswith('curl '):
		a=a.replace('""','')
	if a.startswith('http'):
		cmd('curl',a)
	
from pprint import pprint


# def isfile

def pyshell():
	a=1
	f=sys._getframe().f_back
	__import__('code').interact(banner="",local=f.f_locals)
	
	return
	
	try:
		from ptpython.repl import embed
		embed(f.f_globals, f.f_locals, vi_mode=False, history_filename=None)
		return
	except:pass
	
	try:import IPython;IPython.embed();return
	except:pass
	
repl=pys=pyshell

def reload(mod=None):
	if mod==None:
		mod=sys._getframe().f_back.f_globals['U']
	__import__('imp').reload(mod)
r=reload

def tab():
	import readline, rlcompleter;readline.parse_and_bind("tab: complete")
autoc=tab
	
def clear():
	if iswin():os.system('cls')
	if isnix():os.system('clear')
c=cls=clear
	
gsTestPath='d:/test/'
def chdir(ap=gsTestPath):
	if type(ap)!=type('') or len(ap)<1:ap=gsTestPath
	if path.isdir(ap):os.chdir(ap);return True
	print ap
	ap=path.dirname(ap)
	if path.isdir(ap):os.chdir(ap);return True
	for i in ap:
		if i not in T.filename:raise Exception('need file path')
cd=chdir
# @property
def ls(ap='.'):
	if type(ap)!=type('') or len(ap)<1:ap='.'
	return os.walk(ap).next()[2]

def pwd(p=False):
	if p:print os.getcwd()
	return os.getcwd()
	
def ping():
	pass
	
	
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
def readStdin(size=1024):
	'''size<0 read all,
	help read:If the size argument is negative or omitted, read until EOF is reached.'''
	if not stdin.isatty():
		stdin.seek(0)
		return stdin.read(size)
	else: return ''
getStdin=readStdin

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
	'''diff between eval and exec in python
	return None'''
	exec(s)

def calltimes(a=''):
	import T
	a='count'+T.string(a)
	if calltimes.__dict__.has_key(a): 
		calltimes.__dict__[a]+=1
	else:
		calltimes.__dict__[a]=0
	return calltimes.__dict__[a]
ct=calltimes

if(calltimes()<1):BDEBUG=True;__stdout=None
debug=BDEBUG

def setOut(afileName):
	global __stdout
	if(__stdout != None):
		resetOut()
	__stdout,sys.stdout=sys.stdout,open(afileName,'w+')
setout=setOut	

def resetOut():
	global __stdout
	if(__stdout != None and __stdout != sys.stdout):
		sys.stdout.close()
		sys.stdout=__stdout
resetout=resetOut

def browser(url):
	if iswin():os.system('''start '''+str(url))
txthtml=('<textarea style="width:100%; height:100%;">','</textarea>')
		
def autohtml(file):
	if file==None:
		try:
			file=obj.__name__+'.html'
		except Exception:file='obj.html'
	elif(file.lower()[-1]!='html'):file=file+'.html'
	return file	

	
def shtml(txt,file='',browser=True):
	if type(txt)==type({}):
		if len(txt)==0:return
		s=txt.keys()
		s=T.listToStr(s)
		pass	
	f=open(autohtml(file),'a')
	txt=txt.replace(txthtml[1],txthtml[1][:1]+'!!!qgb-padding!!!'+txthtml[1][1:])	
	f.write(txthtml[0])
	f.write(txt)
	f.write(txthtml[1])
	f.close()
	if(browser==True):globals()['browser'](f.name)
	
def helphtml(obj,file='obj.html'):
	# setOut(file)
	# print txthtml[0]
	# help(obj)
	# print txthtml[1]
	# sf=sys.stdout.name
	# resetOut()
	import pydoc
	txt= pydoc.render_doc(obj,'%s')
	# txt=txt.replace(txthtml[1],txthtml[1][:1]+'!!!qgb-padding!!!'+txthtml[1][1:])
	txt=txthtml[0]+txt+txthtml[1]

	write(file,txt)
	globals()['browser'](file)
h=help=helphtml

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
	
def getTimestamp():
	'''return: float'''
	return __import__('time').time()
time=getime=getTime=timestamp=getTimestamp
	
	
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
def getModPath():
	sp=os.path.abspath(__file__)
	sp=os.path.dirname(sp)
	sp=os.path.dirname(sp)
	return sp
	
def main(display=True,*args):
	# gsImport=gsImport.replace('\n','')
	# for i in getAllMod():
		# if gsImport.find(i)==-1:gsImport+=(','+i) 	
	##get coding line
	# for i in read(__file__).splitlines():
		# if i.startswith('#') and i.find('cod')!=-1:
			# gsImport=i+'\n'+gsImport
	
	gsImport='''import sys,os;sys.path.append('{0}');from qgb import *'''.format(getModPath())
	
	if display:print gsImport,display
	try:
		import Clipboard
		Clipboard.set(gsImport)
	except:print 'Clipboard err'
	return gsImport
if __name__ == '__main__':main()