# coding=utf-8
gsImport='''
from qgb import U,T
'''
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
import sys
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
	
if 'qgb.U' in sys.modules:sys.modules['_U']=sys.modules['qgb.U']
elif 'U' in sys.modules:sys.modules['_U']=sys.modules['U']
################  import python lib  #######################
stdin=sys.stdin;stdout=sys.stdout;stderr=sys.stderr
gsdecode=decoding='utf-8';gsencode=gsencoding=encoding=py.getattr(stdout,'encoding','utf-8')#AttributeError: 'IDAPythonStdOut' object has no attribute 'encoding'
modules=sys.modules
try:
	import os;path=os.path
	from threading import Thread
	thread=Thread
	from threading import Lock as threading_lock
	mutex=threadingLock=threading_lock
	
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

	from pprint import pformat
	if __name__.endswith('qgb.U'):from . import Clipboard
	else:                         import Clipboard
	clipboard=cb=Clipboard#  
	cbs=CBS=Clipboard.set
	cbg=CBG=Clipboard.get
except Exception as ei:
	setErr(ei,msg='#Error import '+str(ei))
	
aError=ArgsErr=argserr=argErr=argerr=argumentError=ArgumentException=py.ArgumentError	
ArgumentUnsupported=py.ArgumentUnsupported
############
true=True;false=False
int_max=INT_MAX=gimax=IMAX=imax=2147483647
int_min=INT_MIN=gimin=IMIN=imin=-2147483648
nan=float_nan=py.float('nan')
inf=float_inf=py.float('inf')
float_max=179769313486231580793728971405303415079934132710037826936173778980444968292764750946649017977587207096330286416692887910946555547851940402630657488671505820681908902000708383676273854845817711531764475730270069855571366959622842914819860834936475292719074168444365510704342711559699508093042880177904174497791
float_min=0-float_max
float_max==2**1024-2**970-1 
'''float(U.float_max+1) or float(U.float_min-1) #OverflowError: int too large to convert to float

float(1.79769313486231580793728971405303415079934132710037826936173778980444968292764750946649017977587207096330286416692887910946555547851940402630657488671505820681908902000708383676273854845817711531764475730270069855571366959622842914819860834936475292719074168444365510704342711559699508093042880177904174497791e+308)  ==   float(1.7976931348623158079372897140530341507993413271003782693617377898044496829276475094664901797758720709633028641669288791094655554785194040263065748867150582068190890200070838367627385484581771153176447573027006985557136695962284291481986083493647529271907416844436551070434271155969950809304288017790417449779199999999999999999999e+308)   ==     1.7976931348623157e+308
'''
#2**1024-U.float_max=9979201547673599058281863565184192830337256302177287707512736212186059459344820328924789827463178505446712234220962476219862189941967968303695858991424157101600028364755428382587688607221814935913266783722719619966654052275604351944444276342240220787535604534378780208211792476151720049639425
float_float_max=float_int_add_max=9979201547673598504324897285072871471186213993555970510405882466533898272496291900571175780142852257200163724564939022373763785492381006715959384438336167193578868484000098586299213046281059798601446904646187766350716006315149259876521361241978618923324738012834739836717385472725200706469887
float_float_max=2**970-2**916-1
float_max_min=0.749999999999999944488848768742172978818416595458984374
float_max_min_min=0.24999999999999998612221219218554324470460414886474609374#==0.24999999999999997
'''
float(U.float_max+float(U.float_float_max))==1.7976931348623157e+308,
float(U.float_max+float(U.float_float_max+1))==U.inf


>>> t,fs=(['0.24999999999999998612221219218554324470460414886474609374'], '
float(2**1024-2**970-1+ float(2**970-2**916-1+ float(2**916-2**862-1+ float(2**862-2**808-1+ float(2**808-2**754-1+ float(2**754-2**700-1+ float(2**700-2**646-1+ float(2**646-2**592-1+ float(2**592-2**538-1+ float(2**538-2**484-1+ float(2**484-2**430-1+ float(2**430-2**376-1+ float(2**376-2**322-1+ float(2**322-2**268-1+ float(2**268-2**214-1+ float(2**214-2**160-1+ float(2**160-2**106-1+ float(2**106-2**52-1+ float(2**52-1+0.749999999999999944488848768742172978818416595458984374+ 0.24999999999999998612221219218554324470460414886474609374+%s ) ))))))))))))))))))
')
>>> eval(fs%'+'.join(t*31368))
1.7976931348623157e+308
>>> eval(fs%'+'.join(t*31369))
1.7976931348623157e+308
>>> eval(fs%'+'.join(t*31370))
1.7976931348623157e+308
>>> eval(fs%'+'.join(t*31371))
# pocess exit!

>>> eval('+'.join(t*31420))
7854.999999999999
>>> eval('+'.join(t*31421))
# pocess exit!

'''




float_0_9999999999999999=f_9_16=float_0_9_16=0.999999999999999944488848768742172978818416595458984374
# float_0_9999999999999999==0.9999999999999999  #True 16个9
# float(0.99999999999999999)==1.0  #True 17个9



NoneType=py.type(None)
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
'all':5    ,
}
SET_NO_VALUE=py.No('U.set value=None',no_raise=True)
GET_NO_VALUE=py.No('U.get ',no_raise=True)
def set(name,value=SET_NO_VALUE,level=gd_sync_level['process'],**ka):
	if level>=gd_sync_level['process']:
		import sys
		d=sys._qgb_dict=py.getattr(sys,'_qgb_dict',{})# 统一用这句
		if value is SET_NO_VALUE: # py.No 比较不能用== ，no==0 ==None ==0.0 ...
			value=name
			name='_'
		d[name]=value
		# sys._qgb_dict=d
	if level>=gd_sync_level['system']:
		import sqlite3
	return value
	
def unset(*names,level=gd_sync_level['process'],**ka):
	if level>=gd_sync_level['process']:
		import sys
		d=sys._qgb_dict=py.getattr(sys,'_qgb_dict',{})
		r=[]
		for name in names:
			if name in d:
				r.append(d.pop(name))
			else:
				r.append(py.No('%r not found to unset'%name))
		if py.len(r)==1:
			return r[0]
		else:
			return r
delset=del_set=delete_set=unset			
			
	
def set_multi(**ka):
	surfix=get_duplicated_kargs(ka,'__surfix','_surfix',default='')
	import sys
	d=sys._qgb_dict=py.getattr(sys,'_qgb_dict',{})
	sys._qgb_dict.update({surfix+k:v for k,v in ka.items()})
	# for name,value in ka.items():
		# d[name]=value	
	return ka
set_ka=set_named=set_multi	
def get(name='_',default=GET_NO_VALUE,level=gd_sync_level['process']):
	if level>=gd_sync_level['process']:
		import sys
		d=sys._qgb_dict=py.getattr(sys,'_qgb_dict',{})
		#TODO 对于不存在的 name ，可以记录最后访问时间为 py.No，方便排查
		# if default==None:
			# default=py.No('can not get name '+py.repr(name),no_raise=True)
		return d.get(name,default)
	#TODO
def get_multi_return_dict():
	return
def get_multi_return_list(*names,**defaults):
	r=[]
	for name in names:
		r.append( get(name) )
	for name,default in defaults.items():
		r.append( get(name,default=default) )
	return r	
multi_get=get_multi=get_multi_return_list

def get_multi_return_exist_one(*names,default=GET_NO_VALUE,no_raise=True):
	for name in names:
		v=get(name,default=default)
		if not (v is default):return v
	if not no_raise:
		raise Exception('can not U.get names:',names)
	return default	
	
def input_and_set(name,default=py.No('auto get last',no_raise=1),default_function=lambda a:a,**ka):
	r=get(name)
	if not py.isno(r) and py.isno(default):
		default=r
		if py.callable(default_function):default=default_function(r)
	return set(name, input('%s :'%name,default=default,**ka))
inset=set_and_input=set_input=input_set=input_or_set=input_and_set		
	
def get_or_set_input(name,default='',type=None):
	r=get(name)
	if r:return r
	return set(name,input('%s :'%name,default=default,type=type) )
get_input=getInput=getOrInput=get_or_input=get_or_input_set=get_or_set_input

def parse_str_auto_type(s):
	U=py.importU()
	ss=s.strip()
	if U.all_in(ss,'.0123456789') and U.unique(ss,ct=1).get('.',0)==1:
		try:return py.float(ss)
		except:pass
	if U.all_in(ss,'0123456789') or ss.lower().startswith('0x'):
		try:return py.int(ss)
		except:pass
	
	# if (ss.startswith('[') and ss.endswith(']')) or :
	T=py.importT()		
	try:return T.unrepr(s)
	except:pass
	
	return s
	
auto_type=input_auto_type=parse_str_auto_type

def get_or_set(name,default=None,lazy_default=None):
	# if not default: # ipy module set {}
	if (py.isno(default) or (default==None)) and not py.callable(lazy_default) :
		raise py.ArgumentError('default cannot be {},lazy_default must callable'.format( repr(default) ))
	r=get(name)
	if not py.isno(r):
		return r
	else:
		# if default:
		if py.callable(lazy_default) and not default:
			default=lazy_default()
		return set(name,default)
getset=getSet=get_set=get_or_set

def get_or_dill_load(name):
	o=get(name)
	if not o:
		o=F.dill_load(file=name)
	return o
get_dl=get_or_dl=get_or_dill_load	

def get_or_dill_load_and_set(name):
	U,T,N,F=py.importUTNF()
	name=F.auto_path(name)
	if '/' in name:
		o=get(T.sub_last(name,'/',''))
	else:
		o=get(name)
	if not o:
		o=F.dill_load(file=name)
	if not o:
		return o
		# raise EnvironmentError('can not dill_load',name)
	else:
		U.set(name,o)
	return o
get_or_dill_load_set=get_or_dill_load_and_set

def set_and_dill_dump(name,value):
	return set(name,value),F.dill_dump(file=name,obj=value)
set_dp=set_and_dp=set_and_dill_dump
	
def get_or_set_and_dill_dump(name,default=None,lazy_default=None):
	o=get_or_set(name=name,default=default,lazy_default=lazy_default)
	U,T,N,F=py.importUTNF()
	print(U.stime(),F.dp(file=name,obj=o),U.len(o))
	return o
get_set_dp=get_or_set_dp=get_or_set_and_dill_dump
	
def set_or_get(name,value,default=SET_NO_VALUE):
	# if py.isno(default) or (default==None):
	if value or not py.isNo(value) :
		return set(name,value)
	else:
		r=get(name)
		if r:
			return r	
		else:
			if default==SET_NO_VALUE:
				raise py.ArgumentError('if not value, default cannot be {} when get {} == {}'.format( repr(default) ,name,repr(r) ))
			return set(name,default)
			
setget=setGet=set_get=set_or_get
#########################
def one_in(vs,*t):
	'''(1,2,3,[t])	or	([vs].[t])
char in s :  这个效率较高	
char in list:比s至少慢了几十 上百倍？	
	'''
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
	
def platform_system():
	'''Traceback (most recent call last):
  File "/var/www/contextlib.py", line 21, in <module>
    from qgb import U
  File "/home/qmm/qgb/U.py", line 356, in <module>
    if iswin() or iscyg():
  File "/home/qmm/qgb/U.py", line 295, in is_windows
    return platform.system().startswith('Windows')
  File "/usr/lib/python3.8/platform.py", line 891, in system
    return uname().system
  File "/usr/lib/python3.8/platform.py", line 857, in uname
    processor = _syscmd_uname('-p', '')
  File "/usr/lib/python3.8/platform.py", line 613, in _syscmd_uname
    output = subprocess.check_output(('uname', option),
  File "/usr/lib/python3.8/subprocess.py", line 411, in check_output
    return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
  File "/usr/lib/python3.8/subprocess.py", line 489, in run
    with Popen(*popenargs, **kwargs) as process:
  File "/usr/lib/python3.8/subprocess.py", line 854, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/usr/lib/python3.8/subprocess.py", line 1650, in _execute_child
    self._close_pipe_fds(p2cread, p2cwrite,
  File "/usr/lib/python3.8/subprocess.py", line 1104, in _close_pipe_fds
    with contextlib.ExitStack() as stack:
AttributeError: partially initialized module 'contextlib' has no attribute 'ExitStack' (most likely due to a circular import)
'''
	import platform
	try:
		return platform.system()
	except Exception as e:
		e
	p=py.getattr(sys,'platform','')	
	if p:return p
	
	if sys.executable.endswith('.exe'):
		return 'Windows .exe'
	else:
		return 'linux qgb_default'
		
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
	return [i for i in glnix if i in platform_system().lower()]
	
def is_windows():
	p=platform_system().lower()
	return p.startswith('windows') or p.startswith('win32')#sys.platform=='win32'
is_win=iswin=isWin=is_windows

def is_linux():return platform_system()=='Linux'
islinux=isLinux=is_linux
def isMacOS():return platform_system()=='darwin'
isMac=is_mac=is_osx=isOSX=ismacos=isMacOS
	
def is_termux():
	return '/com.termux' in sys.executable
istermux=isTermux=is_termux

def is_vercel():
	'''
drwx------  2 sbx_user1051  990 4.0K Jul  1 14:46 tmp
其他全部是 root
drwxr-xr-x  1 root         root 4.0K Jan  1  1970 var
'''	
	return os.getenv('VERCEL')

def iscyg():
	return 'cygwin' in  platform_system().lower()
# gipy=None#这个不是qgb.ipy, 是否与U.F U.T 这样的风格冲突？
def is_ipython(**ka): # e=False
	# global gipy
	raise_EnvironmentError=get_duplicated_kargs(ka,
'raise_err','raise_error','raiseError','raiseErr','raise_EnvironmentError','EnvironmentError','raiseEnvironmentError')
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
get_ipy=get_ipython=getipy=isIpy=is_ipy=isipy=is_ipython

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
	def find_driver_path(a,reverse=True):
		'''from Z to C'''
		if len(a)>1 and a[1]==':':a=a[1:]
		if not a.startswith(':'):a=':'+a
		# try:AZ=T.AZ;exist=F.exist
		# except:
		AZ=''.join([chr(i) for i in py.range(65,65+26)])
		exist=os.path.exists
		if reverse:AZ=AZ[::-1]
		for i in sys.executable[0]+AZ:
			if exist(i+a):return i+a
		return ''	
		driverPath=driver_path=find_driver_path

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
	'''
u1604:  IPython repl  ok	,  bash python -c error  ?
	
	'''
	def is_root():
		return os.getuid()==0
	isroot=isRoot=is_root
	
	def sudo(cmd,password=py.No('auto get_or_input')):
		'''cmd can use pipe 'id|cut -c 2-22'
		'''		
		if password==0:password='0'
		if not password:
			password=get_or_input("root.password")
		
		from subprocess import call
		# try:
		return call("echo {} | sudo -S {}".format(password, cmd), shell=True)
		
		# except:
			# from subprocess import PIPE,Popen
			# p = Popen(['sudo', '-S'] + cmd, stdin=PIPE, stderr=PIPE,
          # universal_newlines=True)
			# sudo_prompt = p.communicate(password + '\n')
			# return sudo_prompt
			# [1]
		#  0
# u1604 # /bin/sh: 1: Syntax error: end of file unexpected
	def tmux_capture_pane(session=0,max_lines=9999,**ka):
		''' unset TMUX '''
		U,T,N,F=py.importUTNF()
		session=U.get_duplicated_kargs(ka,'session','sess',default=session)
		max_lines=U.get_duplicated_kargs(ka,'max_lines','max','m','n','S','s',default=max_lines)
		
		a=N.geta()
		os.environ['TMUX']=''
		rs=U.isipy().getoutput('tmux capture-pane -S -{max_lines} -t {session}:{window};tmux show-buffer'.format(max_lines=max_lines,session=session,window=a))# 不能用 U.cmd
		return T.EOL.join(rs)
	tmux=tmuxc=tmuxcap=tmuxcapture=tmuxCapture=tmux_capture=tmux_capture_pane
	
########################## end init #############################################
def new_2d_list(width,height,default_value=0):
	''' cols=height   rows=width '''
	return [[default_value for i in py.range(width)] for j in py.range(height)]

def list_get_multi_indexs(a,*ins):
	if py.len(ins)==1 and py.islist(ins[0]):
		ins=ins[0]
	r=[]
	for i in ins:
		r.append(a[i])
	return r
get_list_elements_by_multi_indexs=list_multi_get=list_get_multi_indexs
	
def list_del_multi_indexs(a,*ins):
	ins=py.sorted(ins,reverse=1)
	d={}
	for i in ins:
		d[i]=a.pop(i)
	return d
del_list_multi_indexs=list_del_multi_indexs

def multiprocess_pool(*a,**ka):
	'''multiprocess.Pool(
    processes=None,
    initializer=None,
    initargs=(),
    maxtasksperchild=None,
)
原生multiprocessing模块在使用 IPython 时有一个主要限制：

此包中的功能要求__main__子模块可以导入该模块。[...]这意味着某些示例，例如multiprocessing.pool.Pool示例将无法在交互式解释器中运行。[来自文档]

幸运的是，有一个multiprocessing的fork 模块 multiprocess，它使用dill代替pickle进行序列化，并方便地克服了这个问题。

只需在您的导入中安装multiprocess和替换：
https://stackoverflow.com/a/65001152/6239815
'''
	import multiprocess.pool
	return multiprocess.Pool(*a,**ka)

def pprint(object, stream=None, indent=1, width=133, depth=None, *,
           compact=False):
	try:
		ipy=py.from_qgb_import('ipy')
		return print(ipy.format(object),file=stream)
	except:pass
	
	from pprint import pprint as _pprint
	_pprint(object=object,stream=stream,indent=indent,width=width,depth=depth,)

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
			if is_termux():
				home='/data/data/com.termux/files/home'
			elif is_vercel():		
				home='/tmp' #AWS lambda
				
			#elif 添加其他情况
			else:
				home=''
		if home.startswith('/home/coding'):
			home+='/workspace'
		return get('U.gst',home+s)
	if iswin() or iscyg():
		return get('U.gst',find_driver_path('c:/test/'[1:]))
get_gst=getTestPath=get_test_path
gst=gsTestPath=get_test_path()

def set_test_path(sp,cd=False,p=False):
	global gst,gsTestPath
	F=py.importF()
	sp=F.mkdir(sp,no_auto_path=True)
	if not sp:return sp
	sp=sp.replace('\\','/')
	# if not sp.endswith('/'):
		# sp+='/'
		
	gst=gsTestPath=set('U.gst',sp)
	if cd:chdir(gst)
	if p:pln(gst)
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
		s=find_driver_path(s[1:]) or s
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

def print_return(*a,**ka):
	p(*a,**ka)
	if py.len(a)==1:
		return a[0]
	else:
		return a
pr=print_return

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
		if not a and 'a' in ka:a    =(ka[k],);continue
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


def input(prompt='', default='',type=py.str):
	'''  '[U.input]:'
default must be str ,auto convert to str !!

list,tuple,dict 等type，用 type=py.eval， 否则list(input)==单个字符的list
	'''
	if default:
		default=str(default) # default must be str
		if isWin():
			import win32console
			_stdin = win32console.GetStdHandle(win32console.STD_INPUT_HANDLE)
			keys = []
			for c in default:
				evt = win32console.PyINPUT_RECORDType(win32console.KEY_EVENT)
				evt.Char = c
				evt.RepeatCount = 1
				evt.KeyDown = True
				keys.append(evt)

			_stdin.WriteConsoleInput(keys)
		else:
			import readline
			readline.set_startup_hook(lambda: readline.insert_text(default))
	try:		
		if py.is2():
			r= py.raw_input(prompt)
		else:
			r= py.input(prompt)
		if not py.callable(type):
			type=py.str
		return type(r)
	except Exception as e:  #except 233:语法没错，运行到此就 TypeError: catching classes that do not inherit from BaseException is not allowed
		return py.No(e)
	finally:
		import readline
		readline.set_startup_hook()
		
