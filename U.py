# coding=utf-8
gsImport='''
from qgb import U,T
'''
true=True;false=False
INT_MAX=gimax=IMAX=imax=2147483647;INT_MIN=gimin=IMIN=imin=-2147483648
import sys
stdin=sys.stdin;stdout=sys.stdout;stderr=sys.stderr
gsdecode=decoding='utf-8';gsencode=gsencoding=encoding=stdout.encoding
modules=sys.modules
try:
	import py
	if not py.istr:raise Exception('not qgb.py')
except Exception as eipy:
	try:from . import py
	except Exception as ei:
		print(ei)
		import pdb;pdb.set_trace()
	
'''TODO：应该设计一个配置类，__getattr__ on a module 属性拦截,这样可以同步多个变量名， 在python2中没有很好的方法,  在Python 3.7+中，你只需要做一个明显的方法。
# my_module.py
def __getattr__(name: str) -> Any:
	return attr
目前使用单变量名	
'''
gbPrintErr=True
gbLogErr=True

gbDebug=DEBUG=sys.flags.debug or False#gbDebug只在这里出现一次
def debug(a=False):
	# global gbDebug,DEBUG
	if 'debug' in os.environ:#优先环境变量开关
		e=os.getenv('debug').strip()#not .trim()
		if e and e!='0':a=True
		else:a=False
	globals()['DEBUG']=a
	globals()['gbDebug']=a
	return DEBUG

# if(calltimes()<1):DEBUG=True #ct not defined

########
gError=[]
def setErr(ae,msg='#Error '):
	global gError
	if gbLogErr:# U.
		if type(gError) is list:gError.append(ae)
		elif gError:gError=[gError,ae]
		else:gError=[ae]
	else:
		gError=ae
	if gbPrintErr:print (msg,ae)# U.
	
if 'qgb.U' in modules:modules['_U']=modules['qgb.U']
elif 'U' in modules:modules['_U']=modules['U']
################  import python lib  #######################
try:
	import os;path=os.path
	from threading import Thread
	thread=Thread
	from multiprocessing import Process;process=Process
	from collections import OrderedDict
	from concurrent.futures import ThreadPoolExecutor
	threadPool=ThreadPool=ThreadPoolExecutor
except Exception as ei:
	setErr(ei,msg='#Error py lib import')
	
try:
	_U=modules['_U']
	gError=_U.gError
	gbPrintErr=_U.gbPrintErr
except Exception as _e:pass
	# pass# 已经存在于globals 中，是否有必要重新赋值给 gError？
# else:
try:
	if __name__.endswith('qgb.U'):from . import F,T
	else:import F,T
	write,read,ls,ll,md,rm=F.write,F.read,F.ls,F.ll,F.md,F.rm
	IntSize=F.IntSize
	F.fileName=F.filename=T.filename_legalized

	from pprint import pprint,pformat
	if __name__.endswith('qgb.U'):from . import Clipboard
	else:                         import Clipboard
	clipboard=cb=Clipboard#  
	cbs=Clipboard.set
	cbg=Clipboard.get
except Exception as ei:
	setErr(ei,msg='#Error import '+str(ei))
	
aError=ArgsErr=argserr=argErr=argerr=argumentError=ArgumentException=py.ArgumentError	
ArgumentUnsupported=py.ArgumentUnsupported
############
module=py.module
Class=py.Class
instance=py.instance
Class=classtype=classType=py.classType
iterable=py.iterable
#######################################
gd_sync_level={
'process':1,
'python':1,
'py':1,
'system':2 ,
'sys':2 , #not sys module
'lan':3    ,# lan sync  #TODO default rpc to find out qpsu computer
'wan':4    ,# internet sync
'all':4    ,
}
def set(name,value=None,level=gd_sync_level['process']):
	if level>=gd_sync_level['process']:
		import sys
		d=py.getattr(sys,'_qgb_dict',{})
		if value==None:
			value=name
			name='_'
		d[name]=value
		sys._qgb_dict=d
	if level>=gd_sync_level['system']:
		import sqlite3
	return value

def get(name='_',default=py.No('can not get name'),level=gd_sync_level['process']):
	if level>=gd_sync_level['process']:
		import sys
		d=py.getattr(sys,'_qgb_dict',{})
		#TODO 对于不存在的 name ，可以记录最后访问时间为 py.No，方便排查
		return d.get(name,default)
	#TODO

def get_or_set_input(name):
	r=get(name)
	if not py.isno(r):return r
	return set(name,py.input('%r : '%name) )
getInput=getOrInput=get_or_input=get_or_set_input

def get_or_set(name,default):
	if py.isno(default):
		raise py.ArgumentError('default cannot be py.No')
	r=get(name)
	if not py.isno(r):return r
	return set(name,default)
getset=getSet=get_set=get_or_set
#########################
def one_in(vs,*t):
	'''(1,2,3,[t])	or	([vs].[t])'''
	if not hasattr(vs, '__iter__'):vs=[vs]#  is3 str has __iter__  while  is2 not
	if len(t)==1:
		t=t[0]
	elif len(t)>1:
		vs.extend(t[:-1])
		t=t[-1]
	else:raise Exception(one_in.__doc__)
	r=[]
	for i in vs:
		try:
			if i in t:r.append(i)
		except:pass
	return r
#########################
def getPyVersion():
	'''return float 2.713
	'''
	r=T.sub(sys.version,'',' ')
	r=r.replace('.','')
	r=r[0]+'.'+r[1:]
	return float(r)
	

import platform
glnix=['nix','linux','darwin']
def isnix():
	'''
### Linux (64bit) + WSL
os.name                     posix
sys.platform                linux
platform.system()           Linux
sysconfig.get_platform()    linux-x86_64
platform.machine()          x86_64
platform.architecture()     ('64bit', '')

### WINDOWS official python installer                 32bit
-------------------------   -----                     -----
os.name                     nt                        nt
sys.platform                win32                     win32
platform.system()           Windows                   Windows
sysconfig.get_platform()    win-amd64                 win32
platform.machine()          AMD64                     AMD64
platform.architecture()     ('64bit', 'WindowsPE')    ('64bit', 'WindowsPE')

msys2                       64bit                     32bit
-----                       -----                     -----
os.name                     posix                     posix
sys.platform                msys                      msys
platform.system()           MSYS_NT-10.0              MSYS_NT-10.0-WOW
sysconfig.get_platform()    msys-2.11.2-x86_64        msys-2.11.2-i686
platform.machine()          x86_64                    i686
platform.architecture()     ('64bit', 'WindowsPE')    ('32bit', 'WindowsPE')

msys2                       mingw-w64-x86_64-python3  mingw-w64-i686-python3
-----                       ------------------------  ----------------------
os.name                     nt                        nt
sys.platform                win32                     win32
platform.system()           Windows                   Windows
sysconfig.get_platform()    mingw                     mingw
platform.machine()          AMD64                     AMD64
platform.architecture()     ('64bit', 'WindowsPE')    ('32bit', 'WindowsPE')

cygwin                      64bit                     32bit
------                      -----                     -----
os.name                     posix                     posix
sys.platform                cygwin                    cygwin
platform.system()           CYGWIN_NT-10.0            CYGWIN_NT-10.0-WOW
sysconfig.get_platform()    cygwin-3.0.1-x86_64       cygwin-3.0.1-i686
platform.machine()          x86_64                    i686
platform.architecture()     ('64bit', 'WindowsPE')    ('32bit', 'WindowsPE')

'''
	return [i for i in glnix if i in platform.system().lower()]
	
def isWin():
	if platform.system().startswith('Windows'):return True
	else:return False
is_win=iswin=isWin

def isLinux():return platform.system()=='Linux'
islinux=isLinux
def isMacOS():return platform.system()=='darwin'
is_osx=isOSX=ismacos=isMacOS
	
def is_termux():
	return '/com.termux' in sys.executable
istermux=isTermux=is_termux

def iscyg():
	return 'cygwin' in  platform.system().lower()
# gipy=None#这个不是qgb.ipy, 是否与U.F U.T 这样的风格冲突？
def isipy(**ka): # e=False
	# global gipy
	raise_EnvironmentError=get_duplicated_kargs(ka,
'raise_err','raise_error','raiseError','raiseErr','raise_EnvironmentError','EnvironmentError')
	try:
		# if not py.modules('IPython'):return py.No()
		import IPython
		return IPython.get_ipython()
	except Exception as e:
		if raise_EnvironmentError:
			raise
		return py.No(e)
	# ipy=False  #如果曾经有过实例，现在没有直接返回原来
	# f=sys._getframe()
	# while f and f.f_globals:# and 'get_ipython' not in f.f_globals.keys()
		# try:
			# ipy=f.f_globals['get_ipython']()#下个循环没有直接跳出while
			# break
		# except:
			# pass
		# f=f.f_back	
	# return ipy
get_ipy=get_ipython=getipy=isIpy=is_ipy=isipy
def is_ipy_cell():
	''' 和 getArgsDict 一样，最多向上找两层，防止影响到意料之外的代码
f.f_back  ~= None
	'''
	ipy=get_ipython()
	if not ipy:
		return py.No('Not even ipy')
	f=sys._getframe().f_back
	def check(f):
		return f and f.f_code.co_filename.startswith('<ipython-input-')
	return check(f) or check(f.f_back)
is_ipy_call=is_ipy_cell	

def isrepl():
	# i,o=sys.stdin.isatty(),sys.stdout.isatty()  # 这样太简单粗暴了，我想要判断上面两层之内是不是用户手动输入
	# TODO flask——rpc
	return is_ipy_cell()
	if i==o:return i
	else:
		raise Exception('std(in,out) isatty conflit')
isatty=istty=isrepl
########################
if iswin() or iscyg():
	try:
		from ctypes import wintypes#TODO cygwin ValueError: _type_ 'v' not supported
		if __name__.endswith('qgb.U'):from . import Win
		else:import Win
		setWindowPos,msgbox=Win.setWindowPos,Win.msgbox
		pos=cmdPos=setWindowPos
		pid=Win.getpid()
	except Exception as ei:
		# def msgbox(s='',st='title',*a):
			# if(a!=()):s=str(s)+ ','+str(a)[1:-2]
			# if iswin():windll.user32.MessageBoxA(0, str(s), str(st), 0)
		setErr(ei,msg='#Error import Win'  )
	def driverPath(a,reverse=True):
		'''from Z to C'''
		if not a.startswith(':'):a=':'+a
		# try:AZ=T.AZ;exist=F.exist
		# except:
		AZ=''.join([chr(i) for i in py.range(65,65+26)])
		exist=os.path.exists
		if reverse:AZ=AZ[::-1]
		for i in sys.executable[0]+AZ:
			if exist(i+a):return i+a
		return ''	
		
	if iscyg():
		def getCygPath():
			try:r=getProcessPath()
			except:r='G:/QGB/babun/cygwin/'
			if 'cygwin' in r:
				return T.subLast(r,'','cygwin')+'cygwin\\'
			else:
				raise EnvironmentError(r)
elif iscyg():# #TODO this is not windows read pid , only in cyg ps, use Win.getpid
	pid=os.getpid()
else:# *nix etc..， #TODO:isAndroid
	pid=os.getpid()
				
if isnix():
	def isroot():
		return os.getuid()==0
	
	def sudo(cmd,password):
		'''cmd can use pipe 'id|cut -c 2-22'
		'''		
		from subprocess import call
		return call("echo {} | sudo -S {}".format(password, cmd), shell=True)
		#  0
	
########################## end init #############################################
def retry( exceptions,times=3,sleep_second=0):


	"""
	Retry Decorator

	Retries the wrapped function/method `times` times if the exceptions listed
	in ``exceptions`` are thrown

	:param times: The number of times to repeat the wrapped function/method
	:type times: Int
	:param Exceptions: Lists of exceptions that trigger a retry attempt
	:type Exceptions: Tuple of Exceptions
	"""

	if not py.iterable(exceptions):exceptions=[exceptions]
	
	def decorator(func):
		def newfn(*args, **kwargs):
			attempt = 0
			while attempt < times:
				try:
					return func(*args, **kwargs)
				except Exception as e:
					for i in exceptions:
						if isinstance(e,i):
							log(
								'Exception thrown when attempting to run %s, attempt '
								'%d of %d' % (func, attempt, times),
								exc_info=True
							)
							attempt += 1
							if sleep_second:sleep(sleep_second)
							break
					else:#when no break
						raise e
			return func(*args, **kwargs)
			
		return newfn
		
		
	return decorator
		
#TODO: if not has ei,import error occur twice,why?


def get_test_path():
	if isnix():
		s='/test/'
		home=os.getenv('HOME')
		if not home:
			if istermux():
				home='/data/data/com.termux/files/home'
			#elif 添加其他情况
			else:
				home=''
		if home.startswith('/home/coding'):
			home+='/workspace'
		return get('U.gst',home+s)
	if iswin() or iscyg():
		return get('U.gst',driverPath('c:/test/'[1:]))
get_gst=getTestPath=get_test_path
gst=gsTestPath=get_test_path()

def set_test_path(sp):
	global gst,gsTestPath
	sp=sp.replace('\\','/')
	if not sp.endswith('/'):
		sp+='/'
	gst=gsTestPath=set('U.gst',sp)
	return gst
setgst=set_gst=setTestPath=set_test_path

def getShellPath():
	'''wsPath=G:\QGB\babun\cygwin\home\qgb\wshell\
	'''
	if isnix():s='/bin/qgb/'
	if iswin() or iscyg():
		if 'wsPath' in os.environ:
			s=os.environ['wsPath']
		s='G:/QGB/babun/cygwin/home/qgb/wshell/'#如果开头多一个空格，在Pycharm 下返回False，其他环境下为True
		s=driverPath(s[1:]) or s
	return s.replace('\\','/')
gsw=gsWShell=getShellPath()


def pln(*a,**ka):
	'''pln *data,  [en]cod[ing]='gb18030' ,r=False
	if r 应该返回参数  [U.pln(i) for i in _211]
	应该正确处理 中文 list dict ...'''
	# def den(k):
		# if py.type(k) is py.unicode:k=k.encode(encoding)
		# if py.type(k) is py.str:
			# rd=T.detect(k)
			# if rd.popitem()[0]>0.9:dc=rd[1]
			# else:dc=decoding
			# k=k.decode(dc).encode(encoding)
		# return k
	if 	'end' not in ka:ka['end']='\n'
	return p(*a,**ka)	
println=pln
	
def print_(*a,**ka):
	'''
 # in  py 3.6
	print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)
	----> 1 sys.stdout.write(_21)
	TypeError: write() argument must be str, not bytes
	sys.stdout.write('[\u9999')#[香

	in 2.7
	# print(k,end='')#SyntaxError: invalid syntax in 2.7 ;use from __future__ import print_function
	U.p(123,456,file=file ,end='\n')#  输出多个参数没有正确换行
iterable 的元素,没有特殊处理
	'''
	cod=''
	r=False
	sep=' '
	end=''
	file=sys.stdout
	def write(data,default_encoding='utf-8'):
		b='b' in py.getattr(file,'mode','')
		if py.istr(data):
			if b:file.write(data.encode(encoding))
			else:file.write(data)
		elif py.isbyte(data):
			if b:file.write(data)
			else:file.write(data.decode(encoding))
		else:
			raise ArgumentError('write bytes or str')
			
	flush=True#default
	for k in ka:
		k=k.lower()
		if 'sep'   in k:sep  =ka[k];continue
		if 'end'   in k:end  =ka[k];continue
		if 'file'  in k:file =ka[k];continue
		if 'flush' in k:flush=ka[k];continue
		if 'cod'   in k:cod  =ka[k];continue# 解码
		if 'r'     in k:r    =ka[k];continue#  放最后，防止名字冲突
	if py.len(a)==0:#print (end='233') #233
		write(end)
		if flush:
			if getattr(file,'flush',None):file.flush()
