#coding=utf-8
__all__=['KeyCode','Constants','reg']
import sys,ctypes
try:
	if __name__.endswith('qgb.Win'):
		from .. import py
	else:
		import py
except Exception as ei:
	sys.path.append(sys.path[0][:-1-3])
	try:import py
	except:import pdb;pdb.set_trace()
	
try:from . import Constants
except:
	try:import Constants
	except Exception as ei:
		import pdb;pdb.set_trace()
#python G:\QGB\babun\cygwin\lib\python2.7\qgb\Win/__init__.py 	
#sys.path ['G:\\QGB\\babun\\cygwin\\lib\\python2.7\\qgb\\Win',
#sys.path ['G:\\QGB\\babun\\cygwin\\lib\\python2.7\\qgb'   can import py
# 	
	# py.pdb()
	# from . import Constants
globals().update([i for i in Constants.__dict__.items() if not i[0].startswith('__')])	
c=C=Constants

# from Constants import *
#if 'qgb.U' in sys.modules:U=sys.modules['qgb.U']
#elif 'U' in sys.modules:  U=sys.modules['U']
#else:
#	from sys import path as _p
#	# 'G:/QGB/babun/cygwin/lib/python2.7/qgb'
#	_p.insert(-1,_p[0][:-3-1])#-3-1  插入变倒数第二
#	# for i,v in enumerate(_p):  #这会导致 ImportError: No module named Constants
#		# if 'qgb' in v and 'Win' in v:
#			# _p.pop(i)
#	# U.pln( _p
#	try:from qgb import U
#	except:'#Err import U'

class WinDLL(ctypes.CDLL):
	"""This class represents a dll exporting functions using the
	Windows stdcall calling convention.
	"""
	_func_flags_ = 0
	
windll = ctypes.LibraryLoader(WinDLL)
	
if py.iswin() or py.iscyg():
	DWORD,WCHAR,LPSTR=C.DWORD,C.WCHAR,C.LPSTR
	User32=user32=windll.user32
	Kernel32= kernel32=windll.kernel32
	Advapi32= advapi32=windll.advapi32
	C.advapi32=advapi32
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
# U.pln( _p;U.pln( advapi32


try:
	from ctypes import wintypes
	import win32gui
except Exception as ei:pass
#############################################
def send_key_to_window_ctrl(h,c):
	import win32api,win32con
	CTRL_KEY=win32con.VK_LCONTROL
	S_KEY=py.ord(c.upper())
	
	
	# win32api.keybd_event(17,0,0,0)
	# win32gui.SendMessage(win, win32con.WM_KEYDOWN, 86, 0)
	win32api.PostMessage(h, win32con.WM_KEYDOWN, CTRL_KEY, 0);
	win32api.PostMessage(h, win32con.WM_KEYDOWN, S_KEY   , 0);
	# win32api.PostMessage(h, win32con.WM_KEYUP  , S_KEY   , 0);
	win32api.PostMessage(h, win32con.WM_KEYUP  , CTRL_KEY, 0); 
	
def send_key_to_window(h,*a):
	import win32api,win32con
	for i in a:
		if i.lower().startswith('ctrl+'):
			send_key_to_window_ctrl(h,i[5:])
		elif py.istr(i):
			for c in i:
				win32api.PostMessage(h, win32con.WM_CHAR, py.ord(c), 0)
		else:
			raise py.ArgumentUnsupported(i)
def shell_delete(a):
	''' allow undo
	
shellcon.FOF_ALLOWUNDO 删除失败 r'C:\WINDOWS\system32\cmd.exe'
弹框，阻塞，点击取消 ，返回 (1223, True)  1223 - 操作已被用户取消。
	
shellcon.FOF_ALLOWUNDO|shellcon.FOF_NO_UI 删除失败 r'C:\WINDOWS\system32\cmd.exe'
 (120, False)  120 - 这个系统不支持该功能。

 shellcon.FOF_ALLOWUNDO|shellcon.FOF_NO_UI 删除成功
 (0, False)  0 - 操作成功完成。

	'''
	from win32com.shell import shell, shellcon
	return shell.SHFileOperation((0, shellcon.FO_DELETE, a, None, shellcon.FOF_ALLOWUNDO ))
rmtree=delete=delete_dir=shell_delete_dir=shell_del=shell_delete

