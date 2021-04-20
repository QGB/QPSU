# coding=utf-8
import sys
version=sys.version_info
ver=version=float(version.major) + float('0.{}{}'.format(version.minor,version.micro))
def is2():
	'''
'2.7.13 |Anaconda 4.3.1 (32-bit)| (default, Dec 19 2016, 13:36:02) [MSC v.1500 32 bit (Intel)]
'''
	return sys.version[0]=='2'
def is3():
	'''
'3.5.2 (default, Nov 17 2016, 17:05:23) \n[GCC 5.4.0 20160609]'
<ApiModule 'py' version='1.4.34' from 'G:\\QGB\\Anaconda3\\lib\\site-packages\\py\\__init__.py'>
'''
	return sys.version[0]=='3'
	
if is2():
	from __builtin__ import *
	try:
		from io import open
	except Exception as e:
		pass
	
if is3():
	from builtins import *
	from importlib import reload
		
class Class:pass
obj=Class()
instance=type(obj)
classtype=classType=type(Class)
module=type(sys)
class ArgumentError(Exception):
	pass
class ArgumentUnsupported(ArgumentError):#an unsupported argument# 为了能快速找到Arg 开头的异常
	pass

def isNo(a):
	return isinstance(a,No) or \
		'py.No' in repr(getattr(a,'__class__',0)) or\
		(istr(a) and a.startswith('\t\t###<py.No|')) or\
		False		#TO ADD...
isno=isNo		
gno2e=False

def safe_repr(a):
	try:return repr(a)
	except Exception as e:return repr(e)

GS_NO_MSG='\t\t###<py.No|%s>'	
GS_NO='\t\t###<py.No|%s %s>'	
class No:
	''''is a None object with msg and raw args
#TODO
	TypeError: unsupported operand type(s) for +: 'float' and 'No'
	
no_raise=Ture  用法：  py.No 用于配置 . 并非预料之外的异常
	'''
	def __init__(s,*a,msg='',no_raise=False):
		if gno2e and not no_raise:raise Exception(*a)
		import time as tMod
		time=tMod.time()
		s.time=tMod.strftime(' %Y-%m-%d__%H.%M.%S__',tMod.localtime(time )  )
		if msg and istr(msg):s.msg=msg
		else:
			s.msg=''
			# r=''
			# if isException(msg):
				# r+=repr(msg)
			# if a and  isException(a[0]):
				# r+=repr(a[0])
			# r+=time
			# if isfloat(time):
				# r+=str(round(time-int(time),3)  )[1:]
			# s.msg=r
			# a=(msg,)+a
		s.a=a
	def __str__(s):return ''
	def encode(s,encoding):
		return b''
	def decode(s,encoding):
		return u''
	def __repr__(s):
		# r=s.msg if s.msg.startswith('#') else '###<py.No| {0}>'.format(s.msg)
		if s.msg:
			return GS_NO_MSG%s.msg
		else:
			return GS_NO%(','.join(safe_repr(i).strip() for i in s.a),s.time)
		return r
	def __len__(s):return 0
	def __getitem__(s, key):
		return No(s.msg+'[{}]'.format(key),s,key) # https://stackoverflow.com/questions/20551042/whats-the-difference-between-iter-and-getitem 
#是的，这是预期的设计。它被记录，经过充分测试并被诸如str的序列类型所依赖。__getitem__版本是Python拥有现代迭代器之前的传统。这个想法是，使用序列s [0]，s [1]，s [2]，...，直到出现IndexError或StopIteration为止，任何序列（可索引且具有长度的序列）都可以自动迭代
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
	# def __call__(s,*a,**ka):#不要定义这个，否则在ipy中不显示 repr
		#乱来吗？  谁说一定返回 str
		# return s.__str__()
		
	# @staticmethod #obj.__len__()==-1
# no=No() #instance
def isbool(a):
	return (a is True) or (a is False)

def is_generator(a):
	return callable(getattr(a,'__next__',0))
	# import types
	# if isinstance(a, types.GeneratorType):return True
	# import itertools #itertools is native module,no py file
	# if isinstance(a,itertools._tee)      :return True
	# return False
isgen=isGenerator=is_generator

def iterable(a):
	try:
		for i in a:pass
		return True
	except:return False
	
def isunicode(a):
	if is2():return isinstance(a,unicode)
	else    :return isinstance(a,str)
	
def isbyte(a):
	if is2():return type(a) in (str,bytearray,bytes)
	else    :return type(a) in (bytearray,bytes)
