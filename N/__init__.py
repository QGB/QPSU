#coding=utf-8
import sys
if __name__.endswith('qgb.N'):from qgb import py
else:
	from pathlib import Path
	gsqp=Path(__file__).absolute().parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
	# import py  #'py': <module 'py' from '..\\py.py'>,
RPC_BASE_REMOTE='N.RPC_BASE_REMOTE'
U,T,N,F=None,None,None,None
# __all__=['N','HTTPServer']

gError=[]
def setErr(ae):
	U=py.importU()
	global gError
	if U.gbLogErr:# U.
		if type(gError) is list:gError.append(ae)
		elif gError:gError=[gError,ae]
		else:gError=[ae]
	else:
		gError=ae
	if U.gbPrintErr:U.pln('#Error ',ae) # U.

try:
	if __name__.endswith('qgb.N'):
		from . import HTTP
		from . import HTTPServer
		from . import HTML
	else:
		import HTTP
		import HTTPServer
		import HTML
except Exception as ei:
	py.traceback(ei)

	
if py.is3():
	from http.server import SimpleHTTPRequestHandler,HTTPServer as _HTTPServer
else:
	from SimpleHTTPServer import SimpleHTTPRequestHandler
	from BaseHTTPServer import HTTPServer as _HTTPServer

def post_with_new_thread(url,data,**ka):
	from qgb import U,T,N,F
	
	if not py.isbyte(data):
		data=F.dill_dump(data)
	
	return U.thread(
target=lambda :N.HTTP.post(url,proxies='',data=data,**ka)	
	).start()	
		
post=post_with_new_thread	

def sendkey8888(response=None,s=''):
	''' pip install python3-xlib
	
SEMICLN 分号 ;
SLASH 斜杠 /
EQUAL 等号 =
LBRACKET 左括弧（
MINUS 减号 -
RBRACKET 右括弧 )
COMMA 逗号 ,
QUOTE 引号 ‘
PERIOD 句号 . 
##句号（“。”“.”英式英语：Full stop；美式英语：Period，也称作句点）
BSLASH 反斜杠 \	


6, #ENDCALL 关闭屏幕 休眠？
19, #DPAD_UP 粘贴
23, #DPAD_CENTER 换行
HEADSETHOOK 耳机HOOK键 

94, #PICTSYMBOLS 不知道
115, #CAPS_LOCK

cs[26]     #[':', 'COLON'
'''	
	dci={
'*':17, #STAR
'#':18, #POUND

',':55, #COMMA
'.':56, #PERIOD 'FULL STOP'
'\t':61, #tab
' ':62,#space
'\n':66,#enter
'`':68,#GRAVE
'-':69, #MINUS
'=':70, #EQUALS
'[':71, #LEFT_BRACKET
']':72, #RIGHT_BRACKET
'\\':73, #BACKSLASH
';':74, #SEMICOLON
"'":75, #APOSTROPHE 撇号   cs[7]   #["'", 'APOSTROPHE']
'/':76,#SLASH
'@':77, #AT
'+':81, #PLUS
# '':
# '':
# '':
		
	}
	global U,T,N,F
	U,T,N,F=py.importUTNF()
	
	if not s:s=geta()
	for c in s:
		if c in T.az:ic=ord(c)-68
		elif c in T._09:ic=ord(c)-41
		else:
			ic=dci[c]
		# if 
		
		N.HTTP.get('http://192.168.1.12:8888/cmd/sendkey?KeyCode=%s'%(ic),proxy=0)
	if response:response.set_data(s)	
k8888=sendkey8888

def tftp_download(ip,filename,port=69):
	''' pip install TFTPy     
U.enable_log()

2022-08-24:09:30:59,15 INFO     [TftpContexts.py:389] Sending tftp download request to 192.168.1.3
2022-08-24:09:30:59,15 INFO     [TftpContexts.py:390]     filename -> breed.bin
2022-08-24:09:30:59,15 INFO     [TftpContexts.py:391]     options -> {}
2022-08-24:09:30:59,23 INFO     [TftpStates.py:560] Set remote port for session to 58823
2022-08-24:09:30:59,23 INFO     [TftpStates.py:582] Received DAT from server
2022-08-24:09:30:59,24 INFO     [TftpStates.py:173] Handling DAT packet - block 1
......
......
2022-08-24:09:30:59,237 INFO     [TftpStates.py:173] Handling DAT packet - block 180
2022-08-24:09:30:59,238 INFO     [TftpStates.py:120] Sending ack to block 180
2022-08-24:09:30:59,238 INFO     [TftpStates.py:186] End of file detected
2022-08-24:09:30:59,238 INFO     [TftpClient.py:68]
2022-08-24:09:30:59,239 INFO     [TftpClient.py:69] Download complete.
2022-08-24:09:30:59,239 INFO     [TftpClient.py:73] Downloaded 91650.00 bytes in 0.22 seconds
2022-08-24:09:30:59,240 INFO     [TftpClient.py:74] Average rate: 3198.34 kbps
2022-08-24:09:30:59,241 INFO     [TftpClient.py:75] 0.00 bytes in resent data
2022-08-24:09:30:59,245 INFO     [TftpClient.py:76] Received 0 duplicate packets
Out[1022]: b'\xff\x00\	
'''	
	global U,T,N,F
	U,T,N,F=py.importUTNF()
	
	import tftpy
	ip=N.auto_ip(ip)
	
	client = U.get_or_set('tftp_client=%s:%s'%(ip, port),
		lazy_default=lambda:tftpy.TftpClient(ip, port)
		)
	# print(client)
	from io import BytesIO
	f=BytesIO()
	
	client.download(filename,f)
	f.seek(0)
	b=f.read()
	if py.len(b)>99:
		return U.object_custom_repr(b,repr='{}...#{}'.format(b[:99],F.readable_size(b) )  )
	else:
		return b
tftp_client=tftp_get=tftp_download		
		
def udp_send(ip,data=b'',port=0,timeout=9):
	''' 在miio中可以发送，这里不行，ipdb 也 socket.timeout: timed out
	
	'''
	if ':' in ip:
		ip,port=ip.split(':')
	if not py.isint(port):
		port=py.int(port		)
		
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(timeout)
	try:
		s.sendto(data, (ip, port))
	except OSError as ex:
		return py.No(ex)
		
	try:
		rdata,addr = s.recvfrom(4096)	
		return rdata,addr
	except Exception as e:
		return py.No(e)
		
def http_server(PORT):
	import http.server
	import socketserver
	Handler = http.server.SimpleHTTPRequestHandler
	with socketserver.TCPServer(("", int(PORT)), Handler) as httpd:
		print("serving at port", PORT)
		httpd.serve_forever()
	
def curl_get_ipv4(url,print_msg=True,**ka):
	U,T,N,F=py.importUTNF()
	proxy=U.get_duplicated_kargs(ka,'proxies','proxy',default=0)
	if proxy:
		raise py.ArgumentError('can not use proxy to get real ip')
	
	gdebug=[]
	def f_debug(t,msg):
		ips=T.regex_match_all(msg,T.RE_IPV4)
		if t==0 and ips:
			if print_msg:
				print(len(gdebug),t,msg,ips)
			assert len(ips)==1	
			gdebug.append(ips[0])	
		# gdebug.append([t,msg])
		
	try:	
		curl(url,verbose=True,DEBUGFUNCTION=f_debug,**ka)
	except Exception as e:
		if print_msg:
			print(len(gdebug),e)
	
	uip=U.unique(gdebug)
	uip=[ip.decode() for ip in uip]
	if len(uip)==1:
		return uip[0]
	else:
		return uip
curl_get_ip=curl_get_ipv4	
	
def curl_return_bytes(url,verbose=True,proxy=py.No('socks5h://127.0.0.1:21080'),headers=py.No('default use N.HTTP.headers'),max_show_bytes_size=99,user_agent=py.No('auto use N.HTTP.user_agent'),raise_err=True,**ka):
	'''  SSL_VERIFYPEER=0

	CURLOPT_* see:
https://github.com/pycurl/pycurl/blob/master/src/module.c
	'''
	global U,T,N,F
	U,T,N,F=py.importUTNF()
	proxy=U.get_duplicated_kargs(ka,'proxies','proxy',default=proxy)
	user_agent=U.get_duplicated_kargs(ka,'user_agent','useragent','User_Agent',default=user_agent)
	import pycurl
	c = pycurl.Curl()
	for k,v in ka.items():
		if not k.isupper():
			print('===qgb skip',k,v)
			continue
		ik=py.getattr(c,k)
		c.setopt(ik, v)
	c.setopt(c.URL, url)
	c.setopt(c.VERBOSE,verbose)
	if not headers:	
		HTTP=py.from_qgb_import('N.HTTP')
		headers=HTTP.headers.copy()
	if headers:
		if py.istr(user_agent):
			kua='User-Agent'
			for n,k in py.enumerate(headers):
				if kua.lower() in k.lower():
					if py.isdict(headers):
						headers[k]=user_agent
					if py.islist(headers):	
						headers[n]=f'{kua}:{user_agent}'
						
				# user_agent
		if py.isdict(headers):
			c.setopt(pycurl.HTTPHEADER, ["%s:%s"%(k,v) for k,v in headers.items()] )
		elif py.islist(headers) and py.istr(headers[0]) and ':' in headers[0]:
			c.setopt(pycurl.HTTPHEADER, headers )
		
		else:
			raise py.ArgumentError(headers)

	
	if proxy:
		c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
		c.setopt(pycurl.PROXY, N.set_proxy(proxy)['http'])##socks5://127.0.0.1:21080
	from io import BytesIO
	f=BytesIO()
	c.setopt(c.WRITEDATA, f)
	#c.setopt(c.CAINFO, certifi.where())
	if raise_err:
		c.perform()
	else:
		try:c.perform()
		except Exception as e:
			return py.No(e)
	#c.close()
	f.seek(0)
	b=f.read()
	# print(len(b),b)
	# b.decode()
	if max_show_bytes_size and py.len(b)>max_show_bytes_size:
		return U.object_custom_repr(b,repr='{}...#{}'.format(b[:99],F.readable_size(b) )  )
	else:
		return b
curl=curlb=curl_return_bytes	
	
def check_socket( port,host='127.0.0.1'):
	import socket
	from contextlib import closing
	with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
		if sock.connect_ex((host, port)) == 0:
			return True
		else:
			return False
check_port=check_socket
			
def send_smtp_email(mail_from,mail_to,txt,title='',password='',smtp_server='',**ka):
	global U,T,N,F
	U,T,N,F=py.importUTNF()
	from email.mime.text import MIMEText
	from email.header import Header
	import smtplib
	mail_from=U.get_duplicated_kargs(ka,'mail','email','address','email_address',default=mail_from)
	user,domain= mail_from.split('@')
	if not smtp_server:
		smtp_server='smtp.'+domain
		
	password==U.get_duplicated_kargs(ka,'passwd','pw','p',default=password)	
	if not password:
		password=U.set_input(mail_from)
	if not title:
		title=U.stime()+txt[:99]
	mail_message = f'''
From: {mail_from}
To: {mail_to}
Subject: {title}

{txt}
'''	
	# msg = MIMEText(title, 'plain', 'utf-8')
	# msg['From'] = _format_addr('您的好友<%s>' % mail_from)
	# msg['To'] = _format_addr('管理员<%s>' % verify_addr)
	# msg['Subject'] = Header(txt, 'utf-8').encode()
	s=U.get(smtp_server)
	if not s:
		s = smtplib.SMTP(smtp_server, 25)
		U.set(smtp_server,s)
	s.starttls()
	s.login(mail_from, password)
	return s.sendmail(mail_from, mail_to, title, mail_message)
	
	
send_email=send_smtp_email	

def dns_lookup(domain,rdtype='A'):
	'''其中，qname参数为查询的域名。rdtype参数用来指定RR资源的类型，常用的有以下几种：
（1）A记录：将主机名转换为IP地址；
（2）MX记录：邮件交换记录，定义邮件服务器的域名；
（3）CNAME记录：别名记录，实现域名间的映射；
（4）NS记录：标记区域的授权服务器及授权子域；
（5）PTR记录：反向解析，与A记录相反，将IP转换成主机名；
（6）SOA记录：SOA标记，一个起始授权区的定义；
'''
	# domain = "google.com" 
	import dns.resolver
	return py.list(dns.resolver.resolve(domain , rdtype) )	
	# resolver = dns.resolver.Resolver(); 
	# answer = 
	# return answer
	# resultant_str=''
	# for item in :
	return resultant_str
resolveDNS=dns_lookup			
	
def get_tornado_rpc_handler(key='/-',locals=None,globals=None):
	'''return tornado.web.Application([
	(r"/-(.*)", N.get_tornado_rpc_handler(key='/-')),
])	
	'''
	import tornado.web
	import tornado.gen
	U,T,N,F=py.importUTNF()
	
	class RPCHandlerTornado(tornado.web.RequestHandler):
		''' def prepare(self):  # 405: Method Not Allowed '''
		@tornado.gen.coroutine
		def options(self, *args, **kwargs):
			nonlocal locals,globals,U,T,N,F
			self.set_status(200)
			self.set_header('content-type', 'text/plain')
			if not self.request.uri.startswith(key):
				return
			# py.pdb()()
			try:
				s=T.url_decode(self.request.uri[py.len(key):])
			except Exception as urlDecodeErr:
				U.print_traceback_in_except()
				s=self.request.uri[py.len(key):]
			if not locals:locals=py.locals()
			if not globals:globals=py.globals()	
				
			self.write(U.execResult(
				s,locals=locals,globals=globals
			)   )
		get=head=post=delete=patch=put=options
	return RPCHandlerTornado
# except Exception as e:
	# setErr(e)
tornado_rpc_handler=RPCHandlerTornado=get_tornado_rpc_handler

def git_https_to_ssh(url=py.No('auto get clipboard'),):
	U,T,N,F=py.importUTNF()
	if not url:
		url=U.cbg(e=1,edit_prompt='git-url:')
	d=T.regex_match_named(url,T.RE_GIT_REPO)
	if not d:return d
	if d['protocol'] in ['https','ssh',]:
		if not d['netloc'].startswith('git@'):
			if '@' in d['netloc']:
				d['netloc']='git@'+T.sub(d['netloc'],'@','')
			else:
				d['netloc']='git@'+d['netloc']
				
		return 'ssh://%(netloc)s/%(user)s/%(repo)s'%d
	else:
		raise py.NotImplementedError(url,d)
		
url_git_https_to_ssh=get_ssh_git=https_to_ssh_git=github_https_to_ssh=git_https_to_ssh	