def get_monitor_resolution(multi_monitor_combined=False):
	import ctypes
	user32 = ctypes.windll.user32
	if multi_monitor_combined:
		return user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
	else:
		return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
get_screen_size=get_screen_resolution=get_monitor_resolution	

def change_file_time(file,time):
	'''
os.utime If times is not None, it must be a tuple (atime, mtime);
atime and mtime should be expressed as float seconds since the epoch.

'''
	import os
	r=os.utime(file,(time,time))#new_atime,new_mtime
	import win32_setctime
	return r,win32_setctime.setctime(file,time) # str,float
cf_time=file_time=set_file_time=change_file_time	
	
def set_window_transparency(hwnd,alpha=180):
	''' alpha:int byte 0-255
	'''
	import win32api,win32gui,win32con,winxpgui
	
	win32gui.SetWindowLong (hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (hwnd, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
	winxpgui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0), alpha, win32con.LWA_ALPHA)	
	return hwnd,alpha
window_transparent=set_transparent=set_window_transparent=set_window_transparency

def get_drive_letters_and_types():
	import os
	import win32api
	import win32file
	# os.system("cls")
	drive_types = {
					win32file.DRIVE_UNKNOWN : "Unknown\nDrive type can't be determined.",
					win32file.DRIVE_REMOVABLE : "Removable\nDrive has removable media. This includes all floppy drives and many other varieties of storage devices.",
					win32file.DRIVE_FIXED : "Fixed\nDrive has fixed (nonremovable) media. This includes all hard drives, including hard drives that are removable.",
					win32file.DRIVE_REMOTE : "Remote\nNetwork drives. This includes drives shared anywhere on a network.",
					win32file.DRIVE_CDROM : "CDROM\nDrive is a CD-ROM. No distinction is made between read-only and read/write CD-ROM drives.",
					win32file.DRIVE_RAMDISK : "RAMDisk\nDrive is a block of random access memory (RAM) on the local computer that behaves like a disk drive.",
					win32file.DRIVE_NO_ROOT_DIR : "The root directory does not exist."
				  }

	drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
	r=[]
	for device in drives:
		type = win32file.GetDriveType(device)
		r.append([device,type,drive_types[type],] )
		# print("Drive: %s" % device)
		# print(drive_types[type])
		# print("-"*72)
	return r


def get_text(h):
	import win32gui,win32con
	
	control = win32gui.FindWindowEx(h, 0, "static", None)
	return win32gui.GetWindowText(control)
	
	buf = " " * 255
	length = win32gui.SendMessage(h, win32con.WM_GETTEXT, 255, buf)
	return buf,length
	result = buf[:length]

def shell_copy(src, dest):
	"""
	Copy files and directories using Windows shell.

	:param src: Path or a list of paths to copy. Filename portion of a path
				(but not directory portion) can contain wildcards ``*`` and
				``?``.
	:param dst: destination directory.
	:returns: ``True`` if the operation completed successfully,
			  ``False`` if it was aborted by user (completed partially).
	:raises: ``WindowsError`` if anything went wrong. Typically, when source
			 file was not found.

	.. seealso:
		`SHFileperation on MSDN <http://msdn.microsoft.com/en-us/library/windows/desktop/bb762164(v=vs.85).aspx>`
	"""
	from win32com.shell import shell, shellcon
	U,T,N,F=py.importUTNF()
	if py.istr(src):  # in Py3 replace basestring with str
		src = F.abspath(src).replace('/','\\')
	else:  # iterable
		src = '\0'.join(F.abspath(path) for path in src)

	result, aborted = shell.SHFileOperation((
		0,
		shellcon.FO_COPY,
		src,
		F.abspath(dest).replace('/','\\'),
		shellcon.FOF_NOCONFIRMMKDIR,  # flags
		None,
		None))

	if not aborted and result != 0:
		# Note: raising a WindowsError with correct error code is quite
		# difficult due to SHFileOperation historical idiosyncrasies.
		# Therefore we simply pass a message.
		raise WindowsError('SHFileOperation failed: 0x%08x' % result)

	return not aborted	
copy=win32_shellcopy=shell_copy

