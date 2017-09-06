#coding=utf-8
import sys,ctypes
if 'qgb.U' in sys.modules:U=sys.modules['qgb.U']
elif 'U' in sys.modules:  U=sys.modules['U']
else:
	from sys import path as _p;_p.insert(-1,_p[0][:-4-4])
	# for i,v in enumerate(_p):  #这会导致 ImportError: No module named Constants
		# if 'qgb' in v and 'Win' in v:
			# _p.pop(i)
	# print _p
	from qgb import U

class WinDLL(ctypes.CDLL):
	"""This class represents a dll exporting functions using the
	Windows stdcall calling convention.
	"""
	_func_flags_ = 0
	
windll = ctypes.LibraryLoader(WinDLL)
	
if U.iswin() or U.iscyg():
	user32=windll.user32
	kernel32=windll.kernel32
	advapi32=windll.advapi32
# elif U.iscyg():#Not Win
	# try:
		# from ctypes import cdll
		# user32=cdll.LoadLibrary("user32.dll")
		# kernel32=cdll.LoadLibrary("kernel32.dll")
		# advapi32=cdll.LoadLibrary("advapi32.dll")
	# except:
		# pass
else:
	raise NotImplementedError
# print _p;print advapi32

import Constants as C;c=C
C.advapi32=advapi32
from Constants import *

try:import win32gui
except Exception as ei:pass


gdAddressType={1: ['MIB_IPADDR_PRIMARY', 'Primary IP address', '主IP地址'],
 4: ['MIB_IPADDR_DYNAMIC', 'Dynamic IP address', '动态IP地址'],
 8: ['MIB_IPADDR_DISCONNECTED', 'Address is on disconnected interface', '断开连接的接口对应的IP地址'],
 64: ['MIB_IPADDR_DELETED', 'Address is being deleted', '删除的IP地址'],
 128: ['MIB_IPADDR_TRANSIENT', 'Transient address', '临时IP地址']}

def getAllNetworkInterfaces():
	'''['dwIndex','dwAddr', 'dwBCastAddr',  'dwMask', 'dwReasmSize', 'wType', 'unused1']
dwAddr
Type: DWORD
The IPv4 address in network byte order.
dwIndex
Type: DWORD
The index of the interface associated with this IPv4 address.
dwMask
Type: DWORD
The subnet mask for the IPv4 address in network byte order.
dwBCastAddr
Type: DWORD
The broadcast address in network byte order. A broadcast address is typically the IPv4 address with the host portion set to either all zeros or all ones.
The proper value for this member is not returned by the GetIpAddrTable function.
dwReasmSize
Type: DWORD
The maximum re-assembly size for received datagrams.
unused1
Type: unsigned short
This member is reserved.
wType
Type: unsigned short
The address type or state. This member can be a combination of the following values.
	适配器（Interface Card  ,  Adapter）
	网络接口控制器（英语：network interface controller，NIC），又称网络接口控制器，网络适配器（network adapter），网卡（network interface card）
	http://www.cnblogs.com/leftshine/p/5698732.html'''
	GetIpAddrTable = windll.iphlpapi.GetIpAddrTable
	GetIpAddrTable.argtypes = [
		ctypes.POINTER(MIB_IPADDRTABLE),
		ctypes.POINTER(ctypes.c_ulong),
		ctypes.wintypes.BOOL,
		]
	GetIpAddrTable.restype = DWORD
	table = MIB_IPADDRTABLE()
	size = ctypes.wintypes.ULONG(ctypes.sizeof(table))
	table.dwNumEntries = 0
	rk=['dwIndex','dwAddr', 'dwMask','wType', 'dwBCastAddr',   'dwReasmSize', 'unused1']
	GetIpAddrTable(ctypes.byref(table), ctypes.byref(size), 0)
	r=[]
	for i in rk:print i
	print table.dwNumEntries
	for n in range(table.dwNumEntries):
		row = table.table[n]
		rn=[]
		for i in rk:
			if i in('dwIndex','dwReasmSize'):
				rn.append(getattr(row,i))
			elif i=='wType':
				i=getattr(row,i)
				t=[]
				for j in sorted(gdAddressType.keys(),reverse=True):
					if j<=i:
						t.append(gdAddressType[j][0])
				rn.append(t)
			else:
				rn.append(str(getattr(row,i)))
		r.append(rn)
		
	# raise IndexError("interface index out of range")
		U.repl()
	return tuple(r)
