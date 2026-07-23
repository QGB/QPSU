import sys,ctypes
try:from .. import py
except:
	try:import py
	except Exception as ei:
		import pdb;pdb.set_trace()
	
# try:
	# if __name__.endswith('Constants'):
		# from .. import py
	# else:import py
# except Exception as ei:
	# import pdb;pdb.set_trace()

if py.iswin():
	from ctypes.wintypes import WORD, DWORD, LPSTR, HANDLE,WCHAR
if py.iscyg():
	WORD	= ctypes.c_ushort
	DWORD  = ctypes.c_uint
	LPSTR  = ctypes.c_char_p
	LPBYTE = LPSTR
	HANDLE = DWORD
	WCHAR = ctypes.c_wchar
NULL  = 0
TRUE  = 1
FALSE = 0
INVALID_HANDLE_VALUE = -1
##################################
MAX_INTERFACES = 10
class IPAddr(ctypes.Structure):
	_fields_ = [("S_addr", ctypes.c_ulong)]

	def __str__(self):
		import socket,struct
		return socket.inet_ntoa(struct.pack("L", self.S_addr))
class MIB_IPADDRROW(ctypes.Structure):
	_fields_ = [("dwAddr", IPAddr),
				("dwIndex", DWORD),
				("dwMask", DWORD),
				("dwBCastAddr", IPAddr),
				("dwReasmSize", DWORD),
				("unused1", ctypes.c_ushort),
				("wType", ctypes.c_ushort),
				]
class MIB_IPADDRTABLE(ctypes.Structure):
	_fields_ = [("dwNumEntries", DWORD),
				("table", MIB_IPADDRROW * MAX_INTERFACES)]

# typedef struct _PROCESS_INFORMATION {
#	 HANDLE hProcess;
#	 HANDLE hThread;
#	 DWORD dwProcessId;
#	 DWORD dwThreadId;
# } PROCESS_INFORMATION, *PPROCESS_INFORMATION, *LPPROCESS_INFORMATION;
class PROCESS_INFORMATION(ctypes.Structure):
	#_pack_	= 1
	_fields_ = [
		('hProcess',	HANDLE),
		('hThread',	 HANDLE),
		('dwProcessId', DWORD),
		('dwThreadId',  DWORD),
	]

# typedef struct _STARTUPINFO {
#	 DWORD	cb;
#	 LPSTR	lpReserved;
#	 LPSTR	lpDesktop;
#	 LPSTR	lpTitle;
#	 DWORD	dwX;
#	 DWORD	dwY;
#	 DWORD	dwXSize;
#	 DWORD	dwYSize;
#	 DWORD	dwXCountChars;
#	 DWORD	dwYCountChars;
#	 DWORD	dwFillAttribute;
#	 DWORD	dwFlags;
#	 WORD	wShowWindow;
#	 WORD	cbReserved2;
#	 LPBYTE  lpReserved2;
#	 HANDLE  hStdInput;
#	 HANDLE  hStdOutput;
#	 HANDLE  hStdError;
# } STARTUPINFO, *LPSTARTUPINFO;
class STARTUPINFO(ctypes.Structure):
	#_pack_	= 1
	_fields_ = [
		('cb',				 DWORD),
		('lpReserved',		DWORD),	 # LPSTR
		('lpDesktop',		LPSTR),
		('lpTitle',			ctypes.c_wchar_p), #dans la version original LPSTR mais ne marche pas
		('dwX',				DWORD),
		('dwY',				DWORD),
		('dwXSize',			DWORD),
		('dwYSize',			DWORD),
		('dwXCountChars',	DWORD),
		('dwYCountChars',	DWORD),
		('dwFillAttribute', DWORD),
		('dwFlags',			DWORD),
		('wShowWindow',	 WORD),
		('cbReserved2',	 WORD),
		('lpReserved2',	 DWORD),	 # LPBYTE
		('hStdInput',		DWORD),
		('hStdOutput',		DWORD),
		('hStdError',		DWORD),
	]

