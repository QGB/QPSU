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

gheaders=headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.2171.95 Safari/537.36'}
def random_headers():
	import fake_headers
	return fake_headers.Headers( headers=fake_headers.make_header() ).generate()
	
#8
ghttp_methods=HTTP_METHODS=[
'HEAD', 'GET', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE']	
def request(url,method='GET',headers=gheaders,verify=False,no_raise=False,**ka):	
	import requests
	
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
	ka['verify']=verify
	
	if url and 'url' not in ka:
		ka['url']=url
	if no_raise:
		try:
			return requests.request(**ka)
		except Exception as e:
			return py.No(e,ka)
	return requests.request(**ka)

def download(url, file_path='',default_dir=py.No('set_input',no_raise=1),headers=None):
	import requests,sys,os
	U,T,N,F=py.importUTNF()
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
	r1 = requests.get(url, stream=True, verify=False)
	total_size = int(r1.headers['Content-Length'])

	# 这重要了，先看看本地文件下载了多少
	if os.path.exists(file_path):
		temp_size = os.path.getsize(file_path)  # 本地已经下载的文件大小
	else:
		temp_size = 0
	# 显示一下下载了多少   
	print(temp_size,'/',total_size)
	# 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
	if not headers:
		headers={}
	headers['Range']= 'bytes=%d-' % temp_size
	# 重新请求网址，加入新的请求头的
	r = requests.get(url, stream=True, verify=False, headers=headers)

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
		
def post(url,**ka):
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

	url=N.auto_url(url)
	proxies=U.get_duplicated_kargs(ka,'proxies','proxy')
	if proxies:
		proxies=N.set_proxy(proxy)
	else:
		proxies=N.get_proxy()
	ka['proxies']=proxies
	
	import requests
	return requests.post(url,**ka)

def get_str(url,**ka ,):
	T=py.importT()
	return T.auto_decode(  get_bytes(url,**ka)  )
gets=getStr=get_str

def get_bytes(url,	**ka ,):
	U,T,N,F=py.importUTNF()

	url=N.auto_url(url)
	proxies=U.get_duplicated_kargs(ka,'proxies','proxy')
	file=U.get_duplicated_kargs(ka,'file','f','filename')
	write_zero=U.get_duplicated_kargs(ka,'write0','w0','write_zero','zero',default=False)
	if proxies:
		proxies=N.set_proxy(proxy)
	else:
		proxies=N.get_proxy()
	ka['proxies']=proxies

	import requests
	try:
		b= requests.get(url,**ka).content
		f=repr(b[:77])[2:-1]
		if file and (b or write_zero):
			f=F.write(file,b)
		return U.object_custom_repr(b,repr='{}{}'.format(F.readable_size(b),f)  )
	except Exception as e:
		return py.No(e)
getb=getByte=getBytes=get_byte=get_bytes

AUTO_GET_PROXY=py.No(msg='auto get_proxy',no_raise=1)
def get(url,file='',
		headers = gheaders,
		timeout=9,
		proxies=AUTO_GET_PROXY,
		encoding='',
		**ka ,
	):
	U,T,N,F=py.importUTNF()
	url=N.auto_url(url)

	show=U.get_duplicated_kargs(ka,'show','print','p','print_req')
	proxies=U.get_duplicated_kargs(ka,'proxies','proxys','proxyes','proxy',default=proxies)
	if proxies:#dict or str 均可
		pr=N.set_proxy(proxies)
		if not pr:
			if py.istr(proxies) and 'auto' in proxies.lower():
				proxies=N.get_proxy(target_protocol=('http','https'),)
			else:
				raise py.ArgumentError('proxy format error {}://{}:{}',proxies)
		else:
			proxies=pr
	else:
		if (proxies is AUTO_GET_PROXY) or (py.isNo(proxies) and 'auto get_proxy' in proxies.msg):
			proxies=N.get_proxy(target_protocol=('http','https'),)
		else:
			proxies={}


	def writeFile():
		if file:
			content=r.content
			# if content:
			return F.write(file,content)
			# else:
				# return py.No('response.content is Null!')
			
	b=b''
	try:
		import requests
		r=requests.get(url,verify=False,timeout=timeout,headers=headers,proxies=proxies)
		if show:
			print(U.v.requests.get(url,verify=False,timeout=timeout,headers=U.StrRepr(U.pformat(headers)),proxies=proxies))
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

		
def method(url,amethod='get',*args):
	r'''#TODO: post etc need args'''
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