# coding=utf-8
gsImport='''
from qgb import U,T
'''
true=True;false=False
IMAX=imax=2147483647;IMIN=imin=-2147483648
import  os,sys,socket;stdin=sys.stdin;pid=os.getpid();path=os.path
from threading import *;thread=Thread
from multiprocessing import *;process=Process
import __builtin__ ;py=builtin=__builtin__

gError=None;gbPrintErr=False
# import T
# print T.string;exit()
import platform
def iswin():
	if platform.system().startswith('Windows'):return True
	else:return False
def isnix():
	if 'nix' in platform.system().lower():return True
	else:return False
def iscyg():
	return 'cygwin' in  platform.system().lower()
########################
if iswin() or iscyg():
	try:
		from ctypes import windll, Structure, c_ulong, byref

		def msgbox(s='',st='title',*a):
			if(a!=()):s=str(s)+ ','+str(a)[1:-2]
			if iswin():windll.user32.MessageBoxA(0, str(s), str(st), 0)
	except Exception as ei:
		if gbPrintErr:print ei
########################


try:
	from F import write,read,ls,ll,md,rm
	import F,T
	from pprint import pprint
	import Clipboard;clipboard=cb=Clipboard
except Exception as ei:
	if gbPrintErr:print '#Error import F'
	gError=ei
#TODO: if not has ei,import error occur twice,why?
def driverPath(a):
	for i in T.AZ:
		if F.exist(i+a):return i+a
	return ''

def getTestPath():
	if isnix():return '/test/'
	if iswin() or iscyg():
		s='d:/test/'
		return driverPath(s[1:]) or s
gst=gsTestPath=getTestPath()


def getShellPath():
	if isnix():return '/bin/qgb/'
	if iswin() or iscyg():
		s='E:/sourceCode/shell/'
		return driverPath(s[1:]) or s
gsw=gsWShell=getShellPath()


def pln(*a,**ka):
	s='print '
	for i in range(len(a)):
		s+='a['+str(i)+'],'

	if len(ka)<1:
		exec(s[:-1])###without (del last ,) [:-1] can't flush
	else:
		print a,ka
	sys.stdout.flush()

	
def p(*a,**ka):
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

def readStdin(size=-1):
	'''size<0 read all,
	help read:If the size argument is negative or omitted, read until EOF is reached.'''
	if not stdin.isatty():
		stdin.seek(0)
		return stdin.read(size)
	else: return ''
getStdin=readStdin

def iterable(a):
	'''str is True'''
	try:
		for i in a:pass
		return True
	except:return False

def flat(*a,**options):
	'''Breadth-First Traversal'''
	noNone=False
	for o in options:
		if 'nonone' in o.lower():noNone=options[o]
		if one_in('isnone','hasnone', o.lower()):noNone=not options[o]
		# repl()
		
	a=list(a);r=[];i=0
	while i<len(a):
		if hasattr(a[i], '__iter__'):a.extend(a[i])
		else:
			if noNone and not a[i]:pass
			#TODO other condition
			else:r.append(a[i])
		i+=1
	# repl()
	return tuple(r)
	
# print flat([[1,2,3], [5, 2, 8], [7,8,9]])
##(1, 2, 3, 5, 2, 8, 7, 8, 9)
# print flat([1,2,3,[4,5,[1,2],6]],['aaa'])
##  (1, 2, 3, 'aaa', 4, 5, 6, 1, 2)
	
def md5(a='',file=''):
	'''[a] : string or buffer
	[file]:fileName
	return 32 hex(lowerCase) str'''
	import hashlib   
	
	if file:
		myhash = hashlib.md5()
		f = py.file(file,'rb')
		while True:
			b = f.read(8096)
			if not b :
				break
			myhash.update(b)
		f.close()
		return myhash.hexdigest()
	
	
	md5 = hashlib.md5()   
	md5.update(a)	
	return md5.hexdigest()  
	