# in npp pythonScript :  AttributeError: 'Console' object has no attribute 'flush' 
		return
	if py.len(a)==1:
		a=a[0]
		at=py.type(a)
		# if a=='':file.write(a)#no effect;	#u''==''#True
		if cod:a=a.decode(cod)
		if py.is2():
			if at is py.unicode:a=a.encode(encoding)#编码
			# elif not py.istr(a):
		a=py.str(a)	
		write(a)
		p(end=end,file=file,flush=flush)
		if r:return a
		else:return
	elif py.len(a)>1:
		# if 'sep' in ka.keys():sep=ka['sep']
		# else:sep=' '
		for i in a:
			p(i  ,sep='no useful',r='no useful',end='',file=file,flush=flush,cod=cod)
			p(sep,sep='no useful',r='no useful',end='',file=file,flush=flush,cod=cod)
			#只能使用一个参数位置，不然死循环,最后结尾sep
		p(end,sep='no useful',r='no useful',end='',file=file,flush=flush,cod=cod)
	if r:return a
	else:return
p=print_
# p(4,2,sep='9')
# exit()
def input(msg=''):
	if py.is2():
		return raw_input(msg)
	else:
		return input(msg)

def readStdin(size=-1):
	'''size<0 read all, 
	If the size argument is negative or omitted, read until EOF is reached.'''
	if not stdin.isatty():
		if iswin():
			stdin.seek(0)
		#linux  io.UnsupportedOperation: underlying stream is not seekable
		return stdin.read(size)
	else: return ''
getStdin=readStdin

def rindex(a,sub,start=0,end=-1):
	''' 'print(dir())'
		 _14[::-1]
		 '))(rid(tnirp' 
 '''
	return py.len(a)-a[::-1].index(sub)
def flat(*a,**options):
	'''Breadth-First Traversal'''
	noNone=False
	for o in options:
		if 'nonone' in o.lower():noNone=options[o]
		if one_in('isnone','hasnone', o.lower()):noNone=not options[o]
		# repl()
		
	a=py.list(a);r=[];i=0
	while i<py.len(a):
		# str has __iter__ in py3
		if hasattr(a[i], '__iter__'):a.extend(a[i])
		else:
			if noNone and not a[i]:pass
			#TODO other condition
			else:r.append(a[i])
		i+=1
	# repl()
	return tuple(r)
	
# pln flat([[1,2,3], [5, 2, 8], [7,8,9]])
##(1, 2, 3, 5, 2, 8, 7, 8, 9)
# pln flat([1,2,3,[4,5,[1,2],6]],['aaa'])
##  (1, 2, 3, 'aaa', 4, 5, 6, 1, 2)
	
def md5(a='',file=''):
	'''[a] : string or buffer
	[file]:fileName
	return 32 hex(lowerCase) str'''
	import hashlib   
	
	if file:
		myhash = hashlib.md5()
		f = py.open(file,'rb')
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

def getMethod(a,func):
	if callable(func):
		func=py.getattr(func,'__name__',None)
	if T.istr(func):
		fs=[]
		for i in py.dir(a):
			if i.startswith(func):
				i=py.getattr(a,i,None)
				if py.callable(i):fs.append(i)
		if py.len(fs) >1:raise ArgumentError('need unique func(Name) for a')
		return fs[0]
	return func
getmethod=getMethod

def inMulti(target,elements,*functions):
	if not functions:functions=[None]
	functions=py.set(flat(functions))
	r=[]
	for f in functions:
		for e in elements:
			if f==None:
				if target in e:r.append(e);continue
				continue
			method=getMethod(target,f)
			if method(target):r.append(e);continue
			elif py.callable(f):
				if f(target,e):r.append(e);continue
			#else: # 参数函数 无效
	return r
def multin(elements,target,*functions):
	'''函数为None时：element in target
	element.f(target) #  target.f(element) : py.map
	or f(element,target)
	只要element满足一个函数 ：就会作为结果添加。
		要想得到所有 函数结果，怎么办？
		要想 element满足所有函数，怎么办？ '''
	if not functions:functions=[None]
	functions=py.set(flat(functions))
	if DEBUG:pln(functions)   #set(['startswith', None])=={None, 'startswith'}
	r=[]
	for f in functions:
		for e in elements:
			if f==None:
				if e in target:r.append(e);continue
				continue
			method=getMethod(e,f)
 # '123'.startswith
 # <function startswith>
 # _('1')
 # True
			if method:
				if method(target):r.append(e);continue
#当 混用 inMulti 和 multin 时，注意调用参数应该交换，否则 --> 376 TypeError: startswith first arg must be str, unicode, or tuple, not list				
			elif py.callable(f):
				if f(e,target):r.append(e);continue
			#else: # 参数函数 无效
	return r
def mutin(la,a,func=None):
	'''#TODO : 重写 multin ,同时支持多个函数，方法，func=None 代表 xs[i] in a: '''
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
def in_one(v,*ts):
	'''if v in i:return [v]
U.in_one('p',*Out.values())
Out[142]: ['p']
	'''
	for i in ts:
		try:
			if v in i:return [v]
		except:pass
	return []	
inOne=in_one
def all_in(vs,*t):
	'''for i in vs:i all_in t 
	U.all_in(py.list(string),T.PATH_NAME)  
	
	(1,2,3,[t])	or	([vs].[t])'''
	if not hasattr(vs, '__iter__'):vs=[vs]
	if len(t)==1:
		t=t[0]
	elif len(t)>1:
		vs.extend(t[:-1])
		t=t[-1]
	else:raise Exception(all_in.__doc__)
	# U.pln(vs,t)
	if DEBUG:pprint((vs,'*t:',t)  )
	for i in vs:
		try:
			if i not in t:return []
		except:return []
	return vs
allIn=all_in	
def in_all(v,*ts):
	for i in ts:
		try:
			if v not in i:return []
		except:pass
	return [v]
inAll=in_all
##########################################
def join_as_cmd_str(args,*a):
	import shlex
	a=py.list(a)
	if py.istr(args):
		a.insert(0,args)
	elif py.iterable(args):
		a=py.list(args)+a
	return ' '.join(shlex.quote(x) for x in a)
joinCmd=join_cmd=cmdJoin=cmd_join=shlex_join=join_as_cmd_str

def split_cmd_str(a):
	import shlex
	return shlex.split(a)
splitCmd=split_cmd=cmdSplit=cmd_split=shlex_split=split_cmd_str

def cmd(*a,**ka):
	'''show=False :show command line
	默认阻塞，直到进程结束返回
	if 'timeout' not in ka:ka['timeout']=9     ## default timeout
	
	stdin : str,bytes
	'''
	if iswin() or iscyg():quot='"'
	else:quot="'"
	
	if len(a)==0:
		if iswin() or iscyg():
			a=['cmd']
			if 'timeout' not in ka:ka['timeout']=9
			log('wait cmd.exe 9 sec ...')
		else:
			raise ArgumentError('commands not null',a,ka)
		# TODO #
	if len(a)==1:
		a=a[0]
		if py.istr(a):
			if (' ' in a) and not a.startswith(quot):
				a=split_cmd_str(a)
				# in linux,can't U.cmd("'ls'") ?
				# if iswin():
				# a=quot+a+quot
			elif ':' in a and iscyg():
				a='cmd /c start "" '+ a
			# else:
			# 	a=a
				

	import subprocess as sb	
	
	show   =get_duplicated_kargs(ka,'show','echo')
	stdin  =get_duplicated_kargs(ka,'stdin','input')
	timeout=get_duplicated_kargs(ka,'timeout',default=9)
	
	if show:pln (a)
	if stdin:
		if py.is3() and py.istr(stdin):
			stdin=stdin.encode(gsencoding)
		if not py.isbyte(stdin):
			raise ArgumentUnsupported('stdin type',py.type(stdin),stdin  )
		ka['input']=stdin
		# r.stdin.write(stdin)
	ka['timeout']=timeout     ## default timeout
	
	try:
		# if timeout:
		# r=sb.check_out(a,**ka)
		r=sb.run(a,capture_output=True,**ka)
	except Exception as e:
		print_traceback()
		return py.No('sb.run err', e,a,ka)

	try:
		so=T.auto_decode(r.stdout)
		se=T.auto_decode(r.stderr)
		if not se:
			return so
		else:
			return so,se
		# return os.system(s)
	except Exception as e:
		print_traceback()
		return py.No('T.auto_decode err',e,r,a,ka)
	# exit()
# cmd('echo 23456|sub','3','')	

def get_duplicated_kargs(ka,*keys,default=py.No('Not found matched kargs')):
	'''
def pop(d,k):
	d.pop(k)
pop(_63,25)  #_63 has change

'''
	if not py.isdict(ka):raise ArgumentError('ka should be a dict,but get',ka)
	r=[]
	for i in keys:
		if not py.istr(i):raise ArgumentError('keys should be a list of str,but get',i)
		if i in ka:
			r.append(ka[i])
			ka.pop(i)
	if py.len(r)==0:return default
	if py.len(r)>1:
		rTrue=[i for i in r if i]  
		if not rTrue:
			rTrue=py.list( py.set(r) )
		if py.len(rTrue)>1:
			raise Exception('kargs 存在多个 重复的 key',ka,keys)
		r=rTrue
	#######
	if py.len(r)==1:return r[0]
	else:raise Exception('kargs matched keys len <> 1',ka,keys)

getKargsDuplicated=getKArgsDuplicated=get_kargs_duplicated=get_duplicated_kargs

def sleep(aisecond):
	if not aisecond:return
	__import__('time').sleep(aisecond)
	
def pause(a='Press Enter to continue...\n',exit=True):
	'''a=msg'''
	if iswin():
		# cmd('pause');return
		try:
			raw_input(a)
		except BaseException:#SystemExit is BaseException
			if exit:x()
			return False
	return True	

def os_system(str):
	a=split_cmd_str(str)
	if py.len(a)>1 and '"' in str:
		str='"%s"'%str
	return os.system(str)
system=os_system

def run(a,*args,env=py.No('if you want update env,give dict,path will merged')):
	'''默认不阻塞, args converted to list of str
If you're using Pyhton 3, command.args is the easiest way:
	from subprocess import Popen
	command = Popen(['ls', '-l'])
pln command.args #['ls', '-l']

env PATH  无论在Windows 还是 Linux 统一使用大写是好的选择
'''
	F=py.importF()
	if DEBUG:pln (a,args)
		
	if py.istr(a):
		if not args:
			if not F.exists(a):
				import shlex
				a=shlex.split(a)  #如果不想自动拆分第一个参数 可以 run(cmd,'')  ,这样args 不为空
			else:a=[a]
		else:a=[a]
	if not py.islist(a):a=py.list(a)
	if len(args)>0:a.extend(args)
	# if py.islist(a):
	for i,v in enumerate(a):
		if not py.istr(v):
			a[i]=v=str(v)
		if py.iswin() and v.startswith('"') and v.endswith('"'):
			a[i]=v[1,-1]
	# a 处理完了，接着处理env
	if not env:
		env = os.environ
	else:
		try:
			ec=F.dill_loads(F.dill_dump(os.environ) )
		except:
			ec = os.environ.copy()# 返回 dict ，而不是 env

		p=''
		for k in py.list(env.keys()): # RuntimeError: dictionary changed size during iteration
			if k.upper()=='PATH':
				p=env[k]
				env.pop(k)

		ps=get_env_path().split(os.pathsep)
		if p :
			if (p not in ps):ps.append(p)
			env['PATH']=os.pathsep.join(ps)	

		env=ec.update(env)
	######## 参数处理完毕，准备开始运行
	# r= __import__('subprocess').Popen(a)
	import subprocess
	# env["PATH"] = "/usr/sbin:/sbin:" + env["PATH"]
	r=subprocess.Popen(a, env=env) # Windows下 光标有不回位问题 U.run('cmd /c set',env={'zzzzz':U.stime()})
	if getPyVersion()<3.3:r.args=a
	return r
	'''
In [151]: _131.poll?
Signature: _131.poll()
Docstring:
Check if child process has terminated. Set and return returncode
attribute.
File:      c:\qgb\anaconda2\lib\subprocess.py
Type:      instancemethod

In [152]: _131.poll
--------> _131.poll()
Out[152]: 0

In [153]:

In [153]: U.run 'calc'
--------> U.run('calc')
Out[153]: <subprocess.Popen at 0x24415d0>

In [154]: _153.poll
--------> _153.poll()

In [155]: repr _153.poll()
--------> repr(_153.poll())
Out[155]: 'None'

In [156]: repr _153.poll()
--------> repr(_153.poll())
Out[156]: '0'              #killed
'''	
	
def curl(a):
	if type(a)!=type(''):return
	if a.lower().startswith('curl '):
		a=a.replace('""','')
	if a.startswith('http'):
		cmd('curl',a)
	cmd(a)

# def isfile
# del __name__

def delMuti(a):
	r=[]
	rt= type(a)
	for i in a:
		if i not in r:r.append(i)
	if py.istr(rt):
		return ''.join([rt(i) for i in r])
	return r
delmuti=delMuti
def this():
	''' local dir'''
	repl()
	if not py.globals().has_key('__name__'):
		__name__='233qgb.U'
		# txt(globals())
		pln (__name__)

def ipyEmbed():
	# global ipyEmbed
	from IPython import embed
	# ipyEmbed=embed
	ka={'InteractiveShellApp': {'exec_lines': ["from qgb import *"]},
		'TerminalIPythonApp': {'display_banner': False},
		'TerminalInteractiveShell': {'autocall': 2}
	}
	import functools
	return functools.partial(embed,**ka)# useless ?   ka不对？
	return embed
ipy=ipy_embed=embed=ipyEmbed
'''
try:
	sys._path=sys.path[:]                 #  list.copy() method (available since python 3.3):
	# from IPython import embed                       #NOTICE 在 qpsu中不要修改 sys.path 
	# 如果 导入ipython时出错，可能出现 sys._path 是原来，sys.path 被修改的情况
	sys.path,sys._path=sys._path,sys.path
	ipy=ipyEmbed=ipy_embed=embed#IPython.embed
	
	# 'G:\\QGB\\Anaconda2\\lib\\site-packages\\IPython\\extensions',
	# '/usr/local/lib/python3.5/dist-packages/IPython/extensions',
except:
	sys.path,sys._path=sys._path,sys.path
print( [sys.path.remove(i) for i in sys.path 
		if ('IPython' in i and i.endswith('extensions')  ) or i.endswith('.ipython')]	)
'''
#不能保证sys.path 不被修改，暂时放弃

def repl(_=None,printCount=False,msg=''):
	# a=1
	ic=count('__repl__')
	if printCount:pln (ic)
	if msg:pln (msg)
	######################
	f=sys._getframe().f_back
	locals=f.f_locals
	try:
		locals['U']=sys.modules['qgb.U']
		locals['T']=sys.modules['qgb.T']
		locals['F']=sys.modules['qgb.F']
	except:
		locals['U']=sys.modules['U']
		locals['T']=sys.modules['T']
		locals['F']=sys.modules['F']
	# try:
		# locals['U']=__frame.f_locals['U']
	# except:  #KeyError: 'U'  if use in qgb.U Module
		# locals=mergeDict(locals,py.globals())
	if _!=None:
		if '_' in locals:
			locals['_qgb']=_
		else:
			locals['_']=_
	__import__('code').interact(banner="",local=locals)
	return
	
	# try:
		# from ptpython.repl import embed
		# embed(f.f_globals, f.f_locals, vi_mode=False, history_filename=None)
		# return
	# except:pass
