# coding=utf-8
gsImport='''
from qgb import U,T
'''
true=True;false=False
gimax=IMAX=imax=2147483647;gimin=IMIN=imin=-2147483648
import sys
stdin=sys.stdin;stdout=sys.stdout;stderr=sys.stderr
gsdecode=decoding='utf-8';gsencode=encoding=stdout.encoding
modules=sys.modules
import __builtin__ ;py=builtin=__builtin__

printError=printErr=gbPrintErr=True
if 'qgb.U' in modules:modules['_U']=modules['qgb.U']
elif 'U' in modules:modules['_U']=modules['U']

try:
	import os;path=os.path
	from threading import Thread
	thread=Thread
	from multiprocessing import Process;process=Process
except Exception as ei:
	gError=ei
	if gbPrintErr:print '#Error lib import',ei
try:
	_U=modules['_U']
	gError=_U.gError
	printError=printErr=gbPrintErr=_U.gbPrintErr
except Exception as _e:pass
	# pass# 已经存在于globals 中，是否有必要重新赋值给 gError？
# else:
	
try:
	from F import write,read,ls,ll,md,rm,autof
	import F,T
	from pprint import pprint
	import Clipboard;clipboard=cb=Clipboard
except Exception as ei:
	if gbPrintErr:print '#Error import',ei
	gError=ei
	
class ArgumentError(Exception):
	pass
aError=argumentError=ArgumentException=ArgumentError	
############
module=type(py)
class Class:pass
instance=type(Class())
Class=classtype=classType=type(Class)
#########################
def one_in(vs,*t):
	'''(1,2,3,[t])	or	([vs].[t])'''
	if not hasattr(vs, '__iter__'):vs=[vs]
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

import platform
def iswin():
	if platform.system().startswith('Windows'):return True
	else:return False
def isnix():
	return one_in('nix','linux','darwin',platform.system().lower())
	
def iscyg():
	return 'cygwin' in  platform.system().lower()
ipy=None#这个不是qgb.ipy, 是否与U.F U.T 这样的风格冲突？
def isipy():
	global ipy
	# ipy=False  #如果曾经有过实例，现在没有直接返回原来
	f=sys._getframe()
	while f and f.f_globals and 'get_ipython' not in f.f_globals.keys():
		f=f.f_back
		try:
			ipy=f.f_globals['get_ipython']()#下个循环没有直接跳出while
		except:
			pass
	return ipy
getipy=isipy
def isrepl():
	i,o=sys.stdin.isatty(),sys.stdout.isatty()
	if i==o:return i
	else:
		raise Exception('qgb.U isatty conflit')
isatty=istty=isrepl
########################
if iswin() or iscyg():
	try:
		import Win
		from Win import setWindowPos,msgbox
		pos=cmdPos=setWindowPos
		pid=Win.getpid()
	except Exception as ei:
		# def msgbox(s='',st='title',*a):
			# if(a!=()):s=str(s)+ ','+str(a)[1:-2]
			# if iswin():windll.user32.MessageBoxA(0, str(s), str(st), 0)
		if gbPrintErr:print '#Error import',ei
		gError=ei
	###########################
	
	if iscyg():
		def getCygPath():
			r=Win.getProcessPath()
			if 'cygwin' in r:
				return T.subLast(r,'','cygwin')+'cygwin\\'
			else:
				raise EnvironmentError(r)
elif isnix():
	def isroot():
		return os.getuid()==0
else:#Android *nix
	pid=os.getpid()
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
	'''a'''
	try:AZ=T.AZ;exist=F.exist
	except:
		AZ=''.join([chr(i) for i in range(65,65+26)])
		exist=os.path.exists
	for i in AZ[::-1]:
		if exist(i+a):return i+a
	return ''