def github_release(url):
	'''    "url": "https://api.github.com/repos/octocat/Hello-World/releases/1",
	"html_url": "https://github.com/octocat/Hello-World/releases/v1.0.0",
	"assets_url": "https://api.github.com/repos/octocat/Hello-World/releases/1/assets",
	"upload_url": "https://uploads.github.com/repos/octocat/Hello-World/releases/1/assets{?name,label}",
	
	(?P<name>.*)
#useless r'((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?'
'''
	U,T,N,F=py.importUTNF()
	url=T.regex_match_all(url,T.RE_GIT)[0]

def get_github_raw(q):
	''' 
	api='https://api.github.com/repos/{0}/{1}/contents/'
	
https://github.com/nobodywasishere/SGH-I537_NA_LL_Opensource/blob/d731152178585788b45d6fd9c0168412ced4bfd8/Platform/vendor/samsung/common/packages/apps/SBrowser/src/chrome/test/data/extensions/api_test/webrequest_sendmessage/background.html

https://github.com/nobodywasishere/SGH-I537_NA_LL_Opensource/blob/master/Platform/vendor/samsung/common/packages/apps/SBrowser/src/chrome/test/data/extensions/api_test/webrequest_sendmessage/background.html

https://github.com/Banou26/chromium-issue-1178811/raw/main/content-script.js

https://raw.githubusercontent.com/Banou26/chromium-issue-1178811/main/content-script.js
'''	
	a=get_flask_request_a(q)
	sa=a.split('/')
	['https:', '', 'github.com', 'espressif', 'crosstool-NG', 'releases', 'download', 'esp-2021r2-patch3', 'xtensa-esp32-elf-gcc8_4_0-esp-2021r2-patch3-linux-amd64.tar.gz']
	raise py.NotImplementedError()
	if '://github.com/' in a:
		n0=-1
		for n,i in py.enumerate(sa):
			if i=='github.com':
				n0=n
	
graw=getraw=github_raw=raw_github=get_github_raw	
	
	
def get_public_ip_by_dnspod(methods=['']):
	import socket; sock=socket.create_connection(('ns1.dnspod.net',6666))
	bip=sock.recv(16)
	sock.close()
	return bip
def get_public_ipv4(methods=['myip.ipip.net','ipinfo.io', 'icanhazip.com', 'ifconfig.me', 'ip.appspot.com', 'api.ipify.org', 'ipecho.net/plain', 'ipcalf.com', 'www.trackip.net','https://www.google.com/search?q=my+ip'],
http_external_kargs={'ipinfo.io':{'encoding':'utf-8','headers':{'User-Agent': 'curl'}},
},
	proxy=False,wait=3.4,return_list=True,print_msg=True,**ka):
	from threading import Thread, Lock
	U,T,N,F=py.importUTNF()
	
	print_msg=U.get_duplicated_kargs(ka,'print_msg','print','show_msg','show','p',default=print_msg)
	
	mutex = Lock()
	d={}
	def new_thread(u):
		if print_msg:
			mutex.acquire()
			print(U.stime(),'fetching...',[methods.index(u)],u)  #list tuple all have index
			mutex.release()
		
		d[u]=N.HTTP.get(u,timeout=3,proxies=proxy,**http_external_kargs.get(u,{}) ,)
		if py.istr(d[u]) and py.len(d[u])>77:
			d[u]=U.object_custom_repr(d[u],repr='{}#s.len:{}'.format(
					T.regexMatchAll(d[u],T.RE_IP) ,py.len(d[u]),  
				)    
			)
		if print_msg:	
			mutex.acquire()
			print(U.stime(),'received:  ',[methods.index(u)],U.StrRepr(u,size=17),repr(d[u])[:77])
			mutex.release()

	for u in methods:
		Thread(target=new_thread,args=(u,)).start()
	for i in py.range(py.int(py.max(1,wait))):
		U.sleep(wait)
		if py.len(d)==py.len(methods):
			break
	
	if return_list:
		r=[]
		re=[]
		for k,v in d.items():
			if v:
				r.append((k,v))
			else:
				re.append((k,v))  # 超时3.4 还未得到结果 的不会返回 
		return re+r
	return d
get_all_pub_ip=get_pub_ip=get_public_ip=get_public_ipv4

def get_public_ipv4_return_str(print_msg=False,**ka):
	U,T,N,F=py.importUTNF()
	try:
		dur=get_public_ipv4(return_list=0,print_msg=print_msg,**ka)
		ip=dur['ipcalf.com']
		for u,rs in dur.items():
			if not rs:continue
			if 'no healthy upstream' in rs:#ipecho.net/plain 
				print('@'*55,U.stime(),u,rs)
				continue
			if ip not in rs:
				print('#'*55,u,rs)
				raise py.Exception('ip not match ! %s'%ip,u,rs)
		return ip		
	except Exception as e:
		return py.No(e)
get_pub_ip_str=get_public_ipv4_return_str		
		
def ftp_client(cwd=py.No('history or /',no_raise=1),
	host=py.No('auto get ftp.host',no_raise=1),port=3721,user='', passwd='',ftp_encoding='utf-8', acct='',
				 timeout=None,retry=3,response=None,request=None,text_encoding='',**ka):
	'''
	'''
	import ftplib     
	U,T,N,F=py.importUTNF()
	response=U.get_duplicated_kargs(ka,'resp','rsp','p',default=response)
	request=U.get_duplicated_kargs(ka,'req','q','REQ',default=request)
	return_raw=U.get_duplicated_kargs(ka,'raw','return_raw','RAW',default=None)
	
	ftp_encoding=U.get_duplicated_kargs(ka,'ftpe','fe','encoding','list_encoding',default=ftp_encoding)
	text_encoding=U.get_duplicated_kargs(ka,'txte','te','txt_encoding',default=text_encoding)
	
	def set_user_passwd_host_port_cwd(url):
		nonlocal host,port,user,passwd,cwd
		netloc=T.netloc(url)
		if not netloc:raise py.ArgumentError(cwd)
		user_pw=T.sub(netloc,'','@')
		if user_pw:
			if ':' in user_pw:
				user_pw=user_pw.split(':')
				if not user:user=user_pw[0]
				if not passwd:passwd=user_pw[1]
			else:
				if not user:user=user_pw
			host_port=T.sub(netloc,'@')
			set_host_port(host_port)
		else:
			set_host_port(netloc)
		if not cwd:cwd=T.sub(url,netloc)
		
	def set_host_port(host_port):
		nonlocal host,port
		if ':' in host_port:
			host_port=host_port.split(':')
			if not host:host=host_port[0]
			if port==3721:port=py.int( host_port[1])
		else:
			if not host:host=host_port
			if port==3721:port=21
	
	if not cwd and N.geta(request):
		cwd=N.geta(request)		

	if py.istr(cwd):
		if cwd.startswith('ftp://') :
			cwd,url='',cwd
			#warnning
			set_user_passwd_host_port_cwd(url)
		# or ('@' in host and ':' in cwd):
		# if not host and ':' in cwd:
			
			
	if not host:
		if (py.isnumber(cwd) and cwd>0):
			host,cwd=cwd,''	
			#warnning
		if not host:host=U.get_or_set_input('ftp.host[default]',type=U.parse_str_auto_type)
	if py.istr(host):
		if host.startswith('ftp://') or ('@' in host):
			host,url='',host
			set_user_passwd_host_port_cwd(url)
		elif ':' in host:
			set_host_port(host)
		
	host=auto_ip(host) 
	
	uk='ftp.FTP[netloc={user}{host}:{port}]'.format(
		host=host,port=port,user= user+'@' if user else user)
	self=U.get(uk)
	if not self:
		if not cwd:cwd='/'
		if port==3721 and not user:
			user=U.input_and_set('ftp.user[port=3721]','if_is_es_need_user_to_login')
		if not timeout:
			from socket import _GLOBAL_DEFAULT_TIMEOUT
			timeout=U.get_or_set('ftp.timeout', _GLOBAL_DEFAULT_TIMEOUT)
		ftp=self=ftplib.FTP(timeout=timeout)
		self.host=host
		self.port=port
		self.encoding=ftp_encoding
		try:
			self.connect(host)
			if user:
				self.login(user, passwd, acct)
		except Exception as e:
			if retry>0:retry-=1
			else:raise	
			return ftp_client(cwd=cwd,host=host,port=port,user=user,passwd=passwd,ftp_encoding=ftp_encoding,acct=acct,timeout=timeout,retry=retry,response=response,request=request,text_encoding=text_encoding,**ka,)
	self.encoding=ftp_encoding			
	try:
		pwd=self.pwd()
	except Exception as e:
		self.close()
		U.set(uk,py.No(e))
		if retry>0:retry-=1
		else:raise	
		return ftp_client(cwd=cwd,host=host,port=port,user=user,passwd=passwd,ftp_encoding=ftp_encoding,acct=acct,timeout=timeout,retry=retry,response=response,request=request,text_encoding=text_encoding,**ka,)
		# print(e)
	U.set(uk,self) ### set ftp obj
	if not cwd:cwd=pwd
	try:
		self.cwd(cwd)
	except Exception as e:
		from io import BytesIO
		bio=BytesIO()
		filename=F.get_filename_from_full_path(cwd)
		self.cwd(T.sub_last(cwd,'',filename))
		bio.path=self.pwd()
		bio.filename=bio.name=filename
		U.log(host,port,self.pwd(),filename,'fetching..')
		self.retrbinary("RETR " + filename ,bio.write)
		if response:
			from flask import stream_with_context
			gen=F.read_file_as_stream(bio)
			response.response=stream_with_context(gen)
			response.headers['Content-Disposition'] ="inline; filename=" + T.url_encode(filename)
			if text_encoding:
				if 'auto' in text_encoding.lower():
					text_encoding=T.detect(bio.getvalue()[:2999])
				response.headers['Content-Type']='text/plain;charset='+text_encoding;
		return bio
	if not cwd.endswith('/'):cwd+='/'	
	rd={}
	# hs=[]
	html=''
	dir_size=U.IntRepr(-1,repr='<-1 FTP_DIR_>')
	try:
		mlsd=self.mlsd()
	except ftplib.error_reply as e:#error_reply: 200 Command okay.
		if e.args[0]!='200 Command okay.':raise
		self.passiveserver=0
		mlsd=self.mlsd()
		
	mlsd=py.list(mlsd)
	if not mlsd:#3721
		fs=self.nlst()
		ls=[]
		self.retrlines("LIST",callback=ls.append)		
		nf,nl=U.len(fs,ls)
		if nf!=nl:raise py.EnvironmentError(nf,nl,fs,ls)
		mlsd=[[fs[i],ls[i]] for i in py.range(nf)]
	if return_raw:return mlsd
	for fd in mlsd:
		f,d=fd
		# if py.len(d)>4:raise py.EnvironmentError(f,d)
		# if d['type']=='dir':
		# size=py.int( d.get('size',-1)	)
		if (py.istr(d) and d.startswith('d')) or (py.isdict(d) and d.get('type','')=='dir'):
			# if size!=-1 :raise py.EnvironmentError(f,d)
			# size=dir_size
			if not f.endswith('/'):f+='/'
		rd[f]=d
		# else:
			# size=F.IntSize(size)
		# rd[f]=[size,
				# U.StrRepr(d['modify'],repr=U.stime(d['modify'])),
				# U.StrRepr(d['create'],repr=U.stime(d['create'])),
				# ]
		if response:
			h='<a href="./{0}">{1}</a>{2!r}<br>\n'.format(T.html_encode(f),T.padding(f,size=44,char=chr(65440)),d)
			html=html+h
	if response:
		response.headers['Content-Type']='text/html;charset=utf-8';
		response.set_data(html)
	return rd
		# html=T.html_template('''$
# '<a href=>'		
		# $''',globals=py.globals(),locals=py.locals())
	# fs=self.nlst()
	# def line_callback(line):
		
	# self.retrlines("LIST",callback=line_callback)		
	flask_html_response(response,html='<a href="/{0}">{0}</a>',remove_tag=[])
		# try:
			
		# except Exception as rbe:
			# e
			
	return U.set(uk,self)
FTP=ftp=ftp_client	
# def ftp_list_file(host)
	
def rpc_fifo_put_cmd(s,name='cmd',path=None):
	''' Linux has os.mkfifo(fn)  
Windows:AttributeError: module 'os' has no attribute 'mkfifo' 
	'''
	U,T,N,F=py.importUTNF()
	if not path:path=U.gst+'fifo/'
	if F.isabs(name):
		fn=name
	else:
		path=F.mkdir(path)
		fn=path+name
	import os
	try:
		os.mkfifo(fn)
	except FileExistsError as e:
		print(fn,e)
	t=U.itime()
	with os.fdopen(os.open(fn, os.O_SYNC | os.O_CREAT | os.O_RDWR)) as f:
		os.write(f.fileno, s)
		
		# f.write(s)
	return s,U.itime()-t
def rpc_fifo_eval(cmd='cmd',result='result',path=None,**ka):
	U,T,N,F=py.importUTNF()
	if not path:path=U.gst+'fifo/'
	def get_fn(name):
		if F.isabs(name):
			fn=name
		else:
			path=F.mkdir(path)
			fn=path+name
		try:
			os.mkfifo(fn)
		except FileExistsError as e:
			print(fn,e)
		return fn
	t=[U.itime()]		
	with os.fdopen(os.open(get_fn(cmd), os.O_RDONLY)) as rf:
		s=os.read(rf, -1)
	t.append(U.itime()-t[-1])	
	r=U.execResult(s,**ka)
	t.append(U.itime()-t[-1])	
	with os.fdopen(os.open(fn, os.O_SYNC | os.O_CREAT | os.O_RDWR)) as f:
		os.write(f, r)
	t.append(U.itime()-t[-1])	
	return r,t
	
def pppoe():
	'''
506 192.168.2.1+192.168.1.1 073198799737 777124	

'''

def flask_dill_data():
	from flask import request
	U,T,N,F=py.importUTNF()	
	b=request.get_data()
	return F.dill_load_bytes(b)
	
def flask_request_log(time=True,url=False):
	from flask import request
	U,T,N,F=py.importUTNF()	
	rq=U.dir(request)
	rq=U.StrRepr(U.pformat(rq))
	
	r=[]
	if time:r.append(U.stime())
	if url :r.append(T.url_decode(request.url) )
	
	if r:
		r.append(rq)
	else:	
		r=rq
		
	
	rl=U.get_or_set('req_log',[])
	rl.append(r)
	return py.len(rl)
log_req=req_log=flask_request_log	

