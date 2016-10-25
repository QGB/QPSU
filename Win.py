import win32gui

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
		
		
	U.repl()
	U.pprint(getAllWindows())