input_default=input_with_default=input

def _useless_win_input(msg='',default='',type=py.str):
	if default:
		import readline
		readline.set_startup_hook(lambda: readline.insert_text(default))
	try:
		if py.is2():
			r=py.raw_input(msg)
		else:
			r=py.input(msg)
		return type(r)
	finally:
		readline.set_startup_hook()

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
def flat(*a,**ka,):
	'''Breadth-First Traversal
U.get('generator_types_tuple')	
	
# str has __iter__ in py3
unpack_types=(py.list,py.tuple),skip_types=(py.str,py.bytes)	
	'''
	U=py.importU()
	noNone=not U.get_duplicated_kargs(ka,'isnone','isN','hasnone','None','no','none',default=True)
	noNone=U.get_duplicated_kargs(ka,'nonone','no_none','no_no',default=noNone)
	
		# repl()
	
	# def try_yield(iterable):
		# if py.istr(iterable) or py.isbytes(iterable):
			# yield iterable
		# try:
			# for k in iterable:
				# yield from try_yield(k)
		# except:
			# yield iterable
			
	a=py.list(a);
	r=[];i=0
	while i<py.len(a):
		# r.extend( py.list(try_yield(a[i]) ) )				
		
		if py.istuple(a[i]) or py.islist(a[i]) or py.isset(a[i]):
			a.extend( a[i])
		elif U.is_generator(a[i]):
			a.extend(py.list(a[i]))
			# a[i]=py.list(a[i])
			# a[i].extend(a)
		else:
			if noNone and not a[i]:pass
			###TODO other condition
			else:
				r.append(a[i])
			
		i+=1
		if i%10000==0:print(i,U.len(a,r),)
	# repl()
	return r
	# return tuple(r)
flap=flat	
# pln flat([[1,2,3], [5, 2, 8], [7,8,9]])
##(1, 2, 3, 5, 2, 8, 7, 8, 9)
# pln flat([1,2,3,[4,5,[1,2],6]],['aaa'])
##  (1, 2, 3, 'aaa', 4, 5, 6, 1, 2)

def crc32(bytes=b'',file='',chunk_size=8096):
	import zlib
	if file:
		prev = 0
		with py.open(file,"rb") as f:
			while True:
				b = f.read(chunk_size)
				if not b :
					break
				prev = zlib.crc32(b, prev)
	else:
		prev = zlib.crc32(bytes)
	return "%x"%(prev & 0xFFFFFFFF)

def sha3_256(bytes=b'',file=''):
	return hashlib_hash(bytes=bytes,file=file,hash_func='sha3_256')

def sha3_384(bytes=b'',file=''):
	return hashlib_hash(bytes=bytes,file=file,hash_func='sha3_384')

def blake2b(bytes=b'',file=''):
	return hashlib_hash(bytes=bytes,file=file,hash_func='blake2b')

def blake2s(bytes=b'',file=''):
	return hashlib_hash(bytes=bytes,file=file,hash_func='blake2s')

def sha384(bytes=b'',file=''):
	return hashlib_hash(bytes=bytes,file=file,hash_func='sha384')

def sha1(bytes=b'',file=''):
	return hashlib_hash(bytes=bytes,file=file,hash_func='sha1')

def sha3_224(bytes=b'',file=''):
	return hashlib_hash(bytes=bytes,file=file,hash_func='sha3_224')

def sha224(bytes=b'',file=''):
	return hashlib_hash(bytes=bytes,file=file,hash_func='sha224')

def shake_128(bytes=b'',file='',length=64):
	'''return.length == length*2  ### 128
TypeError: hexdigest() takes exactly one argument (0 given)
<built-in method hexdigest of _sha3.shake_128 object at 0x00000168F6021330>
https://github.com/python/cpython/blob/main/Modules/_sha3/sha3module.c#L673
/*[clinic input]
_sha3.shake_128.hexdigest
    length: unsigned_long
    /
Return the digest value as a string of hexadecimal digits.
[clinic start generated code]*/	
	
	'''
	return hashlib_hash(bytes=bytes,file=file,hash_func='shake_128',hexdigest_args=(length,))  

def shake_256(bytes=b'',file='',length=64):
	'''return.length == length*2  ### 128  
3.6 新版功能: SHA3 (Keccak) 和 SHAKE 构造器 sha3_224(), sha3_256(), sha3_384(), sha3_512(), shake_128(), shake_256().

SHAKE 可变长度摘要
shake_128() 和 shake_256() 算法提供安全的 length_in_bits//2 至 128 或 256 位可变长度摘要。 为此，它们的摘要需指定一个长度。 SHAKE 算法不限制最大长度。

shake.digest(length)
返回当前已传给 update() 方法的数据摘要。 这是一个大小为 length 的字节串对象，字节串中可包含 0 to 255 的完整取值范围。

shake.hexdigest(length)
类似于 digest() 但摘要会以两倍长度字符串对象的形式返回，其中仅包含十六进制数码。 这可以被用于在电子邮件或其他非二进制环境中安全地交换数据值。
'''	
	return hashlib_hash(bytes=bytes,file=file,hash_func='shake_256',hexdigest_args=(length,))

def sha512(bytes=b'',file=''):
	return hashlib_hash(bytes=bytes,file=file,hash_func='sha512')

def sha3_512(bytes=b'',file=''):
	return hashlib_hash(bytes=bytes,file=file,hash_func='sha3_512')

def sha256(bytes=b'',file=''):
	return hashlib_hash(bytes=bytes,file=file,hash_func='sha256')
	
def md5(bytes=b'',file=''):
	'''[a] : string or buffer
	[file]:fileName
	return 32 hex(lowerCase) str'''
	return hashlib_hash(bytes=bytes,file=file,hash_func='md5')
	
def hashlib_hash(bytes=b'',file='',hash_func='sha256',chunk_size=8096,**ka):
	'''hashlib.algorithms_guaranteed=
{'sha3_224', 'shake_256', 'sha3_256', 'sha256', 'sha1', 'sha224', 'md5', 'sha3_512', 'blake2s', 'blake2b', 'sha3_384', 'shake_128', 'sha384', 'sha512'} # len 14	

一个集合，其中包含此模块在所有平台上都保证支持的哈希算法的名称。 请注意 'md5' 也在此清单中，虽然某些上游厂商提供了一个怪异的排除了此算法的 "FIPS 兼容" Python 编译版本。

hashlib.algorithms_available 一个集合，其中包含在所运行的 Python 解释器上可用的哈希算法的名称。 将这些名称传给 new() 时将可被识别。 algorithms_guaranteed 将总是它的一个子集。 同样的算法在此集合中可能以不同的名称出现多次（这是 OpenSSL 的原因）


注解 如果你想找到 adler32 或 crc32 哈希函数，它们在 zlib 模块中。
	'''
	import hashlib   
	hexdigest_args=get_duplicated_kargs(ka,'hexdigest_args',default=[])
	myhash = getattr(hashlib,hash_func)()
	if file:
		f = py.open(file,'rb')
		while True:
			b = f.read(chunk_size)
			if not b :
				break
			myhash.update(b)
		f.close()
		return myhash.hexdigest(*hexdigest_args)
	
	
	# md5 = hashlib.md5()   
	myhash.update(bytes)	
	return myhash.hexdigest(*hexdigest_args)  

def DES_encrypt_return_bytes(byte_or_ascii,password,password_max_length=24):
	''' 'a 16 or 24 byte password' 
	
ValueError: pyDes can only work with encoded strings, not Unicode.	
	'''
	from pyDes import triple_des # pyDes if installed from pip
	password=T.padding(password,size=password_max_length)[:password_max_length]
	ciphertext = triple_des(password).encrypt(byte_or_ascii, padmode=2)  #plain-text usually needs padding, but padmode = 2 handles that automatically
	return ciphertext
	# ')\xd8\xbfFn#EY\xcbiH\xfa\x18\xb4\xf7\xa2'  #gibberish	
jiami=encrypt_DES=des_encrypt=DES_encrypt=DES_encrypt_return_bytes

def DES_decrypt_return_bytes(byte_or_ascii,password,password_max_length=24):
	from pyDes import triple_des
	password=T.padding(password,size=password_max_length)[:password_max_length]
	bytes = triple_des(password).decrypt(byte_or_ascii, padmode=2)
	return  bytes
jiemi=decrypt_DES=des_decrypt=DES_decrypt=DES_decrypt_return_bytes
	
	
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
def which(cmd):
	'''  return str  '''
	import shutil
	# import shutil.which # ModuleNotFoundError: No module named 'shutil.which'; 'shutil' is not a package
	r=shutil.which(cmd)  #  if not exist:return None 
	if py.istr(r):
		r=r.replace('\\','/')
	if not r:return ''
	return r
where=which

def join_as_cmd_str(args,*a,quote=True):
	a=py.list(a)
	if py.istr(args):
		a.insert(0,args)
	elif py.iterable(args):
		a=py.list(args)+a
		
	import subprocess
	return subprocess.list2cmdline(a)

	# abandon      #不是 abundant
	import shlex
	if quote:
		a=[shlex.quote(x) for x in a]
	return ' '.join(a)
joinCmd=join_cmd=cmdJoin=cmd_join=shlex_join=join_as_cmd_str

def split_cmd_str(a):
	'''return list'''
	import shlex
	return shlex.split(a)
splitCmd=split_cmd=cmdSplit=cmd_split=shlex_split=split_cmd_str

def subprocess_check_output(*a, timeout=9,encoding=py.No('try decode,except return bytes'),**kwargs):
	''' subprocess.check_output(*popenargs, timeout=None, **kwargs)
'''
	import subprocess
	if py.len(a)==1:
		if py.istr(a[0]):
			if ' ' in a[0]:
				a=split_cmd_str(a[0])
		else:
			a=a[0]
			
	output = subprocess.check_output(a,timeout=timeout,**kwargs)
	try:
		if encoding:
			output=output.decode(encoding)
		else:
			# if is_win():
				
			output=output.decode()
	except Exception as e:
		pass
	
	return output
check_out=check_output=subprocess_check_output

def cmd(*a,shell=True,**ka):
	'''show=False :show command line
	默认阻塞，直到进程结束返回
	if 'timeout' not in ka:ka['timeout']=9     ## default timeout
	
	stdin : str,bytes
	
在 ipython 中 使用rpcServer 调用U.cmd(shell=True),会造成子进程污染ipython命令窗口
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
	
	show    =get_duplicated_kargs(ka,'show','echo')
	stdin   =get_duplicated_kargs(ka,'stdin','input')
	timeout =get_duplicated_kargs(ka,'timeout',default=9)
	encoding=get_duplicated_kargs(ka,'encoding','encode','coding',default='utf-8')
	if shell:ka['shell']=True
	
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
		#pythonAnywhere  IPython[py2.7] REPL  sb.run does not exist
		#pythonAnywhere  web[py3.6]  TypeError("__init__() got an unexpected keyword argument 'capture_output'",
		if not py.getattr(sb,'run',0) or (
			('capture_output' not in getfullargspec(sb.run).kwonlyargs) and
			('capture_output' not in sb.run.__doc__)
			): 
			#pythonAnywhere T
			ka['stderr']=sb.STDOUT
			r= sb.check_output(a,**ka) # bytes
			try:return r.decode(encoding)
			except:return r
		r=sb.run(a,capture_output=True,**ka)
	except Exception as e:
		print_traceback()
		return py.No('sb.run err', e,a,ka)

	try:
		if encoding:
			so=r.stdout.decode(encoding)
			se=r.stderr.decode(encoding)	
		else:
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
GET_DUPLICATED_KARGS_DEFAULT=py.No('Not found matched kargs',no_raise=True)
def get_duplicated_kargs(ka,*keys,default=GET_DUPLICATED_KARGS_DEFAULT,no_pop=False):
	'''
def pop(d,k):
	d.pop(k)
pop(_63,25)  #_63 has change

'''
	if not py.isdict(ka):raise py.ArgumentError('ka should be a dict,but get',ka)
	r=[]
	for i in keys:
		if not py.istr(i):raise py.ArgumentError('keys should be a list of str,but get',i)
		if i in ka:
			if no_pop:i=ka[i]
			else:i=ka.pop(i)
			r.append(i)
			
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

get_ka=get_multi_ka=getDuplicatedKargs=getKargsDuplicated=getKArgsDuplicated=get_kargs_duplicated=get_duplicated_kargs

def sleep(asecond,print_time_every_n_second=0):
	''' asecond: int or float'''
	if not asecond:return 
	if print_time_every_n_second:
		for i in range(asecond):
			if i%print_time_every_n_second==0:
				pln(stime())
			__import__('time').sleep(1)	
	else:	
		__import__('time').sleep(asecond)
	return IntCustomRepr(asecond,repr='U.sleep(%s)'%asecond)
delay=sleep
	
def sleep_until(time):
	U=py.importU()
	from threading import Event      
	e=U.get_or_set('wait_event',Event())
	e.clear()
	begin=U.itime_ms()
	e.wait(aisecond)
	ms=U.itime_ms()-begin
	e.clear()
	return ms	
	
def wait_can_be_interrupted(aisecond):
	'''interrupt : 
	U.get('wait_event').set()
	'''
	U=py.importU()
	from threading import Event      
	e=U.get_or_set('wait_event',Event())
	e.clear()
	begin=U.itime_ms()
	e.wait(aisecond)
	ms=U.itime_ms()-begin
	e.clear()
	return ms
sleep_with_interrupt=wait=wait_with_interrupt=wait_can_be_interrupted


def interrupt_wait():
	U=py.importU()
	e=U.get('wait_event')
	if not e:
		return py.No('no wait_event')
	return e.set() # None
wb=bw=wait_break=bwait=break_wait=interrupt_sleep=sleep_interrupt=wait_interrupt=interrupt_wait		
	
def pause(a='Press Enter to continue...\n',exit=False):
	'''a=msg'''
	if py.is2():input=py.raw_input
	else:input=py.input

	if iswin():
		# cmd('pause');return
		try:
			input(a)
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

		if p :
			# .split(os.pathsep)
			ps=get_env_path()#return list
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
ipy_repl=ipy=ipy_embed=embed=ipyEmbed
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

def remove_module(m):
	import sys
	if py.istr(m):
		return sys.modules.pop(m)
	for k in py.list(sys.modules):
		v=sys.modules[k]
		if v==m:
			return sys.modules.pop(k)
	return py.No('can not found ',m,'in sys.modules')
del_mod=delete_mod=del_modules=delete_modules=remove_mod=remove_module

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
					if mod not in sys.modules:
						return py.No('not found %r in sys.modules'%mod)
					return reload(sys.modules[mod])
				elif '_module' in py.dir(mod):
					if not isModule(mod._module):raise Exception('instance._module is not module')
					mod=mod._module
					modules[mod.__name__]=mod
					return reload(mod)
					
					# if mod.__name__ in modules:#'qgb.ipy'
				else:
					return py.No('instance._module not exists, U.reload arg is not a module ?')
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
	# global CD_HISTORY
	if not ap:ap=gst
	if not py.istr(ap):raise py.ArgumentError('ap must be str Not:{0}'.format(ap))
	ap=os.path.join(ap,*a) # win auto add '\\'
	ap=ap.replace('\\','/')
	if ap[-1] not in ['\\','/']:
		ap+='/'
	
	show_path=get_duplicated_kargs(ka,'p','show_path','print','print_')

	mkdir=False #默认不创建
	if 'md' in ka:mkdir=ka['md']
	if 'mkdir' in ka:mkdir=ka['mkdir']
	if iscyg():mkdir=False#cyg下可以创建带:的目录，导致切换异常
	if mkdir:F.mkdir(ap)
	# repl()
	# if path.abspath(CD_HISTORY) != pwd():
	CD_HISTORY.append(pwd())
	
	if os.path.isdir(ap):
		if show_path:
			U=py.importU()
			U.pln(ap)
		os.chdir(ap);
		return pwd() #ap#True
	
	app=os.path.dirname(ap)
	if os.path.isdir(app):return chdir(app)
	else:pass
		
	if iswin() or iscyg():
		if ap[0]=='/'==ap[2] and ap[1] in T.az:#!cdv&pwd == '/c/Users/lenovo/Videos'
			return chdir(ap[1]+':'+ap[2:])
			
	for i in ap:
		if i not in T.PATH_NAME:raise Exception('need file path',ap,i)
	return py.No("#Can't cd "+ap)
cd=chdir

CD_HISTORY=get_or_set('CD_HISTORY',[])
def cdBack(index=-1,p=0,**ka):
	'''False: cd path list []'''
	if CD_HISTORY:
		return cd(CD_HISTORY[index],p=p,**ka)
	else:
		return False
cdb=cdBack

def cdCurrentFile(*a,**ka):
	f=sys._getframe().f_back.f_globals
	if '__file__' in f:
		sp=os.path.abspath(f['__file__'])
		sp=os.path.dirname(sp)
		return cd(sp,*a,**ka)
	return False
cd__file__=cdc=cdCurrent=cdcf=cdCurrentFile

def cdTest(a='',**ka):
	return cd(gst+a,**ka)
cdt=cdTest
	
def cdQPSU(a='',**ka):
	return cd(getModPath()+a,**ka)
# @property
cdq=cdqp=cdqpsu=cdQPSU
	
def cdWShell(a='',**ka):
	return cd(gsWShell+a,**ka)
cds=cdws=cdWShell

def cdpm():
	return cd('e:/pm')
	
def cdbabun(a='',**ka):
	s=r'C:\QGB\babun\cygwin\home'+'\\'
	# s=r'C:\QGB\babun\cygwin'+'\\'
	s=find_driver_path(s[1:])#driverPath
	return cd(s,a,**ka)
def cdgit(a='',**ka):
	U,T,N,F=py.importUTNF()
	p=U.get_multi_return_exist_one('git_exe','git.exe',no_raise=False)
	p=F.dir(p)
	return cd(p,a,**ka)
	
def get_current_file_dir():
	frame=sys._getframe().f_back
	g=frame.f_globals
	if '__file__' not in g:
		return py.No('not found __file__ in current module')
	__file__=g['__file__']
	import pathlib
	p=pathlib.Path(__file__)
	spath=p.parent.absolute().__str__()
	sp=p.root#win '\\'  linux '/' ## == '' why?
	if not sp:
		if '\\' in spath:sp='\\'
		elif '/' in spath:sp='/'
		else:raise py.ArgumentError(spath,p,file,sp)
	return spath +sp
	
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
	
def random_choice(seq,size=1,repeat=0,not_repeat_max_try=9999,**ka):
	'''
if not repeat: choice  (size+not_repeat_max_try)	times
	
random.choice(seq) #每次抽取都是独立的 多次调用可能重复
	Choose a random element from a non-empty sequence.
 
random.choices(population, weights=None, *, cum_weights=None, k=1)#可能重复
	Return a k sized list of population elements chosen with replacement.

 
random.choice(dict)
 C:\QGB\Anaconda3\lib\random.py in choice(self, seq)
    260         except ValueError:
    261             raise IndexError('Cannot choose from an empty sequence') from None