skip_response_headers={
	'Transfer-Encoding': 'chunked',
	'transfer-encoding': 'chunked',
}
def copy_request_to_flask_response(target,response=None):
	
	if not response:
		from flask import make_response
		response=make_response()
	response.status_code=target.status_code
	for k,v in target.headers.items():
		if k in skip_response_headers:
			continue
		response.headers[k]=v	
	response.headers['Content-Security-Policy']=''
	#response.headers['Content-Encoding']=gencoding
	b=target.content
	
	response.set_data(b)
	return response
	
def copy_request(a,p=True):
	import requests
	U,T,N,F=py.importUTNF()
	if py.istr(a):a=F.dill_load(a)
	req=py.getattr(a,'request',0)
	if req:a=req
		# params=request.args, # ?a=b  in a.url
		
	if p:print(
U.v.requests.request(method=a.method,url=a.url,headers=a.headers,)
	)
		
	return requests.request(method=a.method, 
		url=a.url, 
		headers=a.headers, )
copy_req=req_copy=rebuild_request=request_copy=copy_request
	

def download_http_everthing(url,save_path=py.No('auto using pwd ?'),r=1,p=1):
	'''   '''
	global U,T,N,F
	U,T,N,F=py.importUTNF()
	from six.moves.urllib.parse import urlsplit

	h=N.get(url)
	if py.istr(h) and '''<a href="/"><img class="logo" src="/Everything.gif" alt="Everything"></a>''' in h:
		pass
			# url+='/'
	else:
		return h
	url=N.auto_url(url)
	# if not url.endswith('/'):url+='/'
	up=urlsplit(url=url)  # obj
	
	netloc=up.netloc
	url_base='http://'+netloc
	
	ups=[s for s in up.path.split('/') if s]	
	if not ups:cu='es-'+U.stime()
	else     :cu=ups[-1]
	
	# icu=url.rindex('/',0,-1)
	# if icu<=6:cu=''#'download_http_everthing'
	# else:
		# cu=url[icu+1 : -1] # 'C%3A'	
		# if ':' in cu:cu=T.url_encode(cu)
	
	#索引 /   indexof">索引 C:</p>     ">索引 C:\test</p>
	# c_folder=T.sub(h,'<tr><td colspan="3"><p class="indexof">','</p></td></tr>')
	# c_folder=F.get_filename(c_folder) # ''      '索引 C:'     'test'
	# save_path=F.mkdir(save_path)
	if not save_path.endswith('/') and not save_path.endswith('\\'):
		save_path+='/'
	save_path_cu=F.mkdir(save_path+cu)
	rfs=[]
	for r4 in parse_everthing_html(h):
		fn=save_path_cu + [s for s in r4[0].split('/') if s] [-1]
		if r4[-1]:
			fn+='/'
			if r:
				rfs.append( 
	{fn:download_http_everthing(url_base+r4[0],save_path=save_path_cu,r=r,p=p) } 
				)
				
			# continue  # skip folder
		else:
			fn=N.HTTP.get(url_base+r4[0],file=fn)	
			rfs.append(fn)
		if p:print(fn)	
	return rfs	
des=down_es=esdl=dl_es=dles=download_es=download_everthing_http=download_http_everthing

	
def parse_everthing_html(html):
	''' 名称	大小	修改日期    isd
	'''
	global T
	if not T:T=py.importT()
	b=T.BeautifulSoup(html)
	r=[]
	for n,e in enumerate(b.select('tr[class*=trdata]')     ):
		p=T.sub(e,'<a href="','"><img alt="')
		size=T.sub(e,'<td class="sizedata"><span class="nobr"><nobr>','</nobr></span>')
		time=T.sub(e,'<td class="modifieddata"><span class="nobr"><nobr><span class="nobr"><nobr>','</nobr></span></nobr></span></td>')
		isd=T.sub(e,'<img alt="" class="icon" src="/','.gif"/') == 'folder'
		# print('%-3s %-80s %-6s %-22s %-5s'%(n,p,size,time,isd)  )
		r.append([p,size,time,isd])
	return r	
parse_es=parse_everthing=parse_everthing_http=parse_http_everthing=parse_everthing_html
	
def zhihu_question(url=py.No('N.geta'),response=None):
	import qgb.tests.zhihu_scrapy_single_QA
	if not( py.istr(url) or py.isint(url) ):
		# url=py.getattr(url,'url')
		url=geta()
	print(repr(url))	
	r= qgb.tests.zhihu_scrapy_single_QA.zhihu(url)
	if response:
		response.set_data(r)
	return r
zhihu=zhihu_question	

def dns_resolve(domain,rdtype='A',return_str_list=True):
	''' dnspython '''
	import dns.resolver   
	try:
		r=dns.resolver.resolve(domain,rdtype)
		if return_str_list:
			return [rdata.address for rdata in r.rrset]
		else:return r.rrset
		# return r.rrset.items
	except Exception as e:
		return py.No(e)
dns=get_ip_from_domain=resolve_domain=dns_resolve
		
def ping(addr,sum=5,sleep=0,timeout= 4,ttl=None,seq=0,size=56,interface=None,p=False,r=True,**ka):
	''' ping3.ping(
	dest_addr: str,
	timeout: int = 4,
	unit: str = 's', ##unit: The unit of returned value. "s" for seconds, "ms" for milliseconds. (default "s")
	src_addr: str = None,
	ttl: int = None,
	seq: int = 0,
	size: int = 56,
	interface: str = None,
) -> float 
Returns:
	The delay in seconds/milliseconds or None on timeout. # qgb return ms
	
C:\QGB\Anaconda3\lib\site-packages\ping3.py in send_one_ping(sock, dest_addr, icmp_id, seq, size)
	189     _debug("Sent ICMP Payload:", icmp_payload)
	190     packet = icmp_header + icmp_payload
--> 191     sock.sendto(packet, (dest_addr, 0))  # addr = (ip, port). Port is 0 respectively the OS default behavior will be used.
	192
	193

OSError: [WinError 10051] 向一个无法连接的网络尝试了一个套接字操作。	
OSError(10065, '套接字操作尝试一个无法连接的主机。', None, 10065, None),'192.168.2.1',56

'''
	import ping3
	U,T,N,F=py.importUTNF()
	addr=auto_ip(addr,**ka)
	sum=U.get_duplicated_kargs(ka,'times','count','n','ct',default=sum)
	if U.isWin():
		Win=py.from_qgb_import('Win')
		_title=U.set('window_title',Win.get_title())
		set_title=Win.set_title
	else:
		_title=''
		set_title=lambda *a,**ka:None
	def _return(msg,*a):
		# nonlocal set_title,_title
		set_title(title=_title)
		if py.islist(msg):return msg
		else:
			return py.No(msg,*a)
	lr=[];re=[]
	if p:
		sv=U.v(dest_addr=addr,timeout=timeout,unit='ms',ttl=ttl,seq=seq,size=size,interface=interface)[1:-2]
		time=U.stime()
		set_title(title='ping '+sv+' '+time)	
		print(time,'%54s'%addr)
		print(sv, )
		print('-'*80)
	for i in py.range(sum):
		try:
			if i and sleep and ms!=None:U.sleep(sleep)
			ms=ping3.ping(dest_addr=addr,timeout=timeout,unit='ms',ttl=ttl,seq=seq,size=size,interface=interface)
		except OSError as e:
			ms=py.No(e)
		except (SystemExit,KeyboardInterrupt,Exception) as e:#必须加括号，否则语法错误
			return _return(e,addr,size,)
		if not py.isnumber(ms):
			re.append(i)
		if p:
			print('%-5s'%i,'%-15s'%U.stime()[12:],'ms=%r'%ms,)
		if r:lr.append([i,ms])
		else:ms #TODO count timeout rate, avg ms
	if py.len(re)==sum:
		return _return('ping %s %s times all faild!'%(addr,sum),addr,timeout,ttl,seq,size,interface)
	else:
		if r:return _return(lr)

def range_http_server(port=2233,**ka):
	'''
#TODO 标准库test 不支持https 

['C:/QGB/npp/notepad++.exe',
 'C:\\QGB\\Anaconda3\\lib\\http\\server.py',
 '-n 1219']
 
def test(HandlerClass=BaseHTTPRequestHandler,
		 ServerClass=ThreadingHTTPServer,
		 protocol="HTTP/1.0", port=8000, bind=""):	
	
	'''
	try				  :import http.server as SimpleHTTPServer	# Python3
	except ImportError:import SimpleHTTPServer					# Python 2
	from RangeHTTPServer import RangeRequestHandler
	U,T,N,F=py.importUTNF()

	ip=U.get_duplicated_kargs(ka,'ip','bind','addr','address','listen','IP',default='0.0.0.0')
	# import RangeHTTPServer

	a=U.parse_args(port=port,ip=ip)
 
	return SimpleHTTPServer.test(HandlerClass=RangeRequestHandler,port=a.port,bind=a.ip)
RangeRequestHandler=RangeHTTPServer=rangeHTTPServer=range_server=range_http_server
	
	
def uploadServer(port=1122,host='0.0.0.0',dir='./',url='/up'):
	'''curl  http://127.0.0.1:1122/up -F file=@./U.py
	'''
	U,T,N,F=py.importUTNF()
	
	from flask import Flask,request,make_response, send_from_directory
	app= Flask('uploadServer'+U.stime_() )
	@app.route(url,methods=['POST','GET'])
	def upload_file():
		file = request.files['file']
		if file:
			filename = U.path.join(dir, file.filename)
			file.save(filename)			
			r= make_response(filename)
			r.headers['Content-Type'] = 'text/plain;charset=utf-8'
			return r
	app.run(host=host,port=port,debug=0,threaded=True)	
############# rpc start ############

def check_local_port_listen(ports):
	''' if multi ports :return first open addr'''
	import psutil
	if py.isint(ports):ports=[ports]
	for conn in psutil.net_connections():
		if conn.status == 'LISTEN' and conn.laddr.port in ports:
			return conn.laddr
	return False
is_port_open=check_port_open=check_local_port_listen

def get_process_all_listen_addr(pid):
	''' addr(ip='0.0.0.0', port=443),
	'''
	import psutil
	# p=psutil.Process(pid=pid)
	ns=psutil.net_connections()
	r=[]
	for sconn in ns:
		if sconn.pid==pid:
			r.append(sconn.laddr)
	return r
get_process_listen_port=get_process_all_listen=get_process_all_listen_addr
	
def get_all_pid_equal_port():
	global U,T,N,F
	U,T,N,F=py.importUTNF()
	import psutil
	ns=psutil.net_connections()
	r=[]
	for sconn in ns:
		if sconn.pid==sconn.laddr.port:
			p=psutil.Process(pid=sconn.pid)
			t=U.object_custom_repr(p._create_time,repr=psutil._pprint_secs(p._create_time),)
			
			r.append([t,sconn])
			# r.append([t,p,sconn])
	return r
get_rpc_port=get_rpc_ports=get_all_rpc_port=get_all_rpc_ports=get_rpc_port_list=get_pid_equal_port=get_port_equal_pid=get_all_pid_equal_port			

DEFAULT_RPC_BASE_REMOTE=py.No('if not base:input',no_raise=1)
def is_remote_rpc_base(base):
	if (not base) or (not py.istr(base)):return py.No(base,'must be str')
	if '://' in base:
		return base
	else:
		return py.No(base,'format error!')
is_rpc_base=is_rpc_base_remote=is_remote_rpc_base
		
def set_remote_rpc_base(base=DEFAULT_RPC_BASE_REMOTE,change=True,ka=None):
	U,T,N,F=py.importUTNF()	
	if py.istr(base):
		if base.lower() in ['set','reset','modify','change']:
			change=True
			base=''
		
		if base.lower() in ['get','last','no_change']:
			change=False
			base=''
			
			
	if not base:
		default=U.get(RPC_BASE_REMOTE)
		if default:
			if not change:
				base=default
		else:
			default='https://'
		while not is_remote_rpc_base(base):
			base=default=U.input(RPC_BASE_REMOTE+' :',default=default)
			base=T.matchRegexOne(base,T.RE_URL)
		# base=U.get_or_set(RPC_BASE_REMOTE,'http://127.0.0.1:23571/')
	if not py.istr(base):
		if py.isfloat(base) or py.isint(base):
			default=U.get(RPC_BASE_REMOTE)
			if not default:default='http://127.0.0.1:23571/'
			netloc=T.netloc(default) # '192.168.43.162:2357' include port
			i=default.index(netloc)  #TODO if netloc=='http'  
			n=netloc.find(':')
			if base<0:
				history
			if base>255:
				if  ':' in netloc:
					template=default.replace(netloc,netloc[:n+1]+'{}',1)
				else:
					i+=py.len(netloc)
					template=default[:i]+':{}'+default[i:]	
				# change_port
			else:
				if  ':' in netloc:
					netloc=netloc[:n]
				template=default[:i]+'{}'+default[i+py.len(netloc):]
				base=N.auto_ip(base)
			base=template.format(base)
		else:
			raise py.ArgumentUnsupported('rpc base_url:',base)

	# if not base.endswith('/'):
		# if ':' not in base:
			# base=base+':23571'
		# base+='/'
	return U.set(RPC_BASE_REMOTE,base)	
rpc_base=change_rpc_base=get_or_set_rpc_base=get_rpc_base_remote=get_remote_rpc_base=set_rpc_base_remote=set_remote_rpc_base
	
DEFAULT_RPC_LOCAL_PORTS=[1122,1133,1166,1177]
def get_local_rpc_base(ports=DEFAULT_RPC_LOCAL_PORTS):
	U,T,N,F=py.importUTNF()
	u=U.get_dl('qgb_domain')
	ip=N.get_lan_ip()
	if u and check_local_port_listen(443):
		return f'''https://{T.sub_last(ip,'.')}.{u}/'''
	else:
		if py.isint(ports):ports=[ports]
			# port=check_local_port_listen(ports).port # addr(ip='0.0.0.0', port=1122)	
		for port in ports:
			addr=check_local_port_listen(port)
			if addr and addr.ip in ['0.0.0.0',ip]:
				url=f'''http://{ip}:{port}/'''
				return url
get_rpc_base_local=get_local_rpc_base

	
def rpc_append_list(*a,name='la',base='',proxies=0,print_req=1):
	''' #TODO  check_row_len=None
	'''
	U,T,N,F=py.importUTNF()
	
	if not base:
		raise py.ArgumentError('need base')
		
	
	rp= N.HTTP.post(f'{base}rpc_a=N.flask_dill_data();{name}.append(rpc_a);r=py.len({name})',F.dill_dump(a if py.len(a)!=1 else a[0]),proxies=proxies,print_req=print_req)
	t=rp.text
	if 'NameError: name' in t and 'is not defined' in t:
		 N.HTTP.post(f'{base}r={name}=[]')
		 return rpc_append_list(*a,name=name,base=base)
	return U.StrRepr(t)
	