def autof(head,ext=''):
	'''return str  
	# TODO # ext=?ext*     '''
	if not py.type(ext)==py.type(head)==py.str or head=='':
		return ''
	
	if len(ext)>0 and not ext.startswith('.'):ext='.'+ext
	
	ap='.'
	if path.isabs(head):
		ap=F.dir(head)
		if not F.isExist(ap):
			if head.endswith(ext):return head
			else:return head+ext

	
	import F
	ls=F.ls(ap)
	if head+ext in ls:return head+ext
	
	for i in ls:		
		if i.startswith(head) and i.endswith(ext):return i
	
	for i in ls:
		if head in i and ext in i:return i
		
	# if inMuti(ext,'*?'):ext=ext.replace('*')
	
	if not head.endswith(ext):head+=ext
	
	return head
autoFileName=autof


def inMuti(a,*la,**func):
	'''bool a.func(la[i])'''
	r=[]
	la=flat(la)
	# repl()
	if len(func)!=1:func=None
	elif not func.keys()[0].startswith('f'):func=None
	else:
		func=func.values()[0]
		if type(func) is str:
			func=a.__getattribute__(func)
		else:func=a.__getattribute__(func.__name__)
			
		# if callable(func):			
	if not callable(func):
		for i in la:
			try:
				if a==i or a in i:r.append(i)
			except TypeError:continue
			except Exception as e:continue
	else:
		for i in la:
			if func(i):r.append(i)
		
		# return False
	# repl()
		
	return r
inmuti=inMuti
	
	
def mutin(la,a,func=None):
	if len(la)<1:return False
	r=[]
	if type(func) not in (str,) and not callable(func) :
		for i in la:
			try:
				if i in a:r.append(i)
			except:
				if i is a:r.append(i)
	else:
		if type(func) is str:
			for j in dir(la[0]):
				if j.startswith(func) and callable(la[0].__getattribute__(j)):
					func=la[0].__getattribute__(j)
			# if not callable(func):
				# raise Exception('not found "{0}" in la[0] methods'.format(func))
		if callable(func):
			if func.__name__ in dir(la[0]):
				for i in la:
					i=i.__getattribute__(func.__name__)(a)
					if i:r.append(i)
			else:
				for i in la:
					i=func(i,a)
					if i:r.append(i)
	return r	
inMutiR=mutiIn=mutin
# exit()	
def one_in(vs,*t):
	'''(1,2,3,[t])	or	([vs].[t])'''
	if not hasattr(vs, '__iter__'):vs=[vs]
	if len(t)==1:
		t=t[0]
	elif len(t)>1:
		vs.extend(t[:-1])
		t=t[-1]
	else:raise Exception(all_in.__doc__)
	r=[]
	for i in vs:
		try:
			if i in t:r.append(i)
		except:pass
	return r
	
def in_one(v,*ts):
	for i in ts:
		try:
			if v in i:return [v]
		except:pass
	return []	
def all_in(vs,*t):
	'''(1,2,3,[t])	or	([vs].[t])'''
	if not hasattr(vs, '__iter__'):vs=[vs]
	if len(t)==1:
		t=t[0]
	elif len(t)>1:
		vs.extend(t[:-1])
		t=t[-1]
	else:raise Exception(all_in.__doc__)
	# U.pln(vs,t)
	for i in vs:
		try:
			if i not in t:return []
		except:return []
	return vs
	
def in_all(v,*ts):
	for i in ts:
		try:
			if v not in i:return []
		except:pass
	return [v]
##########################################
def cmd(*a):
	import T
	s=''
	if iswin():quot='"'
	if len(a)==0:
		if iswin():a=['cmd']
		# TODO #
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
			
	# pln(s)
	# exit()
	try:
		return os.system(s)
	except:return -2
	# exit()
# cmd('echo 23456|sub','3','')	
def sleep(aisecond):
	__import__('time').sleep(aisecond)
	