--> 262         return seq[i]
    263
    264     def shuffle(self, x, random=None):

KeyError: 4

#BUGfixed  U.random_choice(_145,4) .len  有次 ==3 ？ 
In [178]: len(U.random_choice(_145,4))
Out[178]: 2

In [179]: len(U.random_choice(_145,4))
Out[179]: 3

In [180]: len(U.random_choice(_145,4))
Out[180]: 3

In [181]: len(U.random_choice(_145,4))
Out[181]: 4

In [182]: len(U.random_choice(_145,4))
Out[182]: 4

In [183]: len(U.random_choice(_145,4))
Out[183]: 4

In [184]: len(U.random_choice(_145,4))
Out[184]: 3
		# raise py.NotImplementedError('#TODO dict ')

''' 
	import random
	_size=get_duplicated_kargs(ka,'len','k','length','SIZE','i')
	if _size and py.isint(_size) and size==1:size=_size
	len_seq=py.len(seq)
	if not repeat and size > len_seq :
		raise py.ArgumentError('size>%s'%len_seq)
	ids=py.set()
	not_repeat_max_try=size+not_repeat_max_try
	def yrc():
		if repeat:
			yield from random.choices(seq,k=size) 
			return
		times=0
		# r=[]
		while py.len(ids)<size:
			v=random.choice(seq)
			id=py.id(v)
			if id not in ids:
				ids.add(id)
				yield v
				# r.append(v)
			times+=1
			if times>not_repeat_max_try:
				raise py.Exception('not_repeat_max_try reached ，seq中元素id是否有重复？，要不设置 repeat=False ?')
		# return r
		
	if py.istr(seq):
		return ''.join(yrc())
	if py.isdict(seq):
		d=seq
		seq=py.list(d)
		return {k:d[k] for k in yrc()}
	# if py.islist(seq) or py.istuple:
	r=[i for i in yrc()]
	if size==1:return r[0]
	return r
random_choices=random_choice
	
def randomInt(min=0,max=IMAX):
	'''random.randint(a, b)
Return a random integer N such that a <= N <= b.'''
	import random
	return random.randint(min, max)
randint=ramdomInt=randomInt

SORT_KW_SKIP=get_or_set('SORT_KW_SKIP',lazy_default=lambda :py.No('if sort_kw is this, skip sort'))
def sort(a,column=None, cmp=None, key=None, reverse=False,add_index=False,sort_kw=None,**ka):
	''' py2&py3  sorted _3 ,key=lambda i:len(i)        按长度从小到大排序
	在python2.x  sorted _5,cmp=lambda a,b:len(a)-len(b) 实现同上功能， 一般不用cmp 参数
	sorted中cmp参数指定的函数用来进行元素间的比较。此函数需要2个参数，然后返回负数表示小于，0表示等于，正数表示大于。
	#这句可能写错了 a:item of sort list   |  *a: (item,) 
	'''
	repr=py.repr
	if sort_kw is SORT_KW_SKIP:
		return a
	else:
		# if sort_kw:# 0 忽略，用 sort_kw=dict(c=0)
		if py.isint(sort_kw):column=sort_kw
		if py.isdict(sort_kw):
			ka.update(sort_kw)
			# if ka:
				# ka.
			# else :ka=sort_kw
	column=get_duplicated_kargs(ka,'col','C','c',default=column)
	reverse=get_duplicated_kargs(ka,'rervese','revese','rev','re','r',default=reverse)
	
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

def eval_safely(source, globals=None, locals=None,noErr=True):
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
eval=evalSafely=safely_eval=safe_eval=eval_safely

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
		import traceback
		return traceback.format_exc() 
		return py.repr(e)
		
	if 'r' in locals:
		r=locals['r']
		if py.istr(r):return r
		if not pformat_kw:
			pformat_kw=get('pformat_kw',{})
		if isipy():
			try:
				ipy=py.from_qgb_import('ipy')
				return ipy.pformat(r,**pformat_kw)# in U
			except Exception as e:
				return py.repr(e)
		
		try:return pformat(r,**pformat_kw)# in U
		except:return py.repr(r)
	else:
		return 'can not found "r" variable after exec locals'+pformat(locals.keys())
exec_return_str=exec_result=exec_str_result=execReturnStr=execResult=execStrResult

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

def calltimes_return_string(a=''):
	return py.str(calltimes(a=a))
sct=scount=calltimes_return_string	
	
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

def warning(msg,tag='qgb.default.logger',**ka):
	import logging
	logger=logging.getLogger(tag)
	return logger.warning(msg,**ka)
warn=warning
	
def set_log_level(level=False,logger=None):
	''' logging.CRITICAL #50
	return level<int>
	'''
	
	if level==True:level=-1 # 0 useless
	if level==False:
		level=50		
		import urllib3
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

		
	import logging
	if logger:
		if py.istr(logger):
			logger=logging.getLogger(logger)
		logger.setLevel(level)
	else:
		#Disable all logging calls of severity 'level' and below.
		logging.disable(level)
	return level
	# log.setLevel(logging.NOTSET) #0
	# log.setLevel(logging.CRITICAL) #50
setlog=setLogLevel=set_log=set_log_level

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
def max_len(*a,return_value=False,return_index=False):
	'''  max( *map(len,U.col(lr,5)) ) 
max_len(dict)==max_len(dict.keys())	
	'''
	if py.len(a)==1:
		a=a[0]
		if py.isdict(a):
			a=py.list(a.keys())
		else:
			a=flat(a)
	im=-1
	v=c_index=py.No('a is empty?',no_raise=1)
	for index,i in enumerate(a):
		n=len(i)
		if n>im:
			im=n
			v=i
			c_index=index
		
	if return_value:
		return v
	if return_index:
		return c_index
	return im
maxLen=max_len	
	
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
	
def dir_show_in_html(a,b='chrome',console=False,call=False):
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
pa=printattr=printAttr=html_dir=htmlDir=dir_show_in_html
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
	if not __ai:dirValue.start=itime();dirValue.cache=[]
	r={}
	if itime()-dirValue.start>timeout:return py.No('#timeout')#r[i]='!timeout %s s'%timeout;break
	
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

def search_iterable(a,filter='',type=None,depth=2,out_limit=99,_i_depth=0,si='a',return_value=False):
	'''iterable
	# typo deepth
#TODO return_value	当前v 或者 上一级 v 。没有想到很好办法去描述
	'''
	if not (py.islist(a) or py.istuple(a) or py.isdict(a)):
		if filter==a:
			return '%r == %s'%(a,si)
		if (py.istr(a) and py.istr(filter) and filter in a):
			return '%r in %r#%s'%(filter,a,si)
		return ''
	# if py.isnum(a):
		# return a if a==filter else []
	# if py.istr(a):
		# return a if filter in a else []
	if _i_depth>depth:return None
	r=[]
	if py.isdict(a):
		its=a.items()
	# if py.islist(a):
	else:
		its=py.enumerate(a)
	# def return_(st):
		# return st
		
	for k,v in its:
		# try:
		ri=''
		if filter==k:
			ri='%r in %s'%(k,si+'[%r] '%k)
		if (py.istr(k) and py.istr(filter) and filter in k):
			ri='{filter!r} in {k!r}\tand {k!r}\tin {si} '.format(filter=filter,k=k,si=si)
				# r.append(k)
		# except:pass
		try:
			if filter in v:
				nfv=v.index(filter)
				# c0=py.max(nfv-50,0)
				# c1=nfv+py.len(filter)+50
				ri='%r in %s[%r]\t#%r '%(filter,si,k,v[py.max(nfv-50,0):nfv+py.len(filter)+50])
		except:pass
		if not ri:## notice a=v
			ri=search_iterable(a=v,filter=filter,type=type,depth=depth,out_limit=out_limit,_i_depth=_i_depth+1,si=si+'[%r]'%k,)
		if ri:
			if py.islist(ri):
				r.extend(ri)
			else:
				r.append(ri)
			if py.len(r)>out_limit:
				r=r[:out_limit]+['...']
				break
				# return ri		
	if _i_depth==0:
		return [StrRepr(i) for i in py.sorted(r)]
	else:
		return r
# searchIterable.r=[]
dict_search=dict_list_search=search_dict_list=findIterable=iterableSearch=searchIterable=search_iterable

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

def inspect_getframeinfo(*a,**ka):
	import inspect
	return inspect.getframeinfo(*a,**ka)	
getframeinfo=inspect_getframeinfo	

def inspect_findsource(*a,**ka):
	import inspect
	return inspect.findsource(*a,**ka)	
findsource=inspect_findsource	

def get_caller_args_dict(*args,**kwargs):
	''' MUST BE FIRST LINE in caller 
	
无法正确处理 *a，**ka 
	
	#TODO  cache by file,lineno of caller's caller , avoid name searching, only get vars
def tf(*a,k=1,**ka):...
inspect.getargspec(tf) # raise \
ValueError: Function has keyword-only parameters or annotations, use getfullargspec() API which can support them	
	'''
	import inspect,ast
	U,T,N,F=py.importUTNF()
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
			if args:
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
		pln('error in',__name__,getArgsDict.__name__,'. debug vars return')
		return py.dict(e=e,frame=frame,rd=rd,lines=lines,args=args,v=v,v_args=v.args, locals=locals()  ) # 形式参数 不会出现在 locals 中？
	
get_arg=get_args=getargspec=getargs=getarg=getArgs=get_args_dict=getArgsDict=get_function_args_dict =get_caller_args=get_caller_args_dict

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
def enumerate(a,start=0,ignore_no=False,index_size=0,**ka):#todo 设计一个 indexList类，返回 repr 中带有index，用下标访问与普通list一样
	'''enumerate(iterable[, start]) -> iterator for index, value of iterable
	
	list <enumerate at 0x6a58d00>
	ignore_no : return if a[i]
	
	'''
	ignore_no=get_duplicated_kargs(ka,'n','ignore_none','ignoreNull',default=ignore_no)
	r=[]
	# index=start
	for i,v in py.enumerate(a):
		if ignore_no:
			if not v:continue
		if index_size:
			r.append( (IntRepr(start,size=index_size),v) )
		else:
			r.append( (start,v) )
		start+=1
	return r
il=ilist=indexList=enu=enumerate

def map(*a):
	'''TypeError: map() takes no keyword arguments
Init signature: map(self, /, *args, **kwargs)
Docstring:
map(func, *iterables) --> map object

Make an iterator that computes the function using arguments from
each of the iterables.  Stops when the shortest iterable is exhausted.
Type:           type
'''
	return py.list(py.map(*a))

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

def itime_sec(a=py.No('auto current timestamp second')):
	if not a:a=timestamp()
	return py.int(a)
itime=itime_sec

def itime_ms():
	return py.int(timestamp()*1000)
itime_js=itime_ms

def strTimeStamp():
	return py.str(getTimestamp())
stimestamp=strTimeStamp	
	
def get_float_us_time(a=py.No('auto current timestamp(float)')):
	'''return: float
--------> U.time()
Out[304]: 1490080570.265625

In [305]: U.time
--------> U.time()
Out[305]: 1490080571.125
'''
	if not a:
		import time
		a=time.time()
	elif py.istr(a) and one_in('/-',a):
		return parse_time(a).timestamp()#
	elif py.isnum(a) and a>0:
		return
	else:
		raise py.ArgumentUnsupported(a)
		
	return a
ftime=float_time=get_float_time=timestamp=getTimeStamp=getTimestamp=get_float_us_time

def getTime():
	from datetime import datetime
	return datetime.now()
time=getime=get_time=get_time_obj=get_current_time=getCurrentTime=getTime	

def getDate():
	from datetime import datetime
	return datetime.now().date()
date=getdate=getDate
	
def get_float_tail(a,**ka):
	'''  ,ndigits=20,str=False,int=False  # default return float
if str: return '.xxx'
if int: return xxx	
	
	see help(round)
 0.1**5
 1.0000000000000003e-05

 0.1**4
 0.00010000000000000002 小数位数20

 In [77]: U.getFloaTail(f,ndigits=3,s=True)
Out[77]: '.296'

In [78]: U.getFloaTail(f,ndigits=3,i=True)
Out[78]: 296

In [79]: U.getFloaTail(f,ndigits=3,f=True)
Out[79]: 0.296

 '''
	ndigits=get_duplicated_kargs(ka,'n','nd','digit','digits','ndigits')
	str=get_duplicated_kargs(ka,'s','str','string','STR','S')
	int=get_duplicated_kargs(ka,'i','int','integer','INT','I','Integer')

	if py.isfloat(a):
		a=round(a-py.int(a),ndigits)#This always returns a floating point number.
		if str:
			return py.str(a)[1:]
		if int:
			r=py.str(a)[2:]
			m=ndigits-py.len(r)
			return py.int(r)*(10**m)#
		return a	#default
	else:
		return py.No('Not float')	
getFloaTail=get_float_tail
		
def stime_(time=None,ms=True):
	r=getStime(time=time,ms=ms)
	return T.regexReplace(r,'[^0-9_]','_')
	
gsTimeFormatFile=get_or_set('gsTimeFormatFile','%Y-%m-%d__%H.%M.%S')
gsymd=gsYMD=gsTimeFormatYMD='%Y%m%d'
gsTimeFormat='%Y-%m-%d %H:%M:%S'
#ValueError: year=1 is before 1900; the datetime strftime() methods require year >= 1900
def str_to_datetime(a):
	''' #TODO:  转换 字符串 或其他时间格式
	''' 	 
	try:
		import dateutil
		return dateutil.parser.parse( a)
	except ModuleNotFoundError as e:
		print(e)
	except Exception as e:
		pass
	###		
	try:
		import datefinder
		r=py.list(datefinder.find_dates( a) )
		
		if py.len(r)==1:return r[0]
		
	except ModuleNotFoundError as e:
		print(e)
	except Exception as e:
		pass
	if '.' in a and '_' in a:
		ms=0
		if all_in(a[-4:],T._09+'.'):
			ms=T.sub(a[-4:],'.')
			n=0-py.len(ms) # .a[n] in 0-9
			ms=py.int(ms)
			while n<0:
				n=n-1  
				if a[n] in T._09:
					break
			else: #n >=0 aka n==0
				n=py.len(a)
			a=a[:n]
		a=a.replace('.',':').replace('_',' ')
		dt= str_to_datetime(a)
		dt=dt.replace(microsecond=ms)
		return dt
		#datetime是不可变对象，要修改只能 dt.replace
	# if py.len(a)>22:return str_to_datetime(a[:22])
	raise py.ArgumentError(a)
		
try_parse_stime=str_to_datetime
	
def get_time_as_str(time=None,format=gsTimeFormatFile,ms=True,time_zone=py.No('原来，除非指定')):
	'''http://python.usyiyi.cn/translate/python_278/library/time.html#time.strftime
	TODO: 可以指定 ms
U.stime(0.0005)
'1970-01-01__08.00.00__.001'