def rpc_call(name,*a,base='',proxies=0,print_req=1,**ka):
	U,T,N,F=py.importUTNF()
	# base=get_remot_rpc_base(base=base,ka=ka)
	if '://' in name:
		s=T.get_url_path(name)
		base=T.sub(name,'',s)
		name=s
	if name.startswith('r='):
		name=name[2:]
	# if name.endswith(')')	
		
	if not base:
		raise py.ArgumentError('need base')
	rp= N.HTTP.post(f'{base}rpc_a,rpc_ka=N.flask_dill_data();r={name}(*rpc_a,**rpc_ka)',F.dill_dump([a,ka]),proxies=proxies,print_req=print_req)
	return U.StrRepr(rp.text)
	
def rpc_pop_window_127(port=443):
	'''
U.ppid(6672)
30464

U.ppid(30464)
5740

ws[1]==
(1247918,
 '6672 ipy:7.9 py:3.74 at[2022-09-03__10.56.09__.462] C:/test/ipy/',
 5740)
 =========
 ssl_context=('C:/test/ssl/##domain##/fullchain.crt', 'C:/test/ssl/##domain##/private.pem')
''' 
	global U,T,N,F
	U,T,N,F=py.importUTNF()
	if port==443:
		f=U.get_or_dill_load_and_set('ssl_context')[0]
		if '\\' in f:
			domain=T.sub_last(f,'\\','\\')
		else:	
			domain=T.sub_last(f,'/','/')
		rpc_base=f'https://3.{domain}/'
	else:	
		rpc_base=f'http://127.0.0.1:{port}/'
	print(rpc_base)
	b=N.curl(rpc_base+'Win.popw();r=U.pid,U.ppid(),U.ppid(U.ppid())')
	r3=T.unrepr(b.decode())
	return r3

rpc_popw=rpc_pop_window=rpc_pop_window_127

def rpc_iter_U_get(name,bases=None,**ka):
	'''
	bases= ports or urls
	'''
	U,T,N,F=py.importUTNF()

	if not bases:
		bases=[i[1].pid for i in N.get_rpc_port_list()]

	if py.istr(bases):
		bases=[bases]
	r=[]	
	for base in bases:
		if py.isint(base):
			base='http://127.0.0.1:{}/'.format(base)
		u=base+'r=U.get(%r)'%name

		# rq=N.HTTP.post(u)
		rq=N.curl(u)
		r.append([base,rq])
	return r

def rpc_copy_single_file(source,target='',base=DEFAULT_RPC_BASE_REMOTE,**ka):
	U,T,N,F=py.importUTNF()
	base=get_remote_rpc_base(base,ka=ka)
	b=F.read_bytes(source)
	# if not F.isabs()
	r=N.HTTP.post(base+'b=request.get_data();rpc_copy_filename=%r;r=F.write(rpc_copy_filename,b)'%target,verify=False,timeout=9,proxy='',data=b).text
	
	return U.StrRepr(r)
def rpc_copy_files(source_list_or_dict,target='',target_path_base=py.No('U.gst'),base=DEFAULT_RPC_BASE_REMOTE,source_max_size=8*1024*1024,skip_empty_file=True,proxy='',**ka):
	U,T,N,F=py.importUTNF()	
	base=get_remote_rpc_base(base,ka=ka)
	source=U.get_duplicated_kargs(ka,'a','s','source',default=source_list_or_dict)
	d={}
	if py.istr(source) and py.istr(target):
		d={source:target}
	elif py.isdict(source) and not target:
		d=source
	elif U.len(source)==U.len(target) and U.len(source)>1 :
		for n,i in py.enumerate(source):
			d[i]=target[n]
	else:
		raise py.ArgumentUnsupported(source,target)
	
	F.read_multi_files(return_all_bytes=1)
	
	return  
rpc_copy=rpc_copy_file=rpc_copy_files
	
AUTO_GET_BASE=py.No('auto history e.g. [http://]127.0.0.1:23571[/../] ',no_raise=1,)
RPC_GET_TEMPLATE='{base}response.set_data(F.serialize({varname}))'
def rpc_get_variable(varname,
base=AUTO_GET_BASE,
template=RPC_GET_TEMPLATE,
		timeout=9,p=True,return_bytes=False,proxies=None,ipy=False,**ka):
	U,T,N,F=py.importUTNF()	
	return_bytes=U.get_duplicated_kargs(ka,'return_byte','rb','B','b','raw','raw_bytes',default=return_bytes)
	if base is AUTO_GET_BASE:
		base=get_remote_rpc_base(change=False)
	elif not base or (py.istr(base) and base.lower() in ['input','modify','change']):
		base=get_remote_rpc_base(change=True)
	else:	
		base=get_remote_rpc_base(base=base,change=True)
		
	proxies=N.HTTP.auto_proxy_for_requests(proxies,ka)	
	# if not base:raise py.ArgumentError('need base=')
	# if T.regexMatchOne(base,':\d*$') or T.regex_count(base,'/')==2:base+='/'
	# U.set(RPC_BASE_ REMOTE,base)
	
	if py.istr(varname) and template==RPC_GET_TEMPLATE and '{base}' in varname:
		template=varname
		varname=''
		
	
	url=template.format(base=base,varname=varname)
	# import requests,dill
	# dill_loads=dill.loads
	# get=requests.get
	dill_loads=py.importF().dill_loads
	# get=HTTP.get_bytes
	if p:print('Getting...',U.stime()[15:20+2+4],url)
	b=HTTP.get_bytes(url,verify=False,timeout=timeout,proxies=proxies)
	if not b:return b
	if not py.isbytes(b):
		b=b.content
	if p:print('Loading...',U.stime()[15:20+2+4],'<%s B>'%py.len(b))
	if return_bytes:return b
	try:
		v= dill_loads(b)
		if p:print('Success !!',U.stime()[15:20+2+4],U.type(v),U.len(v))
		
		if ipy and U.get_ipy():
			U.get_ipy().user_ns[varname]=v
			return
		return v
	except Exception as e:
		if p:print('LoadErr ##',U.stime()[15:20+2+4],repr(e))
		else:
			return py.No(e,url,b)
rpc_get=rpc_get_var=rpcGetVariable=rpc_get_variable

# grpc_base=''

# class RPC:
	# def __init__(self,parent=None,name='',p=True):
		# self.__parent__=parent
		# self.__child__=None
		# self.__name__=name	
		# self.__v__=p
	# def __getattribute__(self, name):
		# U=py.importU()
		# if name in U.SKIP_ATTR_NAMES:
			# return
		# print(self,name)
		# return 

def rpc_get_variable_local(*names,ipy=True,port=DEFAULT_RPC_LOCAL_PORTS):
	if ipy:
		U,T,N,F=py.importUTNF()
		g=U.get_ipython()
	de={}
	vs=[]
	for name in names:
		v=rpc_get_variable(name,base=get_local_rpc_base(port))
		if ipy:
			g.user_ns[name]=v
		else:
			vs.append(v)
		if not v:
			de[name]=v
	if de:return py.No(de)
	if not ipy:
		if py.len(vs)==1:
			return vs[0]
		else:
			return vs
rpc_get_local=rpc_get_variable_local

def rpc_set_variable_local(**ka):
	U,T,N,F=py.importUTNF()
	base=N.get_local_rpc_base()
	for k,v in ka.items():
		# k
		rpc_set_variable(v,base=base,varname=k)
		
local_rpc_set=set_local_rpc=rpc_set_local=rpc_set_variable_local	
		
def rpc_set_variable(*obj,base=AUTO_GET_BASE,timeout=9,varname='v',ext_cmd='r=U.id({1})',print_req=False,pr=False,proxies=None,**ka):
	''' ext_cmd=  {0}  default is 'v'  , {1}  is ka k
	'''
	U,T,N,F=py.importUTNF()
	ext_cmd=U.get_duplicated_kargs(ka,'ext_cmd','cmd','extCmd','other_cmd',default=ext_cmd)
	varname=U.get_duplicated_kargs(ka,'v','V','name','var_name','var',default=varname)
	print_req=U.get_duplicated_kargs(ka,'print_req','pr',default=print_req)
	proxies=N.HTTP.auto_proxy_for_requests(proxies,ka)
	
	if ext_cmd:
		if '%s'     in ext_cmd:ext_cmd=ext_cmd%varname
		if '{0}'    in ext_cmd:ext_cmd=ext_cmd.format(varname)
		if '{name}' in ext_cmd:ext_cmd=ext_cmd.format(name=varname)

	if len(obj)==1 and ',' not in varname:
		obj=obj[0]
		
	if not obj:
		if py.len(ka)==1:
			varname,obj=U.get_dict_item(ka)	
		if py.len(ka)> 1:
			obj=ka
			if not ext_cmd:
				ext_cmd='globals().update(%s)'%varname
				
#numpy not y ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
	if varname!='v' and U.get_ipy() and  obj==(): 
		obj=U.get_ipy().user_ns[varname]
		
	if not base:
		base=get_remote_rpc_base(change=False)
	else:
		base=set_remote_rpc_base(base)
	url=('{0}{v}=F.dill_loads(request.get_data());'+ext_cmd).format(base,varname,varname=varname,v=varname)
	# import requests,dill
	# dill_loads=dill.loads
	# post=requests.post
	# post=HTTP.post
	# dill_dump=F.dill_dump
	if print_req=='url':
		print(url)
		print_req=''
	
	b=N.HTTP.post(url,data=F.dill_dump(obj),verify=False,timeout=timeout,proxies=proxies,print_req=print_req) # data=list:TypeError: cannot unpack non-iterable int object
	
	# if print_req:
		# print(U.v.N.HTTP.post(url,verify=False,timeout=timeout,proxies=proxies,print_req=print_req,data=U.v.F.dill_dump(obj)) )
		
	if not b:return b
	elif py.istr(b):
		pass
	elif not py.isbytes(b):
		b=b.content
	if py.isbytes(b):
		b= b.decode('utf-8')
	# if py.istr:
	return url,b
set_rpc=set_rpc_var=rpc_set=rpc_set_var=rpcSetVariable=rpc_set_variable

def rpc_get_file(filename,name='v',return_b=False,**ka):
	U,T,N,F=py.importUTNF()
	base=set_remote_rpc_base(**ka)
	u=base+'response.set_data(F.readb(N.geta()))%23-'+T.url_encode(filename)
	
	try:
		b=curl_return_bytes(u)
	except:
		b=N.HTTP.get_bytes(u)
	if py.isno(b):return b	
	
	f=F.write(filename,b)
	if return_b:
		return f,u,b
	return f	
	
def rpc_set_file(obj,filename=py.No('if obj exists: auto '),name='v',**ka):
	''' local_obj , remote_filename
'''	
	U,T,N,F=py.importUTNF()
	if py.istr(obj) and py.len(obj)<999 and F.exists(obj):
		if not filename:
			filename=F.get_filename_from_full_path(obj)
		obj=F.read_bytes(obj)
		
	return rpc_set_variable(obj,name=name,ext_cmd='r=F.write({filename!r},%s,mkdir=True)'.format(filename=filename),**ka)

def rpcServer(port=23571,thread=True,ip='0.0.0.0',ssl_context=(),currentThread=False,app=None,key=None,
execLocals=None,locals=None,globals=None,
qpsu='py,U,T,N,F',importMods='sys,os',request=True,
flaskArgs=None,no_banner=False,
	):
	'''N.rpcServer(globals=globals(),locals=locals(),)
	
	locals : execLocals
	if app : port useless
	key char must in T.alphanumeric
key compatibility :  key='#rpc\n'==chr(35)+'rpc'+chr(10)	
	ssl_context default use https port=443 
	
#TODO 分析请求代码中的变量，如果使用到了 p,response 才去赋值。没用到就不干扰	
	'''
	from threading import Thread
	U=py.importU()
	T=py.importT()
	# if not U.get('pformat_kw'):
		# U.set('pformat_kw',{'width':144})
	U.get_or_set('pformat_kw',{})['width']=333
	
	
	if not flaskArgs:
		flaskArgs=py.dict(debug=0,threaded=True)
	
	if execLocals:
		warnning='### deprecated args execLocals {ip}:{port}'.format(ip=ip,port=port)
		U.log(warnning)
		globals=execLocals
		locals={'warnning':warnning} #同时模仿以前可以保存变量的效果
		
	if not globals:globals={}
	
	for modName in importMods.split(','):
		globals[modName]=U.getMod(modName)
	if qpsu:
		for modName in qpsu.split(','):
			globals[modName]=U.getMod('qgb.'+modName)	
		
	from flask import Flask,make_response
	from flask import request as _request
	if no_banner:
		import flask.cli
		flask.cli.show_server_banner=lambda *a,**ka:print(a,ka)


	app=app or Flask('rpcServer'+U.stime_()   )
	
	def _flaskEval(code=None):
		nonlocal globals,locals 
		
		if U.is_vercel():#为了一个环境而在所有运行时去判断一次，
			payload = T.json_loads(_request.environ['event']['body'])
			_request.url=_request.url_root[:-1]+payload['path']
			code= payload['path'][1+py.len(key):]
			code=T.url_decode(code) # decode %23- to #- to ignore
			if code.endswith('/'):code=code[:-1]
		else:
			if not code:code=T.url_decode(_request.url)
			code=T.sub(code,_request.url_root )
			#url_root host_url 都可以  Win py3.74 flask 1.1.1 root_url 不存在？ 查了文档，确实只有 url_root
			# 所以，为了兼容性考虑 用 url_root
			if key and code.startswith(key):code=code[py.len(key):]
			
		# U.log( (('\n'+code) if '\n' in code else code)[:99]	)
		# U.ipyEmbed()()
		_response=make_response()
		_response.headers['X-XSS-Protection']=0
		_response.headers['Access-Control-Allow-Origin'] = '*'
		_response.headers['Content-Type'] = 'text/plain;charset=utf-8'
		
		if request:#rpcServer config
			globals['request']=_request
			globals['response']=_response
			globals['q']=_request
			globals['p']=_response
		if not globals:globals=None # 如果globals 为空dict，防止闭包保存变量，保持globals在每个请求重新为空这一特性
		r=U.execResult(code,globals=globals,locals=locals) #因为在这里一般指定了 不为None的 globals，所以在每个请求中可以共享 
		if (not _response.response) and (not _response.get_data()):
			_response.set_data(r)
		return _response
	
	if py.istr(key):
		if py.len(key)<1:return py.No('key length < 1',key)
		U.set('rpc.server.base','/'+key,level=1) # 1 py,process
		# for i in key:
			# if i not in T.alphanumeric:
				# return py.No('key char must in T.alphanumeric',key)
		
		@app.route('/'+key+'<path:text>',
			methods=['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE', 'HEAD', 'PATCH'])
		def flaskEval(*a,**ka):return _flaskEval()
	else:
		U.set('rpc.server.base','/',level=1) # 1 py,process
		@app.errorhandler(404)
		def flaskEval(*a,**ka):return _flaskEval()
		
	if not app.name.startswith('rpcServer'):
		return (py.No('caller provide app,so no thread start'),app)
	
	flaskArgs.update(py.dict(host=ip,port=port) ) #可变dict，不能用flaskArgs=
	
	if ssl_context:
		flaskArgs['ssl_context']=ssl_context
		if port==23571:
			port=443
			flaskArgs['port']=port
	# U.log(flaskArgs)
	U.set('rpc.server.port',port)
	if currentThread or not thread:
		U.set('rpc.server.app',app)
		U.set(app.name,app)
		return app.run(**flaskArgs)
	else:
		t= Thread(target=app.run,name='qgb thread '+app.name,kwargs=flaskArgs)
		t.start()
		return (t,app)
