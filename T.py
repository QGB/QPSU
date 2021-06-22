# coding=utf-8	
#考虑qgb 位于另一个包内的情况
if __name__.endswith('qgb.T'):from . import py
else:#['T','__main__']
	import py
FILE_NAME=fileChars=FILE_CHARS="!#$%&'()+,-0123456789;=@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{}~"+' .'
PATH_NAME=pathChars=PATH_CHARS='/\\:'+FILE_NAME# include space, dot
gsNOT_FILE_NAME_WINDOWS=gsNOT_FILE_NAME=NOT_FILE_NAME_WINDOWS=NOT_FILE_NAME=r'"*/:<>?\|'
gsNOT_PATH_NAME_WINDOWS=gsNOT_PATH_NAME=NOT_PATH_NAME_WINDOWS=NOT_PATH_NAME=r'"*<>?|' # : is
gsNOT_FILE_NAME_LINUX=NOT_FILE_NAME_LINUX='/'+py.chr(92) # \

az=a_z='abcdefghijklmnopqrstuvwxyz'
AZ=A_Z=a_z.upper()

alphabet=alphabeT=azAZ=aZ=a_Z=a_z+A_Z # The English Alphabet Has 52 Letters
Alphabet=AZaz=Az=A_z=A_Z+a_z
character=aZ=azAZ###Do not Change

num=s09=_09=number='0123456789'
_10='1234567890'
azAZ09=aZ09=a_Z0_9=alphanumeric=character+number#azAZ09, not gs09AZ
aZ09_=_aZ09=_alphanumeric=alphanumeric_=alphanumeric+'_'
Az09=A_z0_9=A_Z+a_z+number

Hex=gshex='0123456789abcdef'
HEX=gshex.upper()

#0x20-0x7E ,32-126,len=95
visAscii=print_ascii=printAscii=asciiPrint=' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
char256=''.join([chr(i) for i in range(256)])
bytes256=byte256=b''.join( [py.byte(i) for i in range(256)  ] )

CR='\r'
LF=EOL=eol='\n'
TAB=Tab=tab='\t'
gspace=space=py.chr(0x20)
slash='/'
back_slash=backslash='\\'
######### html ######
hr='<hr>'
br='<br>'
u23=s23='%23-'
p23='#-'
#######################
RE_IMG_URL=r'(((http://www)|(http://)|(www))[-a-zA-Z0-9@:%_\+.~#?&//=]+)\.(jpg|jpeg|gif|png|bmp|tiff|tga|svg)'
RE_URL=r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
RE_YMD=r"(19|20)[0-9]{2}[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])"
RE_WhiteSpace=r'\s+'

###############
SQLITE='SELECT * FROM sqlite_master;'

#########################################
squote=quote="'"
dquote=dQuote='"'

import re	

gError=None
try:
	from chardet import detect as _detect
	def detect(abytes,confidence=0.7,default=py.No('default encoding "" ')  ):
		'''
T._detect( b'\x1b'*1)  ### {'encoding': None, 'confidence': 0.0, 'language': None}	
		'''
		r=_detect(abytes)
		if r['encoding'] in ['Windows-1254' ]:
			try:
				if abytes.decode('utf-8').encode('utf-8')==abytes:
					return 'utf-8'
			except Exception as e:
				pass
		if r['encoding'] in ['gb2312','GB2312' ]:
			try:
				if abytes.decode('gb18030').encode('gb18030')==abytes:
					return 'gb18030'
			except Exception as e:
				pass		
				
		if r['confidence']>confidence:return r['encoding']
		else:
			if default:return default
			# raise Exception
			return py.No(
			'{0} encoding {1} confidence {2} less then {3}'.format(
			abytes[:99],r['encoding'],r['confidence'],confidence)  )
except Exception as ei:
	def detect(*a):
		raise Exception('#not install chardet Module')  # <no> is not callable ,see the source
	pass
try:
	from io import StringIO
	strio=StrIO=stringIO=StringIO
	from pprint import pprint,pformat
except:pass
####################################################
# def 

def split_to_2d_list(text,col=re.compile('\s+'),row='\n',strip=True,StrRepr=False):
	'''
numpy.loadtxt("myfile.txt")[:, 1]	
 fname : file, str, or pathlib.Path
        File, filename, or generator to read.  If the filename extension is
        ``.gz`` or ``.bz2``, the file is first decompressed. Note that
        generators should return byte strings for Python 3k.
		
 '1\r\n2\r\n4'.splitlines()
 ['1', '2', '4']
 
 '1\n2\r\n4'.splitlines()
 ['1', '2', '4']
 
'''		
	U=py.importU()
	if row in ['\n','\r\n']:
		r=text.splitlines()
	else:
		r=text.split(row)
	for i,v in py.enumerate(r):
		if strip:v=v.strip()
		cs=re.split(col,v)
		if StrRepr:
			StrRepr_ka={}
			if py.isint(StrRepr) and StrRepr>1:
				StrRepr_ka['size']=StrRepr
			r[i]=[U.StrRepr(i,**StrRepr_ka) for i in cs]
		else:
			r[i]=cs
	return r
	# import numpy as np
	# np.loadtxt("myfile.txt")[:, 1]
	# return [ ]

def is_contains(text,target):
	try:
		return target in text
	except Exception as e:
		return py.No(e)
is_include=include=contains=is_contains
		
def LF_to_CRLF(text):
	if py.istr(text):return regex_replace(text,r'(?<!\r)\n','\r\n')
	if py.isbytes(text):return regex_replace(text,br'(?<!\r)\n',b'\r\n')
	raise py.ArgumentUnsupported(text)
lf2crlf=LF2CRLF=lf_to_crlf=LF_to_CRLF

def get_string_image(text,size=48,w=None,h=None):
	'''
('simsunb.ttf',48) a[5+1行][0:5+37+5]==【5个0，37个1，5个0】  
第6列 【5个0，37+2个1，3个0】 一个方框字符黑色尺寸 37*39

Image.new(mode='P',"L", "RGB"	
	If you have an L mode image, that means it is a single channel image - normally interpreted as greyscale. 
	'''
	from PIL import Image, ImageFont, ImageDraw
	if not w:w=100
	if not h:h=100
	font=ImageFont.truetype('simsunb.ttf',48)     
	image = Image.new('L', (w, h), color='white')
	drawing = ImageDraw.Draw(image)
	drawing.text((0,0), text, font=font)
	return image
get_char_image=get_string_image	
def slice(a,start, stop=None, step=1):
	''' not only for str '''
	if py.isinstance(start,py.slice):
		if stop==None and step==1:
			start,stop,step=start.start,start.stop,start.step
		else:
			raise py.ArgumentError('conflict',start,stop,step)
	if not py.isint(start):
		len=py.len(start)
		if len==1:start=start[0]
		if len==2 and stop==None:start,stop=start
		if len==2 and stop==None and step==1:
			start,stop,step=start
		
	try:
		return a[start:stop:step]
	except Exception as e:
		return py.No(e)
get=char_at=charAt=get_char_at=slice		
		
def search_return_position(text,*targets,case_sensitive=True,a=0,b=0,c=0,dict=False,**ka):
	U=py.importU()
	a=U.get_duplicated_kargs(ka,'A',default=a)
	b=U.get_duplicated_kargs(ka,'B',default=b)
	c=U.get_duplicated_kargs(ka,'C',default=c)
	case_sensitive=U.get_duplicated_kargs(ka,'cs','case','upper','caseSensitive',default=case_sensitive)
	dict=U.get_duplicated_kargs(ka,'d','return_dict','rd',default=dict)
	r=[]
	d={}
	def _append(t,i,sub=''):
		if dict:
			if sub:
				U.dict_add_value_list(d,t,(i,sub))
			else  :U.dict_add_value_list(d,t,i)
		else:
			if sub:
				r.append([t,i,sub ])		
			else  :r.append([t,i, ])
			
	for t in py.set(targets):
		i=0
		# re.finditer(re.escape)
		
		while True:
			i=text.find(t,i)
			if i==-1:break
			else:
				if a or b or c:
					c0=py.max(i-a,0)
					c1=i+py.len(t)+b
					if c:
						c0=py.max(i-c,0)
						c1=i+py.len(t)+c
					_append( t,i,text[c0:c1] )
				else:
					_append(t,i,)
			i+=1 # 不然 死循环		
	if r:return r
	if d:return d
	return py.No('Not found',targets,'in text',py.len(text))
		