U.stime(0.0004)
'1970-01-01__08.00.00__.0'	
	'''
	if not py.istr(format):raise ValueError('format is str')
	
	import time as tMod
	import datetime
	ms_tail=0
	if py.isinstance(time,tMod.struct_time):
		pass
	elif py.isinstance(time,datetime.datetime):
		ms_tail=time.microsecond 
		time=time.timetuple()
	elif py.istr(time):
		time=str_to_datetime(time).timetuple()
	elif py.isnum(time):
		if py.type(time) is not py.float:time=py.float(time)		
		if time > IMAX:
			time=time/1000
		ms_tail=get_float_tail(time,ndigits=3,int=True)
				
		time=tMod.localtime(time) #return time.struct_time
	elif not time:
		time=getTimestamp()
		return get_time_as_str(time)
	else:
		raise py.ArgumentUnsupported(time)
	if format=='':return str(time)
	
	if '%' in format:
		if time:
				# print(type(time ),getFloaTail(time,ndigits=3,s=True) )
			r=tMod.strftime(format,time)
#localtime: time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=8,....
			if ms :
				ms_tail='%03d'%ms_tail
				if '__' in format:
					ms_tail='__.'+ms_tail
				else:
					ms_tail='.'+ms_tail
				r+=ms_tail
			return r
		else:return tMod.strftime(format)
stime=getCurrentTimeStr=timeToStr=getStime=get_time_as_str

def parse_time_str(a,format='%Y-%m-%d__%H.%M.%S'):
	''' return datetime.datetime( '''
	try:
		from dateutil import parser
		return parser.parse(a) #return type datetime.datetime
	except Exception as e:
		pass
	import time,datetime
	struct_time = time.strptime(a,format)#time.struct_time(tm_year=
	return datetime.datetime.fromtimestamp(time.mktime(struct_time))
	# return r
parse_time=stime2time=stime_to_time=parse_stime=parse_time_str	

def timezone_to_timedelta(a):
	'''
In [242]: 0<=i<=1
Out[242]: False

In [243]: 0=<i<=1
  File "<ipython-input-243-0732a0107c4d>", line 1
    0=<i<=1
      ^
SyntaxError: invalid syntax
'''	
	
	# from datetime import datetime, timedelta, tzinfo
	import datetime
	if py.isint(a):
		if -14 <= a <= 14:
			return datetime.timedelta(seconds=3600*a)
		else:
			raise py.ArgumentError(a)
	if py.istr(a):
		import pytz
		return pytz.timezone(a)._utcoffset
	raise py.ArgumentUnsupported(a)	
	
def better_float(x,):
	''' float(x=0, /)  Subclasses:     float64
0.07999999999999999  hangs	

11.200000000000001

rs=T.regex_match_all(s,r'([0-9])\1{11,}') # 12不行，11 返回 最少12 个重复
if not rs:return r

像 1/3==0.3333333333333333 这是正常结果，不用处理
	'''
	r=py.float(x)
	# for i in range(99):
	s=py.str(r)
	for i in py.range(11):
		if '0'*12 in s:
			f=r-(0.1**16*i)
			if py.len(py.str(f)) < py.len(s):return f
		elif '9'*12 in s:
			f=r+(0.1**16*i)
			if py.len(py.str(f)) < py.len(s):return f
		else:
			return r

def float_with_default(obj,*other,default=None):
	''' FuncWrapForMultiArgs: if default!=None:
# FloatRepr	
	'''
	return FuncWrapForMultiArgs(f=better_float,args=(obj,other),default=default)
float=float_with_default	

def int_with_default(obj,*other,default=None):
	''' FuncWrapForMultiArgs: if default!=None:'''
	return FuncWrapForMultiArgs(f=py.int,args=(obj,other),default=default)
int=int_with_default	
	
def least_common_multiple(x,y):
	'''最大公因数（英语：highest common factor，hcf）也称最大公约数（英语：greatest common divisor，gcd）
least common multiple , lcm 最小公倍数
	'''
	# 1. from https://bugs.python.org/msg361033
	from math import gcd
	if x==0:return 0
	return abs(x // gcd(x, y) * y)
	############

	# 2. numpy
	try:
		from numpy import lcm
		return lcm(x,y)
	except Exception as e:
		pass
	############

	# 3. slow version #	
	if x>y:z = x
	else  :z = y
	while(True):
		if((z % x == 0) and (z % y == 0)):
			lcm = z
			break
		z += 1 
	return lcm
	############
lcm=least_common_multiple	

def greatest_common_divisor(x,y):
	'''最大公因数（英语：highest common factor，hcf）也称最大公约数（英语：greatest common divisor，gcd）
least common multiple , lcm 最小公倍数
	'''
	try:
		from math import gcd
		return gcd(x,y)
	except Exception as e:
		pass
	
	 # euclid's algorithm
	if y == 0: return x
	return gcd(y, x%y)
gcd=greatest_common_divisor

def math_factorial(n):
	'''分解质因数
	'''	
	import math
	return math.factorial(n)
jc=factorial=math_factorial

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
	''' Notice：TimeOut ！ 分解大数时可能会消耗较长的时间
	
https://stackoverflow.com/questions/51533621/prime-factorization-with-large-numbers-in-python 
	'''
	if not py.isnum(n):raise ArgumentError(n)
	n=py.int(n)
	try:
		import sympy.ntheory
		return sympy.ntheory.factorint(n) # time may out, 下面的朴素实现耗时更长
	except Exception as e:
		setErr(e)
	
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
factorint=factors=integer_factorization=prime_factorization
# (1917141215419419171412154194191714)
# [2, 3, 13, 449941L, 54626569996995593878495243L]
def get_int_multiplication_expression(a,factor=1024,use_pow=True,add_symbol=' + ',mul_symbol='*'):
	''' 12/3 = 4 的英文说法是12 divided by 3 is 4， 除出来的结果称为「商」，就是quotient，而余数是remainder
	'''
	if not factor or py.abs(factor)==1:
		raise py.ArgumentError(a,factor)
	if not a:return a
	
	def join_m(a,fs):
		if a==0 :
			return
		lfs= py.len(fs)
		if use_pow and lfs>1:
			fs=['%s**%s'%(factor,lfs) ]
		# else:
			
		if a==1:
			if fs:
				ts.insert(0,T.join(*fs,separator=mul_symbol))
			else:
				ts.insert(0,a)
		else:
			ts.insert(0,T.join(a,*fs,separator=mul_symbol))
	ts=[]
	fs=[]
	while a>=factor:
		quotient,remainder=py.divmod(a,factor) #if isint(a): return int tuple ;float return float
		a=quotient
		# if remainder:
		join_m(remainder,fs) 
		fs.append(factor)
	join_m(a,fs)
	return T.join(ts,separator=add_symbol)
num_exp=number_exp=number_expression=int_exp=get_int_exp=get_multiply_exp=get_int_multiplication_expression
		
		
def product_of_integers(*a):
	r=1
	for i in a:
		r=r*i
	return r
multiplication=product_of_integers

def multiply_by_multiples(iterable,times):
	''' 对 iterable 中每个元素 乘以 times.
return list_float
In [1566]: U.multiply_by_multiples(U.range(9),2)
Out[1566]: [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0]
	
	r=a,b,c=list(map((2).__mul__, [1, 2, 3]))
	'''
	if py.iterable(times):
		iterable,time=time,iterable
	times=py.float(times)
	mul=lambda a:times*py.float(a)
	r=py.map(mul,iterable)
	return py.list(r)
mul=mutiply_iterable=mutiply_list=mutiply_tuple=multiply_by_multiples

def tuple_operator(a,operator,b=None,operator_ka={},skip_AttributeError=False):
	''' 对两个长度相等的（tuple，list，...） 操作
如果只对一个tuple操作，可以这样用：  t=U.tuple_operator(t,t,U.StrRepr)	

	'''
	r=[]
	for n,v in enumerate(a):
		try:
			if py.istr(operator):
				if b:
					if py.isnum(b):
						r.append( py.getattr(v,operator)(b) )
					else:
						r.append( py.getattr(v,operator)(b[n]) )
				else:
					r.append( py.getattr(v,operator)()     )
					
			elif py.callable(operator):
				r.append( operator(v,**operator_ka) )
			elif not operator and py.callable(v) and b:
				r.append( v(b[n]) )
				# if 
				
			else:
				raise NotImplementedError('operator type')
		except AttributeError:
			if not skip_AttributeError:raise
			else:
				r.append(v)
	if py.istuple(a):
		return py.tuple(r)
	return r
	
def tuple_add(a,b):return tuple_operator(a=a,b=b,operator='__add__')
add_two_tuple=tuple_add

def tuple_minus(a,b):return tuple_operator(a=a,b=b,operator='__sub__')
minus=tuple_minus

def tuple_multiply(a,b):return tuple_operator(a=a,b=b,operator='__mul__')
mul=multiply_two_tuple=tuple_multiply

def tuple_div(a,b):return tuple_operator(a=a,b=b,operator='__truediv__')
div=div_two_tuple=tuple_div

def time_range_list(*a,**ka):
	return py.list(time_range(*a,**ka))

def traverseTime(start,stop=None,step='day',**ka):
	'''
	#TODO ipy 自动化测试框架 ， 解决 ipy3 兼容问题
	range(start, stop[, step])
	datetime.timedelta(  days=0, seconds=0, microseconds=0,
				milliseconds=0, minutes=0, hours=0, weeks=0)
	step default: 1(day)  [1day ,2year,....]  [-1day not supported]
	
a=-4 # relativedelta(months=+a) ==  relativedelta(months=-4)	

from dateutil.relativedelta import relativedelta

pip install python-dateutil

	'''
	import re,datetime as dt
	from dateutil.relativedelta import relativedelta
	
	U=py.importU()
	sregex='([0-9]*)(micro|ms|milli|sec|minute|hour|day|month|mouth|year)'
	timedeltaKW=('days', 'seconds', 'microseconds',
 'milliseconds', 'minutes', 'hours', 'weeks')
	
	
	
	if py.istr(step):
		step=step.lower()
		rm=re.match(sregex,step)
		if not rm or not step.startswith(rm.group()):
			raise Exception('Invalid argument step '+py.repr(step))
		istep,step=U.int(rm.group(1),default=1,),rm.group(2)
		# if step.startswith('year'):
			# istep,step=365*istep,'day'#没考虑闰年
		if step.startswith('ms'):step='milliseconds'
		astep={}
		for i in timedeltaKW:
			if i.startswith(step):
				astep[i]=istep
		if astep:tdelta=dt.timedelta(**astep)
		
		if one_in(['month','mouth'],step):
			# lsi=T.filter_int(step)
			# if lsi:
				# if py.len(lsi)!=1:raise py.ArgumentError('step=%r int must be none or one'%step)
				# step=py.int(lsi[0])
			# else:step=1
			tdelta=relativedelta(months=istep,)
			tdelta.total_seconds=lambda :60*60*24*30
		if 'year' in step:
			tdelta=relativedelta(years=istep)
			tdelta.total_seconds=lambda :60*60*24*365
			
	elif py.type(step) in (py.int,py.long):
		tdelta=dt.timedelta(days=step)
	elif py.type(step) is py.type(dt.timedelta.min):
		tdelta=step
	# return tdelta
	start=datetime(start)
	if stop:stop=datetime(stop)
	else:stop=dt.datetime.max
	if tdelta.total_seconds()==0.0:
		print("U.set('t3',",set('t3',[start,stop,tdelta]))
		return start,stop,tdelta
	yield start	
	start=start+tdelta
	while start < stop:
		yield start
		start+=tdelta
	# return i #SyntaxError: 'return' with argument inside generator
time_delta=timeDelta=iter_time=range_time=time_range=rangeTime=timeRange=timeTraverser=timeTraversal=traverseTime	

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
		if re.match('[0-9]{6}',a):
			return dt(py.int(a[:4]), py.int(a[4:6]),1)
		if re.match('[0-9]{4}',a):
			return dt(py.int(a[:4]),1,1)
		raise py.ArgumentUnsupported(a)
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
	
def exit(i=2357,msg=''):
	'''terminate process,will not call atexit'''
	if not msg:
		if py.istr(i):
			msg,i=i,2357
		msg='\n{} pid {} exit! {}'.format('#'*22,pid,msg)
	print(msg)
	os._exit(i)

def get_modules_dict_by_file(fileName,return_list=False):
	'''
	return dict {sname:mod ...}
return_list=True : only return [mods]
	
	
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
	if return_list:
		return py.list(dr.values())
	return dr
	
mbf=modByFile=mod_by_file=getModByf=getModf=getModByF=getModF=getmbf=getmf=modulesByFile=getModsByFile=getModulesByFile=get_module_by_file=get_modules_by_file=get_module_dict_by_file=get_modules_dict_by_file
	
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
	
	
def get_modules_by_path(modPath=None):
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
get_qpsu_all_modules=get_modules_by_path

def get_all_modules_list(mods=py.No('default all'),name_padding=57):
	U,T,N,F=py.importUTNF()
	ms=sys.modules.items()
	if mods:
		if py.istr(mods):
			# mods=get_modules_by_path
			ms=U.get_modules_dict_by_file(fileName=mods).items()
			# if not mods:return mods	
		
		if py.islist(mods) and py.istr(mods[0]):
			ms=[(k,v) for k,v in sys.modules.items() if k in mods()]
		
	return [[StrRepr(k,size=name_padding),v] for k,v in ms]
getMods=get_mods=get_modules=getAllMod=getAllModules=getAllMods=get_all_modules_list

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
qpsu_file=get_qpsu_file=get_qpsu_file_path=getQPSUFilePath=getQpsuFilePath=get_qpsu_file_path

def getModPath(mod=None,qgb=True,slash=True,backSlash=False,end_slash=True,trailingSlash=True,**ka):
	'''不返回模块文件，返回模块目录
	@English The leading and trailing slash shown in the code 代码中的首尾斜杠'''
	# if mod:
		# sp=os.path.abspath(mod.__file__)
	end_slash=get_duplicated_kargs(ka,'endslash','endSlash',default=end_slash)	
	if mod:
		m=getMod(mod)
		if not m:
			if '/' in mod:
				if not end_slash and not mod.startswith('/'):
					mod='/'+mod
				if end_slash:
					if mod.startswith('/'):mod=mod[1:]
					if mod.startswith('./'):mod=mod[2:] #这个输入不应该存在
					
				sp=__file__	
			else:
				return py.No('can not get mod:',mod)
		else:		
			sp=os.path.abspath(m.__file__)
			mod=''
	else:
		sp=__file__
		mod=''
	sp=os.path.abspath(sp)
	sp=os.path.dirname(sp)
	sp=os.path.join(sp,'')
	#sp is qgb\ if qgb/.. import
	# if debug():py.pdb()
	if iscyg():#/usr/lib/python2.7/qgb/  
		sp=getCygPath()+sp[1+4:].replace('/','\\')
	if not qgb:
		sp=sp[:-4]
	
	if not end_slash:trailingSlash=False
	if trailingSlash:
		if sp[-1] not in ('/','\\'):sp+='/'
	else:
		while sp[-1] in ('/','\\'):
			sp=sp[:-1]
			
	if backSlash or not slash:
		sp=sp.replace('/','\\')
	else:sp=sp.replace('\\','/')

	return sp+mod
get_qpsu_path=getQPSUPath=getQpsuPath=get_qpsu_dir=getQPSUDir=get_mod_dir=get_module_dir=get_module_path=getModPath

def import_module_by_full_path(f,exec_code=True,add_sys_modules=True):
	''' if not exec_code 模块的属性也不会初始化
	
reload 重新调用此函数 就相当于 reload	
'''	
	import importlib.util
	U,T,N,F=py.importUTNF()
	
	if not f.lower().endswith('.py'):raise py.ArgumentError(f)
	fn=F.get_filename_from_full_path(f)[:-3]
	mod_name=fn
	'''add_sys_modules 只能解决#Error  module www.xiezhen.xyz not in sys.modules
和#Error  parent 'www.xiezhen' not in sys.modules
不能解决 U.r(X) spec not found for the module   所以注释掉了
'''
	# if add_sys_modules:
		# vs=T.regex_match_all(fn,T.RE_VAR_EXACTLY)
		# mod_name='_'.join(vs)
			
		# mod_name=U.input('mod_name:',mod_name)	
	spec= importlib.util.spec_from_file_location(mod_name,f)# mod name 用特殊字符不会报错
	mod=importlib.util.module_from_spec(spec)
	# mod.__spec__ =spec#不能解决 U.r(X) spec not found for the module 'www_xiezhen_xyz'
	if exec_code:spec.loader.exec_module(mod)
	# if add_sys_modules:sys.modules[mod_name]=mod
	
	return mod
reload_from_file=reload_from_path=importf=import_file=import_f=import_from_file=import_module_by_full_path		
	
def len_return_string(a,*other):
	return py.repr(len(a,*other) )
lens=len_return_str=len_return_string

def len_args_as_string(*a):
	'''In [57]: print(i for i in range(8))
<generator object <genexpr> at 0x000001939D3F8E48>
In [59]: print(*[i for i in range(8)])
0 1 2 3 4 5 6 7
'''
	return len(*[T.string(i) for i in a])
slen=str_len=string_len=len_arg_as_string=len_args_as_string

def _len(obj):
	'''len(obj, /)

	'''
	if py.isgen(obj):
		n=-1
		for i in obj :
			n=n+1
		return n+1
	return py.len(obj)

len_generator=generator_len=_len

def _hash(obj):
	if py.islist(obj):
		try:
			return py.hash(py.tuple(obj))
		except Exception as e:
			return py.No(e)
	return py.hash(obj)

def len(obj,*other,return_index=False,**ka):
	'''Exception return py.No or [no...]'''
	return_index=get_duplicated_kargs(ka,'index','i','n','enumerate',default=return_index)
	return FuncWrapForMultiArgs(f=_len,args=(obj,other),index=return_index )# ,default=default
	
def print_len(*a,**ka):
	return pln(len(*a,**ka),)

def hash(obj,*other):
	'''Exception return py.No or [no...]'''
	return FuncWrapForMultiArgs(f=_hash,args=(obj,other))

# def id(obj,*other):
	# return FuncWrapForMultiArgs(f=py.id,args=(obj,other))
	
# def type(obj,*other):
	# return FuncWrapForMultiArgs(f=py.type,args=(obj,other))

# def bin(obj,*other):
	# return FuncWrapForMultiArgs(f=py.bin,args=(obj,other))
# 'complex','float','int','len','hash','repr',
for builtin_function_name in ['bin','bool','callable','chr','hex','id','max','min','oct','ord','type',
		]:
	py.execute('''
def {0}(obj,*other):return FuncWrapForMultiArgs(f=py.{0},args=(obj,other))
	'''.format(builtin_function_name) )		
	
def FuncWrapForMultiArgs(f,args,default=None,index=False,f_ka={}):
	'''Exception return py.No'''
	obj,other=args ########## other is tuple
	all=py.list(other)
	all.insert(0,obj)
	r=[]
	for n,i in py.enumerate(all):
		try:
			r1=f(i,**f_ka)
		except Exception as e:
			if default!=None:
				r1=default
			else:
				r1=py.No(e)
		if index:r1=(n,r1)
		r.append(r1)
	if other:
		return r
	else:
		return r[0]  #U.len(obj) == py.len(obj)
builtinFuncWrapForMultiArgs=FuncWrapForMultiArgs

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

def simulate_key_write(astr, delay=0,restore_state_after=True, exact=None,**ka):
	import keyboard
	delay=get_kargs_duplicated(ka,'Delay','sleep','pause','wait',default=delay)
	keyboard.write(text=astr, delay=delay, restore_state_after=restore_state_after, exact=exact)
	return StrRepr(astr,repr='U.simulate_key_write(%r)'%astr)
text_key=text_key_write=keyboard_write=simulate_key_write	

def get_keyboard_all_mapping():
	'''return dict 
official_virtual_keys = {
    0x03: ('control-break processing', False),
    0x08: ('backspace', False),
    0x09: ('tab', False),
...	
}	
'''
	import keyboard
	return keyboard._os_keyboard.official_virtual_keys
get_keyboard_map=get_keyboard_all_mapping
def simulate_key_press(*akey, delay=0,restore_state_after=True, exact=None,**ka):
	'''pip install keyboard
	
keyboard._os_keyboard.official_virtual_keys

	
U.simulate_key_press('shift+s')    # OK  
U.simulate_key_press(['shift+s'])  #ValueError: ("Key 'shift+s' is not mapped to any known key.", ValueError("Key name 'shift+s' is not mapped to any known key."))
'''	
	
	# parsed=keyboard.parse_hotkey(akey)
	# if py.len(parsed)>1: #如果 多个组合键中间想要delay,使用 action_list 
	import keyboard
	if not delay:delay=get_kargs_duplicated(ka,'Delay','sleep','pause','wait')
	for k in akey:
		keyboard.press_and_release(k, do_press=True, do_release=True)
		if delay and delay>0:sleep(delay)
	return StrRepr(akey,repr='U.simulate_key_press(*{!r})'.format(akey)) # 不要用%r,如果传入一个tuple类型，TypeError: not all arguments converted during string formatting
system_key=pressKey=keyPress=press_key=key_press=simulate_key_press

def simulate_system_actions(a=py.No("str[key|key_write ] or action list[['click',xy],['move',xy],[foreground,title|handle],['k','sss'],['t','text']]"),key='', delay=py.No('using _DELAY'),restore_state_after=True, exact=None,raise_error=False,**ka):
	'''pip install keyboard
key='Win+D'  # mute  ,not min all window	
	
	
Signature: keyboard.write(text, delay=0, restore_state_after=True, exact 精确=None)
Docstring:
Sends artificial keyboard events to the OS, simulating the typing of a given
text. Characters not available on the keyboard are typed as explicit unicode
characters using OS-specific functionality, such as alt+codepoint.

To ensure text integrity, all currently pressed keys are released before
the text is typed, and modifiers are restored afterwards.

- `delay` is the number of seconds to wait between keypresses, defaults to
no delay.
- `restore_state_after` can be used to restore the state of pressed keys
after the text is typed, i.e. presses the keys that were released at the
beginning. Defaults to True.
- `exact` forces typing all characters as explicit unicode (e.g.
alt+codepoint or special events). If None, uses platform-specific suggested
value.
File:      c:\qgb\anaconda3\lib\site-packages\keyboard\__init__.py'''
	Win=py.from_qgb_import('Win')
	_DELAY=0.2
	if not py.isint(delay):
		delay=get_duplicated_kargs(ka,'sleep','delay','wait')
	if not py.isint(delay):
		delay=_DELAY
	if not raise_error:
		raise_error=get_duplicated_kargs(ka,'err','error','exp','exception','Exception',
'raise_err','raise_error','raiseError','raiseErr','raise_EnvironmentError','EnvironmentError','raiseEnvironmentError')
		
	def _sleep(sec=None):
		#TypeError: object of type 'IntCustomStrRepr' has no len()
		# if (index+1)==py.len(a):return #skip last sleep
		if not sec:sec=delay #暂时没用 默认参数
		sleep(sec)
		if sec!=_DELAY:
			r.append(['delay',sec])
	if a and not py.istr(a):
		if py.isdict(a):a=a.items()
		r=[]
		for index,row in py.enumerate(a):
			if py.istr(row):
				try:
					import keyboard
					keyboard.parse_hotkey(row) #将 parsed传入 将会再次parse_hotkey，导致无按键效果
					simulate_key_press(row)
					r.append(['key',row])
				except Exception as e:
					simulate_key_write(row)
					r.append(['txt',row])
				_sleep(delay)
				continue
			if py.isdict(row):
				if py.len(row)!=1:raise py.ArgumentError("a[%s]== %r dict.len != 1,should be {'key|text':'str_data' }"%(index,row))
				for _row in row.items():
					row=_row
				
			if py.islist(row) or py.istuple(row):
				# if py.len(row)!=2:raise py.ArgumentError("a[%s]== %r list.len != 2 ,should be['key|text','str_data']"%(index,row))
				if py.isint(row[0]) and py.isint(row[1]):
					row=['click',row]
				
				action=row[0].lower()
				if 'click' in action:######
					if py.len(row)==1:
						row.append(Win.get_cursor_pos())
					Win.click(*row[1])
					r.append(['click',row[1]])
					_sleep(delay)
					continue
				elif one_in(['move','mv_cur','move_cur','mv','set_cur_pos'],action):
					Win.set_cur_pos(*row[1])
					r.append(['move',row[1]])
					_sleep(delay)
					continue
				elif one_in(['set_window','top','front','window','for','forground','foreground','win32gui.setforegroundwindow','setforegroundwindow','forward'],action):
					a=Win.set_foreground(row[1],raise_error=raise_error)
					r.append(['foreground',a])
					_sleep(delay);continue
				elif one_in(['delay','sleep','wait'],action):
					_sleep(py.int(row[1]))	
					continue
				elif 't' in action:############
					simulate_key_write(row[1])
					r.append(['txt',row[1]])
					_sleep(delay);continue
				elif 'k' in action:############
					simulate_key_press(row[1])
					r.append(['key',row[1]])
					_sleep(delay);continue
				else:###########################
					raise py.ArgumentError("a[%s]== %r[0] not supported!! key|text|delay"%(index,row))
			
		return py.tuple(r)
	if a :simulate_key_write(a)
	
	if key:simulate_key_press(key)
	
	
		
key_action=key_actions=system_actions=system_action=sys_act=sys_acts=sys_actions=sys_action=simulate_system_actions

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

def set_env(name,value):
	os.environ[name]=value
	return value
	
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
			return os.environ[i]
	return py.No('not found in os.environ',name)
get_env_path=get_path_env=get_environ=get_env=getenv=getEnv=getEnviron
	
def getParentPid(pid=None):
	''' os.getpid() '''
	import psutil
	if not pid:
		pid=globals()['pid']
	return psutil.Process(pid).ppid()
ppid=getppid=get_ppid=getParentPid	
	
def getParentCmdLine():
	import psutil
	return psutil.Process(getppid()).cmdline()
getpargv=getParentCmdLine	

def get_process_by_pid(pid):
	'''process_name = process.name()
pid Not exist will NoSuchProcess: psutil.NoSuchProcess no process found with pid 35454	
	'''
	import psutil
	return psutil.Process(pid)			  
getProcessByPid=get_process_by_pid

def get_process_name_by_pid(pid):
	import psutil
	return psutil.Process(pid).name()						
						
def get_all_process_list(name='',cmd='',pid=None,ppid=None):
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
			i.cmd=py.No(e) #NoneObj #TODO 需要一个 空字符 类，携带出错或其他信息				

		if py.isint(pid) and pid>=0:
			if pid==i.pid:r.append(i)
			continue# 找到 找不到 ，都下一条
		if py.isint(ppid) and ppid>=0:
			if ppid==i.ppid():r.append(i)
			continue
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
ps=getTasklist=getProcess=getProcessList=get_all_process_list

def get_all_process_value_list(**ka):
	''' ka : title=True  : return [  [pid      , ppid     , cmd      ] ...] 
	'''
	U=py.importU()
	filter=U.get_duplicated_kargs(ka,'filter','ps',default={})
	column_size_ka=U.get_duplicated_kargs(ka,'column_size_ka','dcol','dc',default={})
	
	size=7 # must <10
	column_size_ka={}
	column_size_ka['pid']=U.get_duplicated_kargs(ka,'pid','PID','p',default=size)
	column_size_ka['ppid']=U.get_duplicated_kargs(ka,'ppid','PPID','pp',default=size)
	column_size_ka['_create_time']=U.get_duplicated_kargs(ka,'_create_time','time',default=26)#,'t' 和title冲突了
	
	column_size_ka['cmd']=U.get_duplicated_kargs(ka,'cmd','CMD','cmdline','command','c',default=1) # cmd 每行最后

	def is_size(k,v):
		nonlocal column_size_ka,size,filter
		if py.isint(v):
			if k in ['pid','ppid']:
				if v<0:raise py.ArgumentError('[p]pid column_size_ka or filter must >=0')
				if 0<v<10:return v
				else  :
					if k not in filter:filter[k]=v
					column_size_ka[k]=size
					return False
			else:#此处不可能 是 filter
				if v>1:return v
				else  :return False
		elif py.islist(v):
			return U.get_slice_len(v)
		else:	
			if k not in filter:filter[k]=v #这个写法很绕，但是懒得改了
			return False
		
		
	###########
	need_title= U.get_duplicated_kargs(ka,'need_title','title','tips','tip','t',default=1)
	title=[]
	for k,v in column_size_ka.items():#if v  default always True
		iss=is_size(k,v)#这个总要执行
		if need_title and v:
			if iss:
				title.append(U.StrRepr(k,size=iss))
			else:	
				title.append(U.StrRepr(k,size=size))
	if need_title:r=[title]			
	else         :r=[]
	###########
	for p in get_all_process_list(**filter):
		row=[]
		for k,v in column_size_ka.items():
			if v:
				try:
					pv=py.getattr(p,k)
					if py.callable(pv):
						pv=pv()
					if v=='raw':
						pass
					elif py.callable(v):
						pv=v(pv)
					elif py.isint(pv):
						pv=U.IntRepr(pv,size=size)
					elif py.isfloat(pv) and ('time' in k):
						pv=U.StrRepr( U.stime(pv) )
					elif py.istr(pv) and py.islist(v):
						pv=U.StrRepr( pv[v[0]:v[1]],size=U.get_slice_len(*v) )
					row.append(pv)

				except Exception as e:
					row.append(py.No(e))
		
		# if cmd:row.append(p.cmd)
		r.append(row)
	return r
ps_path=psCmd=ps_cmd=ps_value=ps_values=GetCommandLine=getCommandLine=get_command_line=getCmdList=get_cmd_list=get_all_process_cmd_list=get_all_process_value_list

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
def kill(*ps,caseSensitive=True,confirm=True,**ka):
	'''TODO:use text Match if any
	'''
	import psutil,subprocess
	confirm=get_duplicated_kargs(ka,'ask','pause','yes','y','kill',default=confirm )
		
	r=[]
	if not ps:ps=py.importU().ps(**ka)
	for a in ps:		
		if isinstance(a,psutil.Process):
			r.append(a)
		elif isinstance(a,(subprocess.Popen,)):
			r.append(psutil.Process(a.pid) )
		elif py.istr(a):
			for i in psutil.process_iter():
				if caseSensitive:
					if i.name() == a:r.append(i)
				else:
					if i.name().lower() == a.lower():r.append(i)
				if confirm and a.lower() in i.name().lower():
					r.append(i)
		elif py.isint(a):
			if not psutil.pid_exists(a):
				return py.No('pid %s not exist!'%a)
			r.append(psutil.Process(a) )
		else:
			raise ArgumentUnsupported()
	if not r:return py.No(msg='Not found {},{}'.format(ps,ka))
	if confirm:
		pprint(r)
		c=py.input('kill Process？(n cancel)')
		if c.lower().startswith('n'):return
	for n,i in py.enumerate(r):
		try:
			r[n]={i:i.kill()==None}
		except Exception as e:
			r[n]={i:py.No(e,msg=py.getattr(e,'msg','')[18:])}
			
	return r		
			

def get_process_all_modules_by_pid(pid,only_name=0):
	import psutil
	try:
		p = psutil.Process( pid )
		r=p.memory_maps()	#  pmmap_grouped list
	except Exception as e:
		return py.No(e)
	if only_name:
		F=py.importF()
		r=[F.get_filename_from_full_path(i.path) for i in r] 
	return r  
	# for dll in p.memory_maps():
	# print(dll.path)
get_dlls=get_dll=getDLL=getDLLs=getDll=getDlls=getdlls=get_dll_list=get_process_dlls_by_pid=get_process_all_dlls_by_pid=get_process_all_modules_by_pid

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
		if is_builtin_function(a):
			return py.No('is_builtin_function',a)
		if py.callable( py.getattr(a,'__init__',None) ):
			r=get_obj_file_lineno(a=a.__init__,lineno=lineno,auto_file_path=auto_file_path)
			if r:return r
		a=get_obj_module(a)#python无法获取class行数？https://docs.python.org/2/library/inspect.html
		return get_obj_file_lineno(a=a,lineno=lineno,auto_file_path=auto_file_path)
get_obj_fn=get_obj_file_lineno

	
def get_net_io_bytes():
	# global F
	# if not 
	import psutil
	c=psutil.net_io_counters()
	m=c.bytes_sent+c.bytes_recv
	return F.IntSize(m)
		
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
			if not F.exist(vsbin):#root用户 下可能没有
				vsbin='/home/qgb/.vscode-server/bin/'#TODO auto find all user
				if not F.exist(vsbin):raise py.EnvironmentError('not found ~/.vscode-server/bin/ ')
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
	get_cmd=False,line_arg='-n',):
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
		npath=editor_path
	else:
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
			npath=find_driver_path(r':\QGB'+'/npp/notepad++.exe')		
		if not os.path.exists(npath):
			npath=find_driver_path(r":\Program Files"+nppexe)#如果最后没有匹配到，则为 空.....
	if DEBUG:pln (repr(npath),nppexe)
	# npath='"%s"'%npath
	# print(233333333333)  # add this work?
	# msgbox(npath,py.dir())  #U.r not work ?

	if a:
		f,lineno=get_obj_file_lineno(a,lineno=lineno,auto_file_path=auto_file_path)
		if py.len(f)>250:
			f=py.importF().nt_short_path(f)
			
		if 'notepad++.exe' in npath.lower():#参数不要分开
			line_arg='{} {}'.format(line_arg,lineno)
			lineno=''
		if 'emeditor.exe' in npath.lower():#参数要分开
			pass# 这是c:\qgb\anaconda3\lib\subprocess.py:769默认行为
		return run(npath,f,line_arg,lineno)
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
	return ast.parse(inspect.getsource(mod))
