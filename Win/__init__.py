# from sys import path as _p;_p.insert(0,_p[0][:-4])
import sys,ctypes
try:
	U=sys.modules['qgb.U']
except:
	U=sys.modules['U']

if U.iswin():
	from ctypes import windll
	user32=windll.user32
	kernel32=windll.kernel32
	advapi32=windll.advapi32
else:#Not Win
	raise NotImplementedError
	# if U.iscyg():
	
	try:
		from ctypes import cdll
		user32=cdll.LoadLibrary("user32.dll")
		kernel32=cdll.LoadLibrary("kernel32.dll")
		advapi32=cdll.LoadLibrary("advapi32.dll")
	except:
		pass
# print _p;print advapi32

import Constants as C;c=C
C.advapi32=advapi32
from Constants import *

try:import win32gui
except Exception as ei:pass

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
	if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
		resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

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
	class POINT(Structure):
		_fields_ = [("x", c_ulong), ("y", c_ulong)]
	pt = POINT()
	user32.GetCursorPos(byref(pt))
	return pt.x,pt.y		
getMousePos=getCursorPos

def CreateProcess(appName,cmd,):pass

def getLastError(errCode=None,p=True):

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
	return 233
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

	error_message = error_message.decode('cp1251').strip()
	return '{} - {}'.format(errCode, error_message)
geterr=getErr=getLastErr=getLastError
##############################################
def main():
	import sys,os;sys.path.append('d:\pm');from qgb import U,T,F
	# CreateProcessWithLogonW(lpUsername='qgb',
	# lpPassword='q',

	# lpApplicationName=r'C:\WINDOWS\system32\calc.exe')	
	print '[%s]'%getTitle()
	# U.repl()
	# U.pprint(getAllWindows())
if __name__ == '__main__':main()