def pause(a='Press Enter to continue...\n',exit=True):
	'''a=msg'''
	if iswin():
		# cmd('pause');return
		try:
			raw_input(a)
		except:
			if exit:x()
			return False
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
	cmd(a)

# def isfile

def pyshell(printCount=False):
	# a=1
	ic=count('__repl__')
	if printCount:print ic
	######################
	f=sys._getframe().f_back
	locals=f.f_locals
	locals['U']=__frame.f_locals['U']
	__import__('code').interact(banner="",local=locals)
	return
	
	# try:
		# from ptpython.repl import embed
		# embed(f.f_globals, f.f_locals, vi_mode=False, history_filename=None)
		# return
	# except:pass
	
	# try:import IPython;IPython.embed();return
	# except:pass
	
repl=pys=pyshell

def reload(mod=None):
	if mod==None:
		mod=sys._getframe().f_back.f_globals['U']
	__import__('imp').reload(mod)
R=r=reload

def tab():
	import readline, rlcompleter;readline.parse_and_bind("tab: complete")
autoc=tab

class __wrapper(object):
	def __init__(self, wrapped):
		self.wrapped = wrapped
	def __getattr__(self, name):
		
		try:
			
			return getattr(self.wrapped, name)
		except AttributeError:
			return 'default' # Some sensible default

__frame=sys._getframe().f_back
	
	
def clear():
	# sys.modules[__name__] = __wrapper(sys.modules[__name__])
	if iswin():os.system('cls')
	if isnix():os.system('clear')
C=c=cls=clear


def chdir(ap=gsTestPath,md=True):
	if type(ap)!=type('') or len(ap)<1:ap=gsTestPath
	if md:globals()['md'](ap)
	
	global gscdb
	# repl()
	# if path.abspath(gscdb) != pwd():
	gscdb=pwd()
	
	if path.isdir(ap):os.chdir(ap);return True

	ap=path.dirname(ap)
	if path.isdir(ap):os.chdir(ap);return True
	for i in ap:
		if i not in T.PATH_NAME:raise Exception('need file path')
cd=chdir

gscdb=''
def cdBack():
	return cd(gscdb)
cdb=cdBack

def cdCurrentFile():
	f=sys._getframe().f_back.f_globals
	if '__file__' in f:
		return cd(path.abspath(f['__file__']))
	return False
cdc=cdCurrent=cdcf=cdCurrentFile

def cdTest(a=''):
	return cd(gst+a)
cdt=cdTest
	
def cdQPSU(a=''):
	return cd(getModPath()+a)
# @property
cdqp=cdqpsu=cdQPSU
	
def cdWShell(a=''):
	return cd(gsWShell+a)
cds=cdws=cdWShell
	
def pwd(p=False,display=False):
	s=os.getcwd()
	if p or display:print s
	return s
	
	
def sortDictV(ad,des=True):
	'''des True,,, python dict key auto sort ?'''
	if type(ad) is not dict:return {}
	return sorted(ad.iteritems(),key=lambda ad:ad[1],reverse=True)
# d={}
# for i in range(7):
	# d[i]=i*i-5*i
	
# d={'ok':1,'no':2}
# d={0: 0, 5: 0, 6: 6, 1: -4, 2: -6, 3: -6, 4: -4}

# d=sortDictV(d)

# exit()

def eval(s):
	'''diff between eval and exec in python
	return None'''
	exec(s)

def calltimes(a=''):
	import T
	a='_count'+T.string(a)
	if calltimes.__dict__.has_key(a): 
		calltimes.__dict__[a]+=1
	else:
		calltimes.__dict__[a]=0
	return calltimes.__dict__[a]
ct=count=calltimes

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


def browser(url,ab='chrome'):
	import webbrowser
	def chrome(url):
		###TODO: auto Find system base everything
		spC='''C:\Program Files\Google\Chrome\Application\chrome.exe'''	
		webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(spC))
		webbrowser.get('chrome').open_new_tab(url)
	for i in py.dir():
		if py.eval('callable({0})'.format(i)):
			if ab.lower()== i:
				exec '{0}(url)'.format(i) in globals(),locals()
		
	 
	# webbrowser.open_new_tab(url)
	# if iswin():os.system('''start '''+str(url))