getModAST=getAST

def rebuild_function_call_self_args_str(a,cbs=False):
	U=py.importU()
	r=a.__name__+'(' # lambda : '<lambda>'
	a=U.getfullargspec(a)
	for s in a.args:
		r+='{0}={0},'.format(s)
	# if a.varargs: # 如果args指定了名称 TypeError: ft() got multiple values for argument 'q'，不指定名称 按顺序调用没事
	if a.varkw:r+='**%s,'%a.varkw
	r=r+')'
	if cbs:U.cbs(r) 
	return U.StrRepr(r)
get_function_call_self_str=get_function_call_self_args=generate_function_call_self_args=rebuild_function_call_self_args=rebuild_function_call_self_args_str	
def argspec_to_str(a):
	U=py.importU()
	a=U.getfullargspec(a)
	
fullargspec_to_str=argspec_to_str	

def get_source(a):
	import inspect
	U=py.importU()
	if py.istr(a):
		if F.exist(a):
			if a.lower().endswith('.pyc'):
				import uncompyle6,io
				out=io.StringIO()
				r=uncompyle6.decompile_file(a,outstream=out)
				# U.get_or_set('uncompyle6.decompile_file return',{})[U.stime()]=r
				return out.getvalue() 
			return F.read(a)
		a=U.get_module_by_file(a)
		# return #fileName
	f,n=U.get_obj_file_lineno(a)
	# _a=a
	if not F.exist(f):
		if py.getattr(a,'__code__',0):
			a=a.__code__
		from xdis import iscode
		if iscode(a):
			import uncompyle6,io
			##注释的是错误做法，改println造成结果不全，要想不显示，正确做法 out=
			# if U.get_or_set('uncompyle6.semantics.pysource.SourceWalker.println',
				# uncompyle6.semantics.pysource.SourceWalker.println,)==\
					# uncompyle6.semantics.pysource.SourceWalker.println:
				# uncompyle6.semantics.pysource.SourceWalker.println=U.AttrCallNo(p=0)
			# s= uncompyle6.deparse_code2str(a,out=io.StringIO())
			out=io.StringIO()
			sw= uncompyle6.uncompyle6.code_deparse(a,out=out)
			s=out.getvalue()
			lines=s.splitlines()
			if 'def ' not in lines[0] and lines[1][0] not in [T.tab,T.space] :
				if [i for i in lines if i.startswith(T.tab)] :indent=T.tab
				else:indent=T.space*4
				# sw.indent_more()
				# sw.gen_source( sw.ast,'qgb',{})
				s='def %s(%s):\n'%(a.co_name,U.fullargspec_to_str(a))
				for n,l in py.enumerate(lines):
					s+=indent+l+T.eol
				return s
			return out.getvalue()+sw.text
			return s
	return inspect.getsource(a) # module, class, method, function, traceback, frame, or code object
decompile=getsource=get_mod_source=getSource=get_source

def is_SyntaxError(a):
	import ast
	try:
		ast.parse(a)
		return False
	except:
		return True
isyntaxError=iSyntaxError=isSyntaxError=is_SyntaxError

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

def parse_code(code,__file='U.parse.file',body=False,one=True):
	from ast import parse,AST,iter_fields
	if body:return parse(code)
	
	body=parse(code).body
	if one and py.len(body)==1:return body[0]
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
parse=parse_code	
	
def extract_variable(a,dsf=0,p=0):
	''' exact:精确  extract[v.]提取
'''
	print(a)
	import _ast
	# if not isinstance(a,_ast.AST):
	for k in a._fields:
		v=getattr(a,k)
		if py.istr(v):
			# dict_key_count_plus_1(dsf,k)
			add_dict_value_set(dsf,k,v)
			yield v
		if isinstance(v,_ast.AST):
			yield from extract_variable(v,dsf,p=p)
		if py.islist(v):
			for n,iv in py.enumerate(v):
				if p:print(k,iv)
				if py.istr(iv):
					yield iv
				elif isinstance(iv,_ast.AST):
					yield from extract_variable(iv,dsf,p=p)
				else:
					raise Exception(k,n,iv)
def get_ast_inner(node,n):
	return
get_ast=get_ast_inner
	
def iter_ast(node,*ns):
	from _ast import AST
	if not ns:ns=(StrRepr('~'),)
	if isinstance( node, AST ):
		key=StrRepr( T.join(ns,splitor='') )
		d={key:StrRepr(node.__class__.__name__)}
		for n,field in py.enumerate(node._fields):
			try:
				d[field]=iter_ast( py.getattr( node, field ),*ns,n )
			except AttributeError:
				pass		
		return d
	if py.islist(node):
		return [iter_ast(i,*ns,[n]) for n,i in py.enumerate(node)]
	return node	
	
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
	U,T,N,F=py.importUTNF()
	if not path or path=='.':path=U.pwd(p=False)
	pt=F.auto_path(path)
	if F.exist(pt):
		path=pt
	else:
		path=F.auto_path(path,default=U.pwd())

	# path=path.replace('/','\\')
	ps='# Not impl in this system'
	if iswin():
		if path.startswith('///') or path.startswith(T.back_slash*3):
			path=path[3:]
		ps=r'''C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command ii {!r}'''.format(path)
		if Win.getVersionNumber()<=6.0:#vista
			ps='explorer.exe '+path
		os.system(ps)
	return StrRepr(ps)

exxp=exp=explorer

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

def itertools_tee(obj,count=2):
	'''itertools.tee(iterable, n=2) --> tuple of n independent iterators.	
#理解错误###itertools.tee返回的第一个是原gen 但是却是<itertools._tee at 0x11c34eab508>类型 ，也就是说调用后如果使用了第一个返回值，原始gen也会改变###

一旦 tee() 实施了一次分裂，原有的 iterable 不应再被使用；否则tee对象无法得知 iterable 可能已向后迭代。
tee 迭代器不是线程安全的。当同时使用由同一个 tee() 调用所返回的迭代器时可能引发 RuntimeError，即使原本的 iterable 是线程安全的。
该迭代工具可能需要相当大的辅助存储空间（这取决于要保存多少临时数据）。通常，如果一个迭代器在另一个迭代器开始之前就要使用大部份或全部数据，使用 list() 会比 tee() 更快。
In [153]: g=iterable=py.enumerate(In)
In [154]: r=U.copy_gen(g,9)
In [155]: for i in r[7]:print(i);break
(0, '')
In [156]: for i in r[7]:print(i);break
(1, 'vsc(U._len)')
In [157]: for i in g:print(i);break
(2, 'g=iterable=py.enumerate(In)')

	'''
	if not count or count < 1:
		raise py.ArgumentError('至少要1个copy吧，但count=',count)
	import itertools
	return itertools.tee(obj,count)
	# if count==1:
	# 	return r[0]
	# else:
	# 	return r#[1:]

gen_copy=copy_gen=generator_copy=copy_generator=tee=itertools_tee
try:
	import itertools	
	gen_multi_iter=iter_multi_gen=iter_multiple_generator=itertools_chain=itertools.chain
	'''
		chain(*iterables) --> chain object
	'''
except:pass
	


def get_one_from_iterable(iterable,index=0): #TODO start, stop[, step])
	if not py.isint(index):
		raise py.ArgumentUnsupported('index must be int',index)
	
	if py.isgen(iterable):
		iterable,i2=copy_generator(iterable)
	else:
		i2=iterable
		
	if index<0:
		index,raw_index=_len(i2)+index,index

	for n,v in py.enumerate(iterable):
		if n==index:
			return v
	return py.No('iterable index out of range',iterable,index,)
get_one_from_set=get_from_set=get_jihe=get_from_jihe=getIterable=get_iterable=get_iterable_item=get_one_from_iterable

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
	
def intersection(a,b):
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
j=intersection
	
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

def get_dict_item(d,index=0):
	if index<0:index=py.len(d)+index
	for n,k in py.enumerate(d):
		if n==index:
			return (k,d[k])
	
	return py.No('d[{}] out of range'.format(index) ,d,index)
	# return d.items().__iter__().__next__()
dict_item=dict_one_item=getDictItem=get_dict_item

def get_dict_all_values(d,start=0,size=500): 
	if not py.isdict(d):
		# try:
		return [v for k,v in d]
	return py.list(d.values())[start:start+size]
get_dict_value_list=dict_values=get_dict_values=get_dict_all_values	

def get_dict_value(d,index=0):
	if index<0:index=py.len(d)+index
	for n,v in py.enumerate(d.values()):
		if n==index:
			return v
getDictV=getDictValue=dict_value=get_dict_value

def setDictListValue(adict,key,value):
	if key in adict:
		adict[key].append(value)
	else:
		adict[key]=[value]
dict_value_list=dict_value_add_list=dict_add_value_list=add_dict_value_list=set_dict_value_list=set_dict_list=setDictList=setDictListValue

def setDictSetValue(adict,key,value):
	if key in adict:
		adict[key].add(value)
	else:
		adict[key]=py.set([value])
dict_value_add_set=dict_value_set=dict_add_value_set=add_dict_value_jihe=add_dict_value_set=set_dict_value_set=set_dict_set=setDictset=setDictSetValue

def setDictValuePlusOne(adict,*keys):
	for key in keys:
		if key in adict:
			adict[key]+=1
		else:
			adict[key]=1
dict_key_count=dict_key_count_plus_1=dict_key_count_plus_one=count_dict_key=set_dict_plus_one=set_dict_plus_1=set_dict_value_plus_1=setDictPlusOne=setDictValuePlusOne		

def count_hashable_in_iterable(iter):
	d={}
	for k in iter:
		dict_key_count_plus_1(d,k)
	return d
ct_iter=count_iter=count_list=count_hashable=count_in_iterable=count_hashable_in_iterable

def dict_value_len(adict,return_list=False,):
	'''
	range(-1) = range(0, -1)
	'''
	d={}
	for k,v in adict.items():
		d[k]=len(v)	
	if return_list:return [[v,k] for k,v in d.items()]	
	return d