find=find_n=search=search_return_position	
	
def regex_encode(a):
	return re.escape(a)
re_escape=regex_escape=regex_encode

def chr_string(chars,alphanumeric=alphanumeric_,quote=quote,chr_func=lambda c:'chr(%s)'%py.ord(c) ,):
	s=''
	last='' #  alphan:a  oherchar:c
	for c in chars:
		if c in alphanumeric:
			if not last:
				c=quote+c
			if last=='c':
				c='+'+quote+c

			last='a'
		else:
			c=chr_func(c)
			if not last:pass
			if last=='a':
				c=quote+'+'+c
			if last=='c':
				c='+'+c
			last='c'
		s+=c
	if last=='a':s+=quote

	U=py.importU()
	return U.StrRepr(s)
get_chr_str=make_chr_str=chr_s=chr_str=chr_string	

def wc_ljust(text, length, padding=' '):
	return text + padding * py.max(0, (length - wcswidth(text)))
def wc_rjust(text, length, padding=' '):
	'''rjust() 返回一个原字符串右对齐, 在左边填充
	'''
	# from wcwidth import wcswidth
	return padding * py.max(0, (length - wcswidth(text))) + text

def wc_cut(s,size):
	from wcwidth import wcwidth
	width = 0
	for n,c in py.enumerate(s):
		wcw = wcwidth(c)
		if width>=size:
			break
		if wcw < 0:
			width += 0
		else:
			width += wcw
	return s[:n]
def wcswidth(pwcs, n=None):
	"""
	Given a unicode string, return its printable length on a terminal.

	Return the width, in cells, necessary to display the first ``n``
	characters of the unicode string ``pwcs``.  When ``n`` is None (default),
	return the length of the entire string.

	 if a non-printable character is encountered. 0 width added
	"""
	# pylint: disable=C0103
	#         Invalid argument name "n"
	from wcwidth import wcwidth
	end = len(pwcs) if n is None else n
	idx = py.slice(0, end)
	width = 0
	for char in pwcs[idx]:
		wcw = wcwidth(char)
		if wcw < 0:
			width += 0
		else:
			width += wcw
	return width  #py.No return 0
display_width=get_str_display_width=wcswidth


def get_javascript_function(source,function_name):
	T=py.importT()
	start='async function {}('.format(function_name)
	end='}}//end {}'.format(function_name)
#format string '}}'表示一个 },否则 ValueError: Single '}' encountered in format string
	r=T.sub(source,start,end)
	if not r:
		start='function {}('.format(function_name)
		r=T.sub(source,start,end)
		if not r:
			return py.No('not found function {} in js source'.format(function_name),source,start,end)
		return start+r+end
	return start+r+end
getjsf=get_js_func=get_js_function=get_javascript_function

def lxml_etree_to_str(e):
	from lxml import etree
	h= etree.tostring(e, pretty_print=True).decode()
	if '&#' in h:
		h=html_decode(h)
	return h
			
x2s=xpath2str=xpath_to_str=xpath_str=xpath_element_to_str=element_to_str=etree_tostring=lxml_to_str=etree_to_str=etree_tostring=lxml_etree_to_str

def xpath(*a,**ka):
	'''  xpath(astr<optional > ,xpath,file=''<only_optional_ka> ):
	'''
	from lxml import etree
	U=py.importU()
	sa_err='ArgumentError: You must provide (either astr or file<only_optional_ka>) and xpath , '
	# print(len(a))
	if len(a)>2:
		return py.No(sa_err+'but got len(a)==%s'% len(a),a,ka)
	astr=U.get_duplicated_kargs(ka,'a','ast','astr','s','st','t','text','txt','h','html')
	file=U.get_duplicated_kargs(ka,'file','f','FILE','fileName','filename')#last
	xpath=U.get_duplicated_kargs(ka,'xpath','x','XPath','xp')
	if not xpath:
		if len(a) == 1:
			if not astr and not file:
				return py.No(sa_err+'but only got 1 argument',a)	
			xpath=a[0]
		elif len(a)==2:
			if astr:return py.No(sa_err+'but got duplicated [astr]')
			astr =a[0]
			xpath=a[1]	
			
	if file:
		if astr or len(a)!=1:
			return py.No(sa_err+'not both. len(a)==%s>1'%len(a))
		F=py.importF()
		file=F.auto_path(file)
		e= etree.parse(file, etree.HTMLParser())
	else:
		e= etree.fromstring(astr, etree.HTMLParser())
	return e.xpath(xpath)
	
def word_wrap(s,width=46,eol=py.No('auto'),**ka):
	'''textwrap.wrap(text, width=70, **kwargs)
47: zhuanlan code max len	
	'''
	U=py.importU()
	replace_whitespace=U.get_duplicated_kargs(ka,'replace_whitespace','remove_old_eol','del_eol','del_old')
	import textwrap
	if not eol:
		if '\r\n' in s:
			eol='\r\n'
		else:
			eol='\n'
	return eol.join(
		textwrap.wrap(s, width=width, replace_whitespace=replace_whitespace)
	)
	
	
break_line=word_wrap

def is_valid_idcard(idcard):
	import re
	IDCARD_REGEX = '[1-9][0-9]{14}([0-9]{2}[0-9X])?'

	if isinstance(idcard, int):
		idcard = str(idcard)

	if not re.match(IDCARD_REGEX, idcard):
		return False

	items = [int(item) for item in idcard[:-1]]

	## 加权因子表
	factors = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)

	## 计算17位数字各位数字与对应的加权因子的乘积
	copulas = sum([a * b for a, b in zip(factors, items)])

	## 校验码表
	ckcodes = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')

	return ckcodes[copulas % 11].upper() == idcard[-1].upper()
sfz=isfz=is_sfz	=is_valid_idcard

def columnize(iterable,width=120):
	''' 144 break line in default Win+R Cmd window
'''
	# from IPython.utils.text import columnize as _columnize
	if not py.iterable(iterable):return py.repr(iterable)
	import IPython.utils.text
#TODO dict columnize
# { k1:v
#	k2:[small list]
# 	k3:[long,list,
# 		auto ident
# 		and columnize]
#	k4:and recursively
# }	
	if py.isdict(iterable):
		return pformat( iterable )
		# return pformat( {k:pformat(v) for k,v in iterable.items() } )
	r= IPython.utils.text.columnize([pformat(i) for i in iterable],
		row_first=True, separator=' , ', displaywidth=width)
	return r

def justify(s,size=0,char=' ',method=wc_ljust,cut=False):#'ljust'
	''' ljust() 方法返回一个原字符串左对齐,并使用空格填充右边至指定长度的新字符串。
	'''
	s= string(s)
	if size<1:
		return s
		# raise py.ArgumentError('size must > 0',size)
	if py.istr(method):
		if cut and len(s)>=size:
			return s[:size]
		return py.getattr(s,method)(size,char)	#
	if py.callable(method):
		if cut and wcswidth(s)>=size:
			return wc_cut(s,size)
		return method(s,size,char) #TODO 统一参数
	raise NotImplementedError('method must str.funcName or callable')
padding=justify
	
def encode(s,encoding):
	'''
	'''

def diff_bytes(b1,b2,p=True):
	all_args=py.importU().getArgsDict()
	U=py.importU();F=py.importF()
	sp=F.mkdir(diff_bytes.__name__)
	rf=[]
	for k,v in  all_args.items():
		# print(k,v)
		if not py.isbytes(v):continue
		f=F.write('{}{}={}'.format(sp,filename_legalized(k),len(v), ) ,v)
		rf.append(f)

	if py.isbytes(b1):b1=b1.splitlines()
	if py.isbytes(b2):b2=b2.splitlines()
	import difflib
	context = difflib.context_diff
	r=difflib.diff_bytes(context, b1 ,b2 )
	r=b''.join(r)
	if p:
		print(r)
	else:
		rf.insert(0,' '*33)
		rf.insert(0,r)

	return rf
