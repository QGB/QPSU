# coding=utf-8
import sys
version=sys.version_info
version=float(version.major) + float('0.{}{}'.format(version.minor,version.micro))
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

class No:	
	def __init__(s,msg='is a None object with msg',*a):
		
		s.msg='{0}'.format(msg)
		
	def __str__(s):return ''
	def __repr__(s):
		r=s.msg if s.msg.startswith('#') else '###<py.No {0}>'.format(s.msg)
		r='\t\t'+r
		return r
	def __len__(s):return 0
	def __getitem__(s, key):return None
	# @staticmethod #obj.__len__()==-1
	# def __len__():return -1
no=No() #instance
	
def iterable(a):
	try:
		for i in a:pass
		return True
	except:return False
	
def isbyte(a):
	if is2():return type(a) in (str,bytearray,bytes)
	else    :return type(a) in (bytearray,bytes)
	
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
	if is2():return type(a) in (int,long,float,complex)#isinstance better?
	else    :return type(a) in (int,float,complex)

def isint(a):
	if is2():return type(a) in (int,long)
	else    :return type(a) in (int,)
	
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
		
def modules(modName):
	return [i[1] for i in sys.modules.items() if modName in i[0] and i[1]] 

def execute(source, globals=None, locals=None):
	''' None is current env '''
	f=sys._getframe().f_back
	if locals==None:locals=f.f_locals
	if globals==None:globals=f.f_globals
	exec(source,globals,locals)   # is2  exec(expr, globals, locals) 等同于exec expr in globals, locals
	
gpdb=True	
def pdb(frame=sys._getframe().f_back):
	'''call pdb in pdb is useless
	
	'''
	if not gpdb:return
	# import os
	# if os.getenv('py.pdb') in (None,'False','false','f','0',''):return 'No py.pdb'
	# "win can set 'PY.PDB': '1'  "
	# if msg:print(msg)
	import pdb
	pdb.Pdb().set_trace(frame)
	
def importU():
	# try:import U
	import sys
	if 'qgb.U' in sys.modules:U=sys.modules['qgb.U']
	elif 'U' in sys.modules:  U=sys.modules['U']
	else:
		try:from qgb import U
		except:pass
		try:from . import U
		except:pass
		try:import U
		except Exception as ei3:pass
	
	if 'U' in locals():
		g=sys._getframe().f_back.f_globals
		if 'U' not in g:g['U']=U
		return U
		# if U.debug():pdb()
	else:
		# pdb()
		import U
		raise Exception('#Error import U in qgb.py')

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
	