dictvlen=dictValueLen=dict_value_len
def dict_value_len_count(adict,show_key_len_range=py.range(-1,-1),return_list=False, ):
	'''
	range(-1) = range(0, -1)
	'''
	d={}
	for k,v in adict.items():
		l=len(v)#U.len
		setDictValuePlusOne(d,l)
		if l and (l in show_key_len_range):
				setDictListValue(d,'%s-len'%l,k)

	if return_list:return py.list(d.items())
		
	return d
	
def dict_replace_value(adict,key_map_dict):
	rd={}
	for ka,kr in key_map_dict.items():
		if py.islist(kr):
			rd[ka]=kr[0]
		else:
			rd[ka]=adict[kr]
	return rd
dict_copy=replace_dict_value=dict_replace_value
	
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

def dict_swap_key_value(d):
	return {v:k for k,v in d.items()}
	r={}
	for k,v in d.items:
		r[v]=k
	return r
swap_dict_key_value=dict_key_value_swap=dict_swap_key_value

def dict_update_dict_merge_value_list(da,db):
	for k,v in db.items():
		if k in da:
			if py.islist(da[k]):
				da[k].append(v)
			else:
				da[k]=[da[k],v]
		else:
			da[k]=v
	return da
dict_update_value_list=dict_update_merge_value_list=dict_update_dict_merge_value_list
	
def is_builtin_function(a):
	'''
dict,list,tuple  should is_builtin_function?  now is False	
object.__init__ not 	(types.BuiltinFunctionType,types.BuiltinMethodType)
	'''
	if not py.callable(a):return False
	import types
	if py.isinstance(a,(types.BuiltinFunctionType,types.BuiltinMethodType)):
		return True	
	bms=get_or_set('builtin_methods',lazy_default=lambda:[
py.object.__class__,
py.object.__delattr__,
py.object.__dir__,
py.object.__eq__,
py.object.__format__,
py.object.__ge__,
py.object.__getattribute__,
py.object.__gt__,
py.object.__hash__,
py.object.__init__,
py.object.__init_subclass__,
py.object.__le__,
py.object.__lt__,
py.object.__ne__,
py.object.__new__,
py.object.__reduce__,
py.object.__reduce_ex__,
py.object.__repr__,
py.object.__setattr__,
py.object.__sizeof__,
py.object.__str__,
py.object.__subclasshook__,
	])
	if a in bms:
		return True
	return one_in(['<built-in function ','builtin_function_or_method'],py.repr(a))
isBuiltinFunction=isBuiltinFunctionType=is_builtin_function	
	
def is_slice(a):
	return py.type(a) in [py.range,py.slice]

def get_slice_len(*a):
	a=py.list(a)
	if py.len(a)==1 :
		if is_slice(a[0]):#stop不可能None
			range=[   a[0].start or 0   ,   a[0].stop    ,   a[0].step or 1   ]
		if py.islist(a[0]) or py.istuple(a[0]):
			a=[*a[0]]
		if py.isint(a[0]):
			range=[0,a[0],1]
		else:
			raise py.ArgumentError(a[0])
	if py.len(a)==2 :
		if a[0]==None:
			if a[1] <0:
				return -1
			a[0]=0
		if a[1]==None:
			if a[0]<0:
				return -1*a[0]
			return -1 # can not count 剩余长度
		return a[1]-a[0]
	if py.len(a)==3 :
		if a[2]==1:
			return get_slice_len(a[0],a[1])
		return todo_count_step
		#TODO
	raise py.ArgumentUnsupported(a)
	# if py.isint(a)
	
def get_slice_range(*a,len=0):
	'''len : to-slice-obj len ,must privide. I don't konw to-slice-obj info here.
return:  slice to [all index list]

	'''
	if (not a)  or  (not len) or (not py.isint(len) ) or (len < 1) :
		raise py.ArgumentError('to-slice-obj len ,must privide  get_slice_range(x,.. ,len=n )')
		return []
	_len=-1 * len
	if py.len(a)==1 :
		if py.type(a[0]) in [py.range,py.slice]:#stop不可能None
			range=[   a[0].start or 0   ,   a[0].stop    ,   a[0].step or 1   ]
		else:
			range=[0,a[0],1]
	elif py.len(a)==2 :
		range=[a[0],a[1],1]
	else:
		range=[a[0],a[1],a[2]]

	if range[0]<0:range[0]+=len
	if range[1]<0:range[1]+=len
	if range[2]<0:
		#TODO
		raise py.NotImplementedError('step < 0')

	return py.list(py.range(*range) )
get_all_index_list=get_index_list=get_slice_range

def getDictItems(a,*range,index=False,key=True, ):
	'''
*range= (stop) 
*range= (start, stop[, step])

#TODO
1. [, step] 未用到
2. value=True
Create a slice object.  This is used for extended slicing (e.g. a[0:10:2]).
'''

	iter=a.items().__iter__()


	t=get_slice_range(*range,len=py.len(a))
	if not t:
		if index==False and key==True:
			return py.list(a.items())
		return py.No('empty get_slice_range( *{} )'.format(range))
	else:
		range=t

	r=[]
	i=-1
	while True:
		try:
			item=iter.__next__()
			if not key:item=item[1]
			
			i+=1
			if range and i>range[-1]:break
			if i in range:
				if index:
					r.append([i, item] )
				else:
					r.append(item)
		except py.StopIteration:
			break
	return r
dict_items=get_dict_items=getDictItems
	
def get_nested_one_value(a,*key):
	'''safely get nested  a[k1][k2][...]
	
setErr( gError 还是要保留，像这种 出错 是正常流程的一部分，但是又想把错误记录下来
#todo
	'''
	if py.len(key)==0:raise ArgumentError('need at least one key')
	if py.len(key)==1:
		try:return a[key[0]]
		except Exception as e:
			try:
				return a[key]
			except Exception as e2:
				return py.No(e2)
	else:
		try:return get_nested_value(a[key[0]],*key[1:]) 
		except Exception as e:return py.No(e)
getDictNestedValue=getNestedValue=get_nested_value=get_nested_one_value
	
	
def dict_get_nested_multi_keys_return_dict(d,*keys,**defaults):
	'''( k,[k0,v[k0_0,...]],)
	# if py.istr(d) or py.isbyte()
	'''
	if not (isgen(d) or py.islist(d) or py.istuple(d) or py.isdict(d)) or (not keys) :
		return d
	dr={}
	for k in keys:
		if py.islist(k):
			if py.len(k)==0:
				raise py.ArgumentError('[k..] can not == []',k)
			# if 
			if py.islist(k[-1]):
				if py.len(k)==2:
					dr[k[0]]=dict_get_multi_return_dict(d[k[0]],*k[1])
					continue
				else:
					raise py.ArgumentError('len [k,[...]] must ==2',k)
			dr.update(dict_get_multi_return_dict(d,*k))
			continue
		try:
			dr[k]=d[k]
		except Exception as e:
			dr[k]=py.No(e,k)
				
		# dr[k]=d.get(k,defaults.get(k,default)) # .get also raise TypeError: unhashable type:
	return dr
get_nested_values=get_multi_dict_keys=get_dict_multi_values_by_keys=dict_get_multi=dict_get_multi_keys=dict_multi_get=dict_multi_get_keys=dict_get_multi_return_dict=dict_get_multi_keys_return_dict=dict_get_nested_multi_keys_return_dict

def dict_multi_pop(adict,*keys,default=py.No('key not in dict')):
	dr={}
	islist=py.islist(adict)
	for k in keys:
		if islist:
			dr[k]=adict.pop(k)#TypeError: pop() takes at most 1 argument (2 given)
		else:	
			dr[k]=adict.pop(k,default)
	return dr	
dict_pop=pop_list_multi_index=pop_dict_multi_key=dict_pop_multi_key=dict_multi_pop
	
GET_DICT_MULTI_VALUES_RETURN_LIST_DEFAULT_DEFAULT=get_dict_multi_values_return_list_DEFAULT_DEFAULT=get_or_set('get_dict_multi_values_return_list_DEFAULT_DEFAULT',lazy_default=lambda:py.No('can not get key'),)

def get_dict_multi_values_return_list(d,*keys,default_dict={},default_default=GET_DICT_MULTI_VALUES_RETURN_LIST_DEFAULT_DEFAULT,**ka):
	default=get_duplicated_kargs(ka,'default')
	if default is GET_DUPLICATED_KARGS_DEFAULT:
		pass
	else:
		if py.isdict(default) and not default_dict:
			default_dict=default
		else:
			default_default=default
	r=[]
	for k in keys:
		if k in default_dict:
			v=d.get(k,default_dict[k])
		else:
			v=d.get(k,default_default)
		r.append(v)
	return r
get_multi_dict_values=get_dict_multi_values=get_dict_multi_values_return_list
	
def dict_contains_dict(d,dsub):
	for k,v in dsub.items():
		if k not in d:
			return py.No('k not in d',k,d,dsub)
		else:
			if d[k]!=v:
				return py.No(' d[k]!=v ',k,d,dsub,v)
	return True
dind=dict_in_dict=dict_contains_dict	

def dict_pop_by_index(d,index):
	if index<0:index=py.len(d)+index
	for n,(k,v) in py.enumerate(d.items()):
		if n==index:
			return k,d.pop(k)
	return py.No('not found match index in dict',d,index)
pop_dict_index=pop_dict_by_index=dict_pop_by_index	
	
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

def print_traceback_in_except(*msg):
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
	if msg:pln(msg)

print_tb=print_tb_stack=print_traceback=print_stack_in_except=print_traceback_in_except

def get_traceback_stack( limit=None, ):
	import traceback
	ex_type, ex, tb = sys.exc_info()
	return traceback.extract_tb(tb, limit=limit)
get_tb_stack=get_traceback_stack


def print_stack(f=None, limit=None, file=None):
	"""Print_stack up to 'limit' stack trace entries  to 'file'.
	"""
	if f is None:
		f = sys._getframe().f_back
	import traceback
	return traceback.print_list(traceback.extract_stack(f, limit=limit), file=file)


def get_stack(frame=None, limit=None, ):
	'''return list
	'''
	if frame is None:
		frame = sys._getframe().f_back
	import traceback
	return traceback.extract_stack(frame, limit=limit)


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
get_obj_hierarchy=get_object_hierarchy=getclassInherit=getClassHierarchy

def get_file_by_object(a):
	import inspect
	try:
		inspect.getfile(a)
	except Exception as e:
		if 'is not a module' in e.message:
			return getFile(py.type(a))
		if 'built-in' in e.message:
			return e.message
getfile=getFile=get_file=get_file_by_object

#def 	#把一个数分解成2的次方之和。

def selectBox(*a):
	if py.is2():
		import Tkinter as tk
	else:
		import tkinter as tk
	top=tk.Tk()
	tk.mainloop()

def get_self_raw_cmdline():
	if iswin() or iscyg():
		return Win.getCmd()
	raise py.EnvironmentError('TODO: NOT Win')
getCmdline=getCmd=get_cmd=get_raw_cmd=get_raw_cmdline=get_self_raw_cmdline

def get_cmdline_by_pid(pid=None):
	if pid==None:
		return get_self_raw_cmdline()

def beep(ms=1000,hz=2357):
	if iswin():
		try:
			import winsound
			return winsound.Beep(hz,ms)
		except:
			pass
	p('\a')

def nircmd(*a):
	'''
The “old style” string formatting syntax %(name)s   auto ignore not use dict key

nircmd.exe sendkeypress 8 6 8 0 5 8' 必须隔开
'''	
	U,T,N,F=py.importUTNF()
	if not U.iswin():raise py.EnvironmentError()
	if len(a)==1 and ( py.islist(a) or py.istuple(a) ):
		a=a[0]
		if py.istr(a):
			a=U.split_cmd(a)
			a[0]=a[0].strip().lower()
			if 'nircmd' in a[0]:a.pop(0)
			
	a=py.list(a)
	for n,v in py.enumerate(a):
		if py.islist(v) or  py.istuple(v) or py.isdict(v) :
			raise py.ArgumentError('a[%(n)s]==%(v)s  ;a=' % py.locals() ,a,n,v)
		if not py.istr(v):  # int ERROR :  File "C:\QGB\Anaconda3\lib\subprocess.py", line 530, in list2cmdline    needquote = (" " in arg) or ("\t" in arg) or not arg
			a[n]=T.string(v)

	nircmd=find_driver_path('C:/QGB/babun/cygwin/home/qgb/wshell/exe/nircmd/nircmd.exe')
	c=nircmd,*a
	cmd(c);return c
	# return cmd(c),c

def system_mute():
	return nircmd( 'mutesysvolume', '1')
mute=mute_system=system_mute

def system_unmute():
	return nircmd( 'mutesysvolume', '0')
unmute=unmute_system=system_unmute

def set_system_volume(a):
	''' 655.35 - 65535  == vol 1 - 100
	'''
	if py.isfloat(a):
		if not 0<=a<=1:raise py.ArgumentError('vol float shoud in [0,1]')
		if a<0.01:a=0
		a=py.int(65535*a)

	elif py.isint(a):
		if a<655:
			if 0<=a<=100:
				a=655*a
			else:
				raise py.ArgumentError('vol int shoud in [0,100]  or [655,65534]')
	else:
		raise py.ArgumentUnsupported(a)
	return nircmd( 'setsysvolume',a )
vol=volume=volume_change=changesysvolume=setVol=setVolume=et_vol=setvolumn=set_volumn=set_volume=set_system_volumn=set_system_volume

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

	
def	rename_dict_key(d,new,old={}):
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
renameDictKey=rename_dict_key
def unique(iterable,count=False,return_list=False,**ka):
	d=get_duplicated_kargs(ka,'d','dict','return_dict','rd','count','ct',default=count)
	if d:
		d={}
		for i in iterable:
			dict_key_count_plus_1(d,i)
		if return_list:
			return list(d.items())
		else:
			return d
	r=[]
	for i in iterable:
		if i not in r:r.append(i)
	return r

def get_column_from_2D_list(matrix, *col_index):
	if not col_index:raise py.ArgumentError('need *col_index ')
	r=[]
	m=py.len(col_index)
	for row in matrix:
		if m==1:
			l=row[col_index[0]]
		else:
			l=[]
			for i in col_index:
				l.append(row[i])
		r.append(l)
	return r	
	# return [ for row in matrix]
col=column=get_col=get_column=get_2D_list_column=get_2d_list_column=get_column_from_2D_list	

def get_2D_list_shape(a):
	import numpy as np
	return np.shape(a)
get_2d_array_shape=get_2d_list_length=get_2d_list_shape=get_2D_list_shape

def get_2D_list_max_min_wcswidth(lr):
	'''  get_2D_list_max_min(a,func=T.wcswidth)
	'''
	U,T,N,F=py.importUTNF()
	irows,icols=U.get_2d_array_shape(lr)
	title=[StrRepr(col,size=5) for col in 'icols,min,max,imin,imax,min_v,max_v'.split(',')]
	tj=[title]
	for i in range(icols):
		y=U.get_2d_list_column(lr,i)
		if not py.istr(y[0]):continue
		ry=[T.wcswidth(s) for s in y]
		max=py.max(*ry)
		min=py.min(*ry)
		imax=ry.index(max)
		imin=ry.index(min)
		tj.append([i,min,max,imin,imax,lr[imin][i],lr[imax][i] ])
	return tj

def pip_install(modName,args=[' -i', 'http://pypi.douban.com/simple', '--trusted-host', 'pypi.douban.com'],pip_main=None):
	''' #TODO 在同一个进程内 pipInstall 只能运行一次
	
清华大学 :https://pypi.tuna.tsinghua.edu.cn/simple/
阿里云: http://mirrors.aliyun.com/pypi/simple/
豆瓣 http://pypi.douban.com/simple/
中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/
华中科技大学http://pypi.hustunique.com/	
	
	
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
	if not pip_main and (py.version>3.9 or py.len(py.str(py.version))>4 ):
		from pip._internal.cli.main import main as pip_main
	if not pip_main:	
		from pip.__main__ import _main as pip_main
	return pip_main(['install',*args,modName])
pip=pipInstall=pip_install
	
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
	'''
'''	
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

def get_warnings_filters():
	import warnings
	return warnings.filters
filterWarningList=warnings_filters=get_warnings_filters

def parse_cmd_duplicated_arg(*names,default=py.No('no default'),type=py.No('auto use default')):
	names_list=[]
	for i in names:
		if not i.startswith('-'):
			names_list.append('-'+i)
		else:
			names_list.append(i)
			
	if py.isno(default) and py.isno(type) and 'auto' in type.msg:
		raise py.ArgumentError('no default or no type')
	if default:
		if type:
			if py.type(default)!=type:
				raise py.ArgumentError('default_type and type "conflict with each other" ')
		else:
			type=py.type(default)
	else:
		default=None
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument(*names_list,type=type,default=default,)	# type 参数必须callable，传No肯定不行
	namespace, unparsed_list = parser.parse_known_args()
	
	r=[]
	for k,v in py.vars(namespace).items():
		if v:r.append([k,v])
	if py.len(r)==0:
		return default
	if py.len(r)==1:
		return r[0][1]
	else:
		return py.No('get duplicated arg_name value, cmd should provide only one',namespace,r)
parse_cmd_arg_duplicate=parse_cmd_arg_duplicated=get_duplicated_arg_cmd=get_duplicated_cmd_arg=get_duplicated_cmd_args=parse_cmd_args_duplicated=parse_cmd_duplicated_args=parse_cmd_duplicated_arg
	
def parse_cmd_args(int=0,str='',float=0.0,dict={},list=[],tuple=py.tuple(),**ka,  ):
	'''
	用int=4不行，必须加上 - ，【"C:\\QGB\\Anaconda3\\lib\\argparse.py", line 1470, in _get_optional_kwargs】【 ValueError: invalid option string 'int': must start with a character '-'】，
	如果在命令行中忘记加上 - ，这里则获取不到这个参数
	
	'''
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
	for k,v in ka.items():
		parser.add_argument(
			'--%s'%k,'-%s'%k,
			type=py.type(v) ,  # str 不类型可能不能直接eval, 所以不能直接使用 type=py.eval, 
			default=v,
		)		

	namespace, unparsed_list = parser.parse_known_args() #  return namespace, args
	set('argparse.ArgumentParser',parser)
	set(parse_cmd_args.__name__+'.unparsed_list',unparsed_list)
	# print(namespace.int)
	##ipyEmbed()()
	# print(unparsed_list)
	return namespace
cmd_arg=cmd_args=parse_arg=parse_args=argsParse=argparse=argsParser=args_parse=args_parser=parseArgs=get_cmd_arg=get_cmd_args=parse_cmd_args

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
	''' IntRepr'''
	from pympler.asizeof import asizeof
	return F.IntSize(asizeof(obj))

def sizeof(obj,*other):
	return FuncWrapForMultiArgs(f=sizeof_one_obj,args=(obj,other) )
size=asizeof=sizeof

def gc():
	import gc
	return gc.collect()

def get_objects(type,len=None):
	'''
0==False  # True
0 is False# False	
	'''
	import gc
	isinstance= py.isinstance
	r=[]
	for o in gc.get_objects():
		if isinstance(o,type) or o is type:
			r.append(o)
	return r
search_object=search_objects=find_objects=get_obj=get_objects

def git_init(remote_url='',git_exe=None,**ka):
	cmd=r''' 