########### flaskEval end ###########	
	if py.is3():from http.server import BaseHTTPRequestHandler as h
	class H(SimpleHTTPRequestHandler):
		def do_GET(s):
			code=s.path[1:]
			try:
				r=execResult(code)
				s.send_response(200)
			except Exception as e:
				s.send_response(500)
				
			s.send_header("Content-type", "text/plain")
			s.end_headers()		
			
			if not py.istr(r):
				r=repr(r)
			if py.is3():
				r=r.encode('utf8')
			s.wfile.write(r)
	

		
	# with _HTTPServer((ip,port), H) as httpd:
		# sa = httpd.socket.getsockname()
		# serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
		# print(serve_message.format(host=sa[0], port=sa[1]))
		# try:
			# if currentThread or not thread:httpd.serve_forever()
			# else:
				# t= Thread(target=httpd.serve_forever,name='qgb.rpcServer '+U.stime() )
				# t.start()
				# return t
				
		# except KeyboardInterrupt:
			# print("\nKeyboard interrupt received, exiting.")
	
# class rpcServer(HTTPHandler):
	# def __init__
		# super()
		
	
def rpcClient(url_or_port='http://127.0.0.1:23571',code=''):
	if py.isint(url_or_port):
		url='http://127.0.0.1:'+py.str(url_or_port)
	else:
		url=py.str(url_or_port)
	if not url.endswith('/'):url+='/'
	T=py.importT()
	code=T.urlEncode(code)
	return get(url+code)
	# if py.is3():
		# from xmlrpc.client import ServerProxy,MultiCall
	# server = ServerProxy(url)
	# return server

def parse_pem(pem_str_or_bytes):
	if py.istr(pem_str_or_bytes):
		pem_bytes=pem_str_or_bytes.encode('utf-8')
	elif py.isbytes(pem_str_or_bytes):
		pem_bytes=pem_str_or_bytes
	else:
		raise py.ArgumentError()
	import pem
	list= pem.parse(pem_bytes)
	if py.len(list)==1:
		return list[0]
	else:
		return list
	# with open('cert.pem', 'rb') as f:
	# 	certs = pem.parse(f.read())

def get_all_socket_obj():
	import socket
	return U.get_objects(socket.socket) 
get_socket_all_obj=get_all_socket_obj

def get_socket_req(PORT = 65432,HOST = '127.7.7.7'):
	import socket
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		req, addr = s.accept()
		return req, addr

# LOG_REQ_ENABLE=py.No('')
def flask_kill_server_in_request(pid=None):
	U,T,N,F=py.importUTNF()
	import socketserver
	return U.get_objects(socketserver.BaseServer)
	import os,signal
	if not pid:
		pid=os.getpid()

	sig = getattr(signal, "SIGKILL", signal.SIGTERM)
	os.kill(pid, sig)
	
shutdown=shutdown_flask=flask_shutdown=flask_kill_server=flask_kill_server_in_request

def flask_app_route(app,rule='',view_func=None,methods=('GET','POST'),log_req=False,**ka):
	if not rule:raise py.ArgumentError(rule)
	
	U,T,N,F=py.importUTNF()
	
	log_req=U.get_duplicated_kargs(ka,'req_log','log_req','log',default=log_req)
	
	# , endpoint=U.stime()
	if rule and not view_func:
		if py.isdict(rule):
			for u,v in rule.items():
				flask_app_route(app,rule=u,view_func=v)
			return app.url_map._rules
		
	if py.istr(view_func):
		# view_func=lambda :py.str(view_func) # 不能这样写 ，总是返回重新赋值后 的 view_func
		U.set(py.hex(py.id(app))+rule,view_func)
		def _func():
			if log_req:
				flask_request_log(url=True)
			return U.get(py.hex(py.id(app))+rule)
		view_func=_func	
		# view_func=lambda :U.get(py.hex(py.id(app))+rule)
	
	if not view_func:raise py.ArgumentError(view_func)
	
	app.add_url_rule(rule, view_func=view_func, methods=methods,endpoint=rule)
	
	return app.url_map._rules
	
flask_url_map=app_route=app_router=flask_app_route	

def get_flask_request_post_data(name='y',time=False,save_dill=True,ipy_var=True,return_value=False,**ka):
	from flask import request as q
	U,T,N,F=py.importUTNF()
	save_dill=U.get_duplicated_kargs(ka,'save_dill','dill','save','write','dp',default=save_dill)
	return_value=U.get_duplicated_kargs(ka,'return_value','v','value','only_value','get_value',default=return_value)
	if ka:raise py.NotImplementedError(ka)
	
	b=q.data
	y=T.js_loads(b)#demjson
	
	if ipy_var:
		name=T.varname(name)
		U.get_ipy().user_ns[name]=y
	if return_value:
		return y
	f=f'{name}-{U.len(y)}'
	if time:f+=f'={U.stime()}'
	if save_dill:
		return F.dill_dump(obj=y,file=f'C:/test/{f}.dill')
	else:
		return U.StrRepr('# '+f)
rec=recv=recive=receive=get_flask_request_post_data


def get_flask_request_a(request=None,return_other_url=False,return_request=False,raise_err=False,**ka):
	''' #TODO raise_err
a=T.subr(u,T.u23)#'%23-'	

pythonAnywhere : multi[ // or  %2F%2F%2F%2F%2F ] in url will auto convert to one / ,it can't bypass

vercel : !curl -vvvik "https://vercel-django-example-ten.vercel.app/r=T.az%23-/a"   
< HTTP/1.1 308 Permanent Redirect
< location: /r=T.az%23-/a/
< Refresh: 0;url=/r=T.az%23-/a/

	'''
	U,T,N,F=py.importUTNF()
	def _return(ax):
		nonlocal u,return_other_url,U,request
		if return_other_url:
			if py.isdict(return_other_url):
				ro_url_decode=U.get_duplicated_kargs(return_other_url,'url_decode','decode','urlDecode','urldecode')
				ro_23=U.get_duplicated_kargs(return_other_url,'%23','%23-','_23','add_23')
			else:
				ro_url_decode,ro_23=False,False
				
			if ax:u=u[:0-py.len(ax)]	
			if ro_23:
				if '%23' in u[-4:]:
					if ro_url_decode:
						u=T.url_decode(T.sub_tail(u,'','%23'))+'%23-'
					else:
						u
				else:
					if ro_url_decode:
						u=T.url_decode(u)+'%23-'
					else:	
						u+='%23-'
						
						
			if ax:
				return_r= u,T.url_decode(ax)
			else:
				return_r=  u,ax
		else: #return_other_url
			if ax:return_r=  T.url_decode(ax)
			else :return_r=ax
		if return_request:	
			return_r=py.list(return_r)
			return_r.insert(0,request)
		return return_r
		
	u=''
	if py.istr(request):return _return(request)
	if not request:from flask import request
	if py.islist(request):
		try:
			for index,name,value in request:
				if name=='url':
					u=value
					break
		except Exception as e:
			return _return( py.No(e) )
	# elif py.isdict(request) and 'PATH_INFO' in request: # wsgi def app(env,start_response):
		# u=request['PATH_INFO']  #  'PATH_INFO': '/r=env%23-4/',not %2523
	else:
		try:
			u=request.url
		except RuntimeError as e:
			return _return( py.No(e) )
		
	U,T,N,F=py.importUTNF()
	return_other_url =U.get_duplicated_kargs(ka,'return_other_url','return_head_code','return_url','return_head_url','return_url_head','return_front_url',default=return_other_url)
	
	
	if '%23=' in u:
		a=T.sub_tail(u,'%23=')
	elif '%23-' in u:
		a=T.sub_tail(u,'%23-')
	elif '#-' in u: # pythonAnywhere
		a=T.sub_tail(u,'#-')
	elif '%2523-' in u: # vercel
		a=T.sub_tail(u,'%2523-')
	else:
		if '%23' not in u:
			msg_23='%23 not in request.url'
			if raise_err:
				raise py.ArgumentError(msg_23)
			else:
				return _return( py.No(msg_23) )
		a=T.sub_tail(u,'%23')
		
	if U.is_vercel(): #todo 速度优化
		if a.endswith('/'):
			a=a[:-1]
		hs=['https:/','http:/']
		for v in hs:
			if v in a and v+'/' not in a:
				a=a.replace(v,v+'/')
		
		
		
	
	return _return(a )
geta=get_a=get_request_a=get_rpc_request_a=get_flask_request_a

def get_flask_request_a_file(request=None,raise_err=False):
	''' 很奇怪,移动版 Yandex 浏览器 在下载大文件时，手动暂停。原来大文件url地址（192.168.1.3）端口 就彻底无法访问了，换同地址的其他端口可以访问。
但是将原大文件url放在其他端口url后面也会导致该 地址无法访问。去除大文件url后面5个字符（此时len(a)==38），放在后面可以访问。去除4个字符，不能访问 
一直显示黄色进度条，最后报 【192.168.1.3 没有发送任何数据】
去除5个字符，后面随便加其他字符只要不和大文件url原位置字符相同，照样可以访问。

重启everything后，原来大文件端口可以访问，但是原url依旧不能访问
移动端换浏览器，可以正常下载
	
	'''
	U,T,N,F=py.importUTNF()
	a=N.get_flask_request_a(request=request,raise_err=raise_err)
	if not a:
		if raise_err:raise py.ArgumentError('not N.geta()')
		else:return py.No('not N.geta()')
	if a.startswith('http://'):
		file=T.get_url_full_path(a)
	else:
		file=a
		
	return file	
		
getaf=getafile=get_flask_request_a_file

def get_flask_request_file(q):
	''' dir(f)  
[__...,'_parse_content_type', '_parsed_content_type', 'close', 'content_length', 'content_type', 'filename', 'headers', 'mimetype', 'mimetype_params', 'name', 'save', 'stream']
'''	
	f=q.files['file']
	r=f.save(dp+f.filename)  # None
	return f,r

def pdf2html(url,response=None,zoom=None,path=None,pw=None):
	U,T,N,F=py.importUTNF()
	if not zoom:
		zoom=U.get('pdf2html_zoom',1)
	if not path:
		path=U.get('pdf2html_path','/root/pdf/')
	U.cd(path)
	fn=T.url2fn(url[-200:])
	if not fn.lower().endswith('.pdf'):fn+='.pdf'

	def do_resp(a):
		if not response:return a
		if not (py.istr(a) or py.isbytes(a)):
			a=T.pformat(a)
			response.set_data(a)	
		else:
			response.headers['Content-Type']='text/html;charset=utf-8';
			response.set_data(a)	
		return a
	
	if not F.exists(path+fn):
		U.cmd('wget','-O',fn, url,timeout=30)
		# b=N.HTTP.getBytes(url)
		# if not b:return do_resp(b)
		# U.pln(F.write(path+fn,b))
	html_file=path+fn[:-4]+'.html'
	if not F.exists(html_file):
		if not pw:
			pw=U.get('sudo_pw')
		if not pw:
			return do_resp('wocao,no pw')
	# -it : the input device is not a TTY
		cmd='docker run --rm -v {path}:/pdf bwits/pdf2htmlex pdf2htmlEX --no-drm 1 --zoom {zoom} {fn}'
		cmd=cmd.format(path=path,fn=fn,zoom=zoom)
		U.sudo(password=pw,cmd=cmd)
	if not F.exists(html_file):
		fs=F.ls(path,f=1)
		return do_resp(['not found html of pdf : ',fn,
		U.v.U.sudo(password=pw,cmd=cmd),fs])
	else:
		return do_resp(F.read(html_file))

def flask_text_response(response,data='',encoding=py.No('auto',no_raise=1),file='',download_char='\x02\x06\x0f\x11\x12\x19\x1c\x1e'):
	''' 手机浏览器 保存链接  如果是 utf-8 乱码 ，gb18030 正常
	
'''	
	U,T,N,F=py.importUTNF()
	if py.istr(data):
		if U.one_in(download_char,data):
			response.headers['Content-Type']='text/html;charset=utf-8';
		else:
			response.headers['Content-Type']='text/plain;charset=utf-8'	
		if encoding:
			response.headers['Content-Type']=response.headers['Content-Type'].replace('utf-8',encoding)
			data=data.encode(encoding)
	elif py.isbyte(data):
		if not encoding:encoding=T.detect(data[:9999])
		response.headers['Content-Type']='text/plain;charset=%s'%(
			encoding if encoding else 'latin')
	else:
		data=T.pformat(data)
		response.headers['Content-Type']='text/plain;charset=utf-8'	
	response.set_data(data)
	return response
txt=text=flask_text_response
	