getAllNetwork=getAllNetworkInterfaces

def getCmdHandle():
	return kernel32.GetConsoleWindow()
getcmdw=getCmdHandle
	
def getTitle(h=0,size=1024):
	'''h:window Handle'''
	if not h:h=getCmdHandle()
	title = ctypes.create_string_buffer(size)
	user32.GetWindowTextA(h,title,size)
	return title.value
getitle=getTitle
	
def setTitle(st,h=0):
	if type(st)!=str:st=str(st)
	if not h:h=getCmdHandle()
	return user32.SetWindowTextA(h,st)
setitle=setTitle

def EnumWindowsProc(hwnd, resultList):
	if win32gui.IsWindowVisible(hwnd) and getitle(hwnd) != '':
		resultList.append((hwnd, getitle(hwnd)))

def getAllWindows():
	mlst=[]
	win32gui.EnumWindows(EnumWindowsProc, mlst)
	# for handle in handles:
		# mlst.append(handle)
	return mlst
EnumWindows=getAllWindows
	
def setWindowPos(h=0,x=199,y=-21,width=999,height=786,top=None,flags=None):
	if not h:h=getCmdHandle()
	if not top:top=HWND_TOP
	if not flags:flags=SWP_SHOWWINDOW
	if top is True:top=HWND_TOPMOST
	return user32.SetWindowPos(h,top,x,y,width,height,flags)
setPos=setpos=setWPos=setWindowPos
	
def setOskPos(w=333,h=255,x=522,y=-21):
	flags=SWP_SHOWWINDOW
	if x<1 or y<-21:flags+=SWP_NOMOVE
	if w<30 or h <30:flags+=SWP_NOSIZE
	for i,k in getAllWindows():
		if k=='\xc6\xc1\xc4\xbb\xbc\xfc\xc5\xcc':
			setPos(i,width=w,height=h,x=x,y=y,flags=flags)
	
def msgbox(s='',st='title',*a):
	if(a!=()):s=str(s)+ ','+str(a)[1:-2]
	return user32.MessageBoxA(0, str(s), str(st), 0)		

def getCursorPos():
	from ctypes import Structure,c_ulong,byref
	class POINT(Structure):
		_fields_ = [("x", c_ulong), ("y", c_ulong)]
	pt = POINT()
	user32.GetCursorPos(byref(pt))
	return pt.x,pt.y		
getMousePos=getCursorPos

def CreateProcess(appName,cmd,):pass
# aa= 233
def getLastError(errCode=None,p=True):
	'''  need .decode('gb18030') '''
	from ctypes import c_void_p,create_string_buffer
	GetLastError = kernel32.GetLastError
	FormatMessage = kernel32.FormatMessageA
	LocalFree = kernel32.LocalFree
	
	FORMAT_MESSAGE_ALLOCATE_BUFFER = 0x00000100
	FORMAT_MESSAGE_FROM_SYSTEM = 0x00001000
	FORMAT_MESSAGE_IGNORE_INSERTS = 0x00000200

	try:
		msg = create_string_buffer(256)
		FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM,
						c_void_p(),
						2,
						0,
						msg,
						len(msg),
						c_void_p())
	except Exception as e:
		print e
	# return 233
	# from win32con import (
		# FORMAT_MESSAGE_FROM_SYSTEM,
		# FORMAT_MESSAGE_ALLOCATE_BUFFER,
		# FORMAT_MESSAGE_IGNORE_INSERTS)

	if errCode is None:
		errCode = GetLastError()
	print errCode
	message_buffer = ctypes.c_char_p()
	FormatMessage(
		FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_IGNORE_INSERTS,
		None,
		errCode,
		0,
		ctypes.byref(message_buffer),
		0,
		None
	)

	error_message = message_buffer.value
	LocalFree(message_buffer)

	r= '{} - {}'.format(errCode, error_message).decode('gb18030')#unicode
	# error_message = error_message.decode('cp1251').strip()
	if U.isipy():
		print r
	else:
		return r