def getTestPath():
	if isnix():
		s='/test/'
		if isroot():
			return s
		else:
			return os.getenv('HOME')+s
	if iswin() or iscyg():
		s='c:/test/'
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
	def den(k):
		if type(k) is py.unicode:k=k.encode(encoding)
		if type(k) is py.str:
			rd=T.detect(k)
			if rd.popitem()[0]>0.9:dc=rd[1]
			else:dc=decoding
			k=k.decode(dc).encode(encoding)
		return k
	
	for k in a:
		if type(k) in (list,set,tuple):
			pln()
		print k,

	# if len(ka)<1:
		# exec(s[:-1])###without (del last ,) [:-1] can't flush
	# else:
		# print a,ka
	sys.stdout.flush()

	
def p(*a,**ka):
	if len(a)==1:
		a=a[0]
		at=type(a)
		if at is py.unicode:a=a.encode(encoding)
		# elif at is 
		else:a=py.str(a)
		sys.stdout.write(a)
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
	If the size argument is negative or omitted, read until EOF is reached.'''
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
def cmd(*a,**ka):
	'''show=False :show command line
	默认阻塞，直到进程结束返回'''
	import T
	s=''
	if iswin() or iscyg():quot='"'
	else:quot="'"
	
	if len(a)==0:
		if iswin() or iscyg():a=['cmd']
		# TODO #
	if len(a)==1:
		if type(a[0])==type(''):
			if not s.startswith(quot):
				s=quot+a[0]+quot
			if ':' in s and iscyg():
				s='cmd /c start "" '+s
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
		if 'show' in ka and ka['show']:print repr(s)
		return os.system(s)
	except Exception as e:return e
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
	'''默认不阻塞'''
	if type(a)==type(''):a=[a]
	if type(a)!=type([]):a=list(a)
	if len(args)>0:a.extend(args)
	if type(a)==type([]):
		for i,v in enumerate(a):
			if py.type(v) not in (py.str,py.unicode):
				a[i]=v=str(v)
			if iswin() and v.startswith('"') and v.endswith('"'):
				a[i]=v[1,-1]
			
		return __import__('subprocess').Popen(a)
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
	if rt in (py.str,py.unicode):
		return ''.join([rt(i) for i in r])
	return r
delmuti=delMuti
def this():
	''' local dir'''
	repl()
	if not py.globals().has_key('__name__'):
		__name__='233qgb.U'
		# txt(globals())
		print __name__
	
def pyshell(printCount=False):
	# a=1
	ic=count('__repl__')
	if printCount:print ic
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

def reload(*mods):
	''' 不是一个模块时，尝试访问mod._module'''
	import sys,imp
	global gError
	if len(mods)<1:#如果 mods 中含有长度为0的元素，会导致U重新加载
		# sys.modules['qgb._U']=sys.modules['qgb.U'] #useless, _U is U
		#if pop qgb.U,can't reload
		if 'qgb.U' in sys.modules:   imp.reload(sys.modules['qgb.U'])
		elif 'U' in sys.modules:     imp.reload(sys.modules['U'])
		elif 'qgb._U' in sys.modules:imp.reload(sys.modules['qgb._U'])
		else:raise EnvironmentError('not found qgb.U ?')
		# print 233
	elif len(mods)==1:
		mod=mods[0]
		if not isModule(mod):
			# sys.a=mod
			# return
			try:
				if '_module' in py.dir(mod):
					if not isModule(mod._module):raise Exception('instance._module is not module')
					mod=mod._module
					modules[mod.__name__]=mod
					reload(mod)
					
					# if mod.__name__ in modules:#'qgb.ipy'
				else:raise Exception('instance._module not exists')
			except Exception as em:
				raise em
			
			# else:gbPrintErr=True#在函数局域覆盖全局属性
		try:
			imp.reload(mod)
		except Exception as ei:
			gError=ei
			if gbPrintErr:print ei
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

__frame=sys._getframe().f_back
	
	
def clear():
	# sys.modules[__name__] = __wrapper(sys.modules[__name__])
	if iswin():os.system('cls')
	if isnix():os.system('clear')
C=c=cls=clear


def chdir(ap=gsTestPath,*a,**ka):
	if type(ap)!=type('') or len(ap)<1:ap=gsTestPath
	ap=path.join(ap,*a)
	
	mkdir=True
	if 'md' in ka:mkdir=ka['md']
	if 'mkdir' in ka:mkdir=ka['mkdir']
	if iscyg():mkdir=False#cyg下可以创建带:的目录，导致切换异常
	if mkdir:md(ap)
	
	global gscdb
	# repl()
	# if path.abspath(gscdb) != pwd():
	gscdb.append(pwd())
	
	if path.isdir(ap):os.chdir(ap);return True

	ap=path.dirname(ap)
	if path.isdir(ap):os.chdir(ap);return True
	for i in ap:
		if i not in T.PATH_NAME:raise Exception('need file path',ap,i)
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
cdqp=cdqpsu=cdQPSU
	
def cdWShell(a=''):
	return cd(gsWShell+a)
cds=cdws=cdWShell

def cdpm():
	return cd('e:/pm')
	
def cdbabun(a=''):
	return cd(r'C:\QGB\babun\cygwin\home\qgb/'+a)
def pwd(p=False,display=False):
	s=os.getcwd()
	if p or display:print s
	try:pwd.sp=F.getsp(s)
	except:pass
	return s
	
def sort(a, cmp=None, key=None, reverse=False):
	'''sorted _5,cmp=lambda a,b:len(a)-len(b)  按长度从小到大排序
	在python2.x中cmp参数指定的函数用来进行元素间的比较。此函数需要2个参数，然后返回负数表示小于，0表示等于，正数表示大于。'''
	t=py.type(a)
	a=py.sorted(a,cmp,key,reverse)
	if t in (py.str,py.unicode):
		return ''.join([t(i) for i in a])
	else:
		return a
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

def execHelp(s):
	'''diff between eval and exec in python
	exec not return 
	    a=exec('1')
         ^
		SyntaxError: invalid syntax