diffb=diffBytes=diff_bytes

def diff(expected, actual,p=True,pformat=False):
	"""
	Compare two sequences of lines; generate the delta as a unified diff.
	Helper function. Returns a string containing the unified diff of two multiline strings.
	"""

	import difflib
	if pformat:
		U,T,N,F=py.importUTNF()
		pformat=T.pformat
		try:
			pformat=py.from_qgb_import('ipy').pformat
		except:pass
		if not py.istr(expected):
			expected=pformat(expected)
		if not py.istr(actual):
			actual=pformat(actual)
	expected=expected.splitlines(1)
	actual=actual.splitlines(1)

	diff=difflib.unified_diff(expected, actual)
	r=''.join(diff)
	if p:
		print(r,'\n diff_len:%s'%len(r))
	else:
		return r

def recursive_join(s,iter,prepend_layer=False,append_layer=False,format_layer=False,_layer=0):
	if py.istr(iter):
		return iter
	else:
		si=py.str(_layer)
		if prepend_layer:
			return s.join([recursive_join(si+s,i,_layer=_layer+1,
					prepend_layer=True,append_layer=append_layer,format_layer=format_layer
				) for i in iter])
		
		if append_layer:
			return s.join([recursive_join(s+si,i,_layer=_layer+1,
					prepend_layer=prepend_layer,append_layer=True,format_layer=format_layer
				) for i in iter])
		
		if format_layer:
			return s.join([recursive_join(s.format(_layer),i,_layer=_layer+1,
					prepend_layer=prepend_layer,append_layer=append_layer,format_layer=True
				) for i in iter])
		return s.join([recursive_join(s.format(_layer),i,_layer=_layer+1, ) for i in iter])

recursiveJoin=recursive_join

def join(*iterable,separator=',',**ka):#separator=','
	'''T.join( ###<py.No )==''  
In [1612]: T.join(1)
Out[1612]: '1'

In [1613]: T.join(1,2)
Out[1613]: '1,2'

In [1614]: T.join(765432)
Out[1614]: '765432'

In [1615]: T.join(range(43))
Out[1615]: '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,1
'''	
	U=py.importU()
	if separator==',':separator=U.get_duplicated_kargs(ka,'s','split','splitor','separator',default=',')
	if py.len(iterable)<1:
		raise py.ArgumentError('need iterable')
	if py.len(iterable)==1:
		iterable=iterable[0]
	if py.istr(iterable):return iterable
	if (not U.is_generator(iterable)) and (not py.iterable(iterable)):
		return string(iterable)
	return separator.join( string(i) for i in iterable )
	
def intToHex(number,uppercase=True):
	'''
'{:02X}'.format(257)=='101'

'''
	sf='{:02{}}'
	if uppercase:sf=sf.format('X')
	else:sf=sf.format('x')
	return sf.format(number)

gURL_unreserved_mark=('-','_','.','!','~','*',"'",'(',')')
gURL_reserved=(';','/','?',':','@','&','=','+','$',',')
gsURL_not_escaped=gURL_not_escaped='-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz.'

def parse_url_arg(url):
	if py.is2():
		from urlparse import urlparse,parse_qs
	else:
		from urllib.parse import urlparse,parse_qs
	o = urlparse(url)
	return parse_qs(o.query)
parse_qs=parse_url_arg

def get_url_arg(url,arg_name):
	d=parse_url_arg(url)
	if arg_name not in d:
		return py.No('not found {} in [{}]'.format(arg_name,url),d)
	v=d[arg_name]
	if py.len(v)==1:
		return v[0]
	else:
		return v
url_get_arg=get_url_arg

def get_url_args(url,*a,default=py.No('Not found')):
	d=parse_url_arg(url)
	r=[]
	for i in a:
		v=d.get(i,default)
		if py.len(v)==1 and py.islist(v):
			v=v[0]
		r.append(v)
	return r
	
def FileNameToURL(a):
	'''
	urllib.parse.unquote(string, encoding='utf-8', errors='replace')
	'''
	# r=[]
	# skip=0
	# rskip=''
	# for i,c in enumerate(a):
		# if skip>0:
			# skip-=1
			# continue
		# if c=='-'
			# skip=2
			
		# r.append() 
	import urllib
	a=a.replace('-','%')
	a=urllib.parse.unquote(a)
	return a # always return str
fn2url=FileNameToURL

def urlToFileName(url):
	'''
	args : url_or_bytes
	'''
	if py.istr(url):url=url.encode('utf-8')
	url=py.list(urlEncode(url) )
	
	for i,c in enumerate(url):
		if c not in '%'+gsURL_not_escaped[1:] :
			url[i]='%{0:02X}'.format( py.ord(c) ) 
	
	return ''.join(url).replace('%','-')
	
url2fn=url2file=url2fileName=url_to_filename=urlToFileName


def get_domain_parts_by_url(url_or_domain,**ka):
	'''(url,
                fail_silently=False,
                fix_protocol=True,#False,
                search_public=True,
                search_private=True)
	
	
	In [513]: domain_parts, non_zero_i, parsed_url
Out[513]:
(['buyertrade', 'taobao', 'com'],
 2,
 SplitResult(scheme='https', netloc='buyertrade.taobao.com', path='/trade/itemlist/list_bought_items.htm', query='', fragment=''))
 
 T.get_domain_parts_by_url(websocket,fix_protocol=False)   
'''
	if 'fix_protocol' not in ka:
		ka['fix_protocol']=True
	
	import tld
	return tld.utils.process_url(url=url_or_domain,**ka)[0]

def getFLD(url_or_domain,fix_protocol=True):
	"""Extract the first level domain.
# Source path of Mozilla's effective TLD names file.
NAMES_SOURCE_URL = 'http://mxr.mozilla.org/mozilla/source/netwerk/dns/src/' \
                   'effective_tld_names.dat?raw=1'

# Relative path to store the local copy of Mozilla's effective TLD names file.
NAMES_LOCAL_PATH = 'res/effective_tld_names.dat.txt'	
	"""
	import tld
	try:
		return tld.get_fld(fix_protocol=fix_protocol,url=url_or_domain)
	except Exception as e:
		return py.No(url_or_domain,e)
		#TldDomainNotFound: Domain 网站域名 didn't match any existing TLD name!
get_fld=getFLD



################### zh #############################
# u'([\u4e00-\u9fff]+)'  
RE_ZH_PATTERN = re.compile(u'[\u4e00-\u9fa5]+')

def list_filter_zh(a):
	return RE_ZH_PATTERN.findall(a )
filter_zh_as_list=list_filter_zh

def str_filter_zh(a,max_not_zh=0,splitor=' '):
	if not max_not_zh:
		return splitor.join(RE_ZH_PATTERN.findall(a ) )
	return regexReplace(a,r'[^\u4e00-\u9fa5]{%s,}'%max_not_zh,'')
filter_zh_as_str=filter_zh=filterZh=str_filter_zh

def hasZh(word):
	'''
	判断传入字符串是否包含中文
	:param word: 待判断字符串
	:return: True:包含中文  False:不包含中文
	'''
	global RE_ZH_PATTERN
	match = RE_ZH_PATTERN.search(word)
	return match
contain_zh=has_zh=hasZh	
################# zh end ##############
def filter_sint_list(a,digits=py.range(1,999)):
	if py.isint(digits):
		digits=py.range(digits,999)
	# digits=py.list(digits)
	r=[]
	# pint=False
	si=''
	for i in a:
		if i in number:
			si+=i
		else:
			if py.len(si) in digits:
				r.append(si)
			si=''
	if py.len(si) in digits:
		r.append(si)
	return r
int_filter=matchInt=match_int=filter_sint=filter_int=filterInt=filter_sint_list

RE_HTML_TAG = re.compile(r'<[^>]+>')
def filter_html(text):
	return RE_HTML_TAG.sub('', text)
html_filter=filter_html

def html2text(html,baseurl='',ignore_images=True,ignore_links=True,):
	from html2text import HTML2Text
	if not html:return html
	
	h=HTML2Text(baseurl=baseurl)
	h.ignore_images=ignore_images
	h.ignore_links=ignore_links
	return h.handle(html)
