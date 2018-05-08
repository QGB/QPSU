# coding=utf-8
import sys
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
	
class Class:pass
obj=Class()
instance=type(obj)
classtype=classType=type(Class)

def iterable(a):
	try:
		for i in a:pass
		return True
	except:return False
	
def istr(a):
	if is2():return isinstance(a,basestring)#py.type(a) in (py.str,py.unicode)
	else:    return isinstance(a,str)

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
	else:    return type(a) in (int,float)
	
def pdb(msg=''):
	'''call pdb in pdb is useless
	
	'''
	# import os
	# if os.getenv('py.pdb') in (None,'False','false','f','0',''):return 'No py.pdb'
	# "win can set 'PY.PDB': '1'  "
	# if msg:print(msg)
	import pdb
	pdb.Pdb().set_trace(sys._getframe().f_back)
	
def importU():
	# try:import U
	import sys,os
	if 'qgb.U' in sys.modules:U=sys.modules['qgb.U']
	elif 'U' in sys.modules:  U=sys.modules['U']
	try:from qgb import U
	except:pass
	try:from . import U
	except:pass
	try:import U
	except:pass
	
	if 'U' in locals():
		g=sys._getframe().f_back.f_globals
		g['U']=U
	else:
		pdb()
		raise Exception('#Error import U in qgb.py')
	
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
	