def mkfifo(path):
	'''
os.mkfifo(path, mode=438, *, dir_fd=None)
Docstring:
Create a "fifo" (a POSIX named pipe).

If dir_fd is not None, it should be a file descriptor open to a directory,
  and path should be relative; path will then be relative to that directory.
dir_fd may not be implemented on your platform.
  If it is unavailable, using it will raise a NotImplementedError.
'''
	
	

def is_monitor_off():
	''' #TODO msg loop
只有这四种：
'MONITORINFOF_PRIMARY',
'MONITOR_DEFAULTTONEAREST',
'MONITOR_DEFAULTTONULL',
'MONITOR_DEFAULTTOPRIMARY',
 
 '''
	import win32gui,win32con,win32api
	hMonitor=win32api.MonitorFromPoint((0, 0), win32con.MONITOR_DEFAULTTOPRIMARY)
	
	return
	
def get_cursor_pos_color(x=None,y=None,**ka):
	''' x or y arg 优先
	
	return [x,y],color  '''
	U,T,N,F=py.importUTNF()
	
	if not py.isint(x) and y==None:
		pos=x
	if x==None or y==None:
		pos=U.get_duplicated_kargs(ka,'pos','xy')
		if not pos:
			pos=get_cursor_pos()
	else:
		pos=[x,y]
	pos=py.list(pos)
	if py.isint(x):pos[0]=x
	if py.isint(y):pos[1]=y
	
	import win32gui
	color=win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()),*pos)
	if color<256:color=256*256*color
	color=U.IntCustomRepr(color,repr=U.rgb_name(color))
	return pos,color
get_color=get_xy_color=get_cursor_pos_color

def run_as_user(cmd=r"notepad.exe C:\Windows\System32\drivers\etc\hosts",user=py.No('use current USER, no password window, privileg also can be elevated')):
	'''#带有 / -  的命令参数， 一定要三个引号。 三个以下都不行，示例：
Win.runAs('cmd """ /k ping 192.168.43.1"""') 
Win.runAs('python """-c input(233)""" ')  
Win.runAs('ssh-keygen ')  # 运行程序名中含有 - 没关系
Win.runAs('cmd """ -k echo 233 """') # -k 参数无效，只能/k
Win.runAs('cmd """ /k whoami """',user='administrator')

	user='Administrator' ,
'''
	if user:
		if not user.strip().startswith('-Credential '):
			user="-Credential '%s'"%user
	else:
		user='' # 不提供-Credential 参数，就好像右键 管理员运行一样，不要密码。是这个原因吗？
	ps=['powershell.exe',
# '-WindowStyle',
# 'Hidden',# 在外层使用这个会将调用的python cmd窗口一起隐藏 ，要像下面一样在内层

 '-ExecutionPolicy', 
 'Bypass',# 多参数不能写成一项，否则不允许使用与号(&)。& 运算符是为将来使用而保留的；请用双引号将与号引起来("&")，以将其作为字符串的一部分传递。: ParserError: (:) [], ParentContainsErrorRecordException

 '-command',
r"""& {Start-Process powershell.exe %(user)s -WindowStyle Hidden -ArgumentList 'Start-Process %(cmd)s -Verb runAs'} """ % py.locals()]
	U,T,N,F=py.importUTNF()
	return ps,U.cmd(ps)

	# import subprocess as sp
	# p = sp.Popen(['runas', '/noprofile', '/user:'+user.strip(), r"notepad.exe C:\Windows\System32\drivers\etc\hosts"],stdin=sp.PIPE)
	# p.stdin.write(b'0') #password
	# p.communicate()
npp_hosts=edit_hosts=runAs=powershell_run_as=run_as=runAsAdmin=run_as_admin=run_as_administrator=cmd_as_user=run_as_user
	
def test():
	import subprocess as sp
	p = sp.Popen([r'E:\QGB\Anaconda3\python.exe'],stdin=sp.PIPE)
	p.stdin.write(b'print(2333)') #password
	p.communicate()
	return p.pid
	
def ntHash(a):
	'''pip3 install passlib
	case sensitive'''
	from passlib.hash import nthash
	return nthash.hash(a).upper()
	
def lmHash(a):
	'''case Insensitive'''
	import hashlib,binascii
	hash = hashlib.new('md4', "1".encode('utf-16le')).digest()
	return binascii.hexlify(hash).decode('ascii').upper()
	