h2t=html2txt=html_to_text=html2text

def html_prettify(html, formatter="html5",p=py.No('auto')):
	'''
	formatter =  'html',"html5","minimal",None
	'''
	import bs4
	if py.isinstance(html,bs4.element.Tag):
		return html.prettify(formatter=formatter)
	if py.isinstance(html,bs4.BeautifulSoup):
		bs=html
	else:
		bs=BeautifulSoup(html)
	r= bs.prettify(formatter=formatter)
	for tag in ['<html>','</html>','<head>','</head>','<body>','</body>']:
		if tag not in html:
			r=r.replace(tag,'')
	#TODO last line strip()
	r= r.strip()
	if py.isno(p):
		U=py.importU()
		if U.is_ipy_call():
			p=True
		else:
			p=False
	if p:
		print(r)
		return None
	else:
		return r
nice_html=htmlBeautify=html_beautify=html_prett=pretty_html=html_pretty=prettify_html=html_prettify

def BeautifulSoup(html):
	if not html:return html
	from bs4 import BeautifulSoup
	t=py.str(py.type(html) )
	if 'requests.models.Response' in t:
		html=html.text
	try:
		import lxml
		bs=BeautifulSoup(html,features='lxml' )	
	except:
		bs=BeautifulSoup(html,features="html5lib" )	
	return bs
bs=beautifulSoup=BeautifulSoup

def readableTimeText(txt,browser=False):
	U=py.importU()
	def ref(a):
		a=a.group()
		if '.' in a:
			a=py.float(a)
		else:
			it=py.int(a)
			if py.len(a)==13:
				it=it/1000
			a=it	
		return U.stime(a)

	r= regexReplace(txt , r'\d{10,}[.\d]{0,4}',ref)
	if browser:
		U.browserObj(r)
	else:
		return U.StrRepr(r)
timeText=readableTimeText

RE_IP= re.compile('''(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))''')
def ipLocationText(text,location_format=' [{0}] ',reverse_ip=True,**ka):
	''' p='deprecated'
	'''
	U=py.importU()
	N=py.importN()
	
	def fr(a):
		# i0,i=a.span()
		# a=py.int(text[i0:i] )
		a=a.group()
		location=N.ipLocation(a,reverse_ip=reverse_ip)
		return location

	r=regexReplace(text,RE_IP,fr)
	# if p:U.pln(r)
	# else:return r
	return U.StrRepr(r)
readableIPLocationText=ipLocationText

	
def readableSizeText(text,sizeMultiple=1,p=True):
	''' if not p :return text'''
	U=py.importU()
	F=U.F
	def fr(a):
		# i0,i=a.span()
		# a=py.int(text[i0:i] )
		a=py.int(a.group())*sizeMultiple
		a=F.readableSize(a)
		return a
	r=regexReplace(text,r'\d{5,}',fr)
	if p:U.pln(r)
	else:return r

	
	
	
def regex_count(a,regex):
	return py.len(re.findall(regex, a))
countRegex=regexCount=count_regex=regex_count
	
def regex_replace(a,regex,str_or_func):
	''' str_or_bytes_or_func
func( a: <_sre.SRE_Match object; span=(2388, 2396), match='21758465'>  ):
	match==a.group()	
	
	
\QGB\Anaconda3\Lib\site-packages\jedi\evaluate\compiled\fake\_sre.pym
	class SRE_Match():
			yield SRE_Match(self)	
	'''
	if py.istr(str_or_func) or py.isbyte(str_or_func):
		def func(_a):
			#   <_sre.SRE_Match object; span=(2388, 2396), match='21758465'>
			# match==a.group()	
			return str_or_func
	else:
		func=str_or_func
	if not py.callable(func):raise py.ArgumentError('str_or_func',str_or_func)
	
	if py.istr(regex) or py.isbyte(regex):
		p=re.compile(regex)
	else:
		p=regex
	return p.sub(func,a)
regexReplace=regex_replace
##################  regex end  ############################
def iter_detect(b,range=[]):
	'''

	'''
	U=py.importU()
	r=[]
	size=len(py.str(len(b)))+2
	ib=U.IntRepr(len(b),size=size)
	hb=U.IntRepr(hash(b),size=22)
	iz=U.IntRepr(0,size=size)
	hz=U.IntRepr(0,size=22)
	for c in charset:#max len(c) == 18 , #max hash len == 20
		w=[U.StrRepr(c,size=18),ib,hb]
		try:
			s=b.decode(c)
			w.append( U.IntRepr(len(s),size=size) )
		
			w.append( U.IntRepr(hash(s),size=22) )
			# w=w+[, ] # TODO repr more info obj
		except:
			w=w+[iz,hz,iz,hz]
			r.append(w)
			continue
			
		try:
			bb=s.encode(c)
			w=w+[U.IntRepr(len(bb),size=size),U.IntRepr(hash(bb),size=22)]
		except:
			w=w+[iz,hz]

		if py.isint(range):
			w.append( U.StrRepr(s[range:range+22],size=22) )
		elif U.len(range)==2:
			w.append( U.StrRepr(s[range[0]:range[1]],size=22) )
		


		r.append(w)
	return r
iterDecode=iter_decode=iterDetect=iter_detect		
		
def autoDecode(abytes,confidence=0.7,default=py.No('default encoding "" ')  ):
	if abytes==b'':return ''
	if py.isunicode(abytes):return abytes
	if not py.isbyte(abytes):
		raise py.ArgumentError('is not bytes',abytes)
	encoding=detect(abytes=abytes,confidence=confidence,default=default)
	if not encoding:return encoding
	return abytes.decode( encoding )
detect_decode=detectDecode=detectAndDecode=auto_decode=autoDecode

def decode(abytes,codecs=('gb18030','utf-8','auto','latin' ) ):
	for i in codecs:
		i=i.lower()
		try:
			if i=='auto':return detectAndDecode(abytes)
			return abytes.decode(i)
		except Exception as e:
			pass
	return py.No('can not decode',codecs,e,abytes)#large var in last	

def print_unicode_escape(a):
	print(	a.encode('unicode-escape').decode('ascii')  )
	
def strFormDataToDict(a):
	'''true value can not convert
in js:
	{1:2}  >   "{"1":2}"
	'''
	U=py.importU()
	r={}
	for i in a.splitlines():
		i=i.strip()
		if not i:continue
		if ':' not in i:raise ValueError('unexpected chrome DevTools Form Data:',i)
		key=sub(i,'',':')
		v=sub(i,':','')
		if v==str( U.eval(v) ):
			r[key]=v
		else:
			r[key]=py.repr(v)
	return r


def html_encode(a):
	if py.is3():
		from html import escape
	if py.is2():
		from HTMLParser import HTMLParser
		escape = HTMLParser().escape #TODO not test 
	# 
	return escape(a)

def html_decode(a):
	''' will not remove html tag '''
	if py.is3():
		from html import unescape
	if py.is2():
		from HTMLParser import HTMLParser
		unescape = HTMLParser().unescape
	r=a
	# r=replacey(a,['<br>','<br/>','<br />'],'\n')
	r= unescape(r).replace(py.chr(0xA0),' ')  # \xa=\n  not \xa0
	return r
html_unescape=htmlDecode=html_decoded=html_decode

# data = "U.S. Adviser&#8217;s Blunt Memo on Iraq: Time &#8216;to Go Home&#8217;"
# print decode_unicode_references(data)
def netloc(url):
	''' return "ip:port" '''
	from six.moves.urllib.parse import urlsplit
	url=url.strip()
	if '://' not in url:
		url='http://'+url
	up=urlsplit(url=url)
	return up.netloc
hostname=host_name=get_url_netloc=netloc

def url_split(url):
	from six.moves.urllib.parse import urlsplit
	return urlsplit(url=url)  # obj
urlsplit=url_split	

def urlEncode(a,safe='/', encoding=None, errors=None):
	''' a : str_or_bytes
	#todo 	convert Non-string objects
#TODO 重复调用 会出现 "%252525252525...."	
	
quote real path	
 'C:\\QGB\\Anaconda3\\lib\\urllib\\parse.py',
 '-n 782'	
	'''
	from six.moves.urllib.parse import quote
	return quote(a,safe=safe, encoding=encoding, errors=errors) # if a is function: TypeError: quote_from_bytes() expected bytes
