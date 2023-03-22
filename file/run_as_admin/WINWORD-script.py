#!c:\QGB\Anaconda3\python.exe
import sys, os, traceback, types
ps=os.environ['PATH'].split(os.pathsep)
ps.extend(['c:/QGB/Anaconda3/',
 'c:/QGB/Anaconda3/Library/mingw-w64/bin',
 'c:/QGB/Anaconda3/Library/usr/bin',
 'c:/QGB/Anaconda3/Library/bin',
 'c:/QGB/Anaconda3/Scripts',
 'c:/QGB/Anaconda3/lib/site-packages/numpy/.libs'])
os.environ['PATH']=os.pathsep.join(ps)

def runAsAdmin(cmdLine, wait=True):
	if os.name != 'nt':
		raise RuntimeError("This function is only implemented on Windows.")

	import win32api, win32con, win32event, win32process
	from win32com.shell.shell import ShellExecuteEx
	from win32com.shell import shellcon

	python_exe = sys.executable
	# elif type(cmdLine) not in (types.TupleType,types.ListType):
		# raise ValueError("cmdLine is not a sequence.")
	cmd = '"%s"' % (cmdLine[0],)
	# XXX TODO: isn't there a function or something we can call to massage command line params?
	params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
	cmdDir = ''
	showCmd = win32con.SW_SHOWNORMAL
	#showCmd = win32con.SW_HIDE
	lpVerb = 'runas'  # causes UAC elevation prompt
	procInfo = ShellExecuteEx(nShow=showCmd,
							  fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
							  lpVerb=lpVerb,
							  lpFile=cmd,
							  lpParameters=params)

	if wait:
		procHandle = procInfo['hProcess']
		obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
		rc = win32process.GetExitCodeProcess(procHandle)
		#print("Process handle %s returned code %s" % (procHandle, rc))
	else:
		rc = None
	return rc

import pathlib
p=pathlib.Path(__file__)
spath=p.parent.absolute().__str__()	
	
from threading import Thread
import time

if __name__ == "__main__":
	# import pdb;pdb.set_trace()
	# sys.exit(runAsAdmin(['notepad',r'C:\Windows\System32\drivers\etc\hosts']))
	a=[r'C:\QGB\software\Office2007\WINWORD.EXE',*sys.argv[1:]]
	print(sys.argv,a)
	t=Thread(target=runAsAdmin,args=(a,),)
	t.start()
	time.sleep(1)
	# os.system('pause')
	os._exit(0)