repl=pys=pyshell=repl

def reload(*mods):
	''' 不是一个模块时，尝试访问mod._module'''
	import sys,imp
	if len(mods)<1:#如果 mods 中含有长度为0的元素，会导致U重新加载
		# sys.modules['qgb._U']=sys.modules['qgb.U'] #useless, _U is U
		#if pop qgb.U,can't reload
		if 'qgb.U' in sys.modules:   imp.reload(sys.modules['qgb.U'])
		elif 'U' in sys.modules:     imp.reload(sys.modules['U'])
		elif 'qgb._U' in sys.modules:imp.reload(sys.modules['qgb._U'])
		else:raise EnvironmentError('not found qgb.U ?')
		# pln 233
	elif len(mods)==1:
		mod=mods[0]
		if not isModule(mod):
			# sys.a=mod
			# return
			try:
				if py.type(mod) is py.str:
					return reload(sys.modules[mod])
				elif '_module' in py.dir(mod):
					if not isModule(mod._module):raise Exception('instance._module is not module')
					mod=mod._module
					modules[mod.__name__]=mod
					return reload(mod)
					
					# if mod.__name__ in modules:#'qgb.ipy'
				else:
					return py.No('instance._module not exists, It is not a module ?')
			except Exception as em:
				raise em
			
			# else:gbPrintErr=True#在函数局域覆盖全局属性
		try:
			imp.reload(mod)
		except Exception as ei:
			setErr(ei)
	else:
		for i in mods:
			reload(i)
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
	
	
def clear():
	# sys.modules[__name__] = __wrapper(sys.modules[__name__])
	if iswin():os.system('cls')
	if isnix():os.system('clear')
C=c=cls=clear


def chdir(ap=gst,*a,**ka):
	if not ap:ap=gst
	if not py.istr(ap):raise py.ArgumentError('ap must be str Not:{0}'.format(ap))
	ap=path.join(ap,*a)
	

	mkdir=False #默认不创建
	if 'md' in ka:mkdir=ka['md']
	if 'mkdir' in ka:mkdir=ka['mkdir']
	if iscyg():mkdir=False#cyg下可以创建带:的目录，导致切换异常
	if mkdir:F.mkdir(ap)
	
	global gscdb
	# repl()
	# if path.abspath(gscdb) != pwd():
	gscdb.append(pwd())
	
	if path.isdir(ap):
		os.chdir(ap);return ap#True
	
	app=path.dirname(ap)
	if path.isdir(app):return chdir(app)
	else:pass
		
	if iswin() or iscyg():
		if ap[0]=='/'==ap[2] and ap[1] in T.az:#!cdv&pwd == '/c/Users/lenovo/Videos'
			return chdir(ap[1]+':'+ap[2:])
			
	for i in ap:
		if i not in T.PATH_NAME:raise Exception('need file path',ap,i)
	return py.No("#Can't cd "+ap)
cd=chdir

gscdb=[]
def cdBack(index=-1):
	'''False: cd path list []'''
	if gscdb:
		return cd(gscdb[index])
	else:
		return False
cdb=cdBack

def cdCurrentFile(*a):
	f=sys._getframe().f_back.f_globals
	if '__file__' in f:
		sp=os.path.abspath(f['__file__'])
		sp=os.path.dirname(sp)
		return cd(sp,*a)
	return False
cd__file__=cdc=cdCurrent=cdcf=cdCurrentFile

def cdTest(a=''):
	return cd(gst+a)
cdt=cdTest
	
def cdQPSU(a=''):
	return cd(getModPath()+a)
# @property
cdq=cdqp=cdqpsu=cdQPSU
	
def cdWShell(a=''):
	return cd(gsWShell+a)
cds=cdws=cdWShell

def cdpm():
	return cd('e:/pm')
	
def cdbabun(a=''):
	s=r'C:\QGB\babun\cygwin\home\qgb/'
	s=driverPath(s[1:])
	return cd(s+a)
	
def get_current_file_dir():
	frame=sys._getframe().f_back
	g=frame.f_globals
	if '__file__' not in g:
		return py.No('not found __file__ in current module')
	__file__=g['__file__']
	import pathlib
	p=pathlib.Path(__file__)
	sp=p.root#win '\\'  linux '/'
	return p.parent.absolute().__str__() +sp
	
getCurrentFilePath=get_file_dir=get_current_file_dir
	
def pwd(p=False,display=False):
	s=os.getcwd()
	if p or display:pln (s)
	# try:pwd.sp=F.getsp(s)
	# except:pass
	if not py.getattr(pwd,'sp',''):
		pwd.sp='/'
	s=s.replace('\\','/')
	
	return s+pwd.sp#带sp方便使用者拼接路径
getCurrentPath=cwd=pwd
	
def random_choice(*a,**ka):
	import random
	return random.choice(*a,**ka)
	
def randomInt(min=0,max=IMAX):
	'''random.randint(a, b)
Return a random integer N such that a <= N <= b.'''
	import random
	return random.randint(min, max)
randint=ramdomInt=randomInt

def sort(a,column=None, cmp=None, key=None, reverse=False):
	''' py2&py3  sorted _3 ,key=lambda i:len(i)        按长度从小到大排序
	在python2.x  sorted _5,cmp=lambda a,b:len(a)-len(b) 实现同上功能， 一般不用cmp 参数
	sorted中cmp参数指定的函数用来进行元素间的比较。此函数需要2个参数，然后返回负数表示小于，0表示等于，正数表示大于。
	#这句可能写错了 a:item of sort list   |  *a: (item,) 
	'''
	repr=py.repr
	
	def key_func(ai,size=99,is_column=True):# ai :  item of a
		
		if is_column and py.isint(column) and column > -1:ai=ai[column]
		if py.isnum(ai):
			return ai
		elif py.istr(ai):
			r=0xffff_ffff_ffff
			for n,b in py.enumerate(ai[:size][::-1]):
				r+=py.ord(b)*(0x110000**n)
			return r
		elif py.isbytes(ai):
			r=0xffff_ffff
			for n,b in py.enumerate(ai[:size][::-1]):
				r+=py.ord(b)*(256**n)
			return r
		else:
			ai=py.repr(ai)[:size] # 不会再次回到这个分支，istr
			return key(ai=ai,size=size,is_column=False)

	if not key:key=key_func
	#TypeError: '<' not supported between instances of 'int' and 'str';key=None also err
	if py.is2():
		a=py.sorted(a,cmp=cmp,key=key, reverse=reverse)
	else:
		if cmp:#这个 arg 优先级最高
			import functools
			key=functools.cmp_to_key(cmp)
		a=py.sorted(a,key=key, reverse=reverse)
	if py.istr(a):
		return ''.join(a)
	else:
		return a
def sortDictV(ad,key=lambda item:item[1],des=True):
	'''des True,,, python dict key auto sort ?'''
	if type(ad) is not dict:return {}
	return sorted(ad.items(),key=key,reverse=True)
# d={}
# for i in range(7):
	# d[i]=i*i-5*i
	
# d={'ok':1,'no':2}
# d={0: 0, 5: 0, 6: 6, 1: -4, 2: -6, 3: -6, 4: -4}

# d=sortDictV(d)
# exit()
def dictToList(a):
	return py.list(a.items())

def evalSafely(source, globals=None, locals=None,noErr=False):
	''' '''
	if globals==locals==None:
		f=sys._getframe().f_back
		globals=f.f_globals
		locals =f.f_locals		
	try:
		return py.eval(source,globals,locals)
	except Exception as e:
		if noErr:
			return py.No(e)
		else:
			return e
eval=evalSafely

def execStrResult(source, globals=None, locals=None,pformat_kw={}):
	""".pformat(object, indent=1, width=80, depth=None, *, compact=False)
exec('r=xx') ;return r # this has been tested in 2&3
当没有定义 r 变量时，自动使用 最后一次 出现的值 作为r
当定义了 r ，但不是最后一行，这可能是因为 还有一些收尾工作
	
# U.log(locals)
		# body=ast.parse(code).body
		# r_lineno=0
		# for i,b in py.reversed(py.list( enumerate(body) )  ): # 从最后一条语句开始解析，序号还是原来的
			# if isinstance(b, ast.Assign):
				# if b.targets[0].id=='r':
					# r_lineno=i
					# break# r之前的就不管了
			# [ 可能在r 之后 还有表达式 或者 根本没有出现 r ，Expr 都看成 r 
			# if isinstance(b, ast.Expr):
				# Assign
			
	"""
	if globals==None:globals={}
	if locals==None :locals ={}
	try:
		exec(source, globals, locals)
	except Exception as e:
		return py.repr(e)
		
	if 'r' in locals:
		r=locals['r']
		if py.istr(r):return r
		if not pformat_kw:
			pformat_kw=get('pformat_kw',{})
		try:return pformat(r,**pformat_kw)# in U
		except:return py.repr(r)
	else:
		return 'can not found "r" variable after exec locals'+pformat(locals.keys())
execReturnStr=execResult=execStrResult

def execHelp():
	'''use py.execute(s,{g:},{l:})
	is2 ： exec_stmt ::=  "exec" or_expr ["in" expression ["," expression]]
	参数1  字符串，文件对象，代码对象，或者元组。如果它是一个字符串，该字符串将被当做Python 语句组解析，然后执行（除非发生语法错误）。[1] 如果它是一个打开的文件，将解析该文件直到EOF并执行。如果它是一个代码对象，将简单地执行它。对于元组的解释，参见下文。对于所有的情况，都期望执行的代码和文件输入一样有效（参见文件输入一节）。注意即使在传递给exec语句的代码中，return和yield语句也不可以在函数定义之外使用。

在所有情况下，如果可选的部分被省略，代码将在当前的作用域中执行。如果in 之后给出第一个表达式，它应该是一个字典，全局和局部变量都将使用它。如果给出两个表达式，它们将分别用于全局和局部变量。如果给出，局部变量可以是任意一个映射对象。记住在模块级别，全局变量和局部变量是同一个字典。如果给出两个不同的对象作为全局变量 和 局部变量，代码的执行将像是在类定义中一样。

第一个表达式也可以是一个长度为2或者3的元组。在这种情况下，可选的部分必须被省略。exec(expr, globals) 形式等同于exec expr in globals， 而exec(expr, globals, locals) 等同于exec expr in globals, locals。exec 的元组形式提供了与Python 3的兼容性，在Python 3中exec 是一个函数而不是语句。

Changed in version 2.4: Formerly, locals was required to be a dictionary.

As a side effect, an implementation may insert additional keys into the dictionaries given besides those corresponding to variable names set by the executed code. 例如，当前的实现可能以键__builtins__添加一个指向内建模块__builtin__ 的引用(!)。

给程序员的提示：内建函数eval()支持动态计算表达式。内建函数 globals()和locals()分别返回当前的全局变量和局部变量字典，可传递给exec使用。
	diff between eval and exec in python
	exec not return 
		a=exec('1')
		 ^
		SyntaxError: invalid syntax
'''
	return py.help('exec')  # py2 & py3  OK
	# exec(s)

def calltimes(a=''):
	'''U.ct.clear.__dict__
	'''
	a='_count_%s' % T.string(a).__hash__()
	if a in calltimes.__dict__: 
		calltimes.__dict__[a]+=1
	else:
		_ct_clear.__dict__[a]=stime() # 记录首次 初始化的时间，并且只更新不删除？
		calltimes.__dict__[a]=0
	return calltimes.__dict__[a]
ct=count=counter=calltimes
def _ct_clear():
	r=calltimes.__dict__
	calltimes.__dict__={'clear':_ct_clear}
	return {k:v for k,v in r.items() if k.startswith('_count')}
calltimes.clear=_ct_clear


def setLogLevel(level=False):
	''' logging.CRITICAL #50
	'''
	
	if level==True:level=-1 # 0 useless
	if level==False:
		level=50		
		import urllib3
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

		
	
	import logging
	#Disable all logging calls of severity 'level' and below.
	logging.disable(level)
	
	# log.setLevel(logging.NOTSET) #0
	# log.setLevel(logging.CRITICAL) #50
setlog=setLogLevel

def disableLog():return setLogLevel(False)
disable_log=disableLog
def enableLog():return setLogLevel(True)
enable_log=enableLog

def setStd(name,file):
	'''name=[std]out err in'''
	name=name.lower()
	if py.istr(file):
		file=open(file,'w+')
	if py.isfile(file):
		if file.closed:raise ArgumentError('need an opened mode=w+ file')
	if py.len(name)<4:name='std'+name
	d=py.globals()
	if d.has_key('__'+name) and d['__'+name]:
		old=getattr(sys,name)
		old.close()
		py.execute('''sys.{0}=file'''.format(name))
	else:
		
		py.execute("d['__{0}'],sys.{0}=sys.{0},file".format(name))
	return True
setstd=setStd	

def resetStd(name=''):
	name=name.lower()
	if py.len(name)<4:
		std='std'+name
		name='__std'+name
	elif not name.startswith('__'):
		if name.startswith('std'):
			std=name
		name='__'+name
	else:
		raise ArgumentError('stdxxx')
		
	try:
		sm=globals()[name]
		stdm=getattr(sys,std)
	except Exception as e:
		setErr(e)
		return False
	if(sm and sm != stdm):
		stdm.close()#以前设置的std
		py.execute('sys.{0}=sm'.format(std))
	return True
resetstd=resetStd#=resetStream
gsBrowser=''
def browser(url,browser=gsBrowser,b='yandex'):
	'''b,browser='yandex'
	'''
	if istermux():return run('termux-open-url',url) 
	import webbrowser
	if gsBrowser:browser=gsBrowser
	if b:browser=b
	sp=''
	def _open(asp,url):
		b=sys._getframe().f_back.f_code.co_names[-1]#get caller function name 
		webbrowser.register(b, None, webbrowser.BackgroundBrowser(asp))
		return webbrowser.get(b).open_new_tab(url)
	def chrome(url):
		###TODO: auto Find system base everything
		try:sp=getProcessList(name='chrome.exe')[-1].cmdline()[0]
		except:sp='''C:\QGB\Chrome\Application\chrome.exe'''
		_open(sp,url)		
	def yandex(url):
		sp=getProcessList(name='browser.exe')[-1].cmdline()[0]
		_open(sp,url)
	for i in py.dir():
		if not browser:
			webbrowser.open(url)
			break
		if py.eval('callable({0})'.format(i)):
			if browser.lower()== i:
				py.execute('{0}(url)'.format(i) ) in globals(),locals()  
	return url
	# webbrowser.open_new_tab(url)
	# if iswin():os.system('''start '''+str(url))
# browser('qq.com')
def browser_obj(obj,file='',b='yandex'):
	#pformat(obj,indent=3)
	if not file:
		file=stime()+'browser_obj.txt'
	return browser(F.write(data=obj,file=file )    ,b=b)
browserObj=browser_obj

gsHtmlTextarea=('<textarea style="width:100%; height:100%;">','</textarea>')
def autohtml(file=None):
	import T
	if not py.istr(file):
		if file is None:file=stime()+'.html'
		else:
			if hasattr(file,'__name__'):
				if '.htm' not in file.__name__:
					file=file.__name__+'.html'
			else:file='obj_{0}.html'.format(hash(file))
	elif  len(T.filename(file))<1:file=stime()+'.html'
	elif '.htm' not in file.lower():file=file+'.html'
	return file	

	