urlencode=url_encode=urlEncode

def urlDecode(a):
	''' a : str_or_bytes
	'''
	if py.is3():
		import urllib
		if isinstance(a, py.bytes):a=a.decode()
		# if not py.istr():
		return urllib.parse.unquote(a)
	raise NotImplementedError()
urldecode=url_decode=urlDecode

def startsEnds(a,chars):
	'''S.strip([chars]) -> str
'1234'.strip('1') # '234'
	'''
	if a.startswith(chars) and a.endswith(chars):return True
	else:return False
startsends=startsEnds

def strValue(a):
	try:return int(a)
	except:pass
	# try:return py.list(a)
	# try:return py.dict(a)
	# try:return py.tuple(a)
	try:return py.tuple(a)
	except:pass

def match_wildcard(a,exp):
	'''Wildcard character'''
	import fnmatch
	exp=fnmatch.translate(exp)
	exp=re.compile(exp)
	try:
		return exp.match(a).group()	
	except:
		return ''
wildcard=matchWildcard=match_wildcard

def regex_match_named_return_dict(a,regex):
	''' #not    ,**defaults
re.search('(?P<name>.*) (?P<phone>.*)', 'John 123456').group('name')=='John'
#py3.7 ka的顺序与调用顺序一致	
'''
	regex = re.compile(regex)
	if not regex.groupindex:
		raise py.ArgumentError(regex,'need (?P<name>regex) ... ')
	d={}
	r= re.search(regex,a) # if not match return None
	if not r:
		return py.No('NotMatch:',regex,a)
	# 一组没匹配到 {'protocol': None} 与 匹配到空 {'aaa':''}  是不一样的
	return r.groupdict()
	# for name,v in r.items():
		
	
	re.search(a,regex)
regex_groupdict=regex_named=named_regex_match=regex_match_named=match_regex_named=regex_match_named_return_dict
	
def regexMatchAll(a,regex):
	return [i.group() for i in re.finditer(regex,a)]
matchRegex=matchRegexAll=regexMatchAll
		
def regexMatchGroups(a,regex,flags=0):
	''' return [list of re.search group [s]]
re.search(pattern, string, flags=0)
pattern	匹配的正则表达式
string	要匹配的字符串。
flags	标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。
	'''
	r= re.search(regex,a,flags=flags)
	if r:
		if r.groups():#返回一个包含所有小组字符串的元组，从 1 到 所含的小组号。
			r=[r.group()]+py.list(r.groups())
		else:r=[r.group()]
		return r
	else:
		return []
match_groups=matchGroups=regexMatchGroups

def regex_match_one(a,*regexs,**ka):
	'''  raise_exception=False

	return :str  match_groups first
	
	
正则表达式的先行断言和后行断言一共有4种形式：

(?=pattern) 零宽正向先行断言(zero-width positive lookahead assertion) 代表字符串中的一个位置，紧接该位置之后的字符序列能够匹配pattern。


(?!pattern) 零宽负向先行断言(zero-width negative lookahead assertion)

(?<=pattern) 零宽正向后行断言(zero-width positive lookbehind assertion) 代表字符串中的一个位置，紧接该位置之前的字符序列能够匹配pattern。


(?<!pattern) 零宽负向后行断言(zero-width negative lookbehind assertion)	
	'''
	U=py.importU()	
	
	raise_exception=U.get_duplicated_kargs(ka,'raise_exception','exception','exp','throw_err')
	for regex in regexs:
		r=regexMatchGroups(a,regex)
		if r:
			while py.len(r)>1:
			#T.matchRegexOne('http://3.3.32.3',T.RE_IP)==['3.3.32.3', None]
				rt=[i for i in r if i]
				if r!=rt:
					r=rt
					continue # 如果 去除 None后 len ==1 。 自动跳出while，否则 下面
				print('#TODO :fix regex_match_one return all match list')
				return r
			return r[0]		
	if raise_exception:
		raise Exception('Not match regexs in a',a,regexs)
	return ''
match=match_one=matchRegexOne=regexMatch=regexMatchOne=regex_match_one

def re_search(regex,a):
	'''不是 research 研究 ！,跟 match()  只有参数顺序不同，方便 re.search 改写'''
	return match(a,regex)
regexSearch=reSearch=re_search

# gsV='?'	#todo and test
def parseWildcardExp(a,wildcard='*',value='?'):
	if py.istr(a):
		pass
	elif py.type(a) is py.list:
		return a
	else:
		raise Exception('arg need str or list')
	
	r=[]
	tmp=''
	
	na=py.len(a)
	nw=py.len(wildcard)
	nv=py.len(value)
	i=0
	while i <na:
		if a[i] in (wildcard[:1],value[:1]):
			r.append(tmp)
			tmp=''
			if a[i:].startswith(wildcard):
				i+=nw
				r.append({})
				break
			if a[i:].startswith(value):
				i+=nv
				r.append([])
				break
		else:
			tmp+=a[i]
		i+=1
	return r
parseWildcard=parseWildcardExp	
def matchValue(a,exp):
	''' * wildcard
	? value'''
	a=parseMatchExp(a)
	r=[]

	return r	

def parseReMatch(rm,s):
	'''s: iii [or use 'i'*3 ] :return int,int,int
	short name i int,s string ,L long,f float,...
	case insensitive
	some different from https://docs.python.org/2/c-api/arg.html#c.Py_BuildValue'''
	r=[]
	for n,i in py.enumerate(s.lower()):
		n=rm.group(n+1)
		if i=='i':r.append(py.int(n))
		if i=='s':r.append(py.str(n))
		if i=='l':r.append(py.long(n))
		if i=='f':r.append(py.float(n))
	return py.tuple(r)
def matchHead(txt,regex):
	r=re.match(regex,txt)
	if r:return r.group()
	else:return ''

def strToHex(a,split=''):
	return split.join(py.hex(py.ord(x))[2:] for x in a).upper()
s2h=strToHex
####################
def bytesToStr(a,coding='ISO-8859-1'):
	if not py.isbyte(a):
		return py.No('a is not bytes!',a)
	if py.is3():
		return a.decode(coding)
	else:
		return a
		
def StrToBytes(a,coding='ISO-8859-1'):
	if not py.istr(a):
		return py.No('a is not str!',a)
	if py.is3():
		return a.encode(coding)
	else:
		return a
		
###################
gdBaseN={
54:'abcdefghijkmnpqrstuvwyzABCDEFGHJKLMNPQRSTUVWYZ23456789',#T.replacey(T.alphanumeric,['0','1','l','o','O','I','x','X'],'')  
56:'abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789',#T.replacey(T.alphanumeric,['0','1','l','o','O','I'],'')  
58:"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz",
62:alphanumeric,
63:alphanumeric_,
64:Az09+'+/',#注意 不是alphanumeric+'+/',即 azAZ09
94:printAscii[1:],
256:char256
}
gs09AZ=number+AZ
for i in range(2,37):
	gdBaseN[i]=gs09AZ[:i]
###################
def bytesToBase64(a):
	'''return str'''
	import base64
	if py.is3():
		return base64.b64encode(a).decode('ascii')
	else:
		return base64.b64encode(a)

def base64_to_str(a):
	import base64
	if py.istr(a):
		return detectAndDecode(base64.b64decode(a))
	if py.isbyte(a):
		return base64.b64decode(a) #type bytes
base64decode=b64_str=base64_to_str	

def base64_to_bytes(a):
	import base64
	if py.istr(a):
		return base64.b64decode(a)
	if py.isbyte(a):
		return base64.b64decode(a) #type bytes
b64_bytes=base64_to_bytes	

		
def strToBaseN(a,base=64,symbols=None):
	''' #TODO #BUG
T.baseN_encode(b'http://klk')
'BodHRwOi8wAAAr'

T.baseN_decode(_)
'http:/0\x00\x00+'

'''	
	if not symbols:symbols=gdBaseN[base]
	r=parseInt(a,256)
	return intToStr(r,base,symbols)
base64=baseN=baseN_encode=s2baseN=strToBaseN

