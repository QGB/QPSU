#coding=utf-8
try:
	if __name__.startswith('qgb.Win'):
		from .. import py
	else:
		import py
except Exception as ei:
	raise ei
	raise EnvironmentError(__name__)
	
if py.is2():
	import _winreg as winreg
	from _winreg import *
else:
	import winreg
	from winreg import *

def get(skey,name,root=HKEY_CURRENT_USER,returnType=True):
	'''	from qgb.Win import reg
		reg.get(r'Software\Microsoft\Windows\CurrentVersion\Internet Settings','ProxyEnable')
	reg.get(r'HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters\Size' 	)
	There are seven predefined root keys, traditionally named according to their constant handles defined in the Win32 API
	skey不能包含 name，否则 FileNotFoundError: [WinError 2] 系统找不到指定的文件。
	'''
	
	
	r = OpenKey(root,skey)
	r = QueryValueEx(r,name)
	if returnType:return r[0],'{} : {}'.format(REG_TYPE[r[1]],r[1])
	else         :return r[0]        
	
def set(skey,name,value,root=HKEY_CURRENT_USER,type='auto,or REG_TYPE int',returnType=True):
	r  = OpenKey(root,skey,0,KEY_SET_VALUE)
	if not py.isint(type):
		if py.isint(value):type=4
		if py.istr(value):type=1
		if py.isbyte(value):type=3 #TODO test,and add more rule
		
	SetValueEx(r,'ProxyEnable',0,type,value)
	if get(skey,name,root=root,returnType=False)==value:
		return 'reg.set [{}] {}={} sucess!'.format(skey[-55:],name,value)
	else:
		return 'reg.set [{}] {}={} Failed !'.format(skey,name,value)
		
REG_TYPE={	0 : 'REG_NONE',
			1 : 'REG_SZ',
			2 : 'REG_EXPAND_SZ', 
			3 : 'REG_BINARY', 
			4 : 'REG_DWORD', 
			5 : 'REG_DWORD_BIG_ENDIAN', 
			6 : 'REG_LINK', 
			7 : 'REG_MULTI_SZ', 
			8 : 'REG_RESOURCE_LIST', 
			9 : 'REG_FULL_RESOURCE_DESCRIPTOR',  
			10: 'REG_RESOURCE_REQUIREMENTS_LIST',  
			11: 'REG_QWORD'}