"{git_exe}"
	'''
	U,T,N,F=py.importUTNF()
	U.pwd(p=1)
	commit_msg=U.get_duplicated_kargs(ka,'commit_msg','commit','cmsg','msg','s')
	git_exe=get_git_exe(git_exe)
	ipy=U.get_ipy(raise_EnvironmentError=False)
	if ipy:
		system=ipy.system
	else:
		args_dict=get_args_dict_from_format_string(cmd,py.locals())
		cmd=cmd.format(**args_dict)
		import os
		system=os.system
		
	return

def get_git_exe(git_exe='',win_git_list=(
'C:/Program Files/Zerynth/python/Library/cmd/git.exe',
r"D:\Program Files\Git\bin\git.exe"
r"C:\Program Files\Git\bin\git.exe"
,)
	):
	U,T,N,F=py.importUTNF()
	if not git_exe: # U.get('git_exe')
		if U.isWin():
			for g in win_git_list:
				if F.exist(g):
					git_exe=U.get_or_set('git_exe',g)
					break
		if U.isLinux():
			git_exe=U.get_or_set('git_exe',r"/usr/bin/git")
	if not F.exist(git_exe):
		raise py.EnvironmentError(git_exe,'not exists!')
	return U.set('git_exe',git_exe)

def get_args_dict_from_format_string(text,locals,regex=r'\{\w+\}'):
	'''raise KeyError '''
	U,T,N,F=py.importUTNF()
	ks=[i[1:-1] for i in U.unique(T.regexMatchAll(text,regex)) ]
	if not ks:return {}
	if not U.all_in(ks,locals):
		print('text.ks:',ks)
		print('locals.keys:',py.list(locals))
	#debug	
	if 'git_exe' in ks and locals['git_exe'	]==None:
		py.pdb()()
	####	
	return {i:locals[i] for i in ks}
	
def git_psuh(remote,dir='.',git_exe=None,):
	'''#TODO '''
	raise py.NotImplementedError()
	

def git_commit(commit_msg=None,dir='.',	git_exe=None,git_add='"{git_exe}" add -A', user_email='qgbcs1@gmail.com', user_name='qgb',):
	cmd=r'''   
"   "{git_exe}" config --global user.email {user_email}
"{git_exe}" config --global user.name {user_name}

"{git_exe}" config --global core.autocrlf false
"{git_exe}" config --global core.filemode false
"{git_exe}" config --global credential.helper store
"{git_exe}" config --global http.sslverify "false"
echo 	 git config done
%(git_add)s
"{git_exe}" commit -m "{commit_msg}"
echo 	 git commit "{commit_msg}" done   "
''' % py.locals() # 其他地方不是用 %py.vars()
	U,T,N,F=py.importUTNF()
	U.cd(dir)
	U.pwd(p=1)
	if not commit_msg:commit_msg=U.stime()
	git_exe=get_git_exe(git_exe)
	
	##代码顺序不能乱，先赋值所有变量，再尝试 格式化
	ipy=U.get_ipy(raise_EnvironmentError=False)
	if ipy:
		system=ipy.system
	else:
		args_dict=get_args_dict_from_format_string(cmd,py.locals())
		cmd=cmd.format(**args_dict)
		import os
		system=os.system
		
	
	
	cmd=T.replace_all(cmd.strip(),'\n\n','\n')
	cmd=cmd.replace('\n',' & ')
	return system(cmd),cmd
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
	U,T,N,F=py.importUTNF()
	a=py.list(a)
	if py.istr(args):
		a.insert(0,args)
	elif py.iterable(args):
		a=py.list(args)+a
		
	ipy=get_ipy(raise_EnvironmentError=True)
	# if git_exe and F.exist(git_exe):
		# U.set('git_exe',git_exe)
	# elif isWin():
		# git_exe=get_or_set('git_exe',*r"""D:\Program Files\Git\bin\git.exe
# C:\Program Files\Zerynth\python\Library\cmd\git.exe
# C:\QGB\babun\cygwin\bin\git.exe
# C:\Program Files (x86)\SparkleShare\msysgit\bin\git.exe""".splitlines())
	# elif isLinux():
		# git_exe=get_or_set('git_exe',r"/usr/bin/git")
		
	git_exe=get_git_exe(git_exe=git_exe)
	cmd=f'''"{git_exe}" {' '.join(a)} '''
	if p:U.pln(cmd)
	ipy.system(cmd)
	return git_exe,a

def git_clone(*a,depth=1,git_exe=None,p=1):
	a=py.list(a)
	if depth:
		#TODO iter a find depth argument
		a.append('--depth=%s'%depth)
	return git('clone',*a,git_exe=git_exe,p=p)
	
def get_or_set_exist_path(name,*sps,no_raise=False):
	r=''
	for s in sps:
		if F.exist(s):
			r=s
			break
	if not r:
		ea=('no path exists!',name,sps)
		if no_raise:
			return py.No(*ea)
		raise py.EnvironmentError(*ea)
	return get_or_set(name,r)
	
def git_upload(commit_msg=None,repo='QPSU',repo_path=get_qpsu_dir(),
			git_remotes=['https://qgbcs@gitee.com/qgbcs/',
				# 'https://git.coding.net/qgb/',
				'https://qgb@github.com/qgb/',
				],
			git_exe=None,
			user_email='qgbcs1'+py.chr(0x40)+'gmail.com',
			user_name='qgb',

		):
	ipy=get_ipy(raise_EnvironmentError=True)
	git_exe=get_git_exe(git_exe=git_exe)
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
	ipy.system(cmd) # using current function variable
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
		if 'python' in sys.executable:
			a.insert(0,sys.executable)
		elif 'uwsgi' in sys.executable: # PythonAnyWhere
			a.insert(0,F.home()+'.local/bin/python')
		else:
			raise NotImplementedError(sys.executable)
			
	a=[py.str(i).strip() for i in a]
	print(U.v.U.cmd(a,**ka) )
	return U.cmd(a,**ka)
python_v=python_V=python

def python_m(*a,**ka):
	return python('-m',*a,**ka)

def python_c(*a,**ka):
	return python('-c',*a,**ka)

def color_to_bgr_tuple(a):
	r,g,b=color_to_rgb_tuple(a)
	return b,g,r
def color_to_rgb_tuple(a):
	'''
ImageColor.colormap = {
    # X11 colour table from https://drafts.csswg.org/css-color-4/, with
    # gray/grey spelling issues fixed.  This is a superset of HTML 4.0
    # colour names used in CSS 1.
'''	
	U,T,N,F=py.importUTNF()
	if py.istr(a):
		try:
			from PIL import ImageColor
			rgb=ImageColor.getcolor(a, "RGB") 
		except py.ImportError as e:pass
		try:
			import matplotlib.colors
			rgb=matplotlib.colors.to_rgb(a) # max 1.0 return (1.0,0,0)
			rgb=U.tuple_multiply(rgb,255)
			rgb=U.tuple_operator(rgb,operator=py.int)
		except py.ImportError as e:pass
		
	elif py.isint(a):
		rgb=integer_to_rgb_tuple(a)
	elif U.len(a)==3:
		r,g,b=a 
		rgb=r,g,b
	else:
		raise py.ArgumentError()
	return rgb
	
def integer_to_rgb_tuple(RGBint):
	blue =  RGBint & 255
	green = (RGBint >> 8) & 255
	red =   (RGBint >> 16) & 255
	return (red, green, blue)
i2rgb=rgbint2rgbtuple=convert_integer_to_rgb_tuple=int2rgb=int_to_rgb=integer_to_rgb_tuple

def RGBAfromInt(argb_int):
	blue =  argb_int & 255
	green = (argb_int >> 8) & 255
	red =   (argb_int >> 16) & 255
	alpha = (argb_int >> 24) & 255
	return (red, green, blue, alpha)

def rgb_tuple_to_integer(rgb,g=None,b=None):
	if py.isint(rgb) and py.isint(g) and py.isint(b):
		rgb=(rgb,g,b)
	elif py.istr(rgb) and not g and not b:
		import matplotlib.colors
		rgb=matplotlib.colors.to_rgb(rgb)
	else:
		raise py.ArgumentError()
	return rgb[2]*256*256+rgb[1]*256+rgb[0]
color2int=color_to_int=color3_to_int=rgb2i=rgb_to_int=rgb_to_integer=rgb_tuple_to_integer

def rgb_name(r,g=None,b=None,hex_format='0x%02x_%02x_%02x',color_comment=True):
	if not py.isint(r):
		if g==None and b==None:
			if py.istr(r):
				if r.startswith('0x'):
					r=py.int(r[:10],16)
				else:
					r=py.int(r)
			else:	
				r,g,b=r
		else:
			raise py.ArgumentError()
	if py.isint(r) and g==None and b==None:
			r,g,b=integer_to_rgb_tuple(r)
	rgb=(r,g,b)
	hex=hex_format%rgb#TypeError: %i format: a number is required, not list
		#rgb 必须用tuple ，不能用list
	name=hex  	
	if color_comment:
		import webcolors
		try:
			name=hex+' #'+webcolors.rgb_to_name(rgb)
		except ValueError:
			pass
	return name
i2srgb=int2srgb=int_to_srgb=color_name=rgb_name			
	
def get_all_color_name_list(index=False,hex_int=False,sort_kw=None,int_delta=False,**ka):
	''' sort_kw c=0 代表第一列 k，（不包括 index）
	
'''	
	U,T,N,F=py.importUTNF()
	index=U.get_duplicated_kargs(ka,'index','n','enumerate','enu',default=index)
	hex_int=U.get_duplicated_kargs(ka,'hex_int','color_int','int','_10','i',default=hex_int)
	sort_kw=U.get_duplicated_kargs(ka,'sort_kw','sort_args','skw','s',default=sort_kw)
	import webcolors
	r=[]
	for k,v in webcolors.CSS3_NAMES_TO_HEX.items():
		row=[U.StrRepr(k,size=20),U.StrRepr(v,size=7+3)]
		
		if hex_int:
			row.append(U.IntRepr(py.int('0x'+v[1:],16),size=9) )
		
		r.append(row)
				
	if sort_kw:
		r=U.sort(r,**sort_kw)
			
	if int_delta:
		for n,row in py.enumerate(r):
			i=row[-1]
			if n==0:
				row.append( -1)
			else:
				row.append( i-r[n-1][-2])
		if py.isdict(int_delta):
			r=U.sort(r,**int_delta)
		
	if index:
		for n,row in py.enumerate(r):
			row.insert(0,U.IntRepr(n,size=3) )	

	return r	
	# return [()  ]
color_list=color_all_names=all_color_names=get_color_list=get_all_color_name_list
	