def baseNToStr(a,base=64,symbols=None):
	'''TODO: '''
	if not symbols:symbols=gdBaseN[base]#先传入符号表，baseN的符号表可以由用户指定
	r=parseInt(a,base,symbols)
	return intToStr(r,256)#这里使用  默认字节符号表
baseN_decode=baseN2s=baseNToStr
	
def intToStr(n,base=16,symbols=None):
	if n<0 or base < 2:raise Exception(n,base,'(n,base) invild')
	if not symbols:symbols=gdBaseN[base]
	r=''
	while n>=base:
		r=symbols[py.int(n%base)]+r
		n=py.int(n/base)
	return symbols[n]+r	
radix=i2s=intToStr

def parseInt(a,base=16,symbols=None):
	# if base==256:#字节流，这样效率更高？
		# r=0
		# for i,v in enumerate(a[::-1]):
			# r+=ord(v)*pow(256,i)
		# return r
	U=py.importU()	
	if base<2:raise Exception(base,'base invild')
	if not symbols:symbols=gdBaseN[base]
	
	if base<36:return py.int(a,base)#int() base must be >= 2 and <= 36
	else:
		is_py3_bytes=py.isbyte(a) and py.is3()
		r=0
		for i,v in enumerate(a[::-1]):
			# try:
			''' str.index(b'1')  #TypeError: must be str, not bytes
			2:  In [1]: for i,v in enumerate(b'MzJyNDIz'):print(i,v)
				(0, 'M')
				(1, 'z')
			3:  In [3]: for i,v in enumerate(b'MzJyNDIz'):print(1,v)
				1 77
				1 122
			'''
			if not is_py3_bytes:
				v=symbols.index(v)	
			r+=v*pow(base,i)
			# except Exception as e:
				# U.pln((symbols,[v])  )# 
		return r
		#TODO
		
		
def literal_eval(str):
	"""
ast.literal_eval("\t'''\n\n '''",)	# *** IndentationError: unexpected indent
#BUGFIXED 前面不能乱空格

	"""
	import ast
	return ast.literal_eval(str.strip())
unrepr=ast_literal_eval=literal_eval

def javascript_object_loads(s):
	'''	js_obj = '{x:1, y:2, z:3}'

	'''
	import demjson 
	return demjson.decode(s)

load_js=loads_js=load_js_obj=load_js_object=js_loads=js_obj_loads=javascript_object_loads

def jsonToDict(a):
	'''py2: 不同于 json_loads ，不会自动转换 到unicode'''
	import ast
	return ast.literal_eval(a.replace('false','False').replace('true','True'))
js2py=jsonToDict
	
def json_load(astr='',file=None,comment=lambda s:re.sub("//.*","",s,flags=re.MULTILINE),**ka):
	import json
	if not (astr or file):
		return py.No('either astr or file, but not any') #一个也没有 不用 both not
	if (astr and file):
		return py.No('either str or file, but not both') # not all 可以吗
	
	if file:
		if py.istr(file):
			F=py.importF()
			file=F.auto_path(file)
			file=py.open(file,'rb')
		if not py.isfile(file):
			return py.No('file must be str or file-like-obj')
			
		with file:
			try:
				return json.load(file,**ka)
			except Exception as e:
				return py.No(e,file)	
	#######			
	if comment and py.callable(comment):
		astr=comment(astr)
		
	try:
		return json.loads(astr,**ka)
	except Exception as e:
		return py.No(e,astr)
json_loads=json_load

def json_dumps(obj):
	U=py.importU()
	def default(obj):# not json basic class
		return py.repr(obj)
		# return {'obj-%s'%U.count(obj):py.repr(obj)}

	import json
	try:
		return json.dumps(obj ,default=default )
	except Exception as e:
		return py.No(e)
json_dump=json_dumps

def string(a,decode=''):
	'''return unicode'''
	# if py.istr(a):return a # 
	if py.is2():
		if py.type(a) is py.str and decode:return a.decode(decode)
		U=py.importU()
		if py.type(a) is py.unicode:return a#.encode(U.encoding)
		try:return py.str(a)
		except:return ''
	else:
		if isinstance(a,py.bytes) and decode:return a.decode(decode)
		if py.isint(a):# in case : U.IntCustomStrRepr
			a=py.int(a)
		if py.isfloat(a):## 添加一种 CustomStrRepr
			a=py.float(a) 

		try:return py.str(a)
		except Exception as e:return py.No(e,a)
		
def stringToChars(a):
	'''TODO:flap'''
	a=string(a)

def inMutiChar(a,asc):
	'''(1,2)False  ('13','abc1')True'''
	if type('')==type(a) and len(a)>0:
		if len(asc)<1:return True
		for i in asc:
			if i in a:return True
	return False
def listToStr(a):
	if type(a)!=type([]):return ''
	sr=''
	for i in a:
		sr=sr+py.str(i)+','
	return '['+sr+']'
def ishex(a):
	if type('')!=type(a):return False
	if len(a)<1:return False
	for i in a.lower():
		if i not in hex:return False
	return True	
	
def isUpper(a):
	for i in az:
		if i in a:return False
	return True
def isLower(a):
	for i in az:
		if i in a:return False
	return True
	
def isString(a):
	if py.is2():return isinstance(a,basestring)#py.type(a) in (py.str,py.unicode)
	else:return isinstance(a,str)
istr=isStr=isString	


# def sub_head_if_not_s2(s,s1,s2=''):

def sub_head(s,s1,s2=''):
	if(s==None):return ()
	if py.isbytes(s):
		null=b''
	else:
		s= string(s)
		null=''	
	i1=s.find(s1)
	if not s2:
		i2=s.__len__()
	else:
		i2=s.find(s2,i1+len(s1))
	if(-1==i1 or -1==i2):
		return null
	i1+=len(s1)
	# U.pln( i1,i2
	return s[i1:i2]
subh=sub_left=subLeft=sub=sub_head

def sub_tail(s,s1,s2=''):
	'''
T.subLast('C:/test/list_bought_items.htm/10_15_知乎周源_list_bought_items.htm','_','_list_bought_items',)
应该等于 	知乎周源
'''	
	if(s==None):return ()
	if py.isbytes(s):
		null=b''
	else:
		s= string(s) # def string(a
		null=''
	i1=0
	if s2:
		i2=s.rfind(s2)
		if i2==-1:return null
		if s1:
			i1=s[:i2].rfind(s1)
			if i1==-1:return null
			i1+=len(s1)
		else:
			i1=0
	else:
		i1=s.rfind(s1)
		if i1==-1:return null
		i1+=len(s1)
		i2=s.__len__()
	return s[i1:i2] 

	# if(s2==''):
	# 	i2=s.__len__()
	# else:
	# 	i2=s.rfind(s2,i1+1)
	# if(-1==i1 or -1==i2):
	# 	return ''
	# i1+=len(s1)
	# U.pln( i1,i2
	# return s[i1:i2]
sublast=subt=sub_last=subLast=subr=sub_right=subRight=sub_tail
	
def replace_all_space(a,to='',target=r"\s+"):
	'''  多个连续空白字符会 缩减成 一个空格
	in char256 {' ', '\x0b', '\x1c', '\x1d', '\t', '\x0c', '\x1e', '\x85', '\xa0', '\x1f', '\r', '\n'}  removed'''
	import re
	return re.sub(target, to, a, flags=re.UNICODE)
del_space=del_spaces=remove_all_space=replace_all_spaces=delAllSpace=removeAllSpaces=removeAllSpace=replace_all_space

def replacey(a,olds,new='',case_sensitive=True):
	'''
#TODO case_sensitive	
	'''
	if not py.istr(a):return py.No('a is not str',a)
	if py.isdict(olds):
		if new:raise py.ArgumentError('replacey(a,dict) Conflict with new',new)
		for k,v in olds.items():
			a=a.replace(k,v)
	# else:a=str(a)
	# if(len(olds)<1):raise Exception('Target chars Null')
	else:
		if not case_sensitive:
			return re.sub('|'.join(re.escape(i) for i in olds),new,a,flags=re.IGNORECASE)
		for i in olds:
			a=a.replace(i,new)
	return a
	