#######################################################################
class SYSTEM_POWER_STATUS(ctypes.Structure):
	_fields_ = [
		('ACLineStatus', wintypes.BYTE),
		('BatteryFlag', wintypes.BYTE),
		('BatteryLifePercent', wintypes.BYTE),
		('Reserved1', wintypes.BYTE),
		('BatteryLifeTime', wintypes.DWORD),
		('BatteryFullLifeTime', wintypes.DWORD),
	]
SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)
GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
GetSystemPowerStatus.restype = wintypes.BOOL
systemPowerStatus = SYSTEM_POWER_STATUS()

def batteryIsOn():
	if not GetSystemPowerStatus(ctypes.pointer(systemPowerStatus)):
		raise ctypes.WinError()
	return systemPowerStatus.ACLineStatus == 0
	
def batteryPercent():
	if not GetSystemPowerStatus(ctypes.pointer(systemPowerStatus)):
		raise ctypes.WinError()
	return systemPowerStatus.BatteryLifePercent

def batteryFlag():
	if not GetSystemPowerStatus(ctypes.pointer(systemPowerStatus)):
		raise ctypes.WinError()
	return systemPowerStatus.BatteryFlag
#########################################################################

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
	U=py.importU()
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
	# for i in rk:U.pln( i)
	U.pln('Interface count:', table.dwNumEntries)
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
		# U.repl()
	return tuple(r)
getAllNetwork=getAllNetworkInterfaces

def CommandLineToArgvW(cmd):
	import ctypes
	if py.is2():
		cmd=py.unicode(cmd)
	nargs = ctypes.c_int()
	ctypes.windll.shell32.CommandLineToArgvW.restype = ctypes.POINTER(ctypes.c_wchar_p)
	lpargs = ctypes.windll.shell32.CommandLineToArgvW(cmd, ctypes.byref(nargs))
	args = [lpargs[i] for i in range(nargs.value)]
	if ctypes.windll.kernel32.LocalFree(lpargs):
		raise AssertionError
	return args
splitCmd=split_cmd=cmdSplit=cmd_split=shlex_split=split_cmd_str=CommandLineToArgvW

def GetConsoleWindow():
	return kernel32.GetConsoleWindow()
get_current_cmd_windows=getcmdw=getCmdHandle=GetConsoleWindow
	
def getCmdLine(bytes=False):
	'''------> k.GetCommandLineW()
Out[9]: 'G'
	'''
	if bytes:
		kernel32.GetCommandLineA.restype=LPSTR
		b= kernel32.GetCommandLineA()
		return b
	else:
		kernel32.GetCommandLineW.restype=ctypes.wintypes.LPCWSTR
		s=kernel32.GetCommandLineW()
		return s
get_cmd=get_cmdline=get_command_line=GetCommandLine=getCmd=getCmdLine
	
def get_title(h=0,size=1024):
	'''h:window Handle'''
	if not h:h=getCmdHandle()
	if py.is2():
		# size= user32.GetWindowTextLengthA(h) + 1  # always =2 in py3?
		title = ctypes.create_string_buffer(size)
		user32.GetWindowTextA(h,title,size)
	else:
		length = user32.GetWindowTextLengthW(h) + 1
		title = ctypes.create_unicode_buffer(length)
		user32.GetWindowTextW(h, title, length)
	return title.value
getitle=getTitle=get_title
	
def set_title(title,h=0):
	'''在python内设置的，退出后 会还原  
	py3 : SetWindowTextW
'''
	if not py.istr(title):title=py.str(title)
	if not h:h=getCmdHandle()
	if py.is3():
		return user32.SetWindowTextW(h,title)
	else:
		return user32.SetWindowTextA(h,title)
setitle=settitle=setTitle=set_title

def EnumWindowsProc(hwnd, resultList):
	if win32gui.IsWindowVisible(hwnd) and getitle(hwnd) != '':
		resultList.append((hwnd, getitle(hwnd)))

def getAllWindows():
	'''  return [ [h,title,pid] ,...]
	'''
	mlst=[]
	win32gui.EnumWindows(EnumWindowsProc, mlst)
	# for handle in handles:
		# mlst.append(handle)
	if py.is2():
		return [(i[0],i[1].decode('mbcs'),get_pid_by_hwnd(i[0])) for i in mlst]
	else:
		return [(i[0],i[1] ,get_pid_by_hwnd(i[0])) for i in mlst]