def shtml(txt,file='',browser=True,b=''):
	# import T,F
	import pprint
	if file=='' and not py.istr(txt):
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
	file=F.write(file,txt)
	# f=open(file+'.txt','a')
	# rm(f.name)
	# txt=txt.replace(gsHtmlTextarea[1],gsHtmlTextarea[1][:1]+'!!!qgb-padding!!!'+gsHtmlTextarea[1][1:])	
	# f.write(gsHtmlTextarea[0])
	# f.write(txt)
	# f.write(gsHtmlTextarea[1])
	# f.close()
	if b:browser=b 
	if(browser):
		if T.istr(browser):
			globals()['browser'](file,browser=browser)
		else:globals()['browser'](file)
	return file
txt=shtml	

def add(*a):
	a=flat(a)
	r=0
	for i in a:
		if py.isnum(i):
			r+=i
		else:
			raise NotImplementedError('not num type')
	return r		
def maxLen(*a):
	if py.len(a)==1:a=flat(a)
	im=-1
	for i in a:
		i=len(i)
		if i>im:im=i
	return im
def minLen(*a):
	if py.len(a)==1:a=flat(a)
	if not a:return -1
	im=gimax
	for i in a:
		i=len(i)
		if i<im:im=i
	return im
def avgLen(*a):
	if py.len(a)==1:a=flat(a)
	if not a:return -1
	im=0
	for i in a:
		im+=len(i)
	return float(im)/len(a)	
	
def printAttr(a,b='chrome',console=False,call=False):
	'''if call: aoto call __methods which is no args
	
	py.dir  request  'werkzeug.local.LocalProxy'  ==   []
	'''
	d=py.dir(a)
	
	if console:
		sk='%-{0}s'.format(maxLen(d))
		si='%-{0}s'.format(len(py.len(  d  )))
		for i,k in py.enumerate(d):
			pln (si%i,sk%k,py.eval('a.{0}'.format(k)))
		return
		
	sh='''<tr>
	 <td>{0}</td>
	 <td id=name>{1}</td>
	 <td><textarea>{2}</textarea></td>
	 <td>{3}</td>
	</tr>'''
	sp=getModPath()+'file/attr.html'
	r='';v='';vi=-1
	for i,k in py.enumerate(d):
		try:
			v=getattr(a,k,'Error getattr')#py.eval('a.{0}'.format(k))			
			vi=len(v)
			# import pdb;pdb.set_trace()
			# if py.callable(v):
				# if k.startswith('__'):
					# vv='# ErrCall {0}()'.format(k)
					# try:
						# if isipy():#在ipython 中存在用户名字空间自动清空的问题
							# pass
						# else:
							# vv=v()
					# except:pass
					# v='{0} == {1}'.format(v,vv)
				
				# v=str(v)
				# v+=getHelp(v)
			if not py.istr(v):
				import pprint				
				try:#  调用非内置函数可能会造成严重的副作用
					if call and py.callable(v) and k.startswith('__'):vv=v()
					else:vv=''
				except Exception as ev:vv='#call Err:'+py.repr(ev)
				if v in (None,True,False) or py.isnum(v):v=str(v)
				else:
					if isinstance(v,(py.list,py.tuple,py.dict,py.set)):
						v=pprint.pformat(v)
					else:
						v='{0}=========== {1} \n{2}'.format(getHelp(v,del_head_line=2),vv,pprint.pformat(v))
		except Exception as e:v=py.repr(e)
		
		v=v.replace(gsHtmlTextarea[0], '*'*33)
		v=v.replace(gsHtmlTextarea[1], '*'*11)
		
		r+=sh.format(i,k,v,vi)
	# cdt('QPSU')
	# import T,F
	name=gst+'QPSU/'
	F.mkdir(name)
	name+=T.filename(getObjName(a))+'.html'
	# pln (name)
	browser(name,b)
	# if not r.strip():py.pdb()
	return F.write(name,F.read(sp).replace('{result}',r),mkdir=False)
	
	
	# cdBack()
pa=printattr=printAttr
# repl()
# printAttr(5)

def dir(a,type_filter=py.No('default not filter'),raw_value=False,**ka):
	'''
	[attr_]filter='',
	skip
	'''
	if py.istr(type_filter):type_filter=type_filter.lower()
	filter=get_duplicated_kargs(ka,'filter','keyFilter','key_filter','attr_filter','attrFilter')
	skip=get_duplicated_kargs(ka,'skip','skipKey','key_skip','skip_key','attr_skip','attrSkip')
	attrs=py.dir(a)
	if filter:
		attrs=[i for i in attrs if filter in i]
	if skip:
		attrs=[i for i in attrs if skip not in i]
	rv=[]
	err=py.No("#can't getattr ")
	for i in attrs:
		ok=True
		v=getattr(a,i) # py.getattr(a,i,err)
		if (not raw_value) and i in {'f_builtins','__builtins__'}:
			v='{} : {}'.format(py.len(v),py.type(v) )
		if (not raw_value) and i in {'f_globals','f_locals'}:
			v='{} : {}'.format(py.len(v),' '.join(v) )
		# if not py.issubclass(type_filter,py.No):# 这里很奇怪，这样判断 type_filter始终不是py.No
		if type_filter:
			# 类型过滤 ,过滤只剩type_filter类型（如果指定了的话）        只要满足以下一条 就ok
			ok=False

			if type_filter==py.callable or type_filter=='callable':
				if py.callable(v):ok=1
				else:             ok=0
			#############
			elif ok or py.type(v) is type_filter or isinstance(v,type_filter) or py.type(v)==py.type(type_filter):
				ok=1
			else:ok=0
			
		if ok:rv.append([py.len(rv),i,v])
	return rv

gAllValue=[]
def dirValue(a=None,filter='',type=None,recursion=False,depth=2,timeout=6,__ai=0):
	'''a=None is dir()
	约定：只有无参数函数才用 getXX  ?'''
	if not __ai:dirValue.start=getTime();dirValue.cache=[]
	r={}
	if getTime()-dirValue.start>timeout:return py.No('#timeout')#r[i]='!timeout %s s'%timeout;break
	
	if a==None:
		import inspect
		f=inspect.currentframe().f_back
		dr=f.f_locals
	else:	
		dr=py.dir(a)
	for i in dr:
		
		try:
			if a==None:
				tmp=dr[i]
			else:
				tmp=getattr(a,i,'!Error getattr')#py.eval('a.'+i)
			if tmp in dirValue.cache:r[i]=('!cache',tmp);continue
			else:dirValue.cache.append(tmp)
			if recursion:
				if __ai>depth:return '!depth reached'
				tmp=dirValue(tmp,filter,type,recursion,__ai=__ai+1,depth=depth,timeout=timeout)
			if filter not in i:continue	
			if type!=None:
				if T.istr(type):type=type.lower()
				if type==py.callable or type=='callable':
					if py.callable(tmp):
						r[i]=tmp
						continue
				if py.type(i)==type or isinstance(i,type):pass
				else:continue	
			r[i]=tmp
				
		except Exception as e:
			r[i]=Exception('can not get value '+i)
			r[i]=e
	return r
DirValue=getdir=getDirValue=dirValue

def searchIterable(a,filter='',type=None,depth=2,ai=0):
	'''iterable
	# typo deepth
	'''
	if ai>depth:return
	r=[]
	for i in a:
		try:
			if filter in i or searchIterable(i,filter,type,depth,ai+1):
				r.append(i)
				if ai==0:continue
				else:break
		except:pass
	return r	
searchIterable.r=[]
findIterable=iterableSearch=searchIterable
def isinstance(obj,Class):
	'''isinstance(obj, class_or_tuple, /)
	#3:isinstance(None, None)#False
#2:TypeError: isinstance() arg 2 must be a class, type, or tuple of classes and types
'''
	try:
		return py.isinstance(obj,Class)
	except Exception as e:
		return py.No(e)

def issubclass(cls, class_or_tuple):
	try:
		return py.issubclass(cls,class_or_tuple)
	except Exception as e:
		return py.No(e)
		
def getObjName(a,value=False):
	try:#is3 len(None)==4
		if a.__name__ and len(a.__name__)>0:
			return a.__name__
	except:pass
	
	try:
		r=str(a.__class__)
		if 'type' in r:
			return T.sub(r,T.quote,T.quote).strip()
	except:pass
	
	if py.isnum(a) and not type(a) is py.float:return 'i_'+str(a)
	if py.istr(a):return 's_'+a[:7]
		
	return str(type(a))
	# exit()
getName=getObjName

def getVarName(a,funcName='getVarName'):
	'''funcName :defined for recursion frame search
	
	在python2中 str unicode 字面相同情况下， == True
	
	'''
	import inspect#,re,T
	for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
		return line[line.index('(')+1:line.rindex(')')].strip()
		#2017-6-24 01:29:13   正常
		
		r=T.sub(line,'(',')')
		if '(' not in r:
			return r
		# if funcName not in line:continue
		# line=T.sub(line,funcName,'').strip()
		# i0=line.find('(')
		# i1=line.find('(',i0+1)
		# if i1==0:return T.sub(line,'(',')').strip()
		# else:
		
		
		pln (repr(line))
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
					pln (il,i,repr(line[il:i])   )
					if line.find(funcName,il,i)!=-1:
						il=il+line[il:i].find('(')+1 
						i =il+line[il:i].rfind(')')
						
						pln (repr(line[il:i].strip())  )
					else:
						pass
					# ra(i,c)
				else:
					return False
	
	# pln il,i,repr(line)
		# if inMuti():return line
name=getArgName=getVarName
# repl()
# exit()
# getVarName(1l)
def ast_parse(source):
	''' _ast.Module  '''
	import ast
	if py.istuple(source):
		source=source[0]
	if py.islist(source):
		source=''.join(source) 
	return ast.parse(source)

def getArgsTest(a,b,c,d=2,**ka):
	return getArgsDict()

def getArgsDict(*args,**kwargs):
	''' MUST BE FIRST LINE in caller 
	#TODO  cache by file,lineno of caller's caller , avoid name searching, only get vars
def tf(*a,k=1,**ka):...
inspect.getargspec(tf) # raise \
ValueError: Function has keyword-only parameters or annotations, use getfullargspec() API which can support them	
	'''
	import inspect,ast
	F=py.importF()
	frame=inspect.currentframe()
	if args or kwargs:
		rd=py.dict(kwargs)
	else:
		frame=frame.f_back
		args=[]
		rd={}
		for k ,v in frame.f_locals.items():
			args.append(v)
		else:
			if args :
				if py.isdict(v):
					rd=v
					args.pop()
				else:rd={}
	if py.getattr(getArgsDict,'debug',0):
		pln(getArgsDict.__name__,'frame','args','rd')
		# return frame,args,rd	
		__import__('pdb').Pdb().set_trace()
	# while F.dir(frame.f_back.f_code.co_filename).endswith('qgb'):
	tb=inspect.getframeinfo(frame.f_back)
	# return frame
	lines, lnum=inspect.findsource(frame.f_back)
	am=ast.parse(''.join(lines) )
	def recursive_find(am):
		for a in py.reversed(am.body):
			if a.lineno > tb.lineno:
				continue
			if py.isinstance(a,(ast.ClassDef,ast.FunctionDef) ):
				return recursive_find(a)
			if py.isinstance(a,(ast.Assign,ast.Expr,) ):
				v=a.value
				if py.isinstance(v,ast.Call) :# and 'arg' in v.func.attr.lower():
					return v
	try:
		for ia,va in enumerate(recursive_find(am).args ):
			name=astToSourceCode(va).strip()
			if name[0]=='(' and name[-1]==')':name=name[1:-1]
			rd[name]=args[ia]
		return rd
	except Exception as e: # name全部获取到了。但是args 少了
		'''
此问题是由于对,*a,**ka 支持不好
先获取调用者的函数，再匹配vars
from inspect import signature 
sg.bind(#vars 如何处理，详细研究下 )    

'''
		log(e)
		v=recursive_find(am) 
		pln('error in',getArgsDict.__name__,'. debug vars return')
		return py.dict(e=e,frame=frame,rd=rd,lines=lines,a=args,v=v,v_args=v.args,   )
	
get_arg=get_args=get_caller_args=getargspec=getargs=getarg=getArgs=get_args_dict=getArgsDict

def getattr(object, *names,default=None):
	''' py2.7 
  File "qgb/U.py", line 1613
	def getattr(object, *names,default=None):                                                        
SyntaxError: invalid syntax  

	'''
	# U=py.importU()
	try:
		r = py.getattr(object, names[0])
		if py.len(names)<=1:
			return r
		else:
			return getattr(r, *names[1:],default=None) # 多重取值，保留出错信息
	except Exception as e:
		if default==None:
			return py.No(e,object,names)
		else:
			return default
			
#npp funcList 不索引注释
def enumerate(a,start=0,ignoreNull=False,n=False):#todo 设计一个 indexList类，返回 repr 中带有index，用下标访问与普通list一样
	'''enumerate(iterable[, start]) -> iterator for index, value of iterable
	
	list <enumerate at 0x6a58d00>
	ignoreNull : return if a[i]
	
	'''
	if n:ignoreNull=True
	r=[]
	# index=start
	for i,v in py.enumerate(a):
		if ignoreNull:
			if not v:continue
		r.append( (start,v) )
		start+=1
	return r
il=ilist=indexList=enumerate

def range(*a):
	'''return list
range(stop) 
range(start, stop[, step]) 
	'''
	return py.list(py.range(*a))
	
def isModule(a):
	return type(a) is module
is_module=isMod=ismod=ismodule=isModule

def getHelp(a,del_head_line=0):
	import pydoc,re
	try:a=pydoc.render_doc(a,'%s')
	except:a='#getHelp Err'
	a=re.sub('.\b', '', a)
	originURL='docs.python.org/library/'
	targetURL='python.usyiyi.cn/documents/python_278/library/{0}.html\n'+originURL
	# msgbox(isModule(a))
	if originURL in a:
		a=a.replace(originURL,targetURL.format(T.sub(a,originURL,'\n')))
	elif isModule(a):
		a=a.replace('NAME',   targetURL.format(T.sub(a,'NAME',' - ').strip() ) )
		# repl()
	if del_head_line:
		a='\n'.join(a.splitlines()[del_head_line:])
	return a
gethelp=getHelp
	
def helphtml(obj,*aos):
	txt=''
	if aos:
		aos=flat(obj,aos,noNone=True)
		for i in aos:
			txt+=getHelp(i)
			txt+='\n==============%s=======================\n'%ct(aos)
	else:txt=getHelp(obj)	

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
	txt=txt.replace(gsHtmlTextarea[1],gsHtmlTextarea[1][:1]+'!!!qgb-padding!!!'+gsHtmlTextarea[1][1:])	
	f=open(file,'w+')
	f.write(gsHtmlTextarea[0]+txt+gsHtmlTextarea[1])
	f.close()
	if(browser==True):globals()['browser'](f.name)
	# pln vars()
	# vars()['browser'](f.name)

def phtml(file):
	raise Exception('#TODO')
	if(file.lower()[-1]!='l'):file=file+'.html'
	# setOut0(file)
	pln (gsHtmlTextarea[0])
def phtmlend():
	raise Exception('#TODO')
	pln (gsHtmlTextarea[1])
	sf=sys.stdout.name
	# resetOut0()
	globals()['browser'](sf)
# dicthtml('uvars.html',vars())

def mergeDict(*a):
	r={}
	for i in a:
		if not py.isdict(i):
			try:i=py.dict(i)
			except:continue
		for k,v in i.items():
			r[k]=v
	return r
merge_dict=mergeDict
	
def mergeList(*a):
	r=[]
	for i in a:
		r.extend(i)
	return r
add_list=addList=merge_list=mergeList

def itime_sec():
	return py.int(timestamp())
itime=itime_sec

def itime_ms():
	return py.int(timestamp()*1000)
itime_js=itime_ms