def replace_all(a,old,new):
	''' S.replace(old, new[, count]) -> string'''
	while old in a:
		a=a.replace(old,new)
	return a
replaceAll=replace_all

def replace_once(a,old,new):
	''' s.replace(old, new, count=-1, /)
s.replace('lan','==',count=1) ###  TypeError: replace() takes no keyword arguments	
s.replace('lan','==',1) ### OK
	'''
	if not old:return a
	# i=a.index(old) # raise ValueError: substring not found
	i=a.find(old) # -1
	if i==-1:return a
	return a[:i]+new+a[i+py.len(old):]

def index_of_multi(a,*target):
	'''return one of target index in a
	'''
	for t in target:
		i=a.find(t)
		if i>0:return i
	return -1
indexOf=index_of=index_of_multi

def eval_or_exec_return_str_result(s,locals=None,globals=None,raise_SyntaxError=True,pformat_kw=None):
	import traceback
	def modify_traceback_str(st):
		T=py.importT()
		sub=T.sub(st,'eval_or_exec_return_str_result',' File ')
		if 'globals' in st and 'locals' in st:
			i=st.find('eval_or_exec_return_str_result',0)+1
			i=st.find(' File ',i)-1 # -1 为了对齐
			return st[i:]
		else:
			return st
	if not s:return '' #py.No('s is empty')	
	expression= False
	# filename='<>'
	try:
		code= compile(s, '<eval>', 'eval')
		expression=True
	except SyntaxError:
		try:
			code= compile(s, '<exec>', 'exec')
			expression=False
		except (SyntaxError,IndentationError) as e:
			if raise_SyntaxError:raise
			return py.No(e)
		except Exception as e:
			raise
	except IndentationError as e:
		if raise_SyntaxError:raise
		r= traceback.format_exc() 
		return modify_traceback_str(r)
	# if not width:
		# width=U.get_or_set('pformat_kw',{'width':144})['width']
		
	# from io import StringIO

	if locals==None :locals ={}
	if globals==None:globals={}
		
	if expression:
		try:
			r=py.eval(code,globals,locals)
		except Exception as e:
			r= traceback.format_exc() 
			r=modify_traceback_str(r)
	else:
		try:
			exec(code,globals,locals)
			if 'r' in locals:
				r=locals['r']
			else:
				r=py.No('can not find r in exec locals',source)
		except Exception as e:
			r= traceback.format_exc() 
			r=modify_traceback_str(r)
	if py.istr(r):
		return r
	else:
		U=py.importU()
		if not pformat_kw:
			pformat_kw=U.get_or_set('pformat_kw',{'width':144})
		if U.isipy():
			try:
				ipy=py.from_qgb_import('ipy')
				return ipy.pformat(r,**pformat_kw)# in U
			except Exception as e:
				return py.repr(e)
		
		try:return pformat(r,**pformat_kw)# in U
		except:return py.repr(r)
		
def html_template(s,locals=None,globals=None,delimiter='$',raise_SyntaxError=True,**ka):
	''' $[ ]$ 不行，有歧义，返回一个 空list  
[$ $]   <$ $>    {$ $}    ($ $)
	'''
	def find_delimiter():
		return
	if py.istr(delimiter):
		delimiter
		pass
	elif py.callable(py.getattr(rn,'finditer',0)):
		pass
	   	
	i=s.find(delimiter,0)
	rs=s[:i]
	i2=s.find(delimiter,i+1)
	
	rd={}
	while i!=-1 and i2!=-1:
		# i=i+1
		code=s[i+1:i2]
		ri=eval_or_exec_return_str_result(code,locals=locals,globals=globals,raise_SyntaxError=raise_SyntaxError)
		# s=s[:i]+ri+s[i2:]
		# if U.is_SyntaxError(code):
		# if skip_parse_error:
			# continue
			# raise SyntaxError(code,i,i2)
			
		
		# r.append([ code,i,i2])
		i=s.find(delimiter,i2+1)
		#如果此时 i==-1 ,【也没关系。仔细看看】
		rd[(i,i2)]=(ri,s[i2+1:i])
		
		
		i2=s.find(delimiter,i+1)
	for (ri,seg) in rd.values():
		rs+=ri+seg
	return rs+s[i2]
html_format=template=html_templete=html_template	

def format(s,**ka):
	''' 解决 python 自带format 不能跳过 未指定的 {name} 的问题 （ HTML-CSS  格式化）
	
 >  '%(a)s %(b)s'%(3,2)
TypeError: format requires a mapping  
##Solution##  '%(a)s %(b)s' % py.locals()

'%(1)s %("")s'%{'1':1,'""':54353}  # dict key必须为str，%()s支持任意字符串？，dict-key只能多，不能少
	'''
	for k,v in ka.items():
		
		s=s.replace('%({0})s'.format(k),v)
		
		# k=
		s=s.replace('{%s}'%k,v)
	return s

#############  str ops end ########3
def varname(a):
	sv=az+'_'
	if a[0] in sv:r=''
	else:r='_'
	sv+=number
	for i in a:
		if i.lower() in sv :r+=i
		else:r+='_'
	return r
	# return replacey(a,'_',':','.','\\','/','-','"',' ','\n','\r','\t','[',']')
# U.pln( varname(i09)

def filename_legalized(a,space=' '):
	'''  # 多个连续空白字符会 缩减成 一个 space
not auto cut long string

OSError: [Errno 22] Invalid argument: 'C:/test/clipboard/林文\n===\n.png'
	'''
	if not py.istr(a):a=string(a)
	a=replace_all_space(a.strip(),space)
	r=''
	for c in a:
		if c in NOT_FILE_NAME_WINDOWS:
			r+=py.chr(py.ord(c)+0XFEE0)
			continue
		r+=c
	
	return r
fileName=filename=legalized_filename=fileNameLegalized=file_legalized=filename_legalized
# filename.__str__=FILE_NAME	

def pathname_legalized(a):
	if not py.istr(a):a=string(a)
	a=replace_all_space(a.strip(),space)
	r=''
	for n,c in py.enumerate(a.strip()):
		if  (c in NOT_PATH_NAME) or (c==':' and n!=1):
			r+=py.chr(py.ord(c)+0XFEE0)
		else:r+=c
	return r
pathName=pathname=path_legalized=pathname_legalized

def is_have_zh(a):
	zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
	match = zhPattern.search(a)
	if match:return True
	return False
has_zh=haszh=hasZh=is_have_zh
# def har(fileName):

	
class Har():
	def __init__(s,fileName):
		null=None
		true=True
		false=False
		U=py.importU()
		F=U.F
		s.data=eval(F.read(fileName))['log']
		
	
	def __len__(s):
		return
	
def min_len(*a):
	'''return min length string(a[i])'''
	r=''
	for i in a:
		i=string(i)
		if len(i)<len(r):r=i
	return r
	
	
def max_len(*a):
	'''return max length string(a[i])'''
	r=''
	for i in a:
		i=string(i)
		if len(i)>len(r):r=i
	return r
	
def allAscii(a):
	if not py.istr(a):return False
	for i in a:
		if ord(i)>127:return False
		# U.pln( ord(i);break
	return True
	
gzfn=zfn=zf09=gszFinancial='''零壹贰叁肆伍陆柒捌玖拾佰仟萬億'''
#亿的后面 ，大写小写都是同一个。
#参见https://zh.wikipedia.org/wiki/中文数字
gsz09=gsZ09=gz09=z09=znumber=gzn=gszn=zn='''〇一二三四五六七八九'''
gsz10=gsZ10=z10='''一二三四五六七八九十'''
gszi=gsZI='''个、十、百、千、万、十万、百万、千万、亿、十亿、百亿、千亿、兆、十兆、百兆、千兆、京、十京、百京、千京、垓、十垓、百垓、千垓、秭、十秭、百秭、千秭、穰、十穰、百穰、千穰、沟、十沟、百沟、千沟、涧、十涧、百涧、千涧、正、十正、百正、千正、载、十载、百载、千载、极、十极、百极、千极'''
gZi=gzi=glzi=gsZI.split('、')