EnumWindows=get_all_windows=getAllWindow=getAllWindows

def SetForegroundWindow(title=None,handle=None,pid=None,process_name='',raise_error=0,retry=99,**ka):
	U,T,N,F=py.importUTNF()
	if py.isint(title) and not handle:
		handle,title=title,''
	if not title:title=U.get_duplicated_kargs(ka,'t',)
	if not handle:handle=U.get_duplicated_kargs(ka,'hwnd','h')
	if not process_name:process_name=U.get_duplicated_kargs(ka,'name','pn','process')
	no_raise=U.get_duplicated_kargs(ka,'no_raise','noRaise','no_raise_err',default=not raise_error)
	raise_error=(not no_raise) or U.get_duplicated_kargs(ka,'err','error','exp','exception','Exception',
'raise_err','raise_error','raiseError','raiseErr','raise_EnvironmentError','EnvironmentError','raiseEnvironmentError',default=raise_error)

	if not handle and not title and not pid and not process_name:
		handle=get_current_cmd_windows()
	if not handle:
		from qgb import Win
		for h,t,p in Win.getAllWindows():
			if t==title or p==pid:
				handle=h;break
			if process_name and process_name==U.get_process_name_by_pid(p):
				handle=h;break
		else:
			if (not title) and (not process_name):raise py.ArgumentError(py.locals())
			for h,t,p in Win.getAllWindows():
				if title and title in t:
					handle=h;break
				if process_name and process_name in U.get_process_name_by_pid(p):
					handle=h;break
			else:
				if raise_error:raise py.EnvironmentError('cannot find ForegroundWindow title : '+a)
		# if py.isint(title):
			# handle=title		
	# else:
		# raise py.ArgumentError('foreground,a',row)
	import win32gui
	# if not win32gui.IsWindowVisible(handle): #先不考虑
		
	try:
		# win32gui.SetForegroundWindow(handle)
		import win32gui, win32com.client,win32con,pythoncom
		pythoncom.CoInitialize()#加上这句解决 #pywintypes.com_error: (-2147221008, '尚未调用 CoInitialize。', None, None)
		shell=win32com.client.Dispatch("WScript.Shell")
		shell.SendKeys('%')##For ALT   prefix with %
		win32gui.ShowWindow(handle,win32con.SW_SHOW)
		win32gui.SetForegroundWindow(handle)
	except Exception as e:
#BUG 窗口在后台，通过 http_rpc 调用此函数，第一次总会出错：，第二次才成功？
# error(0, 'SetForegroundWindow', 'No error message is available')
		if 'No error message is available' in repr(e):
			for i in py.range(1,retry):
				try:
					if i%9==1:U.sleep(0.01) # sleep一下有奇效，为什么？
					win32gui.SetForegroundWindow(handle)
					return U.IntCustomRepr(handle,repr='Win.set_foreground(%r) #retry:%s'% (handle,i) )
				except:
					pass
			# return py.No(e,'')
		if raise_error:raise
		return py.No(e)
		
	return U.IntCustomRepr(handle,repr='Win.set_foreground(%r)'%handle)
#U.system_actions
fg=forw=popw=pop_window=forground=foreground=set_forground=pop_top=set_foreground=SetForegroundWindow
	
def get_pid_by_hwnd(hwnd):
	try:
		import win32process
		threadid,pid = win32process.GetWindowThreadProcessId(hwnd)
	except Exception as e:
		pid=py.No(e)
	return pid
getPidByHandle=get_pid_by_handle=get_pid_by_hwnd
	
def getWindowHandleByTitle(title):
	for i in getAllWindows():
		if title in i[1]:
			return i[0]
	return py.No('not found window title',title)
getw=getWindow=getWindowHandleByTitle

def getWindowByProcessName(name):
	'''  return [ [h,title,pid] ,...]
	'''
	U=py.importU()
	r=[]
	ws=getAllWindows()
	for p in U.ps(name=name):
		for i in ws:
			if i[2]==p.pid:
				r.append(i)
	return r

def getWindowPos(h=0):
	'''rect : x,y,right,bottom '''
	if not h:h=getCmdHandle()#TODO current on top window
	import win32gui
	return win32gui.GetWindowRect(h)