def strTimeStamp():
	return py.str(getTimestamp())
stimestamp=strTimeStamp	
	
def getTimestamp():
	'''return: float
--------> U.time()
Out[304]: 1490080570.265625

In [305]: U.time
--------> U.time()
Out[305]: 1490080571.125
'''
	return __import__('time').time()
ftime=timestamp=getTimeStamp=getTimestamp

def getTime():
	from datetime import datetime
	return datetime.now()
time=getime=get_time=get_time_obj=get_current_time=getCurrentTime=getTime	

def getDate():
	from datetime import datetime
	return datetime.now().date()
date=getdate=getDate
	
def getFloaTail(a,ndigits=20,s=False,str=False,string=False,i=False,int=False):
	''' see help(round)
 0.1**5
 1.0000000000000003e-05

 0.1**4
 0.00010000000000000002 小数位数20
 '''
 
	if type(a) is float:
		a=round(a-py.int(a),ndigits)#This always returns a floating point number.
		if s or str or string:
			return py.str(a)[1:]
		if i or int:
			return py.int(py.str(a)[2:])#
		return a	
				
def stime_(time=None,ms=True):
	r=getStime(time=time,ms=ms)
	return T.regexReplace(r,'[^0-9_]','_')
	
gsTimeFormatFile='%Y-%m-%d__%H.%M.%S'
gsymd=gsYMD=gsTimeFormatYMD='%Y%m%d'
gsTimeFormat='%Y-%m-%d %H:%M:%S'
#ValueError: year=1 is before 1900; the datetime strftime() methods require year >= 1900

def getStime(time=None,format=gsTimeFormatFile,ms=True):
	'''http://python.usyiyi.cn/translate/python_278/library/time.html#time.strftime
	TODO: 可以指定 ms'''
	if not py.istr(format):raise ValueError('format is str')
	
	import time as tMod
	
	# if ':' in format:format=gsTimeFormatFile.replace('.',':')
	
	if not py.isnum(time):time=getTimestamp()#TODO:  转换 字符串 或其他时间格式
	if not time:time=0.000001
	if py.type(time) is not py.float:time=py.float(time)
	if format=='':return str(time)
	
	if '%' in format:
		if time:
			r=tMod.strftime(format,tMod.localtime(time))
#localtime: time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=8,....
			if type(time) is float and ms:
				if '__' in format:
					if not r.endswith('__'):r+='__'
				# else:#r endswith '.' 
					# pass
				r+=getFloaTail(time,ndigits=3,s=True)#include dot .
			return r
		else:return tMod.strftime(format)
stime=getCurrentTimeStr=timeToStr=getStime
	
def float(x):
	''' float(x=0, /)  Subclasses:     float64
0.07999999999999999  hangs	
	'''
	r=py.float(x)
	# for i in range(99):
	while True:
		s=py.str(r)
		if '0'*12 in s:
			r-=(0.1**16)
		elif '9'*12 in s:
			r+=(0.1**16)
		else:
			break
	return r

def int(a,default=None):
	# if not a:return default
	try:
		return py.int(a)
	except Exception as e:
		if default!=None:
			return default
		return py.No(e)
	
def primes(n):
	''' 

	'''
	#in py3 filter return	<filter at 0x169a9704e80>
	r=filter(lambda x: not [x%i for i in py.range(2, int(x**0.5)+1) if x%i ==0], py.range(2,n+1))	
	return py.list(r)

def isPrime(n, k=5): # miller-rabin
	from random import randint
	if n < 2: return False
	for p in [2,3,5,7,11,13,17,19,23,29]:
		if n % p == 0: return n == p
	s, d = 0, n-1
	while d % 2 == 0:
		s, d = s+1, d/2
	d,n=py.int(d), py.int(n)
	for i in range(k):
		x = pow(randint(2, n-1), d, n)
		if x == 1 or x == n-1: continue
		for r in range(1, s):
			x = (x * x) % n
			if x == 1: return False
			if x == n-1: break
		else: return False
	return True
is_prime=isPrime

def prime_factorization(n, b2=-1, b1=10000): # 2,3,5-wheel, then rho
	'''
https://stackoverflow.com/questions/51533621/prime-factorization-with-large-numbers-in-python 
	'''
	if not py.isnum(n):raise ArgumentError(n)
	n=py.int(n)
	def gcd(a,b): # euclid's algorithm
		if b == 0: return a
		return gcd(b, a%b)
	def insertSorted(x, xs): # linear search
		i, ln = 0, len(xs)
		while i < ln and xs[i] < x: i += 1
		xs.insert(i,x)
		return xs
	if -1 <= n <= 1: return [n]
	if n < -1: return [-1] + factors(-n)
	wheel = [1,2,2,4,2,4,2,4,6,2,6]
	w, f, fs = 0, 2, []
	while f*f <= n and f < b1:
		while n % f == 0:
			fs.append(f)
			n /= f
		f, w = f + wheel[w], w+1
		if w == 11: w = 3
	if n == 1: return fs
	h, t, g, c = 1, 1, 1, 1
	while not isPrime(n):
		while b2 != 0 and g == 1:
			h = (h*h+c)%n # the hare runs
			h = (h*h+c)%n # twice as fast
			t = (t*t+c)%n # as the tortoise
			g = gcd(t-h, n); b2 -= 1
		if b2 == 0: return fs
		if isPrime(g):
			while n % g == 0:
				fs = insertSorted(g, fs)
				n /= g
		h, t, g, c = 1, 1, 1, c+1
	n=py.int(n)
	return insertSorted(n, fs)
factors=integer_factorization=prime_factorization
# (1917141215419419171412154194191714)
# [2, 3, 13, 449941L, 54626569996995593878495243L]
def product_of_integers(*a):
	r=1
	for i in a:
		r=r*i
	return r
multiplication=product_of_integers

def multiply_by_multiples(iterable,times):
	''' r=a,b,c=list(map((2).__mul__, [1, 2, 3]))
	'''
	if py.iterable(times):
		iterable,time=time,iterable
	times=py.float(times)
	mul=lambda a:times*py.float(a)
	r=py.map(mul,iterable)
	return py.list(r)
mul=mutiply_iterable=mutiply_list=mutiply_tuple=multiply_by_multiples

def traverseTime(start,stop=None,step='day'):
	'''
	#TODO ipy 自动化测试框架 ， 解决 ipy3 兼容问题
	range(start, stop[, step])
	datetime.timedelta(  days=0, seconds=0, microseconds=0,
				milliseconds=0, minutes=0, hours=0, weeks=0)
	step default: 1(day)  [1day ,2year,....]  [-1day not supported]'''
	import re,datetime as dt
	sregex='([0-9]*)(micro|ms|milli|sec|minute|hour|day|month|year)'
	timedeltaKW=('days', 'seconds', 'microseconds',
 'milliseconds', 'minutes', 'hours', 'weeks')
	if py.istr(step):
		step=step.lower()
		rm=re.match(sregex,step)
		if not rm or not step.startswith(rm.group()):
			raise Exception('Invalid argument step '+py.repr(step))
		istep,step=int(rm.group(1),default=1,error=0),rm.group(2)
		if step.startswith('year'):
			istep,step=365*istep,'day'#没考虑闰年
		if step.startswith('ms'):step='milliseconds'
		astep={}
		for i in timedeltaKW:
			if i.startswith(step):
				astep[i]=istep
		tdelta=dt.timedelta(**astep)
	elif py.type(step) in (py.int,py.long):
		tdelta=dt.timedelta(days=step)
	elif py.type(step) is py.type(dt.timedelta.min):
		tdelta=step
	# return tdelta
	start=datetime(start)
	if stop:stop=datetime(stop)
	else:stop=dt.datetime.max
	while start<=stop:
		start+=tdelta
		yield start
	# return i #SyntaxError: 'return' with argument inside generator
rangeTime=timeRange=timeTraverser=timeTraversal=traverseTime	

def datetime(a,month=0, day=0,hour=0,minute=0,second=0,microsecond=0):
	''' a : string
	return datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

The year, month and day arguments are required. tzinfo may be None, or an
instance of a tzinfo subclass. The remaining arguments may be ints or longs.
	'''
	from datetime import datetime as dt
	import re
	if py.type(a) is py.type(dt.min):
		return a
	elif py.istr(a):
		rm=re.match('([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}).([0-9]{2}).([0-9]{2}) .([0-9]{3})',a)
		if rm:
			a=T.parseReMatch(rm,'i'*6)+(py.int(rm.group(7))*1000,)
			return dt(*a)
		
		if re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}',a) or\
		re.match('[0-9]{4}-[0-9]{4}',a):a=a.replace('-','')
		if re.match('[0-9]{8}',a):
			return dt(py.int(a[:4]),
				py.int(a[4:6]),py.int(a[6:8]))
	elif py.type(a) in (py.float,py.int):
		return dt.fromtimestamp(a)
	else:
		raise ArgumentError(a)
		
		
		# if '-' in a and py.len:
from threading import current_thread
getCurrentThread=currentThread=current_thread

from threading import enumerate as getAllThreads
threads=gethreads=getThreads=getAllThreads
def get_all_tid():
	r=()
	for threadId, stack in sys._current_frames().items():
		r+=(threadId,)
	return r
	


SG_EXIT='exit'
SG_ASK='ask'
__bsg=False
def __single(port,callback,reply):
	import socket
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
			if(DEBUG):pln (e ,'#%s#'%str(e)  )
			continue
	connection.close()   

def notsingle(port,ip='127.0.0.1'):
	try: 
		import socket
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
	return py.list(y())
	
	# exit()
# pln methods([])	
	
def x(msg=None):
	'''sys.exit'''
	if(msg!=None):pln (msg)
	sys.exit(235)
	
def exit(i=2357,msg=None):
	'''terminate process,will not call atexit'''
	if msg==None:msg='\n{} pid {} exit!'.format('#'*22,pid)
	print(msg)
	os._exit(i)

def getModulesByFile(fileName):
	'''
	return dict {sname:mod ...}
	
('google', <module 'google' (namespace)>) argument of type 'NoneType' is not iterable             
('zope', <module 'zope' (namespace)>) argument of type 'NoneType' is not iterable                 
('mpl_toolkits', <module 'mpl_toolkits' (namespace)>) argument of type 'NoneType' is not iterable 

 <module 'mpl_toolkits' (namespace)> .
'''
	dr={}
	dnf={}
	for name in py.list(sys.modules.keys()):
		mod=sys.modules[name]
		file = py.getattr(mod,'__file__','')#  用getattr， 导致获取失败。。
		if not file:
			dnf[name]=mod
			continue
		if fileName in file:
			dr[name]=mod
	# if py.len(r)==1:return r[0]
	if not dr:return py.No('can not found {} in sys.modules __file__ '.format(fileName),dnf)
	return dr
	
modulesByFile=getModsByFile=getModulesByFile
	
def getModsBy__all__(modPath=None):
	r=[]
	if modPath==None:modPath=getModPath()
	modPath=F.getPath(modPath)
	fs= F.ls(modPath,t='r')
	for f in fs:#大写 畸形 不考虑
		if not f.endswith( '__init__.py'):continue
		content= F.read(f)
		ia=T.re_search('\s*__all__\s*=\s*.*',content)
		if '[' in ia and ']' in ia:
			i=T.sub(ia,'[',']')
		else:
			if '[' not in  ia:
				# print(i[0][-30:-10],'[   ] 都没有',repr(i[1]))
				ct('n [');
				continue
			i=T.sub(content,ia,']')
		i=evalSafely('['+i+']',noErr=1)
		if not i:ct('n i');continue
		r.append(i)
		try:
			print(f[-17-12:-12], i [:8] )
		except Exception as e:
			return f,i
	# for i in:
	return r
	fs=[i for i in fs if i.lower().endswith('.py')]
	
	
def getAllMods(modPath=None):
	r=[]
	if not modPath:modPath=getModPath()
	if 'F' in globals():
		for i in F.ls(modPath,t='r'):
			if not i.lower().endswith('.py'):continue
			i=i.replace(modPath,'')
			# if F.isPath(i):
			if i.lower().endswith('__init__.py'):
				if i.startswith('__init__.py'):continue#/qgb/*  去除qgb
				r.append(path.dirname(i))
			elif '__' not in i:
				r.append(T.subLast(i,'','.'))
	else:raise EnvironmentError('no qgb.F in U')
		# return r
	for i in os.listdir(modPath):
		if(len(i)<3):continue
		if(i.find('__')!=-1):continue
		if(i.lower()[-3:]!='.py'):continue
		r.append(i[:-3])
	if r:return [i.replace('/','.') for i in r]
	else:return   ['U', 'T', 'N', 'F', 'py', 'ipy', 'Win', 'Clipboard']
getAllMod=getAllModules=getAllMods
def getModPathForImport():
	return getModPath(qgb=False)
	sp=os.path.dirname(getModPath())# dirname/ to dirname
	sp=os.path.dirname(sp)
	if iswin():return sp#cygwin None
	else:raise NotImplementedError('todo: cyg  nix')

def get_qpsu_file_path(fn='',base='file/'):
	qpsu=getModPath()+base
	fn=qpsu+fn
	return fn
qpsu_file=get_qpsu_file_path=getQPSUFilePath=getQpsuFilePath=get_qpsu_file_path

def getModPath(mod=None,qgb=True,slash=True,backSlash=False,endSlash=True,endslash=True,trailingSlash=True):
	'''不返回模块文件，返回模块目录
	@English The leading and trailing slash shown in the code 代码中的首尾斜杠'''
	# if mod:
		# sp=os.path.abspath(mod.__file__)
	if mod:sp=os.path.abspath(getMod(mod).__file__)
	else:sp=__file__
	sp=os.path.abspath(sp)
	sp=os.path.dirname(sp)
	sp=os.path.join(sp,'')
	#sp is qgb\ if qgb/.. import
	# if debug():py.pdb()
	if iscyg():#/usr/lib/python2.7/qgb/  
		sp=getCygPath()+sp[1+4:].replace('/','\\')
	if not qgb:
		sp=sp[:-4]
	
	if not endslash or not endSlash:trailingSlash=False
	if trailingSlash:
		if sp[-1] not in ('/','\\'):sp+='/'
	else:
		while sp[-1] in ('/','\\'):
			sp=sp[:-1]
			
	if backSlash or not slash:
		sp=sp.replace('/','\\')
	else:sp=sp.replace('\\','/')

	return sp
get_qpsu_path=getQPSUPath=getQpsuPath=get_qpsu_dir=getQPSUDir=get_module_dir=get_module_path=getModPath

def slen(a,*other):
	return py.repr(len(a,*other) )
	
def len(obj,*other):
	'''Exception return py.No or [no...]'''
	if py.isgen(obj):
		obj=py.list(obj)
	return builtinFuncWrapForMultiArgs(builtinFunc=py.len,args=(obj,other) )# ,default=default

def hash(obj,*other):
	'''Exception return py.No or [no...]'''
	if py.islist(obj):
		if other:return py.No('#TODO hash multi list ',obj,len(other))
		try:
			return py.hash(py.tuple(obj))
		except Exception as e:
			return py.No(e)
	return builtinFuncWrapForMultiArgs(builtinFunc=py.hash,args=(obj,other))
def id(obj,*other):
	return builtinFuncWrapForMultiArgs(builtinFunc=py.id,args=(obj,other))

def builtinFuncWrapForMultiArgs(builtinFunc,args,default=None):
	'''Exception return py.No'''
	obj,other=args ########## other is tuple
	all=py.list(other)
	all.insert(0,obj)
	r=[]
	for i in all:
		try:
			r1=builtinFunc(i)
		except Exception as e:
			if default!=None:
				r1=default
			r1=py.No(e)
		r.append(r1)
	if other:
		return r
	else:
		return r[0]  #U.len(obj) == py.len(obj)