CSS_FONT=r'''*{
 font-size: 50%;
 /*font-family: Arial;*/
}'''
def flask_html_response(response,html='',file='',remove_tag=(
		['<script','</script>'],
['<SCRIPT','</SCRIPT>'],'ondragstart=','oncopy=','oncut=','oncontextmenu=','"return false;"',
	),encoding='utf-8',splitor='<hr>',content_type='text/html;charset=utf-8',
	css='',eol='',
	**ka):
	'''
Resource interpreted as Stylesheet but transferred with MIME type text/html:
不正确设置 type可能导致页面无法正常显示
'''	
	U,T,N,F=py.importUTNF()
	if U.get_duplicated_kargs(ka,'remove_script','del_script','no_script'):
		remove_tag=(
['<script','</script>'], ['<SCRIPT','</SCRIPT>'],
		)
		
	if not html and file:
		import mimetypes
		content_type = (
			 mimetypes.guess_type(file)[0] or content_type #"application/octet-stream"
				)
		# ext= T.subLast(file,'.').lower()
		if 'text' in content_type:
			fencoding=F.detect_encoding(file,print_detect_encoding=False)
			if not fencoding:fencoding=encoding
			content_type+=';charset=%s'%(fencoding,)
		html=F.read_bytes(file)
	if py.istr(html):
		pass
	elif py.isbyte(html):#TODO byte remove tag,no convert
		if remove_tag:html=html.decode(encoding)
		pass
	elif U.iterable(html):#TODO byte remove tag,no convert
		html=splitor.join( py.str(i) for i in html )
	else:#if not py.istr(html):
		html=py.str(html)
	
	if eol:
		if T.CRLF in html:
			html=html.replace(T.CRLF,eol)
		else:
			html=html.replace(T.EOL,eol)
	if remove_tag:
		for itag in remove_tag:
			if py.istr(itag):
				html=html.replace(itag,'')
				continue
			if py.len(itag)==2:
				start,end=itag
			s=True
			while s:
				s=T.sub(html,start,end)
				if not s:break
				html=html.replace(start+s+end,'')
	if css:
		if '</style>' not in css:
			css='''<style type="text/css">
{}		
</style>		'''.format(css)
		html=css+html #TODO parse html and insert to HEAD
		
		
	if not response:
		return html
	response.headers['Content-Type']=content_type;
	response.set_data(html)
	return response
html=htmlp=response_html=html_response=flask_html_response

def get_chunk(full_path,byte1, byte2=None,):
	 # = "try2.mp4"
	file_size = os.stat(full_path).st_size
	start = 0
	length = 102400

	if byte1 < file_size:
		start = byte1
	if byte2:
		length = byte2 + 1 - byte1
	else:
		length = file_size - start

	with open(full_path, 'rb') as f:
		f.seek(start)
		chunk = f.read(length)
	return chunk, start, length, file_size

def flask_get_request_range(request):
	import re
	range_header = request.headers.get('Range', None)
	if not range_header:
		range_header = request.headers.get('range', None)
	byte1, byte2 = 0, None
	if range_header:
		match = re.search(r'(\d+)-(\d*)', range_header)
		groups = match.groups()

		if groups[0]:
			byte1 = int(groups[0])
		if groups[1]:
			byte2 = int(groups[1])
	return byte1,byte2
	# raise py.ArgumentError(request)
get_request_range=flask_get_request_range
	
def flask_media_stream_response(request,response,file=None,):		
	from flask import stream_with_context
	U,T,N,F=py.importUTNF()
	if not file:
		file=get_flask_request_a(request)					
	import re
	range_header = request.headers.get('Range', None)
	byte1, byte2 = 0, None
	if  range_header:
		match = re.search(r'(\d+)-(\d*)', range_header)
		groups = match.groups()

		if groups[0]:
			byte1 = int(groups[0])
		if groups[1]:
			byte2 = int(groups[1])
			
	gen=F.read_as_stream(file,start=byte1) # 这里不会出错，iter generator 才 服务器内部错误
	try:
		py.next(gen)
		response.response=stream_with_context(gen)
		response.headers['Content-Type'] = 'video/mp4'
		response.headers['mimetype'] = 'video/mp4'
		if range_header:
			response.headers.add('Content-Range', 'bytes {0}-'.format(byte1
		#, byte1 + length - 1, file_size
			))
			if byte1>0:
				response.status_code = 206

	except Exception as e:
		# r=T.pformat([e,U.get_tb_stack()],**U.get('pformat_kw',{}))
		r=py.repr(e)
		response.set_data(r)
	return	

	chunk, start, length, file_size = get_chunk(byte1, byte2)
	resp = Response(chunk, 206, mimetype='video/mp4',
					  content_type='video/mp4', direct_passthrough=True)
	resp.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
	return resp	
	
mp4_response=media_response=flask_media_stream_response
	
def flask_file_stream_response(response,file=py.No('if not file:use N.geta()'),):
	'''
< HTTP/1.0 200 OK
< Content-Type: text/plain;charset=utf-8
< X-XSS-Protection: 0
< Access-Control-Allow-Origin: *
< Content-Disposition: inline; filename=typescript-4.8.3.tgz
< Content-Length: <11.389 MiB>
< Server: Werkzeug/1.0.1 Python/3.8.5
< Date: Thu, 06 Oct 2022 17:17:38 GMT
	
	Parse Error: Invalid character in Content-Length".
	
'''	
	from flask import stream_with_context,request
	U,T,N,F=py.importUTNF()
	if not file:
		file=N.get_flask_request_a_file(request)

	# try:
	range=get_request_range(request)
	# request.headers.get('Range','')
	# if range:
		
	gen=F.read_file_as_stream(file) # 这里不会出错，iter generator 才 服务器内部错误
	try:
		py.next(gen)
		response.response=stream_with_context(gen)
		# 不获取filename, 保存文件名是 D__test_7C_荣耀7C-LND-B202_8.0.zip
		# 不进行url_encode,chrome ERR_RESPONSE_HEADERS_TRUNCATED
		# response.headers['Content-Disposition'] = "inline; filename=" + T.url_encode(file)
		response.headers['Content-Disposition'] ="inline; filename=" + T.url_encode(F.get_filename_from_full_path(file))
		response.headers['Content-Length'] =F.size(file,int=True)
		
	except Exception as e:
		# r=T.pformat([e,U.get_tb_stack()],**U.get('pformat_kw',{}))
		response.status_code=500
		r=py.repr(e)
		response.set_data(r)
file=stream_file=file_stream=read_as_stream=read_file_as_stream=flask_file_stream_response

def flask_image_response(response,image,format='png',**ka):
	if not response:return image
	if py.isbytes(image):
		bytes=image
	else:
		U,T,N,F=py.importUTNF()
		if U.is_numpy_ndarray(image):
			from qgb import pil
			bytes=pil.cv2_image_to_bytes(image)
		else:
			from io import BytesIO
			img_io = BytesIO()
			image.save(img_io, format)
			img_io.seek(0)
			# response.response=stream_with_context(gen)
			bytes=img_io.read(-1)
	ctype='image/'+format
	response.headers['Content-Type'] = ctype
	response.headers['mimetype'] = ctype
	response.set_data(bytes)
	return bytes  # huawei Android 旧版 系统浏览器，如果url 不是 .png等 结尾。不会显示图像
	# return response,image,bytes

def flask_screenshot_response(response,rect=py.No('rect=[x,y,x1,y1] or auto get clipboard or full_screen '),transform_function=None,transform_function_ka={},**ka):
	''' rect (crop)  defining the left, upper, right, and lower pixel

Image.open(io.BytesIO(b ))	
Image.open(fp)	
:param fp: A filename (string), pathlib.Path object or a file object.
   The file object must implement `~file.read`,
   `~file.seek`, and `~file.tell` methods,
   and be opened in binary mode.	
   
[20, 'FLIP_LEFT_RIGHT', 0],
[21, 'FLIP_TOP_BOTTOM', 1],
[51, 'ROTATE_90', 2], 
[49, 'ROTATE_180', 3],
[50, 'ROTATE_270', 4],
	'''
	U,T,N,F=py.importUTNF()
	try:
		from PIL import Image
		if U.isWin() or U.isMac():
			from PIL import ImageGrab
	except Exception as e:
		U.log(e)
		Image=None
	transform_function=U.get_duplicated_kargs(ka,
		'f','func','function','operator','transform','transformation_function',default=transform_function)#TODO 名称长的别名应该在前，这样匹配时先详细后模糊
#fix numpy.ndarray ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
	if U.is_numpy_ndarray(rect) or rect: 
		if py.istr(rect) or py.isfile(rect):
			# if F.exist(rect):
			image=rect
			if py.istr(image) and image.startswith('data:image'):
				response.headers['Content-Type'] = 'text/html'
				response.set_data('''<img src="{}"></img>'''.format(image) )
				return image
			im=Image.open(rect)
		# elif Image and (py.isinstance(rect,Image.Image) or py.isbytes(rect) ):
			# im=rect
		elif (py.istuple(rect) or py.islist(rect)) and U.len(rect)==4:
			im = ImageGrab.grab(rect)
			# raise py.ArgumentError('rect must be PIL Image or [ x0,y0,x1,y1 ]')
		elif py.callable(transform_function):
			from qgb import pil
			if py.isbyte(rect):
				im=pil.bytes_to_pil_image(rect)
			# if 	
			else:
				raise py.NotImplementedError()
		else:
		
			im=rect
	else:	
		if U.is_termux() and U.is_root():
			f=U.gst+'screencap.png'
			U.cmd('/system/bin/screencap','-p',f)
			im=F.read_bytes(f)
		else:
			im = ImageGrab.grabclipboard()
#wechat img copy: ['C:\\Users\\qgb\\AppData\\Local\\Temp\\WeChat Files\\8ed1d25c76c76c2ef4f2e53deee64d0.jpg']
			if py.islist(im):im=im[0]
			if not im:
				im=ImageGrab.grab()
	if Image and py.isinstance(im,Image.Image) and py.callable(transform_function):
		im=transform_function(im,**transform_function_ka)
	return flask_image_response(response,im)
img=screenshot=screenshot_response=flask_screenshot_response
	
def is_flask_request(q):
	from werkzeug.local import LocalProxy
	return isinstance(q,LocalProxy)

def set_proxy(host='',port='',protocol='socks5h',target_protocol=('http','https'),**ka):
	''' no args provide,proxy will clean
'proxies','proxy','ip'  =py.No('duplicated arg:host')	
	'''
	U,T,N,F=py.importUTNF()
	d={}
	proxies=U.get_duplicated_kargs(ka,'proxies','proxy','ip')
	if not host and proxies:
		host=proxies
	if py.isint(host) and not port:
		port=host
		host='127.0.0.1'
	if py.isdict(host):
		for k,v in host.items():
			d.update( set_proxy(v,target_protocol=k) ) # 递归
		return d
	
	host=host.strip()
	if '://' in host:
		protocol=T.sub(host,'','://')
		host=T.sub(host,'://','')
	if ':' in host:
		port=T.subLast(host,':','')
		host=T.subLast(host,'',':')

	if py.istr(target_protocol):
		target_protocol=[target_protocol]
	for t in target_protocol:
		# if not ip:
		if not host or not port or not protocol:
			# 跳过格式不对的代理
			continue
		host=U.set('{}.proxy.host'.format(t),host)
		port=U.set('{}.proxy.port'.format(t),port)
		protocol=U.set('{}.proxy.protocol'.format(t),protocol)
		d[t]="{}://{}:{}".format(protocol,host,port)	

	for t in target_protocol:
		if t not in d:
			print('delete:',U.delset_prefix(f'{t}.proxy',confirm=False))
			
	return d
	# {'http': "socks5://myproxy:9191"}
setProxy=set_proxy

def get_proxy(target_protocol=('http','https'), ):
	U,T,N,F=py.importUTNF()
	d={}
	for t in target_protocol:
		host=U.get('{}.proxy.host'.format(t),)
		port=U.get('{}.proxy.port'.format(t),)
		protocol=U.get('{}.proxy.protocol'.format(t),)
		if not host or not port or not protocol:continue
		d[t]="{}://{}:{}".format(protocol,host,port)
	return d
getProxy=get_proxy

def get(url,protocol='http',**ka):
	U,T,N,F=py.importUTNF()
	if F.exist(url):
		return F.read(url)
	if '://' in url:
		p=T.sub(url,'',':')
		if p:protocol=p
		else:raise U.ArgsErr(url)
	else:url=protocol+'://'+url
	if url.startswith('http'):
		# import HTTP
		return HTTP.get(url,**ka)	

def http(url,method='get',*args):
	return HTTP.method(url,method,*args)

def ipToInt(ip):
	ips=ip.split('.')
	if py.len(ips)!=4:return py.No('ip format err',ip)
	r=0
	for n,s in py.enumerate(ips):
		i=py.int(s)
		r+=i*256**(3-n)
	return r
ip_int=ip2int=ipToInt

def ip_location(ip,reverse_ip=False,size=68,
junk=['本机地址','IANA 保留地址','局域网 IP','局域网 对方和您在同一内部网'] ):
	global U,T,N,F
	if size:U,T,N,F=py.importUTNF()

	# port=''
	# if ':' in ip:
		# ip,port=ip.split(':')
		# port=':'+port
	ipq=ip_location_qqwry(ip)
	if not ipq:return ipq
	location=' '.join(ipq)
	location=location.replace('CZ88.NET','').strip() #去除包含的
	
	if location in junk:
		if size:
			return U.StrRepr(ip,size=size)
		return ip
		location=py.No(location)	
	if reverse_ip:
		r='%-15s [%s] '%(ip,location)
		if size:
			r=U.StrRepr(r,size=size)
	else:
		r=location
		if (size-15)>0:
			r=U.StrRepr(r,size=size-15)
	return r
	

sip_location=sipLocation=ipLocation=ip_location