getPos=getpos=getWPos=getWindowPos	

def getWindowSize(h):
	import win32gui
	r=win32gui.GetWindowRect(h)
	return (r[2]-r[0],r[3]-r[1])
getwh=getsize=getSize=getWSize=getWindowSize

def is_window_topmost(handle):
	''' return 0(NOT_TOP) else 8(TOP) '''
	import win32gui,win32con
	return (win32gui.GetWindowLong(handle, win32con.GWL_EXSTYLE) & win32con.WS_EX_TOPMOST)

def setWindowPos(hwnd=0,x=0,y=0,w=0,h=0,rect=(),top=None,flags=None):
	'''if not flags:flags=SWP_SHOWWINDOW  # 无论是否top，是否拥有焦点，默认显示此窗口
	'''
	if not hwnd:
		hwnd=getCmdHandle()
		# if x==y==w==h==0 and not rect:
			# x,y,w,h=(199,-21,999,786)
	if not rect:
		rect=getWindowPos(hwnd)
	if not x:x=rect[0]
	if not y:y=rect[1]
	if not w:w=rect[2]-rect[0]
	if not h:h=rect[3]-rect[1]
	if top:top=HWND_TOPMOST
	else:  top=HWND_NOTOPMOST  #-2
	if not flags:flags=SWP_SHOWWINDOW  # 无论是否top，是否拥有焦点，默认显示此窗口
		
	if user32.SetWindowPos(hwnd,top,x,y,w,h,flags):#1
		return hwnd
	else:return py.No(getLastError())
setPos=setpos=setWPos=set_window_pos=setWindowPos
	
def setOskPos(w=333,h=255,x=522,y=-21):
	flags=SWP_SHOWWINDOW
	if x<1 or y<-21:flags+=SWP_NOMOVE
	if w<30 or h <30:flags+=SWP_NOSIZE
	for i,k in getAllWindows():
		if k=='\xc6\xc1\xc4\xbb\xbc\xfc\xc5\xcc':
			setPos(i,width=w,height=h,x=x,y=y,flags=flags)
	
	
def msgbox(s='',st='title',*a):
	'''
__import__('ctypes').windll.user32.MessageBoxW(0, 'text', 'title', 0)	
	
	'''
	if(a):
		a=py.list(a)
		a.insert(0,s)
		a.insert(1,st)
		st='length %s'%len(a)
		s=str(a)
	# s=str(s)+ ','+str(a)#[1:-2]
	if py.is2():
		return user32.MessageBoxA(0, str(s), str(st), 0)		
	else:
		return user32.MessageBoxW(0, str(s), str(st), 0)		

def mouse_drag(x,y,x2=0,y2=0,time=1.1):
	import pyautogui
	U=py.importU()
	if U.len(x)==2:
		if U.len(y)==2:
			if x2 or y2:
				raise py.ArgumentError('duplicated x2,y2',x2,y2)
			x2,y2=y
		x,y=x
	pyautogui.moveTo(x, y)
	pyautogui.mouseDown(button='left')
	pyautogui.dragTo(x2, y2, 1, button='left')
	U.sleep(time)
	pyautogui.mouseUp(button='left')	
drag=mouse_drag	
		
def get_cursor_pos():
	from ctypes import Structure,byref,c_long# c_ulong 无符号 在第二屏 负数坐标得到(1831, 4294967041)，不能用于 win32api.SetCursorPos((x,y))
	class POINT(Structure):
		_fields_ = [("x", c_long), ("y", c_long)]
	pt = POINT()
	user32.GetCursorPos(byref(pt))
	return pt.x,pt.y		
getMousePos=GetCursorPos=getCurPos=getCursorPos=get_cur_pos=get_cursor_pos

def set_cursor_pos(x,y):
	x,y=py.int(x),py.int(y)
	user32.SetCursorPos(x,y)
	return x,y
move_cur=mv_cur=setMousePos=setCursorPos=SetCursorPos=setCurPos=set_mouse_pos=set_cur_pos=set_cursor_pos