def readNumber(a,split=4,p=True):
	if split<1:return ''
	zh=gZi[::split]
	if py.isnum(a):a=py.int(a)#py2 ok
	if not py.istr(a):a=str(a)
	U=py.importU()
	decimals=''#小数点
	if a.find('.')==a.rfind('.')!=-1:
		decimals=sub_tail(a,'.')
		if decimals:decimals='.'+decimals
	a=''.join(U.one_in(py.list(a),number))
	while(a.startswith('0')):a=a[1:]

	s='';im=py.len(a);
	iz=0;
	zh[0]=''#忽略 个
	# zh=zh[1:]#忽略 个
	b=a[::-1]
	for i,k in enumerate(b):	
		# if i!=0 and i%split==0:
		if i%split==0:
			w=b[i:i+split]
			s=w[::-1]+zh[iz]+s
			iz+=1
			# U.pln(  i,
	if iz*split<im: # 如果不加这个判断  T.readNumber(234556789)== '京2亿3455万6789'
		s=b[iz*split:im][::-1]+zh[iz+1]+s
	s=s+decimals
	# U.repl()
	# for i in zh:U.pln( i.decode('utf-8').encode(U.stdout.encoding) )
	if py.is2():s=s.decode('utf-8').encode(U.stdout.encoding)
	if p:U.pln(s)	
	return s
chcp_all=[37, 437, 500, 708, 720, 737, 775, 850, 852, 855, 857, 858, 860, 861, 862, 863, 864, 865, 866, 869, 870, 874, 875, 932, 936, 949, 950, 1026, 1047, 1140, 1141, 1142, 1143, 1144, 1145, 1146, 1147, 1148, 1149, 1250, 1251, 1252, 1253, 1254, 1255, 1256, 1257, 1258, 1361, 10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10010, 10017, 10021, 10029, 10079, 10081, 10082, 20000, 20001, 20002, 20003, 20004, 20005, 20105, 20106, 20107, 20108, 20127, 20261, 20269, 20273, 20277, 20278, 20280, 20284, 20285, 20290, 20297, 20420, 20423, 20424, 20833, 20838, 20866, 20871, 20880, 20905, 20924, 20932, 20936, 20949, 21025, 21027, 21866, 28591, 28592, 28593, 28594, 28595, 28596, 28597, 28598, 28599, 28603, 28605, 38598, 50220, 50221, 50222, 50225, 50227, 50229, 51949, 52936, 54936, 55000, 55001, 55002, 55003, 55004, 57002, 57003, 57004, 57005, 57006, 57007, 57008, 57009, 57010, 57011, 65000, 65001]
# other 'Invalid code page'
chcp_utf=65001 # also can print zh
chcp_zh=936

gcszh=gZhEncodings=gcodingZh={'gb18030', 'gb2312', 'gbk', 'big5', 'big5hkscs', 'cp932', 'cp949', 'cp950', 'euc-jisx0213', 'euc-jis-2004', 'euc-jp', 'euc-kr', 'hz', 'idna', 'iso2022-jp', 'iso2022-jp-1', 'iso2022-jp-2', 'iso2022-jp-2004', 'iso2022-jp-3', 'iso2022-jp-ext', 'iso2022-kr', 'johab', 'mbcs', 'punycode', 'raw-unicode-escape', 'shift-jis','shift-jisx0213', 'shift-jis-2004', 'unicode-escape', 'unicode-internal', 'utf-16', 'utf-16-be', 'utf-16-le', 'utf-32', 'utf-32-be', 'utf-32-le', 'utf-7', 'utf-8', 'utf-8-sig'}
	
gcscp={'cp819', 'cp1026', 'cp1252', 'cp1140', 'cp1006', 'cp1361', 'cp932', 'cp424', 'cp154', 'cp720', 'cp936', 'cp500', 'cp869', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp1255', 'cp1254', 'cp1257', 'cp1256', 'cp1251','cp1250', 'cp1253', 'cp858', 'cp437', 'cp949', 'cp1258', 'cp737', 'cp367', 'cp850', 'cp852', 'cp855', 'cp857', 'cp856', 'cp775', 'cp875','cp874', 'cp950'}
gcharset=charset=gcs=gencodings=gcoding={'ascii', 'base64-codec', 'big5', 'big5hkscs', 'bz2-codec', 'charmap', 'cp037', 'cp1006', 'cp1026', 'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'cp1361', 'cp367', 'cp424', 'cp437', 'cp500', 'cp720', 'cp737', 'cp775', 'cp819', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp858', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp936', 'cp949', 'cp950', 'euc-jis-2004', 'euc-jisx0213', 'euc-jp', 'euc-kr', 'gb18030', 'gb2312', 'gbk', 'hex-codec', 'hp-roman8', 'hz', 'idna', 'iso2022-jp', 'iso2022-jp-1', 'iso2022-jp-2', 'iso2022-jp-2004', 'iso2022-jp-3', 'iso2022-jp-ext', 'iso2022-kr', 'iso8859-1', 'iso8859-10', 'iso8859-11', 'iso8859-13', 'iso8859-14', 'iso8859-15', 'iso8859-16', 'iso8859-2', 'iso8859-3', 'iso8859-4', 'iso8859-5', 'iso8859-6', 'iso8859-7', 'iso8859-8', 'iso8859-9', 'johab', 'koi8-r', 'koi8-u', 'latin-1', 'mac-arabic', 'mac-centeuro', 'mac-croatian', 'mac-cyrillic', 'mac-farsi', 'mac-greek', 'mac-iceland', 'mac-latin2', 'mac-roman', 'mac-romanian', 'mac-turkish', 'mbcs', 'palmos', 'ptcp154', 'punycode', 'quopri-codec', 'raw-unicode-escape', 'rot-13', 'shift-jis', 'shift-jis-2004', 'shift-jisx0213', 'tis-620', 'unicode-escape', 'unicode-internal', 'utf-16', 'utf-16-be', 'utf-16-le', 'utf-32', 'utf-32-be', 'utf-32-le', 'utf-7', 'utf-8', 'utf-8-sig', 'uu-codec', 'zlib-codec'}	
#https://docs.python.org/2/library/codecs.html#standard-encodings        https://docs.python.org/3/library/codecs.html#standard-encodings
g_arbitrary_codecs={'hex-codec', 'rot-13', 'bz2-codec', 'zlib-codec', 'base64-codec', 'quopri-codec', 'uu-codec'}
# xx is not a text encoding; use codecs.encode() to handle arbitrary codecs
if __name__=='__main__':
	U=py.importU()	
	U.repl()
	exit()
	# h= Har('ping.chinaz.com.har').data.keys()
	s='大多是'
	
	U.write('zh.html',s.decode('utf-8'))
	U.browser('zh.html')
	exit()
	c=set()
	for i in range(99999):
		i='shift-jis-%s'%i
		try:
			r='abc'.decode().encode(i)
			# if i in f:continue
			c.add(i)
			i='%-6s [%-6s] %s'%(i,r,F.b2h(r))
			# U.pln( i
		except:pass
	# U.pln( c
	exit()
	
	gcs=sorted(gcs)
	U.txt(str(gcs)) 
		
	exit()
	f=U.read(__file__)

	# for i in gsZI.split('、'):
		# U.pln( '%-2s %s'%(U.ct(),i.decode('utf-8').encode('gb18030'))
	# exit()
	
	# U.pln( detect(s)
	# s=s.decode('utf-8')
	# U.pln( haszh(s),len(s)
	# exit()
	# U.pln( max()
	# exit()
	# import os
	# os.chdir('cd')
	# sf=''
	# for i in FILE_NAME:
		# U.write(i,'123')
		# if U.read(i)=='123':sf+=i
	# U.pln( sf==FILE_NAME	
			
	# U.pln( U.inMuti('123456.9.9','18','1','',f=inMutiChar)
	# U.pln( len(asciiPrint)
	exit()
	# import urllib2,re
	# url='http://svn.kcn.cn/repos/kbs/'
	# r=urllib2.urlopen(url)
	# s=r.read()


	# U.pln( haszh(s)
	# s='44444.py.py'
	# U.pln( subr(s,'','.py')
	# U.pln( s.find(a,)
	# U.pln( s[:50]
	# U.pln( s.find('1')