def iter_screen_colors(xrange=[855,1311],yrange=[],default_step=3,set_cur_pos=False,**ka):
	# cc=-1
	U,T,N,F=py.importUTNF()
	pos=py.list(Win.get_cur_pos())
	x=U.get_ka(ka,'x','X')
	y=U.get_ka(ka,'y','Y')
	if py.isint(x):pos[0]=x;xrange=None
	elif x and py.iterable(x):xrange=x  ###<py.No  py.iterable(x)==True
	if py.isint(y):pos[1]=y;yrange=None
	elif y and py.iterable(y):yrange=y
	
	if not xrange:xrange=[pos[0],pos[0]+default_step] # 只有一个坐标
	if not yrange:yrange=[pos[1],pos[1]+default_step]
	
	if not U.all_in(U.len(xrange,yrange),[2,3]):
		raise py.ArgumentError(xrange,yrange)
	
	if py.len(xrange)<3:xrange.append(default_step)
	if py.len(yrange)<3:yrange.append(default_step)
	
	print(xrange,yrange,'\n',x,y)
	
	# if set_cur_pos:Win.set_cur_pos(xrange[0],yrange[0])
	

	from PIL import Image, ImageGrab
	im =ImageGrab.grab()

	import win32gui,win32api,win32ui
	
	hwnd = win32gui.WindowFromPoint((xrange[0],yrange[0]))
	dc = win32gui.GetDC(0)
	dcObj = win32ui.CreateDCFromHandle(dc)
	monitor = (0, 0, win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
	dcObj.Rectangle((xrange[0],yrange[0],xrange[1],yrange[1]))
	# win32gui.InvalidateRect(hwnd, monitor, True) 
	win32gui.UpdateWindow(hwnd)
	red = 255#win32api.RGB(255, 0, 0)
	
	rd={}
	for ny,y in py.enumerate(py.range(*yrange)):
		for nx,x in py.enumerate(py.range(*xrange)):
			if set_cur_pos and (ny==0 or nx==0):
				win32gui.SetPixel(dc, x, y, red)
			rgb=im.getpixel((x,y));
			c=U.IntCustomRepr(U.rgb_to_int(rgb),repr=U.rgb_name(rgb))
			# c=Win.get_color(x,y)[-1]
			# rgb=integer_to_rgb_tuple(c)
			if c in rd:
				rd[c].append([nx,ny])
				continue
			# c[0]=
			# c[0].append('| %s'%nx)
			rd[c]=[x,y]
		
		
		# cc=c[-1]
	# U.pprint(rd)
	return rd
color_iter_screen=color_iter=iter_screen_colors
	
def _hotkey_callback():
	try:
		get('hotkey_f')()
	except Exception as e:
		print(stime(),e,)
	except BaseException as e:
		print('#BaseException',stime(),e,)
		# py.traceback()
	
def register_hotkey	(callback=_hotkey_callback,hotkey='alt+c',unregister_all=True,**ka):
	'''  
def f():
    print(23)
U.set('hotkey_f',f)	
	
	U.hotkey(lambda:print(U.stime()))
	
	'''
	import keyboard
	U,T,N,F=py.importUTNF()
	hotkey=U.get_duplicated_kargs(ka,'key','hot_key','k',default=hotkey)
	
	if unregister_all:
		try:
			keyboard.unhook_all_hotkeys() #
		except Exception as e:
			print(e)
		# keyboard._recording = None
		# keyboard._pressed_events.clear()
		# keyboard._physically_pressed_keys.clear()
		# keyboard._logically_pressed_keys.clear()
		# keyboard._hotkeys.clear()
		# keyboard._listener.init()#不加这句 init，第一次运行报AttributeError: '_KeyboardListener' object has no attribute 'blocking_hotkeys'
		# keyboard._word_listeners = {} 	
		

	k=keyboard.add_hotkey(hotkey, callback)
	return hotkey,U.set(hotkey,k),id(k)
on_key_pressed=key_listener=hotkey=hot_key=registe_hotkey=bind_hotkey=register_hotkey	


	
def print_repr(*a):
	return print(*[py.repr(i) for i in a])
	print([*a])
	
def taobao_url_unshorten(a=py.No('auto use clipBoard'),edit_clipboard=0,**ka):
	U,T,N,F=py.importUTNF()
	if not a:
		edit_clipboard=U.get_duplicated_kargs(ka,'e','edit',default=edit_clipboard)
		a=U.cbg(p=1,edit_clipboard=edit_clipboard)
		
	u=T.regex_match_one(a,T.RE_URL)
	if not u:
		return py.No('Not found url in a or clipBoard')
	r=N.HTTP.request(u)
	t=r.text
	atb='https://a.m.taobao.com/i' # case 0
	if atb in t:
		id=T.sub(t,atb,'.htm')
		if id:
			return 'https://item.taobao.com/item.htm?id='+id
	#TODO case 1,2....		
	return py.No(r,a,u,t)		
tb_url=tb_item_url=taobao_url=taobao_url_unshorten

def get_svg_qrcode(text=py.No(msg='auto get clipboard',no_raise=True),
	file=py.No('auto using text',no_raise=True),
	title=py.No(msg='svg html title auto using text',no_raise=True),
	scale=8,browser=True,return_bytes=False,response=None,tb='',**ka):
	'''Signature:
q.svg(
    file, : stream_or_path 
    scale=1,
    module_color='#000',
    background=None,
    quiet_zone=4,
    xmldecl=True,
    svgns=True,
    title=None,
    svgclass='pyqrcode',
    lineclass='pyqrline',
    omithw=False,
    debug=False,
)
text直接传入 title 有问题 , T.html_encode fix it：
	This page contains the following errors:
	error on line 3 at column 66: EntityRef: expecting ';'
	Below is a rendering of the page up to the first error.

	
'''
	import pyqrcode
	U,T,N,F=py.importUTNF()
	return_bytes=U.get_duplicated_kargs(ka,'b','rb','byte','bytes',default=return_bytes)
	response=U.get_duplicated_kargs(ka,'p','rp','resp','P',default=response)
	if not text and tb:
		t='https://item.taobao.com/item.htm?'
		if py.istr(tb) and t in tb:
			# text=tb+'&fpChannel=9'
			tb=T.regexMatchOne(tb,r'(?<=[\?\&]id=)\d{6,}','\d{6,}')
		if py.isint(tb) or U.all_in(tb,T._09):
			text=t+'fpChannel=9&id=%s'%tb
		if not title:
			# print_repr(tb,title,text) #debug
			r=N.HTTP.request(text.replace('://item.','://www.'),Host='item.taobao.com',no_raise=True)
			if r and r.text:
				bs=T.beautifulSoup(r.text)
				title=bs.select('meta[name="keywords"]')
				if title:
					title=title[0].get('content')
					print('tb:[',title,']')
				else:
					# title=py.repr([r,r.text])
					title='##Unexpect '+U.stime()
			else:title=T.pformat(r.a)
	if not text:
		if p:raise py.ArgumentError('not get text',tb,response)
		text=U.cbg(e=1)
	if not file:
		file=U.gst+T.file_legalized(text)[-244:]
		if return_bytes or response:
			import io
			file=io.BytesIO()
	if py.istr(file):
		if not file.lower().endswith('.svg'):file+='.svg'
	elif py.isfile(file):
		pass
	else:
		raise py.ArgumentUnsupported(file)
		
	if py.isno(title) and 'auto ' in title.msg:title='U.qrcode '+text
	if title:title=T.html_encode(title)
	
	q=pyqrcode.create(text)
	q.svg(file=file,scale=scale,title=title)  # None 
	if return_bytes or response:
		b=file.getvalue()
		if tb:
			b=b.decode('utf-8')
			# title=T.html_encode(title)
			html=r'''<html>
<head><title>%(title)s</title>
	<style type="text/css">
		 html, body ,svg{
		  width: 100%;
		  height: 100%;
		}
	</style>	
</head> 
<body> 
	<script>
		var url=window.location.href
		var i=url.indexOf('\4523-') // N.geta '\45'
		if(i!=-1){
			window.history.pushState('state', 'title', url.substring(0,i+4)+"%(text)s")
		}
	</script>
	<h5 style="color:red;margin: 0;"> %(title)s </h6>
	%(b)s
</body></html>'''
			b=T.format(html,title=title,text=text,b=b)
			# i=b.find(b'<path ')
			# b=b[:i]+b'<text fill="red" x="0" y="20" >'+title.encode('utf-8')+b'</text>'+b[i:]
		if response:
			if tb:response.headers['Content-Type']='text/html;charset=utf-8'
			else :response.headers['Content-Type']='image/svg+xml;charset=utf-8'
			response.set_data(b)
		return b
	if browser:U.browser(file)
	return file
qr=qrcode=svg_qrcode=get_svg_qrcode	

def search_image(image,precision=0.9,gray=True,background=py.No('screenshot',no_raise=True),):
	r''' if not gray:
error: OpenCV(4.5.1) C:\Users\appveyor\AppData\Local\Temp\1\pip-req-build-oduouqig\opencv\modules\imgproc\src\templmatch.cpp:1163: 
  error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() && _img.dims() <= 2 in function 'cv::matchTemplate'
'''
	U,T,N,F=py.importUTNF()
	import numpy,cv2
	if U.isWin() or U.isMac():
		from PIL import ImageGrab
	# im = pyautogui.screenshot()
	if not background:
		background=ImageGrab.grab()	
	if U.DEBUG==True:
		im.save('testarea.png')# usefull for debugging purposes, this will save the captured region as "testarea.png"
	background = numpy.array(background)
	if gray:
		background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
	template = cv2.imread(image, 0)
	template.shape[::-1]

	res = cv2.matchTemplate(background, template, method=cv2.TM_CCOEFF_NORMED,mask=None)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	if max_val < precision:
		return [-1,-1]
	return max_loc
image_search=imagesearch=search_image

def search_image_on_screen(image_path=py.No('if not ,attempt to get clipBoard image'),*a,precision=0.9,save_path=None,format='png',return_raw=False):
	'''
thunder_start :  light :	!min_val, max_val, min_loc, max_loc
(-0.35922059416770935, 0.9710590243339539, (207, 372), (122, 46))
图形不变 颜色 fade :
(-0.36415544152259827, 0.8675098419189453, (14, 681), (122, 46))
	
'''	
	try:
		U,T,N,F=py.importUTNF()
		ClipBoard=py.from_qgb_import('Clipboard')
		# from screen_search import  screen_search
	except Exception as e:
		return py.No(e)

	if not image_path:
		if not save_path:save_path=U.stime()
		image_path=ClipBoard.get_image(save_path)
		if not image_path:
			return image_path
	# else:
		# if not F.is_abs(image_path):
	image_path=F.auto_path(image_path,default=U.get('clipboard.dir'),)
	a=py.list(a)
	if py.istr(image_path) or 0 : #TODO is image
		a.append(image_path)
	else:
		a.extend(image_path)
		
	for n,i in py.enumerate(a):
		if not F.exist(i):
			i+='.'+format
		if not F.exist(i):
			# continue
			return py.No('image_path Not Exist!%r'%image_path)
		a[n]=i
	for i in a:
		print('U.search_image_on_screen(%r)'%i)
		x,y=search_image(i,precision=precision)
		if -1 in [x,y]:
			continue
		return x,y
	return py.No('Not found on screen',a)	
			
	# return py.No('image_path Not Exist! '+('%r'%image_path).strip())
	# ss=screen_search.Search(image_path)
	# ss.precision=precision
	# x,y=ss.imagesearch()
find_image_on_screen=seach_image_on_screen=search_image_on_screen


def set_timed_task(func,every='day',time='05:09',unit=1):
	'''U.set_timed_task(baidu_start,'2hour') 
'''
	U,T,N,F=py.importUTNF()
	import schedule
	###  check schedule_background_run 
	SCHEDULE_RUN_PENDING='schedule.run_pending()'
	t=U.get(SCHEDULE_RUN_PENDING)
	if t:
		if not py.getattr(t,'is_alive',lambda:0)():
			t=None 
	if not t:
		def schedule_background_run():
			while True:
				schedule.run_pending()
				U.sleep(1)
		t=U.Thread(target=schedule_background_run)
		U.set(SCHEDULE_RUN_PENDING,t)
		t.start()
	#### check run end ####
	if py.istr(every) and  ':' in every:
		time=every
		every='day'
	if py.istr(time) and ':' in time:
		if py.len( time.split(':')[0]  )==1:
			time='0'+time	
	numbers= U.one_in(every,T._09+'.')
	if numbers:
		every=T.replacey(every,numbers,'').strip()
		unit=py.float(''.join(numbers))
	if every=='sec':every='second'
	if unit>0:
		if not every.endswith('s'):
			every+='s'
	if 'day' in every:
		r=py.getattr(schedule.every(unit),every).at(time).do(func)#type schedule.Job    
	else:	
		r=py.getattr(schedule.every(unit),every).do(func)  # every current time ,Depend Time unit   
	return schedule.jobs,U.StrRepr('\n#######  U.get(%r)'%SCHEDULE_RUN_PENDING+' == '),t #,r
	
schedule=everyday_time_task=set_time_task=timing_task=dsrw=set_schedule=setInterval=set_interval=set_timed_task

def remove_timed_task(index=-1):
	''' -1 is last added
0 is first added'''
	import schedule
	return schedule.jobs,'########## pop:',schedule.jobs.pop(index)
schedule_jobs_pop=pop_time_task=cancel_time_task=del_time_task=remove_time_task=remove_timed_task
	
def get_timed_task_list():
	import schedule
	return schedule.jobs
schedule_jobs=time_task=get_time_task=get_timed_task=get_timed_task_list
	
def iter_2d_from_start_to_stop(stop,start_point_xy=(0,0),step_xy=(1,1),x_limit=(0,7680+1),y_limit=py.No('auto use y'),**ka):
	'''
range(stop) 
range(start, stop[, step]) 

		y_limit[0]
x_limit[0]	start .......... x_limit[1]
............................
............................
............................ x_limit[1]
.....stop 
		y_limit[1]
		
'''
	U,T,N,F=py.importUTNF()
	start_point_xy=U.get_duplicated_kargs(ka,'start','start_point',	'start_xy',default=start_point_xy)
	stop_point_xy=U.get_duplicated_kargs(ka,'stop','stop_point','stop_xy','end','end_point','end_xy',default=stop)
	step_xy=U.get_duplicated_kargs(ka,'step','step_point',default=start_point_xy)
	if step_xy[0]<0 or step_xy[1]<0:
		raise NotImplementedError('TODO')
	
	
	if not y_limit:
		y_limit=(start_point_xy[1],stop_point_xy[1])
	is_start=False
	
	for y in py.range(y_limit[0],y_limit[1],step_xy[1]):
		for x in py.range(x_limit[0],x_limit[1],step_xy[0]):
			if x>=start_point_xy[0] and  y>=start_point_xy[1]:
				if not is_start:
					is_start=True
					yield (x,y)
					continue
			if is_start:				
				if (y+step_xy[1])>stop_point_xy[1] and x>stop_point_xy[0]:
					break
				elif y>stop_point_xy[1]:
					break
				else:
					yield (x,y)
					
			
		
	
iter2d_start_end=iter_2d_from_start_to_end=iter_2d_from_start_to_stop
	
def iter_each_demensional_coordinate(*shape,step=1,start=0):
	'''args: *shape is a max  list (max of each dimension)   (xM,yM,zM....) 
return yield (0,0,0...)  ---  	(xM-1,yM-1,zM-1....) 

#BUG #TODO
list(U.iter2d(2,2))==[[2,0],[2,0],[2,0],[2,0]]
				not  [[0,0],[0,1],[1,0],[1,1]]
for x,y in U.iter2d(2,2):#这样正常
    U.p('[{},{}],'.format(x,y))				

	'''
	if not shape:raise py.ArgumentError('must privide int s')
	nd=py.len(shape)
	if py.isnum(start):
		r=[start]*nd
	elif len(start)== nd:
		r=py.list(start)
	else:
		r=[0]*nd
	start=r.copy()
	
	for n,size in py.enumerate(shape):
		if size<=start[n]:raise py.ArgumentError(' size of each dimension must > start ')
	
	shape_indexes=py.list(py.range(nd-1,-1,-1))
	while True:
		yield r
		r[-1]+=step
		for i in shape_indexes:
			if r[i]>=shape[i]:
				if i==0:return
				r[i]=start[i]
				r[i-1]+=step

range2d=rangen=rangeN=itern=iterN=iterdc=iter2d=iter3d=iternd=iterNd=iter_N_d=iter_all_coordinate=iter_coordinate=iter_high_demensional_coordinate=iter_each_demensional_coordinate

def getfullargspec(callable,no_raise=True):
	'''
In [1069]: inspect.getfullargspec(sb.run)
Out[1069]: FullArgSpec(args=[], varargs='popenargs', varkw='kwargs', defaults=None, kwonlyargs=['input', 'capture_output', 'timeout', 'check'], kwonlydefaults={'input': None, 'capture_output': False, 'timeout': None, 'check': False}, annota
tions={})

In [1070]: sb.run?
sb.run(
    *popenargs,
    input=None,
    capture_output=False,
    timeout=None,
    check=False,
    **kwargs,
)

	
inspect.getargspec : ValueError: Function has keyword-only parameters or annotations, use getfullargspec() API which can support them

ValueError: no signature found for builtin type <class 'dict'>
	'''
	import inspect
	try:
		if py.isinstance(callable,(inspect.FullArgSpec,inspect.ArgSpec)):
			return callable
		return inspect.getfullargspec(callable)
	except Exception as e:
		if not no_raise:raise 
		return py.No(e)
getargspec=getfullargspec

def is_generator(a):
	'''U.set('generator_types_tuple',	types_tuple);
U.is_generator(U.OrderedDict(a=1).items() )==True
	
	'''
	types_tuple=get('generator_types_tuple')
	if types_tuple:
		types_tuple=py.tuple(types_tuple)
		return py.is_generator(a) or py.isinstance(a,types_tuple)
	else:
		types_tuple=(
py.type({}.values()),  #can not dill_dump
py.type({}.keys()),
py.type({}.items()),
py.type(py.range(1)),  #dill_dump  len 46,<80 B>

		
		)
		set('generator_types_tuple',
	types_tuple)
		return is_generator(a)
isgen=isGenerator=is_generator	

def is_numpy_ndarray(a):
	return py.type(a).__module__=='numpy'
isNumpy=is_numpy=isnumpy=is_numpy_ndarray	
	
def try_call_function(function,*a,**ka):
	try:
		return function(*a,**ka)
	except Exception as e:
		return py.No(e,function,a,ka)
try_call =try_call_function	

def get_all_indexes_of_sub_seq(all,sub):
	''' #TODO KMP find '''
	lb=py.len(sub)
	return [(i, i+lb) for i in py.range(py.len(all)) if all[i:i+lb] == sub]
is_sub_seq=get_all_indexes_of_sub_seq
############## qgb type ######################	
def object_custom_repr(obj, *a, **ka):
	'''
In [1306]: float U.obj_repr(2.3,repr=3)
Out[1306]: 2.3

In [1307]: int U.obj_repr(4,repr=3)
Out[1307]: 4

In [1308]: bytes U.obj_repr(b'42ew',repr=3)
Out[1308]: b'42ew'

In [1309]: dict U.obj_repr({1:3},repr=3)
Out[1309]: {}

In [1310]: list U.obj_repr([1,2],repr=43)
Out[1310]: []

In [1312]: list U.obj_repr(set([1,2,3]),repr=43)
Out[1312]: []
'''	
	# if py.len(a)<1:raise py.ArgumentError('')
	target=get_duplicated_kargs(ka,'f','target','repr','__repr__','func','function','custom','custom_repr',default=None)
	if target==None:
		return obj
	t=py.type(obj)
	class QGB_REPR_SUBTYPE(t):
		def __repr__(self):return self.__qgb_custom_repr__()
		def __str__(self) :return self.__qgb_custom_repr__()
		def __qgb_custom_repr__(self):#super().__str__()
			'''
			'''
			if py.callable(self._qgb_repr):
				return self._qgb_repr(self,**self._qgb_ka)
			else:
				if py.getattr(self,'_qgb_ka',None):
					raise py.ArgumentError('when CustomStrRepr target not callable,must no keyword args!')
				if py.istr(self._qgb_repr):
					return self._qgb_repr
				return py.repr(self._qgb_repr)
	d=get_or_set('QGB_REPR_SUBTYPE.mapping',{})			
	if t in d:QGB_REPR_SUBTYPE=d[t]
	else     :d[t]=QGB_REPR_SUBTYPE
	#####
	
	self=t.__new__(QGB_REPR_SUBTYPE,obj,*a,**ka)
	self._qgb_obj=obj
	self._qgb_a=a
	self._qgb_ka=ka
	self._qgb_repr=target
	
	return self
ObjectRepr=objectRepr=obj_repr=object_repr=custom_object_repr=object_custom_repr	

class FloatCustomStrRepr(py.float):
	'''每添加一种 CustomStrRepr ，需要在 T.string 中添加相应的 str 代码
	或者用 self.raw 来保存 # 不行，直接保存参数 类型不对
	'''
	def __new__(cls, *a, **ka):
		if py.len(a)!=1:
			raise py.ArgumentError('only need one intable arg,but get {}'.format(py.len(a)))
		self= py.float.__new__(cls, *a)
		self.target=get_duplicated_kargs(ka,'f','target','repr','__repr__','func','function','custom',default=T.justify)
		self.ka=ka
		return self
		
	def __repr__(self):return self.__str__()
	def __str__(self):#super().__str__()
		'''
		'''
		if py.callable(self.target):
			return self.target(self,**self.ka)
		else:
			if self.ka:
				size=self.ka.get('size',None)
				#没判断target是否为 str
				if py.len(self.ka)==1 and size:
					return T.padding(self.target,size=size)
				raise py.ArgumentError('when CustomStrRepr target not callable,must no keyword args!')
			if py.istr(self.target):
				return self.target
			return repr(self.target)

FloatRepr=FloatStrRepr=FloatCustomStrRepr
	
class IntCustomStrRepr(py.int):
	'''为了避免循环调用，同时保留int 值，请用 T.string 来获取 raw str(int)
	int(x, base=10) -> integer 
	IntCustomRepr(x,target=func(i,ka),a1=..) #default base 10
	'''
	def __new__(cls, *a, **ka):
		# if py.len(a)!=1:
			# raise py.ArgumentError('only need one intable arg,but get {}'.format(py.len(a)))
		self= py.int.__new__(cls, a[0])
		self.target=get_duplicated_kargs(ka,'f','target','func','function',
		'repr','__repr__','str','__str__','custom',default=None)
		
		
		# if not self.target:
		# 	self.target=
		self.a=a
		self.ka=ka
		return self
		
	# def __str__(self):return self.__repr__()
	def __repr__(self):#super().__str__()
		'''
		'''
		if not self.target:
			self.target=T.padding
		if py.callable(self.target):
			return self.target(*self.a,**self.ka)
			
		else:
			if self.ka:
				raise py.ArgumentError('when CustomStrRepr target not callable,must no keyword args!')
			if py.istr(self.target):
				return self.target
			return repr(self.target)

IntRepr=IntStrRepr=IntCustomRepr=IntCustomStrRepr

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
	def __getitem__(self, key):
		self.__name__='[%r]'%key
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
		# if is_ipy_cell():
			# print(self.__v__)
		# else:
		return StrRepr( self.__v__ )
	def __parent_str__(self):
		''' 无法简单得到 U.v.f 的值，因为 f 处于调用者的 变量空间
		gs=sys._getframe().f_back.f_globals
		'''
		if self.__parent__==None:return ''
		if not self.__child__:return py.str(self.__parent__)
		return py.str(self.__parent__)+'.'

	def __repr__(self):return self.__str__()
	def __str__(self):
		# return stime()
		# if self.__name__=
		# log([self.__parent_str__(),self.__name__])
		sp=self.__parent_str__()
		if self.__name__.startswith('[') and sp.endswith('.'):
			sp=sp[:-1]
		return sp+self.__name__
	
v=ValueOfAttr()

class AttrCallNo:
	def __init__(self,parent=None,name='',p=True):
		self.__parent__=parent
		self.__child__=None
		self.__name__=name	
		self.__v__=p
	def __getattribute__(self, name):
		if name in SKIP_ATTR_NAMES:
			return
		if name in ValueOfAttr_NAMES:
			try:
				return py.object.__getattribute__(self, name)
			except Exception as e:
				if name=='__name__':return ''
				raise e
		# self.__name__=name		
		self.__child__= AttrCallNo(parent=self,name=name)		
		return self.__child__
		
	def __call__(self, *args, **kwargs):
		s=''
		while self.__parent__:
			s='.'+self.__name__+s
			self=self.__parent__
		if self.__v__:print(s,*args,kwargs)
		return py.No(s,*args,kwargs) # 有问题，只能 a.b.c() 不能a().b()因为a()返回 No
	# def __repr__(s):
		# s=''
		# while self.__parent__:
			# s='.'+self.__name__+s
			# self=self.__parent__
		# return py.No(s)
		
	# def __str__(s):return ''
	def encode(s,encoding):
		return b''
	def decode(s,encoding):
		return u''
	def __len__(s):return 0
	def __getitem__(s, key):
		return py.No(s.msg+'[{}]'.format(key),s,key) 
	def __iter__(self):return self
	def __next__(self):raise StopIteration

	def __contains__(s, key):return False# ('' in '') == True
	def __hash__(s):return 0
	
	def __lt__(self, other):return 0 <	other#Todo:  user defined Constant 0
	def __le__(self, other):return 0 <=	other
	def __eq__(self, other):return 0 ==	other
	def __ne__(self, other):return 0 !=	other
	def __ge__(self, other):return 0 >=	other
	def __gt__(self, other):return 0 >	other
	
	def upper(s):return s
	def lower(s):return s	
	
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
		# padding      =ka.pop('padding'       ,'\t')
		# padding_times=ka.pop('padding_times;',0)
		# padding_times=ka.pop('padding_width' ,padding_times)
		# padding_times=ka.pop('pi'            ,padding_times)
		# padding_times=ka.pop('ip'            ,padding_times)
		# padding_times=ka.pop('times'         ,padding_times)
		# padding_times=ka.pop('width'         ,padding_times)
		if not a:
			a=(ka.pop('object'),)
		try:
			self= py.str.__new__(cls, *a)
		except Exception as e:
			return py.No(e,cls, a, ka)
			
		self.ka=ka
		return self
		
	def __repr__(self):return self.__str__()
	def __str__(self) :
		repr=get_duplicated_kargs(self.ka,'repr','str','s','st','__repr__','__str__',no_pop=True)
		if repr:
			if py.callable(repr):
				return repr(self, **self.ka ) # try fix：传入 self
			else:
				return py.str(repr)
		#当提供size 参数时，小心 ModuleNotFoundError: No module named 'wcwidth'	
		return T.justify(super().__str__(),**self.ka)
	# return (self.padding*self.padding_times)+ super().__str__() +(self.padding*self.padding_times)
T.sreol=T.RLF=T.reol=T.REOL=StrRepr(T.EOL)
	
class DictAttr(dict):
	def __init__(self, *args, **kwargs):
		super(DictAttr, self).__init__(*args, **kwargs)
		self.__dict__ = self
AttrDict=DictAttr
		
#############################
def main(display=True,pressKey=False,clipboard=False,
	ipyArgs=False,escape=False,
	vsc=False,
	c=False,ipyOut=False,cmdPos=False,reload=False,*args,**ka):
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
	
	if not reload:reload=get_duplicated_kargs(ka,'R','r','rr')
	if reload:sImport+=";R=r=U.reload"
		
	if ipyOut:sImport+=';O=o=U.ipyOutLast'

	if not cmdPos:cmdPos=get_duplicated_kargs(ka,'cmdpos','pos','window_pos')	
	if cmdPos:sImport+=";POS=pos=U.cmdPos;npp=NPP=U.notePadPlus;ULS=Uls=uls=F.ls;ll=ULL=Ull=ull=F.ll"
	
	if not vsc:vsc=get_duplicated_kargs(ka,'edit','editor','npp')
	if vsc:   sImport+=";npp=U.npp;vsc=U.vsc"

	if not clipboard:clipboard=get_duplicated_kargs(ka,'cb','cbs','clipBoard','clip_board','ctrl_v')
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

	if not clipboard:clipboard=get_duplicated_kargs(ka,'cb','CB','clip_board')
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