######################  qqwry   ###########################
gw_qqwry=['CoreLink骨干网', '不丹', '东帝汶', '中非', '丹麦', '乌克兰', '乌兹别克斯坦', '乌干达', '乌拉圭', '乍得', '也门', '亚太地区', '亚洲', '亚美尼亚', '以色列', '伊拉克', '伊朗', '伯利兹', '佛得角', '俄罗斯', '保加利亚', '克罗地亚', '关岛', '冈比亚', '冰岛', '几内亚', '几内亚比绍', '列支敦士登', '刚果共和国', '刚果民主共和国', '利比亚', '利比里亚', '加勒比海地区', '加拿大', '加纳', '加蓬', '匈牙利', '北美地区', '北马其顿', '北马里亚纳群岛', '南极洲', '南苏丹', '南非', '博茨瓦纳', '卡塔尔', '卢旺达', '卢森堡', '印尼', '印度', '印度尼西亚', '危地马拉', '厄瓜多尔', '厄立特里亚', '叙利亚', '古巴', 
'台湾省', '台湾省云林县', '台湾省南投县', '台湾省南投县南投市', '台湾省台东县', '台湾省台中市', '台湾省台北市', '台湾省台南市', '台湾省嘉义县', '台湾省嘉义市', '台湾省基隆市', '台湾省宜兰县', '台湾省屏东县', '台湾省彰化县', '台湾省新北市', '台湾省新竹县', '台湾省新竹市', '台湾省桃园市', '台湾省澎湖县', '台湾省花莲县', '台湾省苗栗县', '台湾省金门县', '台湾省高雄市', 
'吉尔吉斯斯坦', '吉布提', '哈萨克斯坦', '哥伦比亚', '哥斯达黎加', '喀麦隆', '图瓦卢', '土库曼斯坦', '土耳其', '圣卢西亚', '圣基茨和尼维斯', '圣多美和普林西比', '圣巴泰勒米', '圣文森特和格林纳丁斯', '圣皮埃尔和密克隆群岛', '圣诞岛', '圣马力诺', '圭亚那', '坦桑尼亚', '埃及', '埃塞俄比亚', '基里巴斯', '塔吉克斯坦', '塞内加尔', '塞尔维亚', '塞拉利昂', '塞浦路斯', '塞舌尔', '墨西哥', '多哥', '多米尼克', '多米尼加', '奥兰群岛', '奥地利', '委内瑞拉', '孟加拉', '孟加拉国', '安哥拉', '安圭拉', '安提瓜和巴布达', '安道尔', '密克罗尼西亚联邦', '尼加拉瓜', '尼日利亚', '尼日尔', '尼泊尔', '巴勒斯坦', '巴哈马', '巴基斯坦', '巴巴多斯', '巴布亚新几内亚', '巴拉圭', '巴拿马', '巴林', '巴西', '布基纳法索', '布隆迪', '希腊', '帕劳', '库克群岛', '库拉索', '开曼群岛', '德国', '意大利', '所罗门群岛', '托克劳', '拉美地区', '拉脱维亚', '挪威', '捷克', '摩尔多瓦', '摩洛哥', '摩纳哥', '文莱', '斐济', '斯威士兰', '斯洛伐克', '斯洛文尼亚', '斯里兰卡', '新加坡', '新喀里多尼亚', '新西兰', '日本', '智利', '朝鲜', '柬埔寨', '根西岛', '格林纳达', '格陵兰', '格鲁吉亚', '梵蒂冈', '欧洲', '欧洲地区', '欧盟', '欧美地区', '比利时', '毛里塔尼亚', '毛里求斯', '汤加', '沙特阿拉伯', '法国', '法属圣马丁', '法属圭亚那', '法属波利尼西亚', '法罗群岛', '波兰', '波多黎各', '波斯尼亚和黑塞哥维那', '泰国', '泽西岛', '津巴布韦', '洪都拉斯', '海地', '澳大利亚', '澳洲', '澳门', '爱尔兰', '爱沙尼亚', '牙买加', '特克斯和凯科斯群岛', '特立尼达和多巴哥', '玻利维亚', '瑙鲁', '瑞典', '瑞士', '瓜德罗普', '瓦利斯和富图纳群岛', '瓦努阿图', '留尼汪岛', '白俄罗斯', '百慕大', '直布罗陀', '福克兰群岛', '科威特', '科摩罗', '科特迪瓦', '科索沃', '秘鲁', '突尼斯', '立陶宛', '索马里', '约旦', '纳米比亚', '纽埃', '缅甸', '罗马尼亚', '美国', '美属维尔京群岛', '美属萨摩亚', '美洲地区', '老挝', '肯尼亚', '芬兰', '苏丹', '苏里南', '英国', '英属印度洋领地', '英属维尔京群岛', '荷兰', '荷兰加勒比', '荷兰省', '荷属圣马丁', '莫桑比克', '莱索托', '菲律宾', '萨尔瓦多', '萨摩亚', '葡萄牙', '蒙古 ', '蒙特塞拉特岛', '西班牙', '诺福克岛', '贝宁', '赞比亚', '赤道几内亚', '越南', '阿塞拜疆', '阿富汗', '阿尔及利亚', '阿尔巴尼亚', '阿曼', '阿根廷', '阿联酋', '阿鲁巴', '非洲地区', '韩国', '韩国首尔', '香港', '马尔代夫', '马恩岛', '马拉维', '马提尼克', '马来西亚', '马约特', '马绍尔群岛', '马耳他', '马达加斯加', '马里', '黎巴嫩', '黑山'] 
#278

g_reserved_qqwry=[ 'IANA机构', 'IANA保留地址', '运营商级NAT','本机地址', '本地', 'IANA', '局域网']
# 7
	
gn_qqwry=['上海', '云南', '内蒙古', '北京', '南京', '吉林', '四川', '天津', '宁夏', '安徽', '山东', '山西', '广东', '广西', '新疆', '江苏', '江西', '河北', '河南', '浙江', '海南', '湖北', '湖南', '甘肃', '福建', '西藏', '贵州', '辽宁', '重庆', '陕西', '青海', '黑龙江', '东北三省', '广州市清', '长春工业', '西安石油', '北方工业', '首都经贸', '首都师范', '宁波大学', '华中农业', '中国人民', '华东师范', '中南大学', '长江大学', '东北农业', '对外经济', '东华大学', '华南理工', '华中科技', '武汉大学', '大连理工', '南开大学', '中国', '中国青岛嘉华网络BGP', '中国农业科学院', '雅虎中国', '雅虎中国公司', '中国CEI(中国经济信息网)骨干网', '中国国际电子商务中心', '中国电信', '南昌理工学院', '电信'] 
#63
# 203.14.187.0-255 ('电信', ' CZ88.NET')

	
def ip_location_qqwry(ip,dat_path=py.No('auto get or gst',no_raise=1),):
	'''return ('地区' , '运营商')
if want update qqwry.dat , reloa N module,and call this with dat_path !!!
warnning: NOT thread safe !!!

pip install qqwry-py3

pip install qqwry  # Not have cz88update
	'''	
	
	import qqwry
	U=py.importU()
	QQwry=U.get('QQwry')
	if not QQwry:
		F=py.importF()
		
		dat_path=dat_path or U.get('qqwry.dat') # value or not py.isNo(value) :
		if not dat_path:
			# fgst=py.importU().gst+'qqwry.dat'
			# if F.exist( fgst ):
				# dat_path=fgst
			if U.isWin():
				qqwry_path=r'C:\Program Files (x86)\cz88.net\ip\qqwry.dat'
				if F.exist(qqwry_path):
					dat_path=qqwry_path
			if not dat_path:
				dat_path=U.get_gst(base_gst=1)+'qqwry.dat'
				
		if not F.exist(dat_path):
			U.log(['updateQQwry length:', qqwry.updateQQwry(dat_path)] )
			
		QQwry = qqwry.QQwry()
		QQwry.load_file(dat_path,loadindex=True)
		U.set('QQwry',QQwry)
		U.set('qqwry.dat',dat_path)
	
	r=QQwry.lookup(ip)  #('北京市', '联通')
	if not r:
		return py.No('NotFound %s'%ip,QQwry,U.stime())
	return r	

###################  qqwry end ###########################
def address_coordinate(address,raw_response=True):
	import requests
	cookies = {
		'BAIDUID': '7240C1BD73BF5509083867D8372AA3C8:FG=1',
		'PSTM': '1547906786',
		'BDUSS': 'dnamEzZk5OT3N6R3J2QnJVckMtdjdIMm54ZjY3VWNsTGQ5SmtodjVOS2JaOE5jQVFBQUFBJCQAAAAAAAAAAAEAAACYT6sRUUdCQ1MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJvam1yb2ptcaV',
		'MCITY': '-%3A',
		'H_WISE_SIDS': '131410_126124_128701_129321_114744_128142_120764_120189_131601_118886_118868_131402_118843_118833_118797_130762_131650_131577_131535_131534_131529_130222_131390_129565_107320_131394_130123_131518_131240_131195_117327_130347_117436_130075_129647_124635_130690_131435_131687_131036_131047_129981_130989_129901_129479_129646_124802_131467_131424_110085_127969_131506_123290_131094_131297_128200_131550_131264_131262_128600',
		'BIDUPSID': '2DD44AA3F0CF69531B5E310CF80AEBD8',
		'pgv_pvi': '6249972736',
		'pgv_si': 's660814848',
		'ZD_ENTRY': 'google',
		'H_PS_PSSID': '1453_21112_18560_29523_29521_29720_29568_29220_22159',
	}
	headers = {
		'Pragma': 'no-cache',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 YaBrowser/19.3.1.779 Yowser/2.5 Safari/537.36',
		'Accept': '*/*',
		'Referer': 'https://maplocation.sjfkai.com/',
		'Connection': 'keep-alive',
		'Cache-Control': 'no-cache',
	}
	# '湖南省长沙市长沙县长沙经济技术开发区开元东路华润置地广场一期12幢'
	params=(('address', address),
	('output', 'json'),
	('ak', 'gQsCAgCrWsuN99ggSIjGn5nO'),
	('callback', 'showLocation0'))

	response = requests.get('https://api.map.baidu.com/geocoder/v2/', headers=headers, params=params, cookies=cookies)
	s=response.content.decode('utf-8')
	s=s.replace('showLocation0&&showLocation0(','')
	s=s.replace('}})','}}')
	T=py.importT()
	try:
		json=T.json_loads(s)
	except Exception as e:
		json={'err_s':s,
			  'err':e}
	response.close()
	if raw_response:
		json['raw_response']=response
	return json
	
map_location=address_coordinate	
	
	
	
def jsonwhois_com(domain,key=py.No('get_or_input',no_raise=True),raw_response=False):
	global U,T,N,F
	import requests
	U,T,N,F=py.importUTNF()
	domain=T.get_fld(domain)
	url="https://jsonwhois.com/api/v1/whois"
	if not key:
		key=U.get_or_input(url,type=py.str)
	
	response = requests.get(url,

	   headers={
		  "Accept": "application/json",
			"Authorization": key
		  },

	   params={
		   "domain": domain
		})
	if raw_response:return response
	try:
		return response.json()
	except Exception as e:
		return py.No(e,response.text[:26],response)

def whois(domain,raw_response=False):
	'''
 域名状态: clientTransferProhibited ( 禁止转移) renewPeriod ( 禁止自动续费). 
 
In [59]: [i for i in dw if 'admin_name' not in dw[i] ] #58643
['csfangyi.com', 'xn--xuw24ggz9aile.cn', '06jd.com', 'yzy88.com', 'cshelong.com']

''' 
	T=py.importT()
	import requests
	domain=T.get_fld(domain)
	cookies = {	'st': '95f5609d7aaadb13806df43e2ca1961c',	}
	headers = {
		'Pragma': 'no-cache',
		'Origin': 'http://whois.4.cn',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
	'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 YaBrowser/19.3.1.779 Yowser/2.5 Safari/537.36',

		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Cache-Control': 'no-cache',
		'X-Requested-With': 'XMLHttpRequest',
		'Connection': 'keep-alive',
		'Referer': 'http://whois.4.cn/batch',
	}

	data = {'domain': domain,  'isRefresh': '1'}
	try:
		response=requests.post('http://whois.4.cn/api/main',headers=headers,cookies=cookies,data=data)
		json=T.json_loads(response.content.decode('utf-8'))
		response.close()
		if raw_response:
			json['raw_response']=response
		return json
	except Exception as e:
		return py.No(e)
	
def bulk_whois(domain_list,args):
	import requests,json,logging
	bulkwhois_base_url = 'https://www.whoisxmlapi.com/BulkWhoisLookup/bulkServices/'
	session = requests.session()
	data = {
		"domains": domain_list,
		"password": args.password,
		"username": args.username,
		"outputFormat": 'json'
	}
	header = {'Content-Type': 'application/json'}
	# Posting task to API
	response = session.post(bulkwhois_base_url + 'bulkWhois',
							 data=json.dumps(data),
							 headers=header,
							 timeout=5)
	if response.status_code != 200:
		logging.error("wrong response code: %i" % response.status_code)
		return response
	response_data = json.loads(response.text)
	if response_data['messageCode'] == 200:
		logging.debug('Response: ' + response.text)
		del data['domains']
		data.update({
			'requestId': response_data['requestId'],
			'searchType': 'all',
			'maxRecords': 1,
			'startIndex': 1
		})
	else:
		logging.error('Response: ' + response.text)
		return response

	# waiting for job complete
	logging.debug("data:" + str(data))
	recordsLeft = len(domain_list)
	while recordsLeft > 0:
		time.sleep(args.interval)
		response = session.post(bulkwhois_base_url + 'getRecords',
								headers=header,
								data=json.dumps(data))
		if response.status_code != 200:
			logging.error("wrong response code: %i" % response.status_code)
			exit(1)
		recordsLeft = json.loads(response.text)['recordsLeft']
		logging.debug('Response: ' + response.text)

	data.update({'maxRecords': len(args.domains)})
	# dump json data
	time.sleep(args.interval)
	response = session.post(bulkwhois_base_url + 'getRecords',
							headers=header,
							data=json.dumps(data))
	with open(args.output + '.json','w') as json_file:
		json.dump(json.loads(response.text),json_file)
		print(json_file)
	# download csv data
	time.sleep(args.interval)
	with open(args.output + '.csv', 'wt') as csv_file:
		response = session.post(bulkwhois_base_url + 'download',
								headers=header,
								data=json.dumps(data))
		for line in response.text.split('\n'):
			clear_line = line.strip()
			# remove blank lines
			if clear_line != '':
				csv_file.write(clear_line + '\n')
		print(csv_file)		
################### whois end #####################


def netplan_add_routes(ip,gateway=py.No('auto use first'),
	adapter=py.No('auto use first who has routes'),
	yamlFile=r'/etc/netplan/50-cloud-init.yaml' ):
	''' '''
	U=py.importU()
	F=U.F
	n=F.readYaml(yamlFile)
	for adapterName,v in n['network']['ethernets'].items():
		if ( (not gateway) or (not adapter) ) and 'routes' in v:
			for dipg in v['routes']:
				gateway=dipg['via'] if not gateway else gateway
				adapter=adapterName if not adapter else adapter
				break
	if ('.' not in ip ) or (not gateway) or (not adapter):
		raise py.ArgumentError('please specify ip gateway adapter',ip,gateway,adapter)
	adapterV=n['network']['ethernets'][adapter]
	if 'routes' not in adapterV:
		adapterV['routes']=[]
	routes= adapterV['routes']
			
	for i in routes:
		if ip==i['to']:
			i['via']=gateway
			break
	else:
		routes.insert(0,{'to':ip,'via':gateway } )
		
	# import os;os.system('sudo netplan apply')
	
	return (ip,gateway,adapter,F.writeYaml(yamlFile,n) )
	