def mouse_click(x=None,y=None,*a,_1=False,debug=0):
	''' click(*xy+(2,3)) == click(x,y,2,3) == click(x+2,y+3)
	'''
	import win32api, win32con
	if not x and not py.isint(x):x=get_cursor_pos()[0]
	if not y and not py.isint(y):y=get_cursor_pos()[1]
	x,y=py.int(x),py.int(y)
	if not _1:
		if x==-1 or y==-1:
			U=py.importU()
			return x,U.IntRepr(y,repr='%s # -1 not click! #'%y)
			
	if a:
		if py.len(a)!=2:raise py.ArgumentError('a must be 2 int tuple')
		x=x+a[0]
		y=y+a[1]
	if debug:print(x,y)
	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
	return py.importU().object_custom_repr( (x,y) ,repr='Win.click({0},{1})'.format(x,y))
ck=click=mouse_click	
# click(10,10)
######################
def mouse_event(x,y,event=0,abs=True,move=True):
	'''
	x,y int :depand abs (Don't input base 65535)
	x,y float 0-1.0:  rel screen x
	
	abs False:从上一次鼠标位置移动
	Win.mouse_event(0,0)  没有反应？
	Return value

	This function has no return value.
	Remarks

	dwData>0 scroll up
	<0  down

If the mouse has moved, indicated by MOUSEEVENTF_MOVE being set, dx and dy hold information about that motion. The information is specified as absolute or relative integer values.
If MOUSEEVENTF_ABSOLUTE value is specified, dx and dy contain normalized absolute coordinates between 0 and 65,535. The event procedure maps these coordinates onto the display surface. Coordinate (0,0) maps onto the upper-left corner of the display surface, (65535,65535) maps onto the lower-right corner.

If the MOUSEEVENTF_ABSOLUTE value is not specified, dx and dy specify relative motions from when the last mouse event was generated (the last reported position). Positive values mean the mouse moved right (or down); negative values mean the mouse moved left (or up).	
=======================================
	MOUSEEVENTF_ABSOLUTE
0x8000
The dx and dy parameters contain normalized absolute coordinates. If not set, those parameters contain relative data: the change in position since the last reported position. This flag can be set, or not set, regardless of what kind of mouse or mouse-like device, if any, is connected to the system. For further information about relative mouse motion, see the following Remarks section.
MOUSEEVENTF_LEFTDOWN
0x0002
The left button is down.

x,y useless?  |MOUSE_MOVE
Win.mouse_event(90,90,2|1,False)#x,y 无用
Win.mouse_event(90,90,2|1,True)#有用，并立即返回

Win.mouse_event(65536,65536,0)
-------> Win.getCursorPos()
Out[76]: (1365L, 767L)

	'''
	
	
	W,H=getScreenSize()
	
	if type(x) is float :
		if abs:x=int(65535*x);y=int(65535*y)
		else:x=int(W*x);y=int(H*y)
	else:
		if abs:
			x=float(x)/W;	y=float(y)/H
			x=int(65535*x);y=int(65535*y)
	dwData=0
		
	if abs:	event=event|mouse_event.ABSOLUTE
	if move:event=event|mouse_event.MOVE  #2|1|1|1== 3
	# if WHEEL&event:
	if mouse_event.WDOWN&event:dwData=-9;event|=mouse_event.WHEEL
	if mouse_event.WUP&event:dwData=9;event|=mouse_event.WHEEL
	
	
	User32.mouse_event.argtypes=[DWORD,
								 DWORD,
								 DWORD,
								 DWORD,
								 ctypes.wintypes.c_void_p]#ULONG_PTR	
	U=py.importU()
	if U.debug():U.pln(event,x,y,dwData,None)
	User32.mouse_event(event,x,y,dwData,None)
mouse_event.ABSOLUTE = 0x8000
mouse_event.HWHEEL = 0x01000
mouse_event.LEFTDOWN = 0x0002
mouse_event.LEFTUP = 0x0004
mouse_event.MIDDLEDOWN = 0x0020
mouse_event.MIDDLEUP = 0x0040
mouse_event.MOVE = 0x0001
mouse_event.MOVE_NOCOALESCE = 0x2000
mouse_event.RIGHTDOWN = 0x0008
mouse_event.RIGHTUP = 0x0010
mouse_event.VIRTUALDESK = 0x4000
mouse_event.WHEEL = 0x0800
mouse_event.XDOWN = 0x0080
mouse_event.XUP = 0x0100
mouse_event.WDOWN=0x200
mouse_event.WUP=0x400
mouse_event.RC=mouse_event.RIGHTDOWN|mouse_event.RIGHTUP
mouse_event.LC=mouse_event.LEFTDOWN|mouse_event.LEFTUP
	