'''
	return py.help('exec')
	# exec(s)

def calltimes(a=''):
	import T
	a='_count'+T.string(a)
	if calltimes.__dict__.has_key(a): 
		calltimes.__dict__[a]+=1
	else:
		calltimes.__dict__[a]=0
	return calltimes.__dict__[a]
ct=count=calltimes
def _ct_clear():
	r=calltimes.__dict__
	calltimes.__dict__={'clear':_ct_clear}
	return {k:v for k,v in r.items() if k.startswith('_count')}
calltimes.clear=_ct_clear


if(calltimes()<1):BDEBUG=True
debug=BDEBUG

def setStd(name,file):
	'''name=[std]out err in'''
	t=py.type(file)
	name=name.lower()
	if t in (py.str,py.unicode):
		file=open(file,'w+')
	if t is py.file:
		if file.closed:raise ArgumentError('need an opened mode=w+ file')
	if py.len(name)<4:name='std'+name
	d=py.globals()
	if d.has_key('__'+name) and d['__'+name]:
		old=getattr(sys,name)
		old.close()
		exec('''sys.{0}=file'''.format(name))
	else:
		
		exec("d['__{0}'],sys.{0}=sys.{0},file".format(name))
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
		gError=e
		return False
	if(sm and sm != stdm):
		stdm.close()#以前设置的std
		exec('sys.{0}=sm'.format(std))
	return True
resetstd=resetStd#=resetStream

def browser(url,ab='chrome'):
	import webbrowser
	def chrome(url):
		###TODO: auto Find system base everything
		spC='''C:\QGB\Chrome\Application\chrome.exe'''	
		webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(spC))
		webbrowser.get('chrome').open_new_tab(url)
	for i in py.dir():
		if py.eval('callable({0})'.format(i)):
			if ab.lower()== i:
				exec '{0}(url)'.format(i) in globals(),locals()
		
	 
	# webbrowser.open_new_tab(url)
	# if iswin():os.system('''start '''+str(url))
# browser('qq.com')

gshtml=htmltxt=txthtml=('<textarea style="width:100%; height:100%;">','</textarea>')
		
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
			if py.callable(v):
				if k.startswith('__'):
					vv='!ErrGetV()'
					try:
						if isipy():#在ipython 中存在用户名字空间自动清空的问题
							pass
						else:
							vv=v()
					except:pass
					v='{0} == {1}'.format(v,vv)
				v=str(v)
				v+=getHelp(v)
			if type(v) is not str:
				import pprint
				v= pprint.pformat(v)
		except Exception as e:v=py.repr(e)
		
		v=v.replace(txthtml[0], '*'*33)
		v=v.replace(txthtml[1], '*'*11)
		
		r+=sh.format(i,k,v,vi)
	# cdt('QPSU')
	import T,F
	name=gst+'QPSU/'+T.filename(getObjName(a))+'.html'
	print name
	browser(name)
	return F.write(name,read(sp).replace('{result}',r))
	
	
	# cdBack()
pa=printattr=printAttr
# repl()
# printAttr(5)
gAllValue=[]
def DirValue(a,fliter='',recursion=False,ai=0,depth=9):
	'''约定：只有无参数函数才用 getXX  ?'''
	r={}
	for i in py.dir(a):
		
		try:
			tmp=py.eval('a.'+i)
			if recursion:
				if ai>depth:return '!depth reached'
				tmp=DirValue(tmp,fliter,recursion,ai+1,depth)
			if fliter not in i:continue	
			r[i]=tmp
				
		except:
			r[i]=Exception('can not get value '+i)
	return r
dir=dirValue=getdir=getDirValue=DirValue

def getObjName(a,value=False):
	try:
		if len(a.__name__)>0:
			return a.__name__
	except:pass
	
	try:
		r=str(a.__class__)
		if 'type' in r:
			return T.sub(r,T.quote,T.quote).strip()
	except:pass
	
	if type(a) in (py.int,py.long):return 'i_'+str(a)
	if type(a) in (py.str,py.unicode):return 's_'+a[:7]
		
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
name=getArgName=getVarName
# repl()
# exit()
# getVarName(1l)

def isModule(a):
	return type(a) is module
ismod=ismodule=isModule

def getHelp(a):
	import pydoc,re
	a=pydoc.render_doc(a,'%s')
	a=re.sub('.\b', '', a)
	originURL='docs.python.org/library/'
	targetURL='python.usyiyi.cn/documents/python_278/library/{0}.html\n'+originURL
	msgbox(isModule(a))
	if originURL in a:
		a=a.replace(originURL,targetURL.format(T.sub(a,originURL,'\n')))
	elif isModule(a):
		a=a.replace('NAME',   targetURL.format(T.sub(a,'NAME',' - ').strip() ) )
		repl()
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
	txt=txt.replace(txthtml[1],txthtml[1][:1]+'!!!qgb-padding!!!'+txthtml[1][1:])	
	f=open(file,'w+')
	f.write(txthtml[0]+txt+txthtml[1])
	f.close()
	if(browser==True):globals()['browser'](f.name)
	# print vars()
	# vars()['browser'](f.name)

def phtml(file):
	raise Exception('#TODO')
	if(file.lower()[-1]!='l'):file=file+'.html'
	# setOut0(file)
	print txthtml[0]
def phtmlend():
	raise Exception('#TODO')
	print txthtml[1]
	sf=sys.stdout.name
	# resetOut0()
	globals()['browser'](sf)
# dicthtml('uvars.html',vars())

def mergeDict(*a):
	r={}
	for i in a:
		if type(i) != py.dict:
			try:i=py.dict(i)
			except:continue
		for k,v in i.iteritems():
			r[k]=v
	return r
	
def getTimestamp():
	'''return: float