# BOOL WINAPI CreateProcessWithLogonW(
#	__in			LPCWSTR lpUsername,
#	__in_opt	 LPCWSTR lpDomain,
#	__in			LPCWSTR lpPassword,
#	__in			DWORD dwLogonFlags,
#	__in_opt	 LPCWSTR lpApplicationName,
#	__inout_opt  LPWSTR lpCommandLine,
#	__in			DWORD dwCreationFlags,
#	__in_opt	 LPVOID lpEnvironment,
#	__in_opt	 LPCWSTR lpCurrentDirectory,
#	__in			LPSTARTUPINFOW lpStartupInfo,
#	__out		 LPPROCESS_INFORMATION lpProcessInfo
# );
def CreateProcessWithLogonW(lpUsername = None, lpDomain = None, lpPassword =
None, dwLogonFlags = 0, lpApplicationName = None, lpCommandLine = None,
dwCreationFlags = 0, lpEnvironment = None, lpCurrentDirectory = None,
lpStartupInfo = None):
	if not lpUsername:
		lpUsername			= NULL
	else:
		lpUsername			= ctypes.c_wchar_p(lpUsername)
	if not lpDomain:
		lpDomain				= NULL
	else:
		lpDomain				= ctypes.c_wchar_p(lpDomain)
	if not lpPassword:
		lpPassword			= NULL
	else:
		lpPassword			= ctypes.c_wchar_p(lpPassword)
	if not lpApplicationName:
		lpApplicationName	= NULL
	else:
		lpApplicationName	= ctypes.c_wchar_p(lpApplicationName)
	if not lpCommandLine:
		lpCommandLine		= ctypes.c_int(NULL)
	else:
		lpCommandLine		= ctypes.create_unicode_buffer(lpCommandLine)
	if not lpEnvironment:
		lpEnvironment		= NULL
	else:
		lpEnvironment		= ctypes.c_wchar_p(lpEnvironment)
	if not lpCurrentDirectory:
		lpCurrentDirectory  = NULL
	else:
		lpCurrentDirectory  = ctypes.c_wchar_p(lpCurrentDirectory)
	if not lpStartupInfo:
		lpStartupInfo				 = STARTUPINFO()
		lpStartupInfo.cb			 = ctypes.sizeof(STARTUPINFO)
		lpStartupInfo.lpReserved	= 0
		lpStartupInfo.lpDesktop	= 0
		lpStartupInfo.lpTitle		= 0
		lpStartupInfo.dwFlags		= 0
		lpStartupInfo.cbReserved2  = 0
		lpStartupInfo.lpReserved2  = 0
	lpProcessInformation				 = PROCESS_INFORMATION()
	lpProcessInformation.hProcess	 = INVALID_HANDLE_VALUE
	lpProcessInformation.hThread		= INVALID_HANDLE_VALUE
	lpProcessInformation.dwProcessId  = 0
	lpProcessInformation.dwThreadId	= 0
	success = advapi32.CreateProcessWithLogonW(lpUsername,
lpDomain, lpPassword, dwLogonFlags, lpApplicationName,
ctypes.byref(lpCommandLine), dwCreationFlags, lpEnvironment,
lpCurrentDirectory, ctypes.byref(lpStartupInfo),
ctypes.byref(lpProcessInformation))
	if success == FALSE:
		raise ctypes.WinError()
	return lpProcessInformation

