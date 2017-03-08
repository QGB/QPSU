# coding=utf-8
gsImport='''
from qgb import U,T
'''
true=True;false=False
gimax=IMAX=imax=2147483647;gimin=IMIN=imin=-2147483648
import  os,sys;path=os.path
stdin=sys.stdin;stdout=sys.stdout;stderr=sys.stderr
decoding='utf-8';encoding=stdout.encoding
modules=sys.modules
from threading import Thread
thread=Thread
from multiprocessing import Process;process=Process
import __builtin__ ;py=builtin=__builtin__
module=type(py)

if 'qgb.U' in modules:modules['_U']=modules['qgb.U']
elif 'U' in modules:modules['_U']=modules['U']

# if '_U' in modules:
	
try:
	_U=modules['_U']
	gError=_U.gError
	printError=printErr=gbPrintErr=_U.gbPrintErr
except Exception as _e:
	# pass# 已经存在于globals 中，是否有必要重新赋值给 gError？
# else:
	gError=None
	printError=printErr=gbPrintErr=False

		
try:
	from F import write,read,ls,ll,md,rm
	import F,T
	from pprint import pprint
	import Clipboard;clipboard=cb=Clipboard
except Exception as ei:
	if gbPrintErr:print '#Error import',ei
	gError=ei
#########################
import platform
def iswin():
	if platform.system().startswith('Windows'):return True
	else:return False
def isnix():
	if 'nix' in platform.system().lower():return True
	else:return False
def iscyg():
	return 'cygwin' in  platform.system().lower()
ipy=None
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
	if isnix():return '/test/'
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
	

def autof(head,ext=''):
	'''return str  
	# TODO # ext=?ext*     '''
	if not py.type(ext)==py.type(head)==py.str or head=='':
		return ''
	
	if len(ext)>0 and not ext.startswith('.'):ext='.'+ext
	head.head.lower();ext=ext.lower()
	
	ap='.'
	if path.isabs(head):
		ap=F.dir(head)
		if not F.isExist(ap):
			if head.endswith(ext):return head
			else:return head+ext

	
	import F
	ls=[i.lower() for i in F.ls(ap)]
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
def cmd(*a,**ka):
	'''show=False :show command line'''
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
# del __name__
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
		if type(mod) != module:
			if '_module' in py.dir(mod):
				mod=mod._module
				if mod.__name__ in modules:#'qgb.ipy'
					modules[mod.__name__]=mod
			else:gbPrintErr=True#在函数局域覆盖全局属性
		try:
			imp.reload(mod)
		except Exception as ei:
			global gError
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


def chdir(ap=gsTestPath,md=True):
	if iscyg():md=False#cyg下可以创建带:的目录，导致切换异常
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
	try:pwd.sp=F.getsp(s)
	except:pass
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
def _ct_clear():
	r=calltimes.__dict__
	calltimes.__dict__={'clear':_ct_clear}
	return {k:v for k,v in r.items() if k.startswith('_count')}
calltimes.clear=_ct_clear


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
					try:vv=v()
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
	import T
	name=gst+'QPSU/'+T.filename(getObjName(a))+'.html'
	print name,write(name,read(sp).replace('{result}',r))
	
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
	if(file.lower()[-1]!='l'):file=file+'.html'
	setOut(file)
	print txthtml[0]
def phtmlend():
	print txthtml[1]
	sf=sys.stdout.name
	resetOut()
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
	'''return: float'''
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
		
def getStime(time=None,format='%Y-%m-%d %H.%M.%S'):
	'''http://python.usyiyi.cn/translate/python_278/library/time.html#time.strftime'''
	import time as tMod
	
	if ':' in format:format='%Y-%m-%d %H.%M.%S'.replace('.',':')
	
	if type(time) not in (int,float,long):time=getTimestamp()
	if format=='' or type(format) is not str:return str(time)
	
	if '%' in format:
		if time:
			r=tMod.strftime(format,tMod.localtime(time))
			if type(time) is float:
				if not r.endswith(' '):r+=' '
				r+=getFloaTail(time,s=True)
			return r
		else:return tMod.strftime(format)
stime=timeToStr=getStime
	
		

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
	return ls
def getModPathForImport():
	sp=os.path.dirname(getModPath())# dirname/ to dirname
	sp=os.path.dirname(sp)
	if iswin():return sp

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
	
	
def notePadPlus(a):
	cmd(driverPath(r":\Program Files\Notepad++\notepad++.exe"),autof(a))
	# cmd('npp',str(a))
	
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
def replaceModule(modName,new,package='',backup=True):
	if package:
		if not package.endswith('.'):package+='.'
		if package+modName in modules:
			modName=package+modName
	if backup:
		modules['_'+modName] = modules[modName]
	
	if modName in modules:
		modules[modName]=new	
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
	gsImport='''import sys,os;sys.path.append('{0}');from qgb import *'''.format(getModPathForImport())
	###############################
	'''call order Do Not Change! '''
	###############################
	if c:gsImport+=';C=c=U.clear'
	
	if reload:gsImport+=";R=r=U.reload"
		
	if ipyOut:gsImport+=';O=o=U.ipyOutLast'
	
	if cmdPos:gsImport+=";POS=pos=U.cmdPos;npp=NPP=U.notePadPlus;ULS=Uls=uls=F.ls;ULL=Ull=ull=F.ll"
		
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
def test():
	gm=getAllMod()
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
if __name__ == '__main__':main()