# coding=utf-8

gsImport='''
from qgb import U,T
'''

imax=2147483647
imin=-2147483648

import  os,sys,socket
from threading import *;thread=Thread
from multiprocessing import *;process=Process
cmd=os.system

import platform
def iswin():
	if platform.system().startswith('Windows'):return True
	else:return False
def isnix():
	if 'nix' in platform.system().lower():return True
	else:return False


if iswin():
	from ctypes import windll, Structure, c_ulong, byref
	msgbox=windll.user32.MessageBoxA

def sleep(aisecond):__import__('time').sleep(aisecond)
	
	
def pause():
	if iswin():cmd('pause');return
	
def run(a,*args):
	if type(a)==type(''):a=[a]
	if type(a)!=type([]):a=list(a)
	if len(args)>0:a.extend(args)
	if type(a)==type([]):
		return __import__('subprocess').Popen(a)
	
	
def curl(a):
	if type(a)!=type(''):return
	if not a.lower().startswith('curl '):return
	a=a.replace('""','')
	cmd('cur')
	
from pprint import pprint

def pyshell():
	a=1
	f=sys._getframe().f_back
	try:
		from ptpython.repl import embed
		embed(f.f_globals, f.f_locals, vi_mode=False, history_filename=None)
		return
	except:pass
	
	try:import IPython;IPython.embed();return
	except:pass
	__import__('code').interact(banner="",local=f.f_locals)
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
	
def chdir(ap='d:/test'):
	os.chdir(ap)
cd=chdir

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
	'''diff between eval and exec in python
	return None'''
	exec(s)

def string(a):
	if type(a)==type(''):return a
	try:a=str(a)
	except:a=''
	return a
def calltimes(a=''): 
	a='count'+string(a)
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
	if iswin():windll.user32.MessageBoxA(0, str(s), str(st), 0)

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
def getModPath():
	sp=os.path.abspath(__file__)
	sp=os.path.dirname(sp)
	sp=os.path.dirname(sp)
	return sp
	
def main(*args):
	# gsImport=gsImport.replace('\n','')
	# for i in getAllMod():
		# if gsImport.find(i)==-1:gsImport+=(','+i) 	
	##get coding line
	# for i in read(__file__).splitlines():
		# if i.startswith('#') and i.find('cod')!=-1:
			# gsImport=i+'\n'+gsImport
	
	gsImport='''import sys,os;sys.path.append('{0}');from qgb import *'''.format(getModPath())
	
	print gsImport
	try:
		import Clipboard
		Clipboard.set(gsImport)
	except:print 'Clipboard err'
	
if __name__ == '__main__':main()