--------> U.time()
Out[304]: 1490080570.265625

In [305]: U.time
--------> U.time()
Out[305]: 1490080571.125
'''
	return __import__('time').time()
time=getime=getTime=timestamp=getCurrentTime=getTimestamp
	
	
	
def getFloaTail(a,s=False,str=False,string=False,i=False,int=False):
	if type(a) is float:
		a=round(a-py.int(a),3)
		if s or str or string:
			return py.str(a)[1:]
		if i or int:
			return int(py.str(a)[2:])
		return a	
gsTimeFormat='%Y-%m-%d %H.%M.%S'
gsymd=gsYMD=gsTimeFormatYMD='%Y%m%d'
#ValueError: year=1 is before 1900; the datetime strftime() methods require year >= 1900

def getStime(time=None,format=gsTimeFormat):
	'''http://python.usyiyi.cn/translate/python_278/library/time.html#time.strftime'''
	import time as tMod
	
	if ':' in format:format=gsTimeFormat.replace('.',':')
	
	if py.type(time) not in (int,float,long):time=getTimestamp()
	if not time:time=0.000001
	if py.type(time) is not py.float:time=py.float(time)
	if format=='' or type(format) is not str:return str(time)
	
	if '%' in format:
		if time:
			r=tMod.strftime(format,tMod.localtime(time))