# browser('qq.com')

# txthtml=('<textarea style="width:100%; height:100%;">','</textarea>')
		
def autohtml(file=None):
	import T
	if type(file)  is not str:
		if file is None:file=stime()+'.html'
		else:
			if hasattr(file,'__name__'):
				if '.htm' not in file.__name__:
					file=file.__name__+'.html'
			else:file='obj_{0}.html'.format(hash(file))
	elif  len(T.filename(file))<1:file=stime()+'.html'
	elif '.htm' not in file.lower():file=file+'.html'
	return file	

	
def shtml(txt,file='',browser=True):
	import T,pprint,F
	if file=='' and type(txt) is not str:
		try:file=T.filename(T.max(txt.__str__(),txt.__repr__(),txt.__name__)[:19])
		except:pass
	
	# if type(txt) in (dict,list):
	txt=pprint.pformat(txt)
		# if len(txt)==0:return
		# s=[]
		# for i in txt.keys():
			# s.append(T.string(i)+'   :   '+T.string(txt[i])+'\n')
		# txt=T.listToStr(s)
		# 
	if len(file)<1:file=T.filename(getObjName(txt)+stime())[:19]
	if not file.lower().endswith('.txt'):file+='.txt'
	F.write(file,txt)
	# f=open(file+'.txt','a')
	# rm(f.name)
	# txt=txt.replace(txthtml[1],txthtml[1][:1]+'!!!qgb-padding!!!'+txthtml[1][1:])	
	# f.write(txthtml[0])
	# f.write(txt)
	# f.write(txthtml[1])
	# f.close()
	if(browser==True):globals()['browser'](path.abspath(file))
txt=shtml	

def maxLen(*a):
	if py.len(a)==1:a=a[0]
	im=-1
	for i in a:
		i=len(i)
		if i>im:im=i
	return im

def printAttr(a,console=False):
	'''aoto call __methods which is no args'''
	d=py.dir(a)
	
	if console:
		sk='%-{0}s'.format(maxLen(d))
		si='%-{0}s'.format(len(py.len(  d  )))
		for i,k in py.enumerate(d):
			print si%i,sk%k,py.eval('a.{0}'.format(k))
		return
		
	sh='''<tr>
	 <td>{0}</td>
	 <td id="n">{1}</td>
	 <td><textarea>{2}</textarea></td>
	 <td>{3}</td>
    </tr>'''
	sp=getModPath()+'file/attr.html'
	r='';v='';vi=-1
	for i,k in py.enumerate(d):
		try:
			v=py.eval('a.{0}'.format(k))
			vi=len(v)
			if py.callable(v) and k.startswith('__'):
				vv='!ErrGetV()'
				try:vv=v()
				except:pass
				v='{0} == {1}'.format(v,vv)
			
			if type(v) is not str:
				import pprint
				v= pprint.pformat(v)
		except Exception as e:v=py.repr(e)
		r+=sh.format(i,k,v,vi)
	# cdt('QPSU')
	import T
	name=gst+'QPSU/'+T.filename(getObjName(a))+'.html'
	write(name,read(sp).replace('{result}',r))
	browser(name)
	# cdBack()
dir=printAttr
# repl()
# printAttr(5)
	
def getObjName(a,value=False):
	try:
		if len(a.__name__)>0:
			return a.__name__
	except:pass
	if type(a) in (py.int,py.long):return 'i_'+str(a)
	if type(a) is py.str:return 's_'+a[:7]
	
	return str(type(a))
	# exit()
getName=getObjName