isbytes=isbyte
	
def istr(a):
	if is2():return isinstance(a,basestring)#type(a) in (str,unicode,bytes)
	else    :return isinstance(a,str)       #bytes is not str

def isnum(a):
	'''
	Number 的类别
		1 自然数
		2 整数
		3 有理数
		4 实数
		5 复数   complex()==0j
		6 其他类型'''
	if is2():return type(a) in (int,long,float,complex) or isint(a) or isfloat(a)#isinstance better?
	else    :return type(a) in (int,float,complex) or isint(a) or isfloat(a)
isnumber=isnum

def isint(a):
	if is2():return type(a) in (int,long)
	# else    :return type(a) in (int,) # 这个不会判断子类
	return isinstance(a,int)

def isfloat(a):
	return isinstance(a,float)
	
def isfile(a):
	if is2():return isinstance(a, file)
	else:
		from io import IOBase
		return isinstance(a, IOBase)

def isbasic(a,recursive=False):
	'''  not file
		#todo recursive
	'''
	return istr(a) or isnum(a) or type(a) in (dict,tuple,list,set,bytes,bytearray) 
		
def istuple(a):
	return isinstance(a,tuple)
		
def islist(a):
	return isinstance(a,list)

def isdict(a):
	return isinstance(a,dict)
	
def isException(a):
	'''isinstance(Exception,BaseException)==False'''
	return isinstance(a, (Exception,BaseException))
	
def byte(aInt):
	'''0 <= aInt < 256.'''
	if is2():return chr(aInt)
	else    :return bytes([aInt])
	
def modules(modName):
	return [i[1] for i in sys.modules.items() if modName in i[0] and i[1]] 

def execute(source, globals=None, locals=None):
	''' None is current env '''
	f=sys._getframe().f_back
	if locals==None:locals=f.f_locals
	if globals==None:globals=f.f_globals
	exec(source,globals,locals)   # is2  exec(expr, globals, locals) 等同于exec expr in globals, locals
	
gpdb=True	
def pdb(frame=No('if no frame use: py.pdb()()')):
	'''import pdb;pdb.set_trace()
	call pdb in pdb is useless
	
	frame=sys._getframe().f_back
	'''
	if not gpdb:return
	# import os
	# if os.getenv('py.pdb') in (None,'False','false','f','0',''):return 'No py.pdb'
	# "win can set 'PY.PDB': '1'  "
	# if msg:print(msg)
	set_trace=__import__('pdb').Pdb().set_trace
	if frame:
		set_trace(  frame)
	else:
		return set_trace
	# __import__('pdb').Pdb().set_trace(  frame)
debug=pdb
	
def from_qgb_import(mod='U'):
	# try:import U
	import sys
	if not mod.startswith('qgb.'):
		if 'qgb.'+mod in sys.modules: 
			return sys.modules['qgb.'+mod]
	if mod in sys.modules: 
		return sys.modules[mod]
	# else: 往下走，不要乱改
		# return No(mod+' not in sys.modules')
		
	s='''
try:from qgb import {0}
except:pass
try:from . import {0}
except:pass
try:import {0}
except Exception as ei3:pass

'''
	s=s.format(mod)  # NO startswith qgb.
	_locals=_globals={}
	exec(s,_locals,_globals)
	
	if mod in _locals:
		g=sys._getframe().f_back.f_globals
		if mod not in g:
			g[mod]=_locals[mod]
		return g[mod]
		# if U.debug():pdb()
	else:
		# pdb()
		import U
		raise Exception('#Error import U in qgb.py')
importU=from_qgb_import

def importT():
	return from_qgb_import('T')
def importN():
	return from_qgb_import('N')
def importF():
	return from_qgb_import('F')
def importUTNF():
	return map(from_qgb_import,'UTNF')
	
def traceback(ae=None):
	import traceback
	if not ae:return traceback.print_last()
	if is3():
		tb=getattr(ae,'__traceback__',0)
		if not tb:return traceback()
		return traceback.print_tb(tb)
	if is2():
		print('NotImplementedError')
		return
	try:
		a,e,tb=sys.exc_info()
		traceback.print_tb(tb)

	except Exception as e:
		print(e)
		return e
		
		
try:
	import platform
	def iswin():
		if platform.system().startswith('Windows'):return True
		else:return False
	glnix=['nix','linux','darwin']
	def isnix():
		return [i for i in glnix if i in platform.system().lower()]
	def iscyg():
		return 'cygwin' in  platform.system().lower()
except:pass 	
	