#localtime: time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=8,....
			if type(time) is float:
				if not r.endswith(' '):r+=' '
				r+=getFloaTail(time,s=True)
			return r
		else:return tMod.strftime(format)
stime=timeToStr=getStime
	
def int(a,default=0,error=-1):
	if not a:return default
	try:return py.int(a)
	except:return error
def traverseTime(start,stop=None,step='day'):
	'''range(start, stop[, step])
	datetime.timedelta(  days=0, seconds=0, microseconds=0,
                milliseconds=0, minutes=0, hours=0, weeks=0)
	step default: 1(day)  [1day ,2year,....]  [-1day not supported]'''
	import re,datetime as dt
	sregex='([0-9]*)(micro|ms|milli|sec|minute|hour|day|month|year)'
	timedeltaKW=('days', 'seconds', 'microseconds',
 'milliseconds', 'minutes', 'hours', 'weeks')
	if py.type(step) in (py.str,py.unicode):
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

timeTraverser=timeTraversal=traverseTime	
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
	elif py.type(a) in (py.str,py.unicode):
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

from threading import enumerate as getAllThreads
threads=gethreads=getAllThreads
def getThreads():
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
			if(BDEBUG):print e ,'#%s#'%str(e) 
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
	return list(y())
	
	# exit()
# print methods([])	
	
def x(msg=None):
	if(msg!=None):print msg
	exit(235)
	
def exit(i=2357):
	'''not call atexit'''
	os._exit(i)
def getAllMod(mp=None):
	ls=[]
	if not mp:mp=getModPath()
	if 'F' in globals():
		for i in F.ls(mp,t='r'):
			if not i.lower().endswith('.py'):continue
			i=i.replace(mp,'')
			if F.isPath(i):
				if i.lower().endswith('__init__.py'):
					ls.append(path.dirname(i))
			elif '__' not in i:
				ls.append(T.subLast(i,'','.'))
		return ls
	for i in os.listdir(mp):
		if(len(i)<3):continue
		if(i.find('__')!=-1):continue
		if(i.lower()[-3:]!='.py'):continue
		ls.append(i[:-3])
	if ls:return ls
	else:return  ['N', 'Win', 'Clipboard', 'F', 'ipy', 'T', 'U']
def getModPathForImport():
	return getModPath()[:-4]
	sp=os.path.dirname(getModPath())# dirname/ to dirname
	sp=os.path.dirname(sp)
	if iswin():return sp#cygwin None

def getModPath(qgb=True,slash=True,backSlash=False,endSlash=True,endslash=True,trailingSlash=True):
	'''@English The leading and trailing slash shown in the code 代码中的首尾斜杠'''
	sp=os.path.abspath(__file__)
	sp=os.path.dirname(sp)
	sp=os.path.join(sp,'')
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
	
	
def len(a,*other):
	if other:
		r=[len(a)]
		for i in other:
			r.append(len(i))
		return r
	try:return py.len(a)
	except:
		# if type(a) in (int,float,list,tuple,dict):
			# return py.len(str(a))
		try:return py.len(str(a))
		except:return -1
		