def get_ip_from_mac(mac):
	'''mac=='' return all ip
	'''
	U=py.importU()
	T=U.T
	r=U.cmd('arp','-a').splitlines() 
	r=[T.sub(i,'  ', '   ') for i in r if mac in i]
	r=[i for i in r if i]
	if py.len(r)==0:
		return py.No('no ip match mac:{} in arp table!'.format(mac))
	if py.len(r)>1:
		return py.No('more then 1 ip matched mac:{} in arp table!'.format(mac),r)
	if py.len(r)==1:
		return r[0]

def getLAN_IP_ALL_HOSTS(ip='192.168.1.{}',count=256):
	import socket
	for i in range(count):
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			s.connect((ip.format(i), 9))
			my_ip = s.getsockname()[0]
			print(my_ip, flush=True)	
	r=getAllAdapter()
	return r
	
def get_lan_ip(adapter=py.No('auto'),adapter_names=('enp0s','wlan0','ens5')):
	'''
	
['lo', 'eth0', 'docker0', 'vetha535de0', 'bond0', 'dummy0']

	
['以太网 2', '本地连接* 9', '本地连接* 10', 'WLAN', '蓝牙网络连接', 'Loopback Pseudo-Interface 1']	
'''	
	import socket
	dals=get_all_adapter()
	daip={}
	for a,ls in dals.items():
		for s in ls:
			# if '192.168.' in s.address:
			if s.family is socket.AddressFamily.AF_INET: # ipv4
				daip[a]=s.address
				break
			# socket.AddressFamily.AF_INET6: #ipv6
	if adapter:
		return daip[adapter]
	U,T,N,F=py.importUTNF()	
	if U.isLinux():
		try:
			return daip['eth0']
		except:
			ips=[]
			for a,ip in daip.items():
				if a[:5] in adapter_names: #adapterName
					ips.append(ip)
			if ips:
				for ip in ips:
					if T.startswith_multi(ip,'192.168','172.','10.'):
						return ip
			raise py.NotImplementedError(daip,ips)	
	elif U.isWin():#TODO
		ks=['WLAN', # 1.3
		'WLAN 2',  # 1.4
		 '以太网',#'192.168.1.5'
		]
		for k in ks:
			if k in daip:
				return daip[k]
		else:
			print(daip)
			raise py.EnvironmentError('win not found lan ip',daip)
	else:
		raise py.NotImplementedError('other system')
	################
	import socket
	import fcntl
	import struct

	def get_ip_address(ifname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(
			s.fileno(),
			0x8915,  # SIOCGIFADDR
			struct.pack('256s', ifname[:15])
		)[20:24])

	return get_ip_address(b'eth0') #if str struct.pack('256s', error: argument for 's' must be a bytes object
	
ip=get_ip=getLAN_IP=getlanip=get_lan_ip

def get_all_adapter():
	import psutil

	return psutil.net_if_addrs() # dict {'eth0': }

	U=py.importU()
	if U.iswin():
		from qgb import Win
		return Win.getAllNetworkInterfaces()
getAllAdapter=get_all_adapter

URL_SCHEME_CHARS=py.No('call N.auto_url will auto set')
def auto_url(a,default_protocol='http',p=0):
	'''According to RFC 2396, Appendix A:
scheme = alpha *( alpha | digit | "+" | "-" | "." )

Scheme names consist(组成) of a sequence of characters beginning with a lower case letter(小写字母开头) and followed by any combination of lower case letters, digits, plus ("+"), period句号 ("."), or hyphen ("-").

#TODO
2.1002  = 2.10 
2.20x2  = 2.20
2.1003  = 2.100
'''
	global URL_SCHEME_CHARS
	T=py.importT()
	URL_SCHEME_CHARS=T.alphanumeric+'+.-'
	# r=''
	
	if not py.istr(a):
		raise py.ArgumentError('url need string')
	a=a.strip()
	if  '://' in a:
		 # 放宽一点要求 ?，不检查首位，有时出现全部大写的URL
		for i,c in py.enumerate(a):
			if c not in URL_SCHEME_CHARS:
				if a[i:i+3]=='://':
					break
				else:
					return py.No('url SCHEME invalid',a,i)
					# raise py.ArgumentError('url SCHEME invalid',a,i)
					
		r=a
	elif a.startswith('//'):
		# if 
		r=default_protocol+':'+a
	else:
		r=default_protocol+'://'+a
	if p:print(r)	
	return r

autourl=autoUrl=autoURL=auto_url


#setip 192.168  ,  2.2	
def auto_ip(ip,ip2=py.No('192.168',no_raise=1),ip1=py.No('1',no_raise=1),print_ip=False,**ka):
	global U
	U=py.importU()
	ip1=U.get_duplicated_kargs(ka,'ip_1','c','C',default=ip1)
	ip2=U.get_duplicated_kargs(ka,'ip_2','ab','AB','a_b',default=ip2)
	print_ip=U.get_duplicated_kargs(ka,'p','print','print_','_print',default=print_ip)
	if py.isint(ip2):
		if ip1 or py.isint(ip1):raise py.ArgumentError('ip2 should be a.b format')
		ip1=ip2
		ip2=U.SET_NO_VALUE
	
	
	ip1=U.set_or_get('auto_ip.1',ip1,default=1)
	ip2=U.set_or_get('auto_ip.2',ip2,default='192.168')
	
	if py.istr(ip):
		try:ip=py.float(ip)
		except:			
			try:ip=py.float(ip)
			except:pass
	if py.isint(ip):#TODO check ip_int < 256 ?
		ip='{0}.{1}.{2}'.format(ip2,ip1,ip)
	if py.isfloat(ip):
		ip='{0}.{1}'.format(ip2,ip)		
	if print_ip:
		U.pln(ip)
	return ip

def setIP(ip='',adapter='',gateway='',source='dhcp',mask='',ip2=192.168,dns=py.No(msg='auto use gateway',no_raise=True) ):
	'''配置的 DNS 服务器不正确或不存在。   # 其实已经设置好了，可以正常使用'''
	U,T,N,F=py.importUTNF()
	if U.islinux():
		import socket,struct,fcntl
		if not py.isbytes(adapter):adapter=adapter.encode('ascii')
		if not py.isbytes(gateway):gateway=gateway.encode('ascii')
		if not py.isbytes(mask)   :mask=mask.encode('ascii')
			
		SIOCSIFADDR = 0x8916
		SIOCSIFNETMASK = 0x891C
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if mask:
			ifreq = struct.pack('16sH2s4s8s', adapter, socket.AF_INET, b'\x00' * 2, 
			socket.inet_aton(mask), b'\x00' * 8)
			fcntl.ioctl(sock, SIOCSIFNETMASK, ifreq)
			
		bin_ip = socket.inet_aton(ip)
		ifreq = struct.pack('16sH2s4s8s', adapter, socket.AF_INET, b'\x00' * 2, bin_ip, b'\x00' * 8)
		return fcntl.ioctl(sock, SIOCSIFADDR, ifreq)
	
	if not adapter:
		#adapter=u'"\u672c\u5730\u8fde\u63a5"'.encode('gb2312')#本地连接
		try:
			adapter=getAllAdapter()[0][0]	#   ( [11,'192.168.1.111',..] , [..] , ..]
		except:	
			if py.is2():adapter="\xb1\xbe\xb5\xd8\xc1\xac\xbd\xd3"
			else:		adapter="本地连接"
		# from qgb import Win
		# if Win.isxp():
			
	if ip:
		source='static'
		ip=N.auto_ip(ip,ip2)	
		
		if not mask:mask='255.255.255.0'
		if not mask.startswith('mask'):mask='mask='+mask
		
		if gateway:
			gateway=N.auto_ip(gateway,ip2)	
		else:
			gateway=T.subLast(ip,'','.')+'.1'
		if not gateway.startswith('gateway'):
			if py.isNo(dns) and 'auto' in dns.msg:
				dns=gateway
			if dns:
				dns=N.auto_ip(dns,ip2)	
				dns='address={}  register=primary'.format(dns)
			gateway='gateway='+gateway
			
		if not ip.startswith('addr'):ip='address='+ip
	else:
		ip=''
	r=[ 'netsh interface ip set address name={0} source={1} {2} {3} {4} '.format(adapter,source,ip,mask,gateway),
		'netsh interface ip set dnsservers name={0} source=dhcp'.format(adapter,)
		]
	if dns:
		dns='netsh interface ip set dnsservers name={0} source={1} {2}'.format(adapter,source,dns)
		if 'dnsservers' in r[-1]:
			r[-1]=dns
		else:
			r.append(dns)
	import os
	for i in r:
		os.system(i)
	return r
setip=setIP
def getComputerName():
	import socket
	return socket.gethostname()
gethostname=getHostName=getComputerName

def getArpTable():
	U=py.importU()
	return U.cmd('arp -a')
		
def scanPorts(host,threadsMax=33,from_port=1,to_port=65535,callback=None,ip2=192.168):
	'''return [opens,closes,errors]
	callback(*scanReturns)
	if callback and ports> threadsMax: 剩下结果将异步执行完成
	'''
	U=py.importU()
	from threading import Thread
	import socket
	# host = raw_input('host > ')
	# from_port = input('start scan from port > ')
	# to_port = input('finish scan to port > ')   
	counting_open = U.set('scanPorts.open',[])
	counting_close = U.set('scanPorts.close',[])
	errors=U.set('scanPorts.error',[])
	threads = U.set('scanPorts.threads',[])
	if isinstance(host,py.float):host='{0}.{1}'.format(ip2,host)
	
	def scan(port):
		# U.count(1)
		try:
			s = socket.socket()
			result = s.connect_ex((host,port))
			# U.pln('working on port > '+(str(port)))	  
			if result == 0:
				counting_open.append(port)
				#U.pln((str(port))+' -> open') 
				s.close()
			else:
				counting_close.append(port)
				#U.pln((str(port))+' -> close') 
				s.close()
		except Exception as e:
			errors.append({port:e})
	def newThread(port):
		t = Thread(name='scanPorts %s:%s'%(host,port),target=scan, args=(port,))		
		threads.append(t)
		try:
			t.start()
		except:
			"can't start new thread"
	im=py.float(to_port-from_port+1)
	percent=0.0
	for i in range(from_port, to_port+1):
		if ((i-from_port)/im>percent):
			U.pln( 'Scanning  %.0f%%' % (percent*100), len(threads)	 )
			percent+=0.01
			
		if len(threads)<=threadsMax:
			newThread(i)
		else:
			for x in threads:
				if x.is_alive():
					x.join()
					newThread(i)
				else:
					threads.remove(x)
				break
	# if callback:
		# return callback
	[x.join() for x in threads]
	return counting_open,counting_close,errors

def traceroute(target,maxttl=60):
	''' '''
	from scapy.layers.inet import traceroute
	from scapy.layers.inet import traceroute_map

	# ans,unans = answered,unanswered packets list
	# They are of type TracerouteResult defined in scapy/inet.py
	# each entry in ans is a 2-entry tuple = send,recv packet
	ans,unans = traceroute(target, maxttl=maxttl, verbose=0)
	index = len(ans)
	for i,v in enumerate(ans):
		if v[0].dst == v[1].src:
			index = i
			break

	# scapy parallelly sends requests for all TTL's and stores results from them.
	# Removing redundant entries after the packet reaches destination
	ans = ans[0:index+1]


	print("List of answered packets:")
	if ans:
		print()
		print("Target: {}:".format(ans[0][0].dst))
	for s,d in ans:
		src = s.sprintf("Hop: %03s,IP.ttl%")
		city,country = get_location(d.src)
		dst = d.sprintf(", Address: %15s,IP.src%, Location: "+city+","+country)
		print(src+dst)


	print("Thee are {} unanswered packets.".format(len(unans)))

	if len(unans) != 0:
		print("List of unanswered packets:")
		print()
		print("TTL  Source IP      Port")
		for s in unans:
			print(s.sprintf("%-03s,IP.ttl%  %IP.dst%  {TCP:%ir,TCP.dport%}{UDP:udp%ir,UDP.dport%}"))	
	return ans,unans



def Tracert_one(dst,dport,ttl_no):#发一个Traceroute包，参数需要目的地址，目的端口，TTL。
	from scapy.all import sr1
	import time,struct,re

	send_time = time.time()#记录发送时间
	Tracert_one_reply = sr1(IP(dst=dst, ttl=ttl_no)/UDP(dport=dport)/b'traceroute!!!', timeout = 1, verbose=False)
	try:
		if Tracert_one_reply.getlayer(ICMP).type == 11 and Tracert_one_reply.getlayer(ICMP).code == 0:
			#如果收到TTL超时
			hop_ip = Tracert_one_reply.getlayer(IP).src
			received_time = time.time()
			time_to_passed = (received_time - send_time) * 1000
			return 1, hop_ip, time_to_passed #返回1表示并未抵达目的地
		elif Tracert_one_reply.getlayer(ICMP).type == 3 and Tracert_one_reply.getlayer(ICMP).code == 3:
			#如果收到端口不可达
			hop_ip = Tracert_one_reply.getlayer(IP).src
			received_time = time.time()
			time_to_passed = (received_time - send_time) * 1000
			return 2, hop_ip, time_to_passed #返回2表示抵达目的地
	except Exception as e:
		if re.match('.*NoneType.*',str(e)):
			return None #测试失败返回None

def Tracert(dst,hops):
	# from scapy.all import *
	import time,struct,re

	dport = 33434 #Traceroute的目的端口从33434开始计算
	hop = 0
	while hop < hops:
		dport = dport + hop
		hop += 1
		Result = Tracert_one(dst,dport,hop)
		if Result == None:#如果测试失败就打印‘*’
			print(str(hop) + ' *',flush=True)
		elif Result[0] == 1:#如果未抵达目的，就打印这一跳和消耗的时间
			time_to_pass_result = '%4.2f' % Result[2]
			print(str(hop) + ' ' + str(Result[1]) + ' ' + time_to_pass_result + 'ms')
		elif Result[0] == 2:#如果抵达目的，就打印这一跳和消耗的时间，并且跳出循环！
			time_to_pass_result = '%4.2f' % Result[2]
			print(str(hop) + ' ' + str(Result[1]) + ' ' + time_to_pass_result + 'ms')
			break
		time.sleep(1)

if __name__=='__main__':
	rpcServer(currentThread=True)
	exit()
	U.pln( getLAN_IP() )
	exit()
	gsurlip=['http://ip.chinaz.com/getip.aspx'][0]

	s=http(gsurlip)#.encode('utf8').decode('mbcs')

	U.pln( s.decode('utf8').encode('mbcs'))
	# import chardet
	# U.pln( chardet.detect(s)
	