def getVarName(a,funcName='getVarName'):
	'''funcName :defined for recursion frame search'''
	import inspect,re,T
	for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
		r=T.sub(line,'(',')')
		if '(' not in r:
			return r
		# if funcName not in line:continue
		# line=T.sub(line,funcName,'').strip()
		# i0=line.find('(')
		# i1=line.find('(',i0+1)
		# if i1==0:return T.sub(line,'(',')').strip()
		# else:
		
		
		print repr(line)
		arr = []
		i=-1
		# repl()
		for c in line:
			i+=1				
			if c=='(':
				arr.append((i,c))
			elif c==')':
				if arr and arr[-1][1] == '(':
					il=arr.pop()[0]+1
					# ir is i
					print il,i,repr(line[il:i])
					if line.find(funcName,il,i)!=-1:
						il=il+line[il:i].find('(')+1 
						i =il+line[il:i].rfind(')')
						
						print repr(line[il:i].strip())
					else:
						pass
					# ra(i,c)
				else:
					return False
	
	# print il,i,repr(line)
		# if inMuti():return line
name=getVarName
# repl()
# exit()
# getVarName(1l)

	
def helphtml(obj,*aos):
	txt=''
	import pydoc,re
	if aos:
		aos=flat(obj,aos,noNone=True)
		for i in aos:
			#TODO
			txt+=re.sub('.\b', '', pydoc.render_doc(i,'%s'))
			txt+='\n==============%s=======================\n'%ct(aos)
	else:txt=re.sub('.\b', '', pydoc.render_doc(obj,'%s'))
	# txt=txt.replace(txthtml[1],txthtml[1][:1]+'!!!qgb-padding!!!'+txthtml[1][1:])
	# txt=txthtml[0]+txt+txthtml[1]
	# msgbox(txt[txt.find(b'\x08'):])
	# repl()
	# exit()
	file='Uhelp_obj.txt'
	try:
		import T
		if obj:file=T.filename(getObjName(obj))+'.txt'
		elif aos:file=T.filename(getObjName(aos[0]))+'..%s.txt'%len(aos)
	except:pass
	

	with open(file,'w') as f:
		f.write(txt)
	# write(file,txt)
	globals()['browser'](file)
h=help=helphtml
# if __name__=='__main__':help(h);exit()

def getLine():
	import inspect,re
	for line in inspect.getframeinfo(sys._getframe().f_back)[3]:
		return line
		# if m:return m.group(1)
	# repl()

	
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
	
	
	
def getFloaTail(a,s=False,str=False,string=False,i=False,int=False):
	if type(a) is float:
		a=round(a-py.int(a),3)
		if s or str or string:
			return py.str(a)[1:]
		if i or int:
			return int(py.str(a)[2:])
		return a	
		
def getStime(format='%Y-%m-%d %H.%M.%S',time=None):
	'''http://python.usyiyi.cn/translate/python_278/library/time.html#time.strftime'''
	import time as tMod
	
	if format==':':format='%Y-%m-%d %H.%M.%S'.replace('.',':')
	
	if type(time) not in (int,float):time=getTimestamp()
	if format=='' or type(format) is not str:return str(time)
	
	if '%' in format:
		if time:
			if type(time) in (int,float) and time>0:
				r=tMod.strftime(format,tMod.localtime(time))
				if type(time) is float:
					if not r.endswith(' '):r+=' '
					r+=getFloaTail(time,s=True)
				return r
		else:return tMod.strftime(format)
stime=getStime
	
		
		
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
	

def fields(obj):
	import inspect
	return inspect.getmembers(obj)

def methods(obj):
	def y():
		for i in py.dir(obj):
			if py.callable(py.eval('obj.'+i)):
				yield i
	# printAttr(y)
	
	# printAttr([])
	return list(y())
	
	# exit()
# print methods([])	
	
def x(msg=None):
	if(msg!=None):print msg
	exit(235)
	
def exit(i=2357):
	os._exit(i)
def getAllMod():
	ls=[]
	for i in os.listdir(getModPath()):
		if(len(i)<3):continue
		if(i.find('__')!=-1):continue
		if(i.lower()[-3:]!='.py'):continue
		ls.append(i[:-3])
	return ls
