from ctypes import windll
import ctypes

def getCmdHandle():
	return windll.kernel32.GetConsoleWindow()

def getTitle(h=0,size=1024):
	'''h:window Handle'''
	if not h:h=getCmdHandle()
	title = ctypes.create_string_buffer(size)
	ctypes.windll.user32.GetWindowTextA(h,title,size)
	return title.value
getitle=getTitle
	
def setTitle(st,h=0):
	if type(st)!=str:st=str(st)
	if not h:h=getCmdHandle()
	return windll.user32.SetWindowTextA(h,st)
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
	
	
	
	
if __name__ == '__main__':
	import sys,os;sys.path.append('d:\pm');from qgb import *
		
	print '[%s]'%getTitle()
	# U.repl()
	# U.pprint(getAllWindows())