def dis(a):
	from dis import dis
	return dis (compile(a,'<str>','exec'))
		
def ipyStart(*a):
	import IPython
	IPython.start_IPython()
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
	
	
def notePadPlusPlus(a=''):
	'''
--------> os.system('"M:\\Program Files\\Notepad++\\notepad++.exe" "IP.py"')
'M:\Program' 不是内部或外部命令，也不是可运行的程序
或批处理文件。
Out[114]: 1

--------> os.system('"M:\\Program Files\\Notepad++\\notepad++.exe" IP.py')
Out[115]: 0

'''
	npath=driverPath(r":\Program Files\Notepad++\notepad++.exe")
	# npath='"%s"'%npath
	if a:
		return run(npath,autof(a))
	else:
		run(npath)
		return npath 
		
	# cmd('npp',str(a))
npp=notePadPlus=notePadPlusPlus
	
def backLocals(f=None,i=0,r=[]):
	print i+1,'='*(20+i*2)
	
	if f is None and i==0:f=__import__('sys')._getframe()
	try:print f.f_locals.keys();r.append(f.f_locals)
	except:return r
	return backLocals(f.f_back,i+1,r)	
printFrame=backLocals
	
def getDate():
	'''return '20170301' #From os time'''
	from datetime import date
	t=date.today()
	return ('%4s%2s%2s'%(t.year,t.month,t.day)).replace(' ','0')
today=getdate=getDate
# sys.argv=['display=t','pressKey=t','clipboard=f']
def isSyntaxError(a):
	if not sys.modules['ast']:import ast
	try:
		sys.modules['ast'].parse(a)
		return False
	except:
		return True
isyntaxError=iSyntaxError=isSyntaxError

def parse(code,file):
	from ast import parse,AST,iter_fields
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
	print >>file,_format(a)
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
def getModule(modName):
	if modName in modules:return modules[modName]
	if modName.startswith('qgb.'):
		modName=modName[4:]
		return getModule(modName)
	return None
getmod=getMod=getModule
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
	###############################
	'''call order Do Not Change! '''
	###############################
	sImport=gsImport
	if c:sImport+=';C=c=U.clear'
	
	if reload:sImport+=";R=r=U.reload"
		
	if ipyOut:sImport+=';O=o=U.ipyOutLast'
	
	if cmdPos:sImport+=";POS=pos=U.cmdPos;npp=NPP=U.notePadPlus;ULS=Uls=uls=F.ls;ULL=Ull=ull=F.ll"
		
	if escape:sImport=sImport.replace("'",r"\'")
	
	if display:print sImport
	
	if pressKey:
		try:
			import win32api
			win32api.ShellExecute(0, 'open', gsw+'exe/key.exe', sImport+'\n','',0)
		except:print 'pressKey err'
	if clipboard:
		try:
			Clipboard.set(sImport)
		except:print 'Clipboard err'
	
	return sImport
def test():
	gm=getAllMod()
	print gm
	repl()
	# gm=['U','T','N','F',].extend(gm)
	gm=set(gm)
	for i in gm:
		print '='*55
		try:
			exec '''
import {0}
print {0}
			'''.format(i) in {}
		except Exception as ei:
			print '###import {0}'.format(i)
			print ei
# print 233
def explorer(path='.'):
	if iswin():
		os.system('explorer.exe '+path)
exp=explorer

def log(*a):
	pln(a)

def logWindow():
	import Tkinter as tk
	#TODO:

def set(name,value=None):
	if py.type(name) is not py.str and value==None:
		set.__dict__['_']=name
		return
	set.__dict__[name]=value
def get(name='_'):
	return set.__dict__[name]
	#TODO
def google(a):
	browser('https://www.google.com.my/#q='+a)
	
#def 	#把一个数分解成2的次方之和。
gsImport='''import sys,os;sys.path.append('{0}');from qgb import *'''.format(getModPathForImport())
if __name__ == '__main__':main()