def getModPathForImport():
	sp=os.path.dirname(getModPath())# dirname/ to dirname
	sp=os.path.dirname(sp)
	if iswin():return sp

def getModPath():
	sp=os.path.abspath(__file__)
	sp=os.path.dirname(sp)
	if iswin():return sp+'\\'
	
def len(a):
	try:return py.len(a)
	except:
		# if type(a) in (int,float,list,tuple,dict):
			# return py.len(str(a))
		try:return py.len(str(a))
		except:return -1
		
def dis(a):
	from dis import dis
	return dis (compile(a,'<str>','exec'))
		
def ipyOutLast(i=None):
	'''use _  ,  __ ,  ___ 
	ORZ'''
	f=sys._getframe()
	while f and f.f_globals and 'get_ipython' not in f.f_globals.keys():
		f=f.f_back
	Out=f.f_globals['Out']
	
	# globals()['gipy']=5
	
	def length():return len(Out)

	ipyOutLast.size=ipyOutLast.len=ipyOutLast.__len__=length
	# print ipyOutLast.size
	if i is None:
		if Out:
			# p("Out.keys ")
			im=len(Out.keys())
			if im<10:return Out.keys()
			elif 9<im<21:return [(k,ct(Out)) for k in Out.keys()] 
			else:
				# repl()
				r=[[]]
				for i,k in py.enumerate(Out):#index ,key
					# print i
					r[-1].append((k,i))
					if i%5==0:
						r.append([])
				return r
		else:
			print "##### IPy No Out #####"
			return
	
	if Out:
		try:
			return Out[i]
		except:return Out[Out.keys()[i]]
	return Out
	
def cmdPos():
	cmd(gsw+'pos')
pos=cmdPos
	
def notePadPlus(a):
	cmd('npp',str(a))
	
# sys.argv=['display=t','pressKey=t','clipboard=f']
def main(display=True,pressKey=False,clipboard=False,escape=False,c=False,ipyOut=False,cmdPos=False,reload=False,*args):
	# print vars()
	# print stime()
	# exit()
	# shtml(vars(),file='vars0')
	anames=py.tuple([i for i in py.dir() if not i .startswith('args')])
	import T
	if not args:args=sys.argv
	
	for i in args:
		for j in anames:
			if i.lower().startswith(j.lower()+'='):
				# args.remove(i)
				i=T.sub(i,'=','').lower()
				if i.startswith('t'):exec j+'=True';break
				if i.startswith('f'):exec j+'=False';break
				
	# gsImport=gsImport.replace('\n','')
	# for i in getAllMod():
		# if gsImport.find(i)==-1:gsImport+=(','+i) 	
	##get coding line
	# for i in read(__file__).splitlines():
		# if i.startswith('#') and i.find('cod')!=-1:
			# gsImport=i+'\n'+gsImport
	# print vars()
	# exit()
	gsImport='''import sys,os;sys.path.append('{0}');from qgb import *'''.format(getModPathForImport())
	###############################
	'''call order Do Not Change! '''
	###############################
	if c:gsImport+=';C=c=U.c'
	
	if ipyOut:gsImport+=';O=o=U.ipyOutLast'
	
	if cmdPos:gsImport+=";POS=pos=U.cmdPos;npp=NPP=U.notePadPlus;ULS=Uls=uls=U.ls"
	
	if reload:gsImport+=";R=r=U.reload"
	
	if escape:gsImport=gsImport.replace("'",r"\'")
	
	if display:print gsImport
	
	if pressKey:
		try:
			import win32api
			win32api.ShellExecute(0, 'open', gsw+'exe/key.exe', gsImport+'\n','',0)
		except:print 'pressKey err'
	if clipboard:
		try:
			Clipboard.set(gsImport)
		except:print 'Clipboard err'
	
	return gsImport
if __name__ == '__main__':main()