######### Windows Constants ##########
ABE_BOTTOM=3
ABE_LEFT=0
ABE_RIGHT=2
ABE_TOP=1
ABM_ACTIVATE=0x00000006
ABM_GETAUTOHIDEBAR=0x00000007
ABM_GETSTATE=0x00000004
ABM_GETTASKBARPOS=0x00000005
ABM_NEW=0x00000000
ABM_QUERYPOS=0x00000002
ABM_REMOVE=0x00000001
ABM_SETAUTOHIDEBAR=0x00000008
ABM_SETPOS=0x00000003
ABM_WINDOWPOSCHANGED=0x0000009
ABN_FULLSCREENAPP=0x0000002
ABN_POSCHANGED=0x0000001
ABN_STATECHANGE=0x0000000
ABN_WINDOWARRANGE=0x0000003
ABS_ALWAYSONTOP=0x0000002
ABS_AUTOHIDE=0x0000001
AW_ACTIVATE=0x00020000
AW_BLEND=0x00080000
AW_CENTER=0x00000010
AW_HIDE=0x00010000
AW_HOR_NEGATIVE=0x00000002
AW_HOR_POSITIVE=0x00000001
AW_SLIDE=0x00040000
AW_VER_NEGATIVE=0x00000008
AW_VER_POSITIVE=0x00000004
GWL_EXSTYLE=-20
GWL_STYLE=-16
GWL_WNDPROC=-4
HTBORDER=18
HTBOTTOM=15
HTBOTTOMLEFT=16
HTBOTTOMRIGHT=17
HTCAPTION=2
HTCLIENT=1
HTGROWBOX=4
HTHSCROLL=6
HTLEFT=10
HTMAXBUTTON=9
HTMENU=5
HTMINBUTTON=8
HTNOWHERE=0
HTREDUCE=HTMINBUTTON
HTRIGHT=11
HTSIZE=HTGROWBOX
HTSYSMENU=3
HTTOP=12
HTTOPLEFT=13
HTTOPRIGHT=14
HTVSCROLL=7
HTZOOM=HTMAXBUTTON
HWND_BOTTOM=1
HWND_NOTOPMOST=-2
HWND_TOP=0
HWND_TOPMOST=-1
SC_MAXIMIZE=0xF030
SC_MINIMIZE=0xF020
SC_MOVE=0xF010
SC_SIZE=0xF000
SC_ZOOM=61488
SWP_ASYNCWINDOWPOS=0x4000
SWP_DEFERERASE=0x2000
SWP_DRAWFRAME=0x0020
SWP_FRAMECHANGED=0x0020
SWP_HIDEWINDOW=0x0080
SWP_NOACTIVATE=0x0010
SWP_NOCOPYBITS=0x0100
SWP_NOMOVE=0x0002
SWP_NOOWNERZORDER=0x0200
SWP_NOREDRAW=0x0008
SWP_NOREPOSITION=0x0200
SWP_NOSENDCHANGING=0x0400
SWP_NOSIZE=0x0001
SWP_NOZORDER=0x0004
SWP_SHOWWINDOW=0x0040
SW_HIDE=0
SW_MAX=10
SW_MAXIMIZE=3
SW_MINIMIZE=6
SW_NORMAL=1
SW_RESTORE=9
SW_SHOW=5
SW_SHOWDEFAULT=10
SW_SHOWMAXIMIZED=3
SW_SHOWMINIMIZED=2
SW_SHOWMINNOACTIVE=7
SW_SHOWNA=8
SW_SHOWNOACTIVATE=4
SW_SHOWNORMAL=1
WMSZ_BOTTOM=6
WMSZ_BOTTOMLEFT=7
WMSZ_BOTTOMRIGHT=8
WMSZ_LEFT=1
WMSZ_RIGHT=2
WMSZ_TOP=3
WMSZ_TOPLEFT=4
WMSZ_TOPRIGHT=5
WM_ENTERSIZEMOVE=0x231
WM_EXITSIZEMOVE=0x232
WM_MOVING=0x216
WM_NCHITTEST=0x084
WM_SIZE=0x0005
WM_SIZING=0x214
WM_SYSCOMMAND=0x0112
WM_USER=0x0400
WM_WINDOWPOSCHANGING=0x046
WS_EX_APPWINDOW=0x40000
WS_EX_LAYERED=0x00080000
WS_EX_TOOLWINDOW=0x80
sideStrings={0:'left',1:'top',2:'right',3:'bottom'}
