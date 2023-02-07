#coding=utf-8
import sys #endswith 是为了适配qgb处于另外一个包内的情况
if __name__.endswith('qgb.N.HTTP'):from .. import py
else:
	from pathlib import Path
	gsqp=Path(__file__).absolute().parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py

if py.is2():
	import urllib2 as urllib
	grequest = urllib.Request
	grequest.urlopen=urllib.urlopen
else:
	import urllib
	from urllib import request as _grequest #  加了这句才不会 AttributeError: module 'urllib' has no attribute 'request
	try:
		grequest = urllib.request.Request
		grequest.urlopen=urllib.request.urlopen		
	except Exception as ei:
		print(urllib,ei)
		py.importU().repl()
ghttp_methods=HTTP_METHODS=[
'HEAD', 'GET', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE']		
user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.2171.95 Safari/537.36'
user_agent_iphone=r'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1'

gheaders=headers={'User-Agent': user_agent}

def thread_pool_request(targets,max_workers=None,request_ka={},print_log=False,**ka):
	'''
	def __init__(self, max_workers=None, thread_name_prefix='',
                 initializer=None, initargs=()):
        """Initializes a new ThreadPoolExecutor instance.

        Args:
            max_workers: The maximum number of threads that can be used to
                execute the given calls.
            thread_name_prefix: An optional name prefix to give our threads.
            initializer: A callable used to initialize worker threads.
            initargs: A tuple of arguments to pass to the initializer.
        """
        if max_workers is None:
            # Use this number because ThreadPoolExecutor is often
            # used to overlap I/O instead of CPU work.
            max_workers = (os.cpu_count() or 1) * 5
			
timeout			
'''			
	import concurrent.futures
	U,T,N,F=py.importUTNF()
	r=[]
	max_workers=U.get_duplicated_kargs(ka,'max_thread','threads','thread_count',default=max_workers)
	print_log=U.get_duplicated_kargs(ka,'P','print','p',default=print_log)
	
	pool=U.get_or_set('U.ThreadPoolExecutor',lazy_default=lambda:U.ThreadPoolExecutor())
	if print_log:U.pprint(pool._threads)
	pool._threads.clear()
	pool._shutdown=False 
	# pool._max_workers=max_workers
	
	with pool:
		future_to_url = {pool.submit(request, url, **request_ka): url for url in targets}
		for future in concurrent.futures.as_completed(future_to_url):
			url = future_to_url[future]
			try:
				data = future.result()
				r.append([U.StrRepr(url,size=15),data,data.elapsed.total_seconds()])
			except Exception as exc:
				if print_log:print('### %r %s' % (url, exc))
			else:
				if print_log:print('%r %s' % (url, data))			print(U.stime(),'### len',U.len(targets,r))
	return r
	
AUTO_GET_PROXY=py.No(msg='auto get_proxy',no_raise=1)
def auto_proxy_for_requests(proxies,ka,return_ka=False):
	''' proxies:#dict or str 均可
return proxies,ka
	'''
	U,T,N,F=py.importUTNF()
	proxies=U.get_duplicated_kargs(ka,'proxies','proxy',default=proxies)
	if proxies:
		proxies=N.set_proxy(proxies)
	else:
		if (proxies is AUTO_GET_PROXY) or (py.isNo(proxies) and 'auto get_proxy' in proxies.msg):
			proxies=N.get_proxy(target_protocol=('http','https'),)
		else:
			proxies={}
	if return_ka:
		ka['proxies']=proxies
		return proxies,ka
	else:
		return proxies
auto_proxy=auto_proxies=auto_proxy_for_requests	
	
def random_headers():
	import fake_headers
	return fake_headers.Headers( headers=fake_headers.make_header() ).generate()
	
#8

def request(url,method='GET',headers=gheaders.copy(),
	proxies=AUTO_GET_PROXY,verify=False,timeout=9,no_raise=False,print_req=False,**ka):	
	''' 
'''
	import requests
	U,T,N,F=py.importUTNF()
	proxies,ka=auto_proxies(proxies,ka,return_ka=True)
	print_req=U.get_duplicated_kargs(ka,'show','print','p','print_req',default=print_req)
	
	if (py.istr(url) and url.upper() in HTTP_METHODS):
		# ka.pop('method','')#D.pop(k[,d]) -> v,
		ka['method']=url
		url=ka['url'] # test url exists
	elif method:
		ka['method']=method
	if headers:
		ka['headers']=headers
		for k in py.list(ka):
			v=ka[k]
			if py.istr(k) and py.istr(v):
				if k[0].isupper():
					ka.pop(k)
					headers[k]=v
	
	if url and 'url' not in ka:
		ka['url']=url
	ka['verify']=verify
	ka['timeout']=timeout
	ka['url']=N.auto_url(ka['url']) # 特意将url放最后，方便显示
		
	if print_req:print(U.v.requests.request(**ka))
		
	if no_raise:
		try:
			return requests.request(**ka)
		except Exception as e:
			return py.No(e,ka)
	return requests.request(**ka)
requests=request

def auto_method(method,ka,return_ka=False):
	if method:
		r=method
	else:
		if 'method' in ka:
			r=ka['method']
		else:
			r='GET'
	if return_ka:		
		ka['method']=r
		r=r,ka
	else:
		if 'method'	in ka:
			ka.pop('method')		
	
	return r
	
def auto_headers(headers,ka,return_ka=False):
	U,T,N,F=py.importUTNF()
	headers=U.get_duplicated_kargs(ka,'headers','header','hd','h',default=headers)		
	if not headers:
		headers={}
	if py.istr(headers):
		if '\n' in headers:raise py.NotImplementedError
		headers=[i.strip() for i in headers.split(':')] 
		headers={headers[0]:headers[1]}
	if return_ka:
		ka['headers']=headers
		return headers,ka
	return headers
	
auto_header=auto_headers
	
def get_json(u,proxies=AUTO_GET_PROXY,method='GET',headers=None,**ka):
	import requests
	proxies,ka=auto_proxies(proxies,ka,return_ka=True) # def auto_proxy_for_requests
	method ,ka=auto_method (method ,ka,return_ka=True)
	headers,ka=auto_headers(headers,ka,return_ka=True)
	r=requests.request(url=u,**ka)
	
	return r.json()
	
def download_one_page_list(url,headers={},**ka):
	U,T,N,F=py.importUTNF()
	
	return
	
def download_seq(url_format,min=0,max=99,headers={},**ka):
	import requests 
	U,T,N,F=py.importUTNF()
	
	while '{' not in url_format or '}' not in url_format:
		url_format=U.set_input('download_seq.url_format',default=url_format)
	
	if U.isWin() and U.gst!='C:/test/':
		U.gst=U.set_input('U.gst',default=U.gst)
	domain=T.get_domain_from_url(url_format)
	file_ext=T.sub_last(url_format,'.')
	if file_ext.lower() not in ['jpg','png','jpeg']:
		file_ext=U.set_input(url_format+' file_ext[NO DOT]',default=file_ext)
	if '.' in file_ext:raise Exception(file_ext)
	
	for n in range(min,max):
		url=url_format.format(n)
		file=T.sub(url,domain)
		if file.startswith('/'):file=file[1:]
		f=r'{gst}{domain}/{file}'.format(gst=U.gst,domain=domain,file=T.filename_legalized(file) , )
		
		if F.size(f):
			print('#'*9,'Exist',f)
			continue
		response = N.HTTP.requests(url,headers=headers,verify=False,no_raise=1) 
		if not response	or response.status_code!=200:
			print(repr(response).strip(),py.getattr(response,'url',' No'))
			return response
		
		b=response.content
		print(U.sizeof(b),F.write(f,b,mkdir=1))#
		
		
			
			
			
def download(url, file_path='',default_dir=py.No('set_input',no_raise=1),headers=None,proxies=AUTO_GET_PROXY,**ka):
	import requests,sys,os
	U,T,N,F=py.importUTNF()
	proxies=auto_proxy(proxies,ka)
	if not headers:
		headers={}
	
	if not F.isabs(file_path) and not default_dir:
		default_dir='D:/'
		if U.is_linux() or U.is_mac():
			default_dir=U.gst+'download/'
		default_dir=U.get_or_input('download.default_dir',default=default_dir)
	
	if not file_path:
		file_path=default_dir+ T.filename_legalized( url.split('/')[-1] )
		print('save_to:',file_path)
	# 屏蔽warning信息
	# requests.packages.urllib3.disable_warnings()
	# 第一次请求是为了得到文件总大小
	r1 = requests.get(url, stream=True, verify=False,headers=headers,proxies=proxies,)
	total_size = int(r1.headers['Content-Length'])

	# 这重要了，先看看本地文件下载了多少
	if os.path.exists(file_path):
		temp_size = os.path.getsize(file_path)  # 本地已经下载的文件大小
	else:
		temp_size = 0
	# 显示一下下载了多少   
	print(temp_size,'/',total_size)
	# 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
	headers['Range']= 'bytes=%d-' % temp_size
	# 重新请求网址，加入新的请求头的
	r = requests.get(url, stream=True, verify=False,headers=headers,proxies=proxies,)

	# 下面写入文件也要注意，看到"ab"了吗？
	# "ab"表示追加形式写入文件
	with open(file_path, "ab") as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				temp_size += len(chunk)
				f.write(chunk)
				f.flush()

				###这是下载实现进度显示####
				done = int(50 * temp_size / total_size)
				sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
				sys.stdout.flush()
	print()  # 避免上面\r 回车符
		
def post(url,data=None,return_text=False,**ka):
	'''
Signature: requests.post(url, data=None, json=None, **kwargs)
Docstring:
Sends a POST request.

:param url: URL for the new :class:`Request` object.
:param data: (optional) Dictionary (will be form-encoded), bytes, or file-like object to send in the body of the :class:`Request`.
:param json: (optional) json data to send in the body of the :class:`Request`.
:param \*\*kwargs: Optional arguments that ``request`` takes.
:return: :class:`Response <Response>` object
:rtype: requests.Response
File:	  e:\qgb\anaconda3\lib\site-packages\requests\api.py
Type:	  function
'''	
	U,T,N,F=py.importUTNF()

	# url=N.auto_url(url)
	# proxies,ka=auto_proxy(proxies,ka,return_ka=True)
	
	data=U.get_duplicated_kargs(ka,'data','v',default=data)
	
	rp= request(url,method='POST',data=data,**ka)
	if return_text:
		return rp.text
	return rp
	# import requests
	# try:
		# return requests.post(url,data=data,**ka)
	# except Exception as e:
		# return py.No(e)

def get_str(url,**ka ,):
	T=py.importT()
	return T.auto_decode(  get_bytes(url,**ka)  )
gets=getStr=get_str

def get_bytes(url,file='',
		headers = gheaders,
		timeout=9,
		proxies=AUTO_GET_PROXY,
		verify=False,
		print_req=False,
		bytes_with_response=True,
		url_as_file=False,
		skip_if_exist=False,
		return_only_filename=False,
		**ka ,):
	'''
url格式不对时：
C:\QGB\Anaconda3\lib\site-packages\socks.py in _write_SOCKS5_address(self, addr, file)
    574                                            socket.SOCK_STREAM,
    575                                            socket.IPPROTO_TCP,
--> 576                                            socket.AI_ADDRCONFIG)
    577             # We can't really work out what IP is reachable, so just pick the
    578             # first.

C:\QGB\Anaconda3\lib\socket.py in getaddrinfo(host, port, family, type, proto, flags)
    746     # and socket type values to enum constants.
    747     addrlist = []
--> 748     for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
    749         af, socktype, proto, canonname, sa = res
    750         addrlist.append((_intenum_converter(af, AddressFamily),

UnicodeError: encoding with 'idna' codec failed (UnicodeError: label too long)

'''	
	U,T,N,F=py.importUTNF()

	url=N.auto_url(url)
	file=U.get_duplicated_kargs(ka,'file','f','filename',default=file)
	if not file and not url_as_file and return_only_filename:
		url_as_file=True
	
	if not file and url_as_file:
		pf=T.sub(T.url_decode(url),'://',)
		ps=[T.file_legalized(pi) for pi in pf.split('/')]
		file=F.mkdir( '/'.join(ps[:-1]) )+ps[-1]
		# mp=py.len(ps)-1
		# lp=[]
		# for pi in ps:
	if file and skip_if_exist:
		fsize=F.size(file)	
		if fsize:
			if return_only_filename:return file
			return U.object_custom_repr(F.read_bytes(file),repr='{}{}'.format(fsize,file)  )
	#else:	不能用，如果文件不存在，else不会执行
	write_zero=U.get_duplicated_kargs(ka,'write0','w0','write_zero','zero',default=False)
	print_req=U.get_duplicated_kargs(ka,'show','print','p','print_req',default=print_req)
	
	proxies,ka=auto_proxy(proxies,ka,return_ka=True)
	
	if not 'headers' in ka:ka['headers']=headers
	
	import requests
	try:
		if print_req:print(U.v.requests.get(url,verify=verify,timeout=timeout,**ka))
		#,headers=U.StrRepr(U.pformat(headers)
		p= requests.get(url,verify=verify,timeout=timeout,**ka)
		b=p.content
		f=repr(b[:77])[2:-1]
		if file and (b or write_zero):
			f=F.write(file,b)
		if return_only_filename:return f
		bo= U.object_custom_repr(b,repr='{}{}'.format(F.readable_size(b),f)  )
		if bytes_with_response:
			bo.p=bo.response=p
		return bo
	except Exception as e:
		return py.No(e)
bytes=byte=getb=getByte=getBytes=get_byte=get_bytes

def get(url,file='',
		headers = gheaders,
		timeout=9,
		proxies=AUTO_GET_PROXY,
		encoding='',
		show=False,
		verify=False,
		**ka ,
	):
	U,T,N,F=py.importUTNF()
	url=N.auto_url(url)

	show=U.get_duplicated_kargs(ka,'show','print','p','print_req',default=show)
	proxies=auto_proxy(proxies,ka)#only return proxies, del proxy keys in ka

	def writeFile():
		if file:
			content=r.content
			# if content:
			return F.write(file,content)
			# else:
				# return py.No('response.content is Null!')
			
	if show:print(U.v.requests.get(url,verify=verify,timeout=timeout,headers=U.StrRepr(U.pformat(headers)),proxies=proxies))
	b=b''
	try:
		import requests
		r=requests.get(url,verify=verify,timeout=timeout,headers=headers,proxies=proxies)
		if file:
			u=T.url_split(url).path
			u=T.sub_last(u,'/')
			if py.isbool(file):
				file=u
			elif F.isdir(file):
				file=file+u
			return F.write(file,r.content)
		#TODO decode
		if 'text' in r.headers.get('Content-Type','').lower():
			return r.content.decode(encoding or T.detect(r.content[:9999]) or 'utf-8')
			# try:return r.content.decode('gb18030')
			# except:pass
			# return r.text
		else:
			b= r.content
			
	except ModuleNotFoundError:
		try:
			b=grequest.urlopen(url).read()
		except Exception as e:
			return py.No(url,e)
		#####################
	except Exception as e:
		return py.No(e)

	# try:
	encoding= T.detect(b[:9999])
		# raise Exception('decode error')
	if b and encoding:
		return b.decode(encoding)
	return b
	

def head(url):
	return method(url,'head').info().items()
	
def options(url):
	return dict(method(url,'options').info().items() )['allow']

		
def method(url,amethod='get',proxies=AUTO_GET_PROXY,*args):
	r'''#TODO: post etc need args  # proxies '''
	U,T,N,F=py.importUTNF()
	try:
		url=N.auto_url(url)
		request = grequest(url)
		request.get_method = lambda : amethod.upper()
		response = grequest.urlopen(request)
		return response
	# except urllib2.HTTPError as eh:
		# setError(eh)
	except Exception as e:
		setErr(e)
gError=None
def setErr(a):
	global gError
	gError=a
	raise a#[eh.msg,eh.headers.items(),eh]