def recursive_basic_type_filter(obj):
	''' dict,tuple,list,set  '''
	def isbasic(a):
		return py.istr(a) or py.isnum(a) or py.isbyte(a)
	if isbasic(obj):return obj
	if py.isdict(obj):
		return {k:recursive_basic_type_filter(v) for k,v in obj.items()}
	if py.type(obj) in (py.tuple,py.list,py.set):
		return [recursive_basic_type_filter(v) for v in obj]
	return py.repr(obj)
basic_filter=basicFilter=filter_basic=filterBasic=filter_basic_type=recursive_basic_type_filter
	
def dis(a):
	import dis
	if py.istr(a):
		a=compile(a,'<str>','exec')
	return dis.dis(a)

def getCallExpression(*a,**ka):
	co=sys._getframe().f_back.f_code
	ast=getAST(co)
	r=ast_to_code(ast)
	if r.endswith('\n'):
		r
	return r
getCallExpr=getCallExpression

def set_env_path(append=[],delete=[]):
	# if not p :raise py.ArgumentError()
	if py.istr(append):append=[append]
	if not py.islist(append):append=py.list(append)

	if py.istr(delete):delete=[delete]
	if not py.islist(delete):delete=py.list(delete)
	if '' not in delete:delete.append('')
	
	ps=os.environ['PATH'].split(os.pathsep)
	for p in append:
		if (p not in ps):ps.append(p)
	for p in delete:
		if (p in ps)    :ps.remove(p)
	os.environ['PATH']=os.pathsep.join(ps)		
	return ps

def getEnviron(name='PATH'):
	'''
linux:
	os.getenv('path')==None                
	os.getenv('PATH')=='/root/qshell/:/usr

'''	
	import os
	# r=os.getenv(name)
	# if r:return r
	
	name_upper=name.upper()
	if name_upper=='PATH':
		return os.environ['PATH'].split(os.pathsep)

	for i in  os.environ:
		if i.upper()==name_upper:
			return os.environ(i)
	return py.No('not found in os.environ',name)
get_env_path=get_path_env=get_environ=get_env=getenv=getEnv=getEnviron
	
def getParentPid():
	import psutil
	return psutil.Process(os.getpid()).ppid()
getppid=getParentPid	
	
def getParentCmdLine():
	import psutil
	return psutil.Process(getppid()).cmdline()
getpargv=getParentCmdLine	

def getProcessByPid(pid):
	'''process_name = process.name()'''
	import psutil
	return psutil.Process(pid)			 
									
def getProcessList(name='',cmd='',pid=0):
	'''if err return [r, {i:err}  ]
_62.name()#'fontdrvhost.exe'
_62.cmdline()#AccessDenied: psutil.AccessDenied (pid=8, name='fontdrvhost.exe')
pid=0, name='System Idle Process', cmdline=[]
	
'''
	import psutil
	r=[]
	err=py.dict()
	for i in psutil.process_iter():
		try:
			i.cmd=' '.join(i.cmdline())
		except Exception as e:
			i.cmd=str(e) #NoneObj #TODO 需要一个 空字符 类，携带出错或其他信息				

		if pid:
			if pid==i.pid:r.append(i)
			continue# 找到 找不到 ，都下一条
		if cmd:
			if cmd in i.cmd:r.append(i)
			continue			
		# if name:
		iname=i.name()
		if name.islower():iname=iname.lower()# 忽略大小写匹配,(是否应该限定在Windows？)
		if name in iname:r.append(i)
		else:continue
				
		# except Exception as e:err[i]=e
	# r=py.list
	# if err:return r,err
	# else:  
	return r
ps=getTasklist=getProcess=getProcessList

def getProcessPath(name='',pid=0):
	if not (name or pid):pid=globals()['pid']
	r=getProcessList(name=name,pid=pid)
	rs=[]
	if r:
		for i,p in enumerate(r):
			i=p.cmdline()
			if i:i=i[0]
			else:continue# 'System Idle Process', cmdline=[]
			if i not in rs:rs.append(i)
		if py.len(rs)!=1:raise Exception('multi path',rs)
		return rs[0].replace('\\','/')
	else:
		return ()
psp=getProcessPath
def kill(a,caseSensitive=True,confirm=True):
	'''TODO:use text Match if any
	'''
	import psutil,subprocess
	if isinstance(a,subprocess.Popen):a=a.pid
		
	ta=py.type(a)
	r=[]
	
	if ta in (py.str,py.unicode):
		for i in psutil.process_iter():
			if caseSensitive:
				if i.name() == a:r.append(i)
			else:
				if i.name().lower() == a.lower():r.append(i)
	elif ta is type(0):
		if not psutil.pid_exists(a):
			raise ArgumentError('pid %s not exist!'%a)
		r=[psutil.Process(a)]
	else:
		raise ArgumentUnsupported()
	if confirm:
		pprint(r)
		c=raw_input('kill Process？(n cancel)')
		if c.lower().startswith('n'):return
	for i in r:
		i.kill()

def get_obj_file_lineno(a,lineno=0,auto_file_path=True):
	T=py.importT()
	args=py.getattr(a,'args',None)
	if args and py.iterable(args):
		args=py.list(args)
		if py.len(args)==3 and '-n' in args[2]: #isWin() and
			ls=T.int_filter(args[2])
			if ls:lineno=py.int(ls[0])
			f=args[1]
			return f,lineno
		# if py.istr(args[0]) and nppexe in args[0].lower():return run(args)
	
	if isModule(a):
		f=a.__file__
		return f,lineno
		
	a=py.getattr(a,'func_code',None) or a
	a=py.getattr(a,'__code__',None)  or a#is3
	
	if py.getattr(a,'co_filename',None): 	
		if not lineno:lineno=a.co_firstlineno#先获取lineno,再改变 a
		f=a.co_filename
		return f,lineno
	if py.getattr(a,'lineno',None):#is3 <FrameSummary  .__module__=='traceback'
		if not lineno:lineno=a.lineno
		f=a.filename
		return f,lineno
	if py.isdict(a) and py.len(a)==1:
		t=dict_one_item(a)
		if not py.istr(t[0]):raise py.ArgumentError('not dict{sfile:inum}',a)
		f=t[0]
		if not lineno and py.isint(t[1]):lineno=t[1]
		return f,lineno
	if py.type(a) in (py.list,py.tuple):
	#,py.set TypeError: 'set' object does not support indexing
		if not lineno and py.len(a)>1 and py.isint(a[1]):lineno=a[1]
		f=a[0]
		return f,lineno
	if py.isfile(a) and py.getattr(a,'name',''):
		f=a.name  # 只能处理文件，其他file对象 AttributeError: 'HTTPResponse' object has no attribute 'name'
		return f,lineno
	
	#########################多个 elif 只会执行第一个匹配到的
	if py.istr(a):
		gsm=[('qgb.ipy.save ',' success!'),
				]
		for i in gsm:
			a=T.sub(a,i[0],i[1]) or a
		
		if a.lower().endswith('.pyc'):#AttributeError: 'code' object has no attribute 'endswith'
			a=a[:-3]+'py'
		f=a
		if auto_file_path:
			F=py.importF()
			f=F.auto_file_path(f)
		return f,lineno
	else:
		# if py.getattr(a,'__module__',None):  
		# #最后的情况，不要判断 get_module 会自动raise ArgumentUnsupported
		a=get_obj_module(a)#python无法获取class行数？https://docs.python.org/2/library/inspect.html
		return get_obj_file_lineno(a=a,lineno=lineno,auto_file_path=auto_file_path)
	
		
def vscode(a='',lineno=0,auto_file_path=True,get_cmd=False,
	editor_path=py.No('config this system editor_path'),):
	'''
	'''
	if editor_path:
		#TODO
		raise NotImplementedError
	F=py.importF()
	def run_vscode():
		pln(args,',env=',env)
		if get_cmd:
			if isWin():
				return args
		if isWin(): #cmd()  : ('', 'socket: (10106) 无法加载或初始化请求的服务提供程序。\r\r\n')
			run(args,env=env)  # def run(
			if isipy():sleep(1) # 解决 Windows光标下一行错位问题
		if isLinux():
			cmd(args,env=env,encoding='UTF-8') 
		if '--goto'  in args:
			return f,lineno
		return executor
	env={}
	
	if isWin():
		executor = get('vscode_win',level=gd_sync_level['system'])
		if not executor:
			vscp=ps('code.exe')
			if vscp:
				executor=vscp[0].cmdline()[0]
				set('vscode_win',executor,level=gd_sync_level['system'])
				# U.log('vscode_win exe path cached %s'%executor)
			else:
				executor=F.expanduser(r'~\AppData\Local\Programs\Microsoft VS Code\_\Code.exe') 

	if isLinux(): # only work when using remoteSSH
		executor = get('vscode_linux',level=gd_sync_level['system'])
		if not executor:
			vsbin=F.expanduser('~/.vscode-server/bin/')
			ctime=0
			for f,stat in F.ll(vsbin,d=True,f=False,readable=False).items():
				if stat[3]>ctime:
					ctime=stat[3]
					executor=F.join(f,'bin/code')
			set('vscode_linux',executor,level=gd_sync_level['system'])
			
		env = get('vscode_linux_env',level=gd_sync_level['process']) or {}
		if not env:
			ctime=0 # this is .sock file
			for f,stat in F.ll('/tmp/',d=False,f=True,readable=False).items():
				if not f.startswith('/tmp/vscode-') or not f.endswith('.sock'):continue
				if stat[3]>ctime:
					ctime=stat[3]
					env={'VSCODE_IPC_HOOK_CLI':f}
			set('vscode_linux_env',env,level=gd_sync_level['process'])

	args=[executor,'--reuse-window']
	if not a:
		return run_vscode()
		

	f,lineno=get_obj_file_lineno(a,lineno=lineno,auto_file_path=auto_file_path)
		# *get_obj_file_lineno(a,lineno=lineno,auto_file_path=auto_file_path) 
	args=args+['--goto','{}:{}'.format( f,lineno )   ]
	# r=run(args,env=env)
	return run_vscode()

code=vsc=VSCode=vsCode=vscode

def notePadPlusPlus(a='',lineno=0,auto_file_path=True,editor_path=py.No('config this system editor_path'),
	get_cmd=False,):
	'''
--------> os.system('"M:\\Program Files\\Notepad++\\notepad++.exe" "IP.py"')
'M:\Program' 不是内部或外部命令，也不是可运行的程序
或批处理文件。
Out[114]: 1

--------> os.system('"M:\\Program Files\\Notepad++\\notepad++.exe" IP.py')
Out[115]: 0

in ipy , npp() not autoReload when U.r(), But U.npp()
'''
	if editor_path:
		#TODO
		raise NotImplementedError
	nppexe='/Notepad++/notepad++.exe'.lower()
	npath=''	
		# if Win.getVersionNumber()>=6.1:#win7
		# appdata=os.getenv('appdata') or ''#win10 not have appdata  ?
		# npath=appdata.replace('\\','/')+nppexe
	if not os.path.exists(npath):	
		npath=getModPath()[:3]+r'QGB'+nppexe
	if not os.path.exists(npath):	
		npath=getModPath()[:3]+r'QGB'+'/npp/notepad++.exe'
	if not os.path.exists(npath):
		npath=driverPath(r":\Program Files"+nppexe)#如果最后没有匹配到，则为 空.....
	if DEBUG:pln (repr(npath),nppexe)
	# npath='"%s"'%npath
	# print(233333333333)  # add this work?
	# msgbox(npath,py.dir())  #U.r not work ?

	if a:
		f,lineno=get_obj_file_lineno(a,lineno=lineno,auto_file_path=auto_file_path)
		return run(npath,f,'-n {0}'.format(lineno))
	else:
		if not get_cmd:run(npath)
		return npath 
npp=notePadPlus=notePadPlusPlus
	
def nppMods(modName='qgb'):
	r=py.modules(modName)
	pprint(r)
	py.input('npp above all ? Ctrl-c cancel')
	for i in r:
		npp(i)
		
def backLocals(f=None,i=0,r=[]):
	pln (i+1,'='*(20+i*2)  )
	
	if f is None and i==0:f=__import__('sys')._getframe()
	try:pln (f.f_locals.keys()  );r.append(f.f_locals)
	except:return r
	return backLocals(f.f_back,i+1,r)	
printFrame=backLocals
	
def getDateStr():
	'''return '20170301' #From os time'''
	t=getDate()
	return ('%4s%2s%2s'%(t.year,t.month,t.day)).replace(' ','0')
sdate=stoday=getdatestr=getDateStr
# sys.argv=['display=t','pressKey=t','clipboard=f']
def getAST(mod):
	import ast,inspect
	return ast.parse(getSource(mod))
getModAST=getAST

def getSource(a):
	import inspect
	if py.istr(a):
		return F.read(a)
		# return #fileName
	return inspect.getsource(a) # module, class, method, function, traceback, frame, or code object
getsource=getSource

def isSyntaxError(a):
	import ast
	try:
		ast.parse(a)
		return F
	except:
		return True
isyntaxError=iSyntaxError=isSyntaxError

def setattr_not_exists(a,name,value):
	if not py.hasattr(a,name):
		py.setattr(a,name,value)

def compile(a,filename='<str>', mode='exec'):
	'''The source code may represent a Python module, statement or expression. '''
	import ast
	if isinstance(a,ast.stmt):
		setattr_not_exists(a,'col_offset',0)
		setattr_not_exists(a,'lineno',1)
		a=[a]
		a=ast.Module(body=a)
	# if isinstance()
	return py.compile(a,filename,mode)

def parseDump(code,ident=2):
	import ast
	from ast import parse,dump
	r='' ; rm='' ;  rd=''
	if py.istr(code):
		a=parse(code)
	if isinstance(a,ast.stmt):
		a=[a]
	if isinstance(a,ast.Module):
		a=a.body
		r='Module(body=[\n'
		rm=',\n'
		rd=']'
	
	for i in a:
		i=dump(parse(i) ) 
		lines=[]
		for line in i.splitlines():
			lines.append(' '*ident + line)
		r+='\n'.join(lines) + rm
	r+=rd
	print(r)

def parse(code,file='U.parse.file'):
	from ast import parse,AST,iter_fields
	body=parse(code).body
	if py.len(body)==1:return body[0]
	else:return body
	
	a=parse(code)
	annotate_fields=True
	include_attributes=False
	def _format(node,i=0):
		msgbox(node,i)
		if isinstance(node, AST):
			fields = [(a, _format(b,i+1)) for a, b in iter_fields(node)]
			rv = '%s\n{0}(%s'.format('\t'*i ) % (
					node.__class__.__name__, ', '.join(
						('%s=%s' % field for field in fields)
						if annotate_fields else
						(b for a, b in fields)
					)
				)
			if include_attributes and node._attributes:
				rv += fields and ', ' or ' '
				rv += ', '.join('%s=%s' % (a, _format(getattr(node, a),i+1))
								for a in node._attributes)
			return rv +'\n'+'\t'*i +')'
		elif isinstance(node, list):
			return '\n' +'[%s]' % ', '.join(_format(x,i+1) for x in node)
		return repr(node)
	F.new(file.name)
	# file.seek(0) 没用
	# print >>file,_format(a)
	pln(a,file=file)
	file.flush()
	return file.tell()
	
	
def replaceModule(modName,new,package='',backup=True):
	if package:
		if not package.endswith('.'):package+='.'
		if package+modName in sys.modules:
			modName=package+modName
	if backup:
		sys.modules['_'+modName] = sys.modules[modName]
	
	# if modName in sys.modules:
	sys.modules[modName]=new
	return sys.modules[modName]
	# else:return False
	# try:
		# sys.modules['qgb.ipy'] = IPy()
	# except:
		# sys.modules['ipy'] = IPy()
