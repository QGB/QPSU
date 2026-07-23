#coding=utf-8
import sys
if 'qgb.U' in sys.modules:U=sys.modules['qgb.U']
elif 'U' in sys.modules:  U=sys.modules['U']
else:
	from sys import path as _p
	_p.insert(-1,_p[0][:-1-1-3-1]) # python2.7\\qgb\\N
	from qgb import U
	if U.iswin():from qgb import Win
# from qgb.Win.KeyCode import *	
T=U.T
import urlparse

# U.pln(  U.read(U.getModPath()+'file/webControl.html')

WDOWN=0x200
WUP=0x400

def forwardReq(a):
	# url_path = urlparse(a.path).path
	# if not url_path == '/0':return a.send_not_found()
	# method U.msgbox(a.command)
	req = urlparse.urlparse(a.path).query
	reqs = urlparse.parse_qs(req, keep_blank_values=True)
	
	if len(reqs)==0:
		a.send_response('text/html', U.read(U.getModPath()+'file/webControl.html'))
		# U.msgbox([i for i in sys.modules if 'webC' in i])
		U.r(sys.modules['qgb.N.webControl'])
		return 
	
	from qgb import Win as w
	
	if len(reqs)==1:
		# t=T.subLast(a.path,'t=','') or 0
		# t=int(t)
		t=int(reqs['t'][0])
		if t&WUP:
			for i in range(5):
				w.mouse_event(0,0,t,move=False,abs=True)
		if  t&WDOWN:
			for i in range(3):
				w.mouse_event(0,0,t,move=False,abs=True)
				
				
		w.mouse_event(0,0,t,move=False,abs=True)
		# a.send_response('text/html',w.getLastErr())
		# a.wfile.write('\r\n'*5)
		return
	if len(reqs)==2:	
		x=int(reqs['x'][0])
		y=int (reqs['y'][0])
		w.setCurPos(x,y)
		return
		# a.send_response('text/html',str(w.getCurPos()))
	# U.msgbox(a.path,type(x),x)
	# import win32api as w
	
	# w.SetCursorPos(x,y)
	# if U.DEBUG:U.pln( x,y,t)

	# U.DEBUG=1
		# if 'webMouse' in sys.modules:m=sys
				# self.send_not_found()
['G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\lib\\noarch', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\launcher', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\python27.zip', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\DLLs', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\lib', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\lib\\plat-win', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\lib\\lib-tk', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\lib\\noarch', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\lib\\win32', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\lib\\noarch', 'G:\\QGB\\software\\xxnet\\code\\3.8.5', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\python27\\1.0\\lib\\win32', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\gae_proxy', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\lib\\noarch', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\lib\\win32', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\x_tunnel', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\lib\\noarch', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\x_tunnel\\common', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\python27\\1.0\\lib\\noarch', 'G:\\QGB\\software\\xxnet\\code\\3.8.5\\smart_router', 'G:/QGB/babun/cygwin/lib/python2.7/']
gsHtml='''
<html>
    <head>
        <title>qgb webControl</title>
		<style>
*{margin:0; padding:0;}
#mousepad {
    width: 100%;
    height: 100%;
    background-color: black;
}
		</style>
        <script type="text/javascript" >
alert(888)
		
		
		</script>
    </head>

    <body>
        <div id="container">
            <div id="mousepad"></div>
        </div>
    </body>
</html>


'''