def getScreenSize():
	return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
	
def CreateProcess(appName,cmd,):pass
# aa= 233
def getLastError(errCode=None,p=True):
	'''  need .decode('gb18030') '''
	U=py.importU()
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
		U.pln( e)
	# return 233
	# from win32con import (
		# FORMAT_MESSAGE_FROM_SYSTEM,
		# FORMAT_MESSAGE_ALLOCATE_BUFFER,
		# FORMAT_MESSAGE_IGNORE_INSERTS)

	if errCode is None:
		errCode = GetLastError()
	U.pln( errCode)
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
	
	r= '{} - {}'.format(errCode, error_message.decode('mbcs'))#unicode
	# if py.is2():
	# else:       r= '{} - {}'.format(errCode, error_message)
	# error_message = error_message.decode('cp1251').strip()
	if U.isipy() and not U.DEBUG:#TODO  如果修改了repr 方式  可以去除这个
		U.pln( r)
	else:
		return r
error_code=lastError=geterr=getErr=getLastErr=getLastError
##############################################
gdWinVerNum={'10':10.0,
			 '7': 6.1,
			 '8': 6.2,
			 '8.1': 6.3,
			 'vista': 6.0,
			 'xp': 5.1,# 6.2,#使用 GetVersionExW  # 桌面系统优先
			 '2000': 5.0,
			 '2003': 5.2,
			 '2008': 6.0,
			 '2008R2': 6.1,
			 '2012': 6.2,
			 '2012R2': 6.3,
			 '2016': 10.0}
for w,i in gdWinVerNum.items():
	py.execute('''def is{0}():return getVersionNumberCmdVer()=={1}'''.format(
		w.replace('.','_'),i)    )			 
			 
def getWinName():
	for w,i in gdWinVerNum.items():
		if i==getVersionNumber():
			return 'Windows '+w
	raise EnvironmentError('Unknown Windows VersionNumber',getVersionNumber())

name=systemName=getSysName=getWinName
def GetProcessImageFileName(pid=None):
	'''if pid ignore Process name
	Windows XP or later
	Windows Server 2003 and Windows XP:  The handle must have the PROCESS_QUERY_INFORMATION access right.'''
	if not pid:
		U=py.importU()
		pid=U.pid
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
	# from Constants import DWORD,WCHAR
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
def getVersionNumberCmdVer():
	'''
Microsoft Windows [版本 10.0.16299.125]
Microsoft Windows [版本 6.1.7601]
Microsoft Windows XP [版本 5.1.2600]
	'''
	U=py.importU()
	import subprocess as sb
	T=U.T
	r=sb.Popen('cmd.exe /c ver',stdout=sb.PIPE)
	r=r.stdout.read(-1)
	r=T.subLast(r,' ',']')
	r=r.split('.')
	if len(r)<3:raise Exception('cmd ver ',r)
	major,minor,build=r[:3]
	return float('{0}.{1}'.format(major,minor))
	
def getVersionNumber():
	'''TODO 实现有问题  在win10下为 6.2
	
	
In [3]: Win.getVersionNumber
------> Win.getVersionNumber()
Out[3]: 6.1

In [4]: Win.is7
------> Win.is7()
Out[4]: True
	
	'''	
	# return getVersionNumberCmdVer()
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
	U=py.importU()
	py.pdb()
	# U=globals()['U']#  为何在此不能自动引用 globals
	import U
	U.pln( getAllNetwork())
	exit()
	import sys,os;sys.path.append('d:\pm');from qgb import U,T,F
	
	o=getVersionInfo()
	U.pln( o.dwMajorVersion,o.dwMinorVersion)
	
	# CreateProcessWithLogonW(
	# lpUsername='qgb',
	# lpPassword='q',

	# lpApplicationName=r'C:\WINDOWS\system32\calc.exe')	
	U.pln( '[%s]'%getTitle(),getProcessPath(),U.getModPath())
	# U.msgbox()
	# U.repl()
# U.pln( 233
if __name__ == '__main__':main()