geterr=getErr=getLastErr=getLastError
##############################################
gdWinVerNum={'10': 10.0,
			 '2000': 5.0,
			 '2003': 5.2,
			 '2008': 6.0,
			 '2008R2': 6.1,
			 '2012': 6.2,
			 '2012R2': 6.3,
			 '2016': 10.0,
			 '7': 6.1,
			 '8': 6.2,
			 '8.1': 6.3,
			 'vista': 6.0,
			 'xp': 5.1}
for w,i in gdWinVerNum.items():
	exec '''def is{0}():return getVersionNumber()=={1}'''.format(
		w.replace('.','_'),i)			 
			 
def getWinName():
	for w,i in gdWinVerNum.items():
		if i==getVersionNumber():
			return 'Windows '+w
	raise EnvironmentError('Unknown Windows VersionNumber',getVersionNumber())

name=systemName=getSysName=getWinName
def GetProcessImageFileName(pid=None):
	'''Windows XP or later
	Windows Server 2003 and Windows XP:  The handle must have the PROCESS_QUERY_INFORMATION access right.'''
	if not pid:pid=U.pid
	PROCESS_ALL_ACCESS = 0x001F0FFF
	# bInheritHandle [in]
# If this value is TRUE, processes created by this process will inherit the handle. Otherwise, the processes do not inherit this handle.
	hprocess=kernel32.OpenProcess(PROCESS_ALL_ACCESS,True,pid)
	dll=windll.psapi
	from ctypes import c_void_p,create_string_buffer
	im=256
	fn = create_string_buffer(im)
	if dll.GetProcessImageFileNameA(hprocess,fn,im)==0:
		return False
	else:
		fn= fn.value
		for d,v in getAllDisk().items():
			if fn.startswith(v):
				return fn.replace(v,d)
		return fn
getProcessPath=GetProcessImageFileName
gversionInfo=gVersionInfo=None
def getVersionInfo():
	global gVersionInfo
	if gVersionInfo:return gVersionInfo
	from Constants import DWORD,WCHAR
	class OSVersionInfo(ctypes.Structure):
		_fields_ = (('dwOSVersionInfoSize', DWORD),
					('dwMajorVersion', DWORD),
					('dwMinorVersion', DWORD),
					('dwBuildNumber', DWORD),
					('dwPlatformId', DWORD),
					('szCSDVersion', WCHAR * 128))

		def __init__(self, *args, **kwds):
			# super(OSVersionInfo, self).__init__(*args, **kwds)
			self.dwOSVersionInfoSize = ctypes.sizeof(self)
			kernel32.GetVersionExW(ctypes.byref(self))
	gVersionInfo=OSVersionInfo()
	return gVersionInfo
def getVersionNumber():
	v=getVersionInfo()
	return float('{0}.{1}'.format(v.dwMajorVersion,v.dwMinorVersion))
def getpid():
	return kernel32.GetCurrentProcessId()
def getAllDisk():
	'''return {'B:': '\\Device\\HarddiskVolumeRD',...'''
	r={}
	from ctypes import create_string_buffer
	im=256
	s=create_string_buffer(im)
	for i in [chr(i) for i in range(65,65+26)]:
		i=i+':'
		if 0==kernel32.QueryDosDeviceA(i,s,im):
			pass
		else:
			r[i]=s.value
		# if U.F.exist(i):r.append(i)
	return r
def main():
	print getAllNetwork()
	exit()
	import sys,os;sys.path.append('d:\pm');from qgb import U,T,F
	
	o=getVersionInfo()
	print o.dwMajorVersion,o.dwMinorVersion
	
	# CreateProcessWithLogonW(
	# lpUsername='qgb',
	# lpPassword='q',

	# lpApplicationName=r'C:\WINDOWS\system32\calc.exe')	
	print '[%s]'%getTitle(),getProcessPath(),U.getModPath()
	# U.msgbox()
	# U.repl()
# print 233
if __name__ == '__main__':main()