replacemod=replaceMod=replaceModule
def getModule(modName=None,surfixMatch=True):
	'''no Arg return U
	surfixMatch ==name All match
	difference between py.modules('name') : return only one matched module
	'''
	if not modName:modName='qgb.U'
	
	if isModule(modName):return modName
	modName=py.getattr(modName,'__module__',0) or modName
	# if debug():pln(modName,type(modName))
	
	if not py.istr(modName):
		raise ArgumentUnsupported(modName)
	for i in sys.modules:
		if surfixMatch:
			if modName ==i:return sys.modules[i]
		else:
			if i.endswith(modName):return sys.modules[i]
	if modName.startswith('qgb.'):
		modName=modName[4:]
		return getModule(modName)
	return ()
get_obj_module=get_module=getmod=getMod=getModule

def test():
	pln('sys.path *U* :',[i for i in sys.modules if 'U' in i])
	
	gm=getAllMods()
	
	# repl()
	gm.extend(['U','T','N','F',])
	gm=py.set(gm)
	
	pln(gm)
	for i in gm:
		pln('='*55)
		try:
			i='''
import {0}
pln({0})
			'''.format(i) #只能顶开头写，不然  unexpected indent (<string>, line 2)
			py.execute(i)
				# exec(i,globals={}, locals={})      TypeError: exec() takes no keyword arguments
		except Exception as ei:
			pln('###import {0}'.format(i))
			pln(ei)
def explorer(path='.'):
	''' exp can not open g:/qgb '''
	if not path or path=='.':path=pwd(p=False)
	path=F.auto_path(path)

	# path=path.replace('/','\\')
	ps='# Not impl in this system'
	if iswin():
		ps=r'''C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command ii {}.'''.format(path)
		if Win.getVersionNumber()<=6.0:#vista
			ps='explorer.exe '+path
		os.system(ps)
	return StrRepr(ps)

exp=explorer

def log(*a):
	''' rewrite bellow 
BASIC_FORMAT %(levelname)s:%(name)s:%(message)s
CRITICAL 50
DEBUG 10
ERROR 40
FATAL 50
INFO 20
NOTSET 0
WARN 30
WARNING 30
_STYLES {'%': (<class 'logging.PercentStyle'>,......}
'''
	pln(a)
try:	
	import logging
	logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
		datefmt='%Y-%m-%d:%H:%M:%S',
		level=logging.INFO)
	log=logging.getLogger(__name__).info
except:pass
	
def logWindow():
	import Tkinter as tk
	#DEL : rpc replace this func
	
########################################	
def google(a):
	a=T.urlEncode(a)
	return browser('https://www.google.com.my/#q='+a)
	# return browser('https://init.pw/search?q='+a)
	
def subprocess_popen(cmd):
	'''
	subprocess
	sb.stdin.close() 才返回  stdout stderr
	'''
	from subprocess import PIPE,Popen
	return Popen(cmd,stdin=PIPE,stdout=PIPE,stderr=PIPE)
subprocess=subprocessPopen=subprocess_popen

def get_iterable(iterable,index=0): #TODO start, stop[, step])
	if not py.isint(index):
		raise py.ArgumentUnsupported('')
	if index<0:
		index=len(iterable)-1
	for n,v in py.enumerate(iterable):
		if n==index:
			return v
	return py.No('iterable index out of range',iterable,index,)
get_one_from_set=get_from_set=get_from_jihe=getIterable=get_iterable

def sub(a,len='default return len 9',start=0,step=1):
	'''sub dict,list,tuple....iterable
	like a[start:start+len:step]
			postive stands for left>right
	minus	negative stands for right<left
	text sub use T.sub
	无法处理子元素过大的输出情况
	'''
	m=py.len(a)
	# if py.max(py.abs(start),py.abs(step))>m or len==0:
		# raise ArgumentError(len,start,step)
	if step==0:return py.type(a)()
	if isinstance(a,py.dict):r={}
	else:r=[]
	
	if start<0:start=m+start
	
	if step<0:reverse=True;step=-step
	else:reverse=False
	
	if py.type(len) is py.str:
		# if m/step>9:len=
		len=py.min(9*step,m/step)
	len=py.int(len)#int(9999999999999999999999999999999)=9999999999999999999999999999999L			
	
	n=-1
	ns=-1
	end=start+len*step
	for i in a:
		n+=1
		if len>0:
			if not start<=n<end:continue
		else:
			if not end<n<=start:continue
		
		ns+=1
		if ns<step and ns>0:continue
		else:ns=0
				
		# if step>0:
		
		# else:
			# if 
		if isinstance(a,py.dict):#所有不能用for in一次取出的类型
			r[i]=a[i]
		else:
			if reverse:r.insert(0,i)
			else:r.append(i)
	return r
def subLast(a,len='default',step=1):
	return sub(reversed(a),len=len,step=step)
subr=subLast
def reversed(a):
	if isinstance(a,py.dict):return reversedDict(a)
	r=[]
	for i in py.reversed(a):
		r.append(r)
	return r
def reversedDict(d):
	r=OrderedDict()
	for i in py.reversed(OrderedDict(d)):
		r[i]=d[i]
	return r
	
def difference(a,b):
	'''差集 a-b
	 U.diff([1,2,4],[1,2,5]) # {4}
	'''
	a=py.set(a)
	b=py.set(b)
	if py.len(a)<py.len(b):a,b=b,a
	return py.list(a-b)
cj=diff=difference	
	
def j(a,b):
	'''intersection 交集
	
	TypeError: unhashable type: 'dictproxy' #TODO
	'''
	isdict=isinstance(a,py.dict) and isinstance(b,py.dict)
	r=[]
	for i in a:
		if i in b:
			if isdict:
				if a[i]==b[i]:r.append((i,a[i]))
				else:		  r.append((i,a[i],b[i]))
				continue
			r.append(i)
			
			
	return r
	# return py.set(a).intersection(py.set(b))

def jDictValue(a,b):
	'''
	'''
	r={}
	vb=b.values()
	for i in a.items():
		if i[1] in vb:
			r[i[0]]=i[1]
	return	r
jdv=jDictValue

def getNestedValue(a,*key):
	'''safely get nested  a[k1][k2][...]
	
setErr( gError 还是要保留，像这种 出错 是正常流程的一部分，但是又想把错误记录下来
#todo
	'''
	if py.len(key)==0:raise ArgumentError('need at least one key')
	if py.len(key)==1:
		try:return a[key[0]]
		except Exception as e:return py.No(e)
	else:
		try:return getNestedValue(a[key[0]],*key[1:]) 
		except Exception as e:return py.No(e)
getDictV=getDictNestedValue=getNestedValue

def getDictItem(d,index=0):
	if index<0:index=py.len(d)+index
	for n,k in py.enumerate(d):
		if n==index:
			return (k,d[k])
	
	return a.items().__iter__().__next__()
dict_item=dict_one_item=get_dict_item=getDictItem

def get_dict_value(d,index=0):
	if index<0:index=py.len(d)+index
	for n,v in py.enumerate(d.values()):
		if n==index:
			return v
getDictValue=dict_value=get_dict_value

def setDictListValue(adict,key,value):
	if key in adict:
		adict[key].append(value)
	else:
		adict[key]=[value]
add_dict_value_list=set_dict_value_list=set_dict_list=setDictList=setDictListValue

def setDictSetValue(adict,key,value):
	if key in adict:
		adict[key].add(value)
	else:
		adict[key]=py.set([value])
add_dict_value_jihe=add_dict_value_set=set_dict_value_set=set_dict_set=setDictset=setDictSetValue

def setDictValuePlusOne(adict,key):
	if key in adict:
		adict[key]+=1
	else:
		adict[key]=1
set_dict_plus_1=set_dict_value_plus_1=setDictPlusOne=setDictValuePlusOne		

def dict_value_len(adict):
	'''
	range(-1) = range(0, -1)
	'''
	d={}
	for k,v in adict.items():
		d[k]=len(v)						
	return d
dictvlen=dictValueLen=dict_value_len
def dict_value_len_count(adict,show_key_len_range=py.range(-1,-1) ):
	'''
	range(-1) = range(0, -1)
	'''
	d={}
	for k,v in adict.items():
		l=len(v)#U.len
		setDictValuePlusOne(d,l)
		if l and (l in show_key_len_range):
				setDictListValue(d,'%s-len'%l,k)							
	return d
	
def dict_value_hash_count(adict,):
	'''
	return {v_hash:count}
	'''
	d={}
	for k,v in adict.items():
		l=hash(v)#U.hash
		if l in d:
			if py.islist(d[l].obj):
				list=d[l].obj
				list.append(k)
			else:
				list=[d[l].obj]
			d[l]=IntWithObj(d[l]+1,list)
		else:
			d[l]=IntWithObj(1,k)
		# setDictValuePlusOne(d,l)
	return d
	
def getDictItems(a,*range,index=False):
	'''
*range= (stop) 
*range= (start, stop[, step])

#TODO
Init signature: slice(self, /, *args, **kwargs)
Docstring:
slice(stop)
slice(start, stop[, step])

Create a slice object.  This is used for extended slicing (e.g. a[0:10:2]).
'''

	r=[]
	iter=a.items().__iter__()
	range=py.list(py.range(*range) )
	i=-1
	while True:
		try:
			item=iter.__next__()
			i+=1
			if i>range[-1]:break
			if i in range:
				if index:
					r.append([i, item] )
				else:
					r.append(item)
		except py.StopIteration:
			break
	return r
dict_items=get_dict_items=getDictItems
	
def dict_multi_pop(adict,*keys,default=py.No('key not in dict')):
	dr={}
	for k in keys:
		dr[k]=adict.pop(k,default)
	return dr	
dict_pop=pop_dict_multi_key=dict_pop_multi_key=dict_multi_pop
	
def split_list(alist,sub_size):
	n=py.int(sub_size)
	return [alist[i:i+n] for i in py.range(0, py.len(alist), n)]
splitList=split_list
	
def getLastException():
	'''a callable
	return Exception'''
	import traceback as tb
	r=tb.extract_tb( sys.last_traceback)
	r.append(sys.last_value)
	return r
	
	if py.callable(a):
		try:a()
		except Exception as e:return e
		return 'No Exception found'
	else:
		return	getException.__doc__
lastErr=err=geterr=getErr=error=getException=getLastException

def print_traceback_in_except():
	'''
try:
    raise Exception
except:
    U.print_tb()  # has effect
finally:
    U.print_tb()  # None
'''
	import traceback
	ex_type, ex, tb_obj = sys.exc_info()
	traceback.print_tb(tb_obj)
print_tb=print_traceback=print_traceback_in_except

def print_stack():
	import traceback
	traceback.print_stack()

def getClassHierarchy(obj):
	'''In [68]: inspect.getmro?
Signature: inspect.getmro(cls)
Docstring: Return tuple of base classes (including cls) in method resolution order.
File:      g:\qgb\anaconda2\lib\inspect.py
Type:      function
'''
	import inspect
	if py.getattr(obj,'__base__',None) or py.getattr(obj,'__mor__',None):
		return inspect.getmro(obj)

	if py.getattr(obj,'__class__',None):
		return inspect.getmro(obj.__class__)
	return ()
getclassInherit=getClassHierarchy

def getFile(a):
	import inspect
	try:
		inspect.getfile(a)
	except Exception as e:
		if 'is not a module' in e.message:
			return getFile(py.type(a))
		if 'built-in' in e.message:
			return e.message
getfile=getFile

#def 	#把一个数分解成2的次方之和。

def selectBox(*a):
	if py.is2():
		import Tkinter as tk
	else:
		import tkinter as tk
	top=tk.Tk()
	tk.mainloop()

def getCmd():
	if iswin() or iscyg():
		return Win.getCmd()
getCmdline=getCmd

def save(a,name=0):
	if not iswin():raise NotImplementedError()
	name=F.autoPath(name,default=sys.executable[0]+':/qgb/') 
	if  py.isbyte(a) or py.istr(a):
		return F.write(name,a)
	elif py.isbasic(a):
		return F.serialize(obj=a,file=name)#0 ascii mode
	else:
		try:
			return F.dill_dump(obj=a,file=name)
		# except ImportError as e:
		except Exception as e:
			log(e)
			
		raise NotImplementedError('序列化非基本类型')
	# if name:
	# else:#TODO 写入一个新文件并保证 别进程 load 可以读到最新的save；可以保存到网络？？
def load(name=0,returnFile=False):
	global gst;gst='g:/qgb/'
	return F.read(name,returnFile=returnFile)
	# if name:#TODO 配合 save 并正确转换到相应类型，使用对象序列化？ 

	
def	renameDictKey(d,new,old={}):
	if not old:
		for i in d:
			old=i
			break
	if isinstance(d, OrderedDict):
		d.rename(old,new)
	else:
		d[new] = d.pop(old)
	return d
		# del d[old]#这个可以删除item,py27
def beep(ms=1000,hz=2357):
	if iswin():
		try:
			import winsound
			return winsound.Beep(hz,ms)
		except:
			pass
	p('\a')

def unique(iterable):
	r=[]
	for i in iterable:
		if i not in r:r.append(i)
	return r

def pipInstall(modName):
	''' #TODO 在同一个进程内 pipInstall 只能运行一次
In [79]: U.pipInstall('dill')
Requirement already satisfied: dill in /usr/local/lib/python3.6/site-packages (0.2.9)
Out[79]: 0
#######################
In [80]: U.pipInstall('dill-')
Invalid requirement: 'dill-'

Out[80]: 1
#######################
In [81]: U.pipInstall('flask')
Collecting flask
  Downloading https://files.pythonhosted.org/packages/7f/e7/08578774ed4536d3242b14dacb4696386634607af824ea997202cd0edb4b/Flask-1.0.2-py2.py3-none-any.whl (91kB)
	100% |████████████████████████████████| 92kB 169kB/s
Could not install packages due to an EnvironmentError: [Errno 2] No such file or directory: '/tmp/pip-req-tracker-04_vcnlz/b0a3f228a91008c9937cc5e1a2c648e5759a1339d8b8d5b2ce88693f'

Out[81]: 1
#######################
'''
	from pip.__main__ import _main as pip
	return pip(['install',modName])
pip_install=pipInstall
	
def pip_clean_cache():
	if isnix():  cachePath=r'~/.cache/pip'  # and it respects the XDG_CACHE_HOME directory.
	if isMacOS():cachePath=r'~/Library/Caches/pip'
	if isWin():  cachePath=os.getenv('LocalAppData')+r'\pip\Cache'
	return F.delete(cachePath)
	
def pip_install_qpsu_required(
	mods='chardet dill psutil requests flask progressbar2 pymysql elasticsearch elasticsearch_dsl '
	):
	if py.istr(mods):  mods=mods.split(' ')
	
	rd={'installed':[],
		'installing':[]
	}
	for i in mods:
		if not i:continue
		r=pipInstall(i)
		if r==0:rd['installed'].append(i)
		if r==1:rd['installing'].append(i)
	return rd
pipqp=pip_install_qpsu_required
	
def progressbar(iterable):
	import progressbar
	return progressbar.progressbar(iterable)

def formatCode(code, indent_with='\t'):
	import ast,astor
	p=ast.parse(code)
	return astor.to_source(p,indent_with=indent_with)
	
def ast_to_code(a,EOL=True):
	import astor
	r= astor.to_source(a)
	if not EOL:
		while r.endswith('\n'):
			r=r[:-1]
	return r
astToSourceCode=ast_to_code
	
def cache(f,*a,**ka):
	'''
	#todo
	'''
	print(a,ka)
	# print(a,ka)
	cache.__dict__[f]={'a':a,'ka':ka}
	return {a:ka}

def filterWarning(category=DeprecationWarning):
	import warnings
	return warnings.filterwarnings("ignore", category=category)	
filterwarnings=filterWarning

def filterWarningList():
	import warnings
	return warnings.filters

def parseArgs(int=0,str='',float=0.0,dict={},list=[],tuple=py.tuple(),
			):
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'--int','-i','-int',# -int 6 ok # -int6 error
		type=py.int,
		default=int,
		help='get int.'
	)
	parser.add_argument(
		'--str','--string','-s','-str',# -int 6 
		type=py.str,
		default=str,
	)
	parser.add_argument(
		'--float','-float','-f',
		type=py.float,
		default=float,
	)	
	parser.add_argument(
		'--dict','-dict','-d',
		type=py.eval,  # dict       # -c: error: argument --dict/-dict/-d: invalid dict value: '{6:9}'
		default=dict,
	)	
	parser.add_argument(
		'--list','-list','-l',
		type=py.eval,  #list list=['[', '1', ',', '2', ']']
		default=list,
	)	
	parser.add_argument(
		'--tuple','-tuple','-t',
		type=py.eval,  #
		default=tuple,
	)	
	
	FLAGS, unparsed = parser.parse_known_args()
	# print(FLAGS.int)
	##ipyEmbed()()
	# print(unparsed)
	return FLAGS
parse_args=argsParse=argparse=argsParser=args_parse=args_parser=parseArgs	

def sha256_fingerprint_from_pub_key(pubkey_str):
	import base64
	import binascii
	import hashlib
	import re
	import sys
	pubkey_str = pubkey_str.strip()

	# accept either base64 encoded data or full pub key file,
	# same as `fingerprint_from_ssh_pub_key
	if (re.search(r'^ssh-(?:rsa|dss) ', pubkey_str)):
		pubkey_str = pubkey_str.split(None, 2)[1]

	# Python 2/3 hack. May be a better solution but this works.
	try:
		pubkey_str = bytes(pubkey_str, 'ascii')
	except TypeError:
		pubkey_str = bytes(pubkey_str)

	digest = hashlib.sha256(binascii.a2b_base64(pubkey_str)).digest()
	encoded = base64.b64encode(digest).rstrip(b'=')  # ssh-keygen strips this
	return "SHA256:" + encoded.decode('utf-8')

def sizeof_one_obj(obj):
	from pympler.asizeof import asizeof
	return F.IntSize(asizeof(obj))
def sizeof(obj,*other):
	return builtinFuncWrapForMultiArgs(builtinFunc=sizeof_one_obj,args=(obj,other) )
size=asizeof=sizeof

def gc():
	import gc
	return gc.collect()

def get_objects(type,len=None):
	import gc
	isinstance= py.isinstance
	r=[]
	for o in gc.get_objects():
		if isinstance(o,type):
			r.append(o)
	return r
find_objects=get_obj=get_objects

def git_commit(commit_msg=None,dir='.',
	git_exe=None, user_email='qgbcs1@gmail.com', user_name='qgb',):
	U,T,N,F=py.importUTNF()
	U.cd(dir)
	U.pwd(p=1)
	ipy=U.get_ipy(raise_EnvironmentError=True)
	if not git_exe:
		if U.isWin():
			git_exe=U.get_or_set('git_exe',r"D:\Program Files\Git\bin\git.exe")
		if U.isLinux():
			git_exe=U.get_or_set('git_exe',r"/usr/bin/git")

	cmd=r'''   
"   "{git_exe}" config --global user.email {user_email}
"{git_exe}" config --global user.name {user_name}

"{git_exe}" config --global core.autocrlf false
"{git_exe}" config --global core.filemode false
"{git_exe}" config --global credential.helper store
"{git_exe}" config --global http.sslverify "false"
echo 	 git config done
"{git_exe}" add -A
"{git_exe}" commit -m "{commit_msg}"
echo 	 git commit "{commit_msg}" done   "
'''
	cmd=T.replace_all(cmd.strip(),'\n\n','\n')
	cmd=cmd.replace('\n',' & ')
	ipy.system(cmd)
	return cmd
commit=commit_git=gitCommit=git_commit

def git_config_list(a='g'):
	''' a : Config file location
g    --global              use global config file
s   --system              use system config file
l   --local               use repository config file
    -f, --file <file>     use given config file
    --blob <blob-id>      read config from given blob object
	'''
	a=a.lower()
	U=py.importU()
	cmd=a
	if U.one_in(['s','y','t','e','m'],a):
		cmd='--system'
	if U.one_in(['g','gl','b'],a):
		cmd='--global'	
	if U.one_in(['l','o','c'],a):
		cmd='--local'

	return git('config --list '+cmd,p=1)

def git(args='config --list --global',*a,git_exe=None,p=1):
	''' --version 
config -l  == config --list --global	
 --global
 --system
 --local

	 '''
	U=py.importU()
	a=py.list(a)
	if py.istr(args):
		a.insert(0,args)
	elif py.iterable(args):
		a=py.list(args)+a
		
	ipy=get_ipy(raise_EnvironmentError=True)
	if isWin():
		git_exe=get_or_set('git_exe',r"D:\Program Files\Git\bin\git.exe")
	if isLinux():
		git_exe=get_or_set('git_exe',r"/usr/bin/git")
	cmd=f'''"{git_exe}" {' '.join(a)} '''
	if p:U.pln(cmd)
	ipy.system(cmd)

def git_upload(commit_msg=None,repo='QPSU',repo_path=get_qpsu_dir(),
			git_remotes=['https://qgbcs@gitee.com/qgbcs/',
				# 'https://git.coding.net/qgb/',
				'https://github.com/qgb/',
				],
			git_exe=None,
			user_email='qgbcs1@gmail.com',
			user_name='qgb',

		):
	ipy=get_ipy(raise_EnvironmentError=True)
	if not git_exe:
		if isWin():
			git_exe=get_or_set('git_exe',r"D:\Program Files\Git\bin\git.exe")
		if isLinux():
			git_exe=get_or_set('git_exe',r"/usr/bin/git")

	if not commit_msg:commit_msg=stime()
	commit_msg=T.replacey(commit_msg,['"'],'')

	if '://' in repo:
		git_remotes=[T.subLast(repo,'','/')]
		repo=T.subLast(repo,'/')
	cmd=r'''
cd /d {repo_path}
"{git_exe}" config --global user.email {user_email}
"{git_exe}" config --global user.name {user_name}

"{git_exe}" config --global core.autocrlf false
"{git_exe}" config --global core.filemode false
"{git_exe}" config --global credential.helper store
"{git_exe}" config --global http.sslverify "false"
echo 	 git config done
"{git_exe}" add -A
"{git_exe}" commit -m "{commit_msg}"
echo 	 git commit "{commit_msg}" done
'''
	for url in git_remotes:
		if not url.endswith('/'):url+='/'
		cmd+='"{git_exe}" '+'push {0} master\necho \t push {0} done\n'.format(url+repo)
	
	cmd=T.replace_all(cmd.strip(),'\n\n','\n')
	cmd=cmd.replace('\n',' & ')
	ipy.system(cmd)
	return cmd
up=git_up=gitUp=git_upload

def python(args='-V',*a,**ka):
	''' for copy paste,import U'''
	U=py.importU()
	a=py.list(a)
	if py.istr(args):
		a.insert(0,args)
	elif py.iterable(args):
		a=py.list(args)+a
	if 'python' not in a[0].lower():
		a.insert(0,sys.executable)
	return U.cmd(a,**ka)

def python_m(*a,**ka):
	return python('-m',*a,**ka)

class IntWithObj(py.int):
	'''int(x, base=10) -> integer 
	IntWithOther(x,obj) #default base 10
	'''
	def __new__(cls, *a, **ka):
		if len(a)!=2:
			raise py.ArgumentError('IntWithOther only need Two args:\
IntWithOther(intable,obj) , but get {}'.format(py.len(a)))
		obj=a[1]
		a=(a[0],)
		# ka.setdefault('base',10) #TypeError: int() can't convert non-string with explicit base
		i= py.int.__new__(cls, *a, **ka)
		i.a=i.arg=i.obj=obj
		return i
	def __repr__(self):
		return '<{}>'.format(self)
IntObj=IntWithOther=IntWithObj	

class IntReprAsOct(py.int):
	def __new__(cls, *a, **ka):
		return py.int.__new__(cls, *a, **ka)
	def __repr__(self):
		U=py.importU()
		return '<{}>'.format(py.oct(self) )
		# return '<{}={}>'.format(super().__repr__(),F.ssize(self) )
IntFileMode=IntOct=IntReprAsOct

class FloatTime(py.float):
	def __new__(cls, *a, **ka):
		return py.float.__new__(cls, *a, **ka)
	def __repr__(self):
		U=py.importU()
		return '<{}>'.format(stime(time=self) )

class IntTime(py.int):
	def __new__(cls, *a, **ka):
		return py.int.__new__(cls, *a, **ka)
	def __repr__(self):
		U=py.importU()
		return '<{}>'.format(stime(time=self) )


def mutableString(obj):
	class MetaClass(type):
		def __new__(mcls, classname, bases, classdict):
			wrapped_classname = '_%s_%s' % ('Wrapped', type(obj).__name__)
			return type.__new__(mcls, wrapped_classname, (type(obj),)+bases, classdict)

	class MutableString(metaclass=MetaClass):
		def set(self, data):
			self.last = mutableString("".join(self.data) )
			self.data = py.list(data)
			
		def __init__(self, data):
			self.data = py.list(data)
						
		def __repr__(self):
			return py.repr(self.__str__())
			
		def __str__(self):
			return "".join(self.data)
			
		def __setitem__(self, index, value):
			self.data[index] = value
		def __getitem__(self, index):
			if type(index) == slice:
				return "".join(self.data[index])
			return self.data[index]
		def __delitem__(self, index):
			del self.data[index]
		def __add__(self, other):
			self.data.extend(py.list(other))
		def __len__(self):
			return len(self.data)

	return MutableString(obj)		


SKIP_ATTR_NAMES=[
	'_ipython_canary_method_should_not_exist_','_repr_mimebundle_',
	'__class__',#TypeError: 'NoneType' object is not iterable
	'__mro__',
	# '__init__', '__getattr__', '__parent_repr__', '__repr__',
	# '_name',
	]
ValueOfAttr_NAMES=['__init__',
 '__parent__',
 '__child__',
 '__getattr__',
 '__getattribute__',
 '__name__',
 '__str__',
 '__parent_str__',
 '__repr__',
'__v__',
#  '__call__',
 ]
class ValueOfAttr(py.object):
	'''  '''
	def __init__(self,parent=None):
		self.__parent__=parent
		self.__child__=None

	# def __getattr__(self, name):
	def __getattribute__(self, name):
		# log([id(self),name])
		if name in SKIP_ATTR_NAMES:
			return
		if name in ValueOfAttr_NAMES:
			try:
				return py.object.__getattribute__(self, name)
			except Exception as e:
				if name=='__name__':return ''
				raise e

		if name=='__class__':return ValueOfAttr()
		
		if name=='__call__':#不会调用实例上的 ,只会检查 类上有没有特殊方法
			print_stack()
			return __call__ 
		
		self.__name__=name

		self.__child__= ValueOfAttr(parent=self)
		return self.__child__

	def __call__(self, *args, **kwargs):
		# return print_stack()
		r='('
		for v in args:
			r+=pformat(v,**get('pformat_kw',{})  ) +','
		for k,v in kwargs.items():
			r+='{}={},'.format(k,pformat(v,**get('pformat_kw',{}) ) )
		r+=')'
		self.__v__ = self.__str__()+r
		if is_ipy_cell():
			print(self.__v__)
		else:
			return StrRepr( self.__v__ )
	def __parent_str__(self):
		if self.__parent__==None:return ''
		if not self.__child__:return py.str(self.__parent__)
		return py.str(self.__parent__)+'.'

	def __repr__(self):return self.__str__()
	def __str__(self):
		# return stime()
		# if self.__name__=
		# log([self.__parent_str__(),self.__name__])
		return self.__parent_str__()+self.__name__
v=ValueOfAttr()

class StrRepr(py.str):
	''' padding_times=0,padding='\t'
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str


'''
	def __new__(cls, *a, **ka):
		'''
U.StrRepr(3232) ##					[<class 'qgb.U.StrRepr'>, (3232 , ), {}] 
U.StrRepr(b'3232',encoding='ascii')	[<class 'qgb.U.StrRepr'>, (b'3232',), {'encoding': 'ascii'}]
		 '''
		# string=a[0]
		# if py.isnum(string):
		# 	string=py.str(string)
		# if not py.istr(string):
		# 	raise ArgumentError('must str,but got',string)
		# self.string=string
		StrRepr.padding=ka.pop('padding','\t')
		StrRepr.padding_times=ka.pop('padding_times;',0)
		StrRepr.padding_times=ka.pop('padding_width',StrRepr.padding_times)
		StrRepr.padding_times=ka.pop('pi',StrRepr.padding_times)
		StrRepr.padding_times=ka.pop('ip',StrRepr.padding_times)
		StrRepr.padding_times=ka.pop('times',StrRepr.padding_times)
		StrRepr.padding_times=ka.pop('width',StrRepr.padding_times)

		return py.str.__new__(cls, *a, **ka)

	def __repr__(self):return self.__str__()
	def __str__(self) :return (StrRepr.padding*StrRepr.padding_times)+ super().__str__() +(StrRepr.padding*StrRepr.padding_times)
	


#############################
def main(display=True,pressKey=False,clipboard=False,
	ipyArgs=False,escape=False,
	c=False,ipyOut=False,cmdPos=False,reload=False,*args):
	anames=py.tuple([i for i in py.dir() if not i .startswith('args')])
	if not args:args=sys.argv
	for i in args:
		for j in anames:
			if i.lower().startswith(j.lower()+'='):
				# args.remove(i)
				i=T.sub(i,'=','').lower()
				if i.startswith('t'):exec(j+'=True' )#only for python2?
				if i.startswith('f'):exec(j+'=False')
				# repl()
	###############################
	'''call order Do Not Change! '''
	###############################
	sImport=gsImport
	if c:sImport+=';C=c=U.clear'
	
	if reload:sImport+=";R=r=U.reload"
		
	if ipyOut:sImport+=';O=o=U.ipyOutLast'
	
	if cmdPos:sImport+=";POS=pos=U.cmdPos;npp=NPP=U.notePadPlus;ULS=Uls=uls=F.ls;ll=ULL=Ull=ull=F.ll"
		
	if ipyArgs:
		sImport=sImport.replace("'",r"\'")
		sImport='''
cmd /k ipython --no-banner  --autocall=2 "--InteractiveShellApp.exec_lines=['{}','U.cdt()']"
'''.format(sImport).strip()
		escape=False
		clipboard=True
		pln('# set below to clipboard')


	if escape:sImport=sImport.replace("'",r"\'")
	
	
	if pressKey:
		try:
			import win32api
			win32api.ShellExecute(0, 'open', gsw+'exe/key.exe', sImport+'\n','',0)
		except:pln('PressKey err')
	if clipboard:
		try:
			Clipboard.set(sImport)
		except:pln('Clipboard err')
	if display:
		pln(sImport)
	else:
		return sImport

gsImport='''import sys;'qgb.U' in sys.modules or sys.path.append('{0}');from qgb import *'''.format(getModPathForImport())	
if __name__ == '__main__':
	main()
