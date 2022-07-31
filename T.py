# coding=utf-8	
#考虑qgb 位于另一个包内的情况
if __name__.endswith('qgb.T'):from . import py
else:#['T','__main__']
	import py
FILE_NAME=fileChars=FILE_CHARS="!#$%&'()+,-0123456789;=@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{}~"+' .'
PATH_NAME=pathChars=PATH_CHARS='/\\:'+FILE_NAME# include space, dot
gsNOT_FILE_NAME_WINDOWS=gsNOT_FILE_NAME=NOT_FILE_NAME_WINDOWS=NOT_FILE_NAME=r'"*/:<>?\|'
gsNOT_PATH_NAME_WINDOWS=gsNOT_PATH_NAME=NOT_PATH_NAME_WINDOWS=NOT_PATH_NAME=r'"*<>?|' # : is
gsNOT_FILE_NAME_LINUX=NOT_FILE_NAME_LINUX='/'+py.chr(92) # \ chr(0x5C)

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
gs256=char256=''.join([py.chr(i) for i in range(256)])
bytes256_list=byte256_list=[py.byte(i) for i in range(256)  ]
bytes256=byte256=b''.join( bytes256_list )
CR='\r'
LF=EOL=eol='\n'
EOLS=EOL+'='*44+EOL

TAB=Tab=tab='\t'
gspace=space=py.chr(0x20)
slash='/'   # chr(0x2F)
back_slash=backslash='\\' # chr(0x5C)
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
RE_VAR_SIMPLE=RE_VAR=RE_variable_name=RE_python_variable_name=r'[_a-zA-Z]\w*'#
#\w（不是W） 一共有 127073个字符，其中有815个不在sv中。sv一共有128491个非空字符。2233个不在\w中。交集有 126258个
#如果不小心用（注意大小写）A-z Matches a character in the range "A" to "z" (char code 65 to 122). Case sensitive.
RE_VARS_COMMAS=RE_vars_separated_by_commas=r'VAR(?:\s*,\s*VAR)+'.replace('VAR',RE_VAR)
RE_GIT_REPO_URL=RE_GIT_REPO=r'((?P<protocol>git|ssh|http(s)?)|(git@[\w\.]+))(:(\/\/)?)(?P<netloc>[\w\@\.\:~]+)\/(?P<user>[\w]+)\/(?P<repo>[\w\-\.]+(\.git)?)'
RE_GIT=RE_GIT_URL=RE_URL_GIT=RE_GIT_REPO_OTHER=RE_GIT_REPO+'(?P<other>[\w\/]*)'
RE_FLOAT=REF=r'[+-]?([0-9]*[.])?[0-9]+'
###############
SQLITE='SELECT * FROM sqlite_master;'

#########################################
squote=quote="'"
dquote=dQuote='"'

import re	
IGNORECASE=re_IGNORECASE=re.IGNORECASE

gError=None
try:
	try   :from cchardet import detect as _detect
	except:from chardet import detect as _detect
	
	def detect(abytes,confidence=0.7,default=py.No('default encoding "" ')  ):
		'''
T._detect( b'\x1b'*1)  ### {'encoding': None, 'confidence': 0.0, 'language': None}	

_detect 可能返回 {'encoding': None, 'confidence': None}
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
				
		if r['confidence'] and r['confidence']>confidence:return r['encoding']
		else:
			if default:return default
			# raise Exception
			return py.No(abytes,r,msg=
			'T.detect encoding {1} confidence {2} less then {3} {0}'.format(
			py.len(abytes),r['encoding'],r['confidence'],confidence)  )
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
def zh_convert(a,lang='zh-cn'):
	''' zh-cn 大陆简体; zh-tw 台灣正體; zh-hk 香港繁體
u'元旦快樂'	
'''	
	from zhconv import convert 
	return convert(a, lang)
zhc=zhconv=zh_convert

def replace_one(a,old,new):
	return a.replace(old, new,1) #count=1 #TypeError: replace() takes no keyword arguments 
replaceOnce=replace_one	

def get_most_common_substring(str_list):
	import operator
	return max(substring_counts(str_list).items(), key=operator.itemgetter(1))[0]
most_common_substring=get_most_common_substring	

def substring_counts(names):
	''' one str list return {}

'''
	from difflib import SequenceMatcher
	substring_counts={}

	for i,s in py.enumerate(names):
		for j in range(i+1,len(names)):
			string1 = names[i]
			string2 = names[j]
			match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
			matching_substring=string1[match.a:match.a+match.size]
			if(matching_substring not in substring_counts):
				substring_counts[matching_substring]=1
			else:
				substring_counts[matching_substring]+=1
	return substring_counts

# def string_index2(a,b,**ka):
	# U,T,N,F=py.importUTNF()
	

def string_index(a,b=None,line_max=122,escape_eol=('\r','\n'),p=0):
	U,T,N,F=py.importUTNF()
	r=[[],[],[],[]] #十位 个位 a b
	if b:mb=py.len(b) 
	else:mb=0
	w10=0
	for n,c in py.enumerate(a):
		if (n+1)%line_max==0:
			r
			# r[2].append('\n'*4)
		if escape_eol and c in escape_eol:
			c=py.repr(c)[1:-1]
			w=T.wcswidth(c)
		else:
			w=T.wcswidth(c)
			
		w10+=w
		r[1].append(T._09[n%10]+' '*(w-1))
		if n%10==9:
			s10=py.str(n//10)
			r[0].append(s10+' '*(w10-py.len(s10)))
			w10=0	
		r[2].append(c)
		if n<mb:
			r[3].append(b[n])
		
		
	r= '\n'.join([''.join(row) for row in r])
	if p:U.pln(r)
	else:return r
enu=enumerate=sindex=str_index=string_index	

def similarity_difflib(a,b,isjunk_function=None):
	''' '''
	import difflib
	seq = difflib.SequenceMatcher(isjunk=isjunk_function, a=a,b=b)
	ratio = seq.ratio()	
	return ratio
	
def char_to_unicode_literal_repr(a,):
	repr=a.encode("unicode_escape").decode('ascii')
	# if StrRepr:
	U,T,N,F=py.importUTNF()
	return U.StrRepr(a,repr=repr)
	# else:
		# return repr
unicode_literal=to_unicode_literal=char_to_unicode_literal_repr
		
def text_to_varname(a):
	''' '''
	T
	RE_VAR
	return
to_varname=text_to_varname
	
def html_table_to_list(html_or_url,**ka):
	'''
pandas.read_html first argument "io" : str, path object or file-like object
    A URL, a file-like object, or a raw string containing HTML. Note that
    lxml only accepts the http, ftp and file url protocols. If you have a
    URL that starts with ``'https'`` you might try removing the ``'s'``.
	
	'''
	U,T,N,F=py.importUTNF()
	if html_or_url.startswith('https://'):
		html_or_url=N.HTTP.get(html_or_url)
	import pandas
	return pandas.read_html(html_or_url) # return list of tables
	
def git_convert_ssh(a):
	''' '''
	U,T,N,F=py.importUTNF()
	u=T.regex_match_all(a,T.RE_GIT)[0]
	us=u.split('/')
	user,repo=us[-2],us[-1]
	return 'git@github.com:'+user+'/'+repo
git=get_git_ssh=git_convert_ssh
	
def format_list(a,):
	U,T,N,F=py.importUTNF()
	r=[]
	row_lens=U.len(*a)
	maxs=[0]* py.max(row_lens)
	
	return
	
def format_dict(d,):
	U,T,N,F=py.importUTNF()
	r={}
	max_k,max_v=0,0
	
	id0=0
	id_1=0
	def fk(a,*aa,**ka):
		nonlocal max_k
		# py.pdb()()
		# U.get_or_set('fk',[]).append([a,py.id(a)])
		
		r=T.padding(py.repr(a._qgb_obj),size=max_k)
		if py.id(a._qgb_obj)==id0:
			r="\n"+r
		return r
	def fv(a):
		nonlocal max_v
		# U.get_or_set('fv',[]).append([a,py.id(a._qgb_obj)])
		r=T.padding(py.repr(a._qgb_obj),size=max_v)
		if py.id(a._qgb_obj)==id_1:
			r=r+",\n\n" #TODO '一个\n 在IPython 中显示不出来。'
		return r
		
	for n,(k,v) in py.enumerate(d.items()):
		s=py.repr(k)
		nk=T.wcswidth(s)
		if nk>max_k:
			max_k=nk
		
		sv=py.repr(v)
		nv=T.wcswidth(sv)
		if nv>max_v:
			max_v=nv
		
		if n==0:
			id0=py.id(k)
			# print('id0:',id0)
		r[U.object_custom_repr(k,repr=fk)]=U.object_custom_repr(v,repr=fv)
	else:#只有break后才不执行else
		id_1=py.id(v)
		# print(n,k,v,id_1)
			
		# r[U.StrRepr(k,repr=s)]=U.StrRepr(v,repr=T.padding(1,size=3))	
	return r
dict_format=format_dict	
	
def parse_cookie_str_to_dict(s):
	T=py.importT()
	dc={}
	for n,l in py.enumerate(s.split(';')):
		l=l.strip()
		name=T.sub(l,'','=')
		v=l[len(name)+1:]
		if name in dc:raise py.Exception('cookie name conflict?',name)
		dc[name]=v
		#print(l)
		# print(n,name,v)
		#break	
	return dc
c2d=parse_cookie=parse_cookie_str=parse_cookie_to_dict=parse_cookie_str_to_dict	

def splitlines(*a):
	r=[]
	for s in a:
		r.extend(s.splitlines())
	return r	

def split_to_2d_list(text,col=re.compile('\s+'),row='\n',strip=True,skip_empty_line=True,StrRepr=False):
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
		rs=text.splitlines()
	else:
		rs=text.split(row)
		
	r=[]	
	for i,v in py.enumerate(rs):
		if strip:v=v.strip()
		if skip_empty_line and not v:continue
		
		cs=re.split(col,v)
		if StrRepr:
			StrRepr_ka={}
			if py.isint(StrRepr) and StrRepr>1:
				StrRepr_ka['size']=StrRepr
			row=[U.StrRepr(i,**StrRepr_ka) for i in cs]
		else:
			row=cs
		r.append(row)	
	return r
	# import numpy as np
	# np.loadtxt("myfile.txt")[:, 1]
	# return [ ]
get_2d_list=split2d=split2dlist=split_to_2d_list

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
		
def search_return_position(text,*targets,case_sensitive=True,a=0,b=0,c=0,default_c_size=100,return_t=False,return_dict=False,c_StrRepr=True,**ka):
	U=py.importU()
	a=U.get_duplicated_kargs(ka,'A',default=a)
	b=U.get_duplicated_kargs(ka,'B',default=b)
	c=U.get_duplicated_kargs(ka,'C',default=c)
	return_t=U.get_duplicated_kargs(ka,'return_t','t','target',default=return_t)
	c_StrRepr=U.get_duplicated_kargs(ka,'c_StrRepr','crepr','cstrrepr',default=c_StrRepr)
	case_sensitive=U.get_duplicated_kargs(ka,'cs','case','upper','caseSensitive',default=case_sensitive)
	return_dict=U.get_duplicated_kargs(ka,'d','return_dict','rd','dict',default=return_dict)
	r=[]
	d={}
	def _append(t,i,sub=''):
		if return_dict:
			if sub:
				U.dict_add_value_list(d,t,(i,sub))
			else  :U.dict_add_value_list(d,t,i)
		else:
			row=[i]
			if sub:
				row.append( sub)		
			if return_t:
				row.insert(0,t)		
				
			r.append(row)
	len_text_digits=py.len(str(py.len(text))) #不是digitals		
	c_isint=py.isint(c)
	c_len_2= U.len(c)==2
	
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
						if c_isint:
							c0=py.max(i-c,0)
							c1=i+py.len(t)+c
						elif c_len_2:
							c0=text.rfind(c[0],0,i)
							c1=text.find(c[1],i)
							if c0==-1 or c0-i>default_c_size:c0=i-(default_c_size//2)
							if c1==-1 or i-c1>default_c_size:c1=i-(default_c_size//2)
							c0+=1
						else:
							raise py.ArgumentUnsupported(c)
					if c_StrRepr:		
						_append( t,U.IntRepr(i,size=len_text_digits+1),U.StrRepr(text[c0:c1],size=default_c_size) )
					else:	
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
length_display=char_display_width=display_width=get_display_width=get_str_display_width=wcsize=wcslength=wcswidth


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

def columnize(iterable,width=120,**ka):
	''' 144 break line in default Win+R Cmd window
'''
	# from IPython.utils.text import columnize as _columnize
	if not py.iterable(iterable):return py.repr(iterable)
	U,T,N,F=py.importUTNF()
	width=U.get_duplicated_kargs(ka,'size','width','row_width',default=width)
	
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
col=column=columnize

def justify(s,size=0,char=' ',method=py.No('try use wc_ljust'),cut=False):#'ljust'
	''' ljust() 方法返回一个原字符串左对齐,并使用空格填充右边至指定长度的新字符串。
#当提供size 参数时，小心 ModuleNotFoundError: No module named 'wcwidth'	 # 已经fix部分情况
rpcServer [U.StrRepr(T.az,size=26)]没有错误详情，  repr(U.StrRepr(T.az,size=26)) 就有出错详情
	'''
	s= string(s)
	if size<1:
		return s
		# raise py.ArgumentError('size must > 0',size)
	if not method:
		try:
			from wcwidth import wcwidth
			method=wc_ljust
		except Exception as e:
			method='ljust'
		
	if py.istr(method):
		if cut and len(s)>=size:
			return s[:size]
		return py.getattr(s,method)(size,char)	#
	if py.callable(method):
		if cut and wcswidth(s)>=size:
			return wc_cut(s,size)
		return method(s,size,char) #TODO 统一参数
	raise NotImplementedError('method must str.funcName or callable')
padding=justfy=justify
	
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

def diff_chars(expected, actual,p=True,enumerate=True,eol=True,**ka):
	import difflib
	U,T,N,F=py.importUTNF()
	enumerate=U.get_duplicated_kargs(ka,'n','index',default=enumerate)
	def tolist(a):
		r=[]
		if enumerate:
			for i,c in py.enumerate(a):
				if eol:
					r.append('{}:{}\n'.format(i,c))
				else:
					r.append('{}:{}'.format(i,c))
		else:
			if eol:
				r=[c+'\n' for c in a]
			else:
				r=py.list(a)
		return r
	expected=tolist(expected)
	actual=tolist(actual)
		
	# diff=difflib.unified_diff(enumerate(expected), enumerate(actual))
	diff=difflib.unified_diff(expected, actual)
	r=''.join(diff)
	if p:
		print(r,'\n diff_len:%s'%len(r))
		return U.StrRepr(r,repr='#T.diff(p=1) result,len:%s'%py.len(r))
	else:
		return r
diffc=diffChar=diffChars=diff_char=diff_chars

def diff(expected, actual,p=True,pformat=False):
	"""https://docs.python.org/zh-cn/3/library/difflib.html
	Compare two sequences of lines; generate the delta as a unified diff.
	Helper function. Returns a string containing the unified diff of two multiline strings.
	
	
s.splitlines(keepends=False)	
	"""

	import difflib
	U,T,N,F=py.importUTNF()
	if pformat:
		pformat=T.pformat
		try:
			pformat=py.from_qgb_import('ipy').pformat
		except:pass
		if not py.istr(expected):
			expected=pformat(expected)
		if not py.istr(actual):
			actual=pformat(actual)
	expected=expected.splitlines(True)
	actual=actual.splitlines(True)

	diff=difflib.unified_diff(expected, actual)
	r=''.join(diff)
	if p:
		print(r,'\n diff_len:%s'%len(r))
		return U.StrRepr(r,repr='#T.diff(p=1) result,len:%s'%py.len(r))
	else:
		return r

def join_recursively(s,iter,prepend_layer=False,append_layer=False,format_layer=False,_layer=0):
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

recursiveJoin=recursive_join=join_recursively

def join_eol(*iterable,separator=EOL,**ka):
	r= join(*iterable,separator=separator,**ka)
	U=py.importU()
	return U.StrRepr(r)
eol_join=join_eol
	
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
	if separator==',':separator=U.get_duplicated_kargs(ka,'s','sep','split','splitor','separator',default=separator)
	if py.len(iterable)<1:
		raise py.ArgumentError('need iterable')
	if iterable[0]==separator:
		U.warn('T.join(*a,separator=',')  not T.join(separator,*a)')
	
		
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

def url_arg_join(url_base='',arg_dict=None):
	if py.isdict(url_base) and not arg_dict:
		arg_dict,url_base=url_base,''
	if url_base and not url_base.endswith('?'):
		url_base+='?'
		
	rs=[]
	for k,v in arg_dict.items():
		v=url_encode(py.str(v) )
		rs.append('{}={}'.format(k,v))
	sr='&'.join(rs)
	return url_base+sr
url_join_arg=join_url_arg=url_join_arg_dict=url_arg_join
	
def parse_url_arg(url,list_len_one=False,return_not_arg_part=False):
	''' if url not contains '?'  return empty dict
	
'''
	if py.is2():
		from urlparse import urlparse,parse_qs
	else:
		from urllib.parse import urlparse,parse_qs
	o = urlparse(url)
	r= parse_qs(o.query)
	for k,v in r.items():
		if not list_len_one and py.islist(v) and py.len(v)==1:
			r[k]=v[0]
	try:
		U=py.importU()
		r=U.DictAttr(r)
	except:pass
	
	if return_not_arg_part:#only py3
		import urllib.parse
		pr=urllib.parse.ParseResult(**py.dict(o._asdict(), query='')).geturl()
		if r:pr+='?'
		return pr,r
	return r
url_arg_dict=url_parse_arg=parse_qs=parse_url=parse_url_arg

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
	
	
def replace_url_arg(url,arg_name_or_dict=py.No('ka or dict'),new=py.No('if dict, this no'),**ka):
	u,d=parse_url_arg(url,return_not_arg_part=True)
	
	if not arg_name_or_dict and ka:
		arg_name_or_dict=ka
	
	if py.isdict(arg_name_or_dict) and py.isno(new):
		for k,v in arg_name_or_dict.items():
			d[k]=v
	elif py.istr(arg_name_or_dict):
		if '=' in arg_name_or_dict and py.isno(new):
			k,v=arg_name_or_dict.split('=')
			d[k]=v
		else:	
			d[arg_name_or_dict]=string(new)
	else:
		raise py.ArgumentError('Not arg_name_or_dict',url,arg_name_or_dict,new)	
	return u+url_arg_join(d)	
	
replace_url=url_replace=url_arg_replace=replace_url_args=replace_url_arg
	
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
	
	for i,c in py.enumerate(url):
		if c not in '%'+gsURL_not_escaped[1:] :
			url[i]='%{0:02X}'.format( py.ord(c) ) 
	return ''.join(url).replace('%','-')
url2fn=url2file=url2fileName=url_to_filename=urlToFileName


def get_domain_parts_by_url_using_tld(url_or_domain,return_str=True,**ka):
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
 
 
netloc: Contains the network location - which includes the domain itself (and subdomain if present), the port number, along with an optional credentials in form of username:password. Together it may take form of username:password@domain.com:80.
 
'''
	if 'fix_protocol' not in ka:
		ka['fix_protocol']=True
	
	import tld
	r= tld.utils.process_url(url=url_or_domain,**ka)[0]
	if return_str:
		return '.'.join(r)
	else:
		return r
get_domain_tld=get_domain_of_url_tld=get_domain_parts_by_url_using_tld
		
		
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
RE_ZH_PATTERN = u'[\u4e00-\u9fa5]+'

def list_filter_zh(a):
	return re.compile(RE_ZH_PATTERN).findall(a )
filter_zh_as_list=list_filter_zh

def str_filter_zh(a,max_not_zh=0,splitor=' '):
	if not max_not_zh:
		return splitor.join(re.compile(RE_ZH_PATTERN).findall(a ) )
	return regexReplace(a,r'[^\u4e00-\u9fa5]{%s,}'%max_not_zh,'')
filter_zh_as_str=filter_zh=filterZh=str_filter_zh

def hasZh(word):
	'''
	判断传入字符串是否包含中文
	:param word: 待判断字符串
	:return: True:包含中文  False:不包含中文
	'''
	global RE_ZH_PATTERN
	match = re.compile(RE_ZH_PATTERN).search(word)
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

RE_HTML_TAG = r'<[^>]+>'
def filter_html(text):
	''' regex 多次 compile 没关系 ，结果相等 
	'''
	return re.compile(RE_HTML_TAG).sub('', text)
html_filter=filter_html

def html2text(html,baseurl='',ignore_images=True,ignore_links=True,str_repr=False):
	try:
		from html2text import HTML2Text
	except:
		return re.sub('<[^<>]+>', '', html)
	if not html:return html
	
	h=HTML2Text(baseurl=baseurl)
	h.ignore_images=ignore_images
	h.ignore_links=ignore_links
	r= h.handle(py.str(html)) # beautifulSoup raise Exception None
	
	if str_repr:
		U=py.importU()
		r=U.StrRepr(r)
	return r
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

def BeautifulSoup(html='',file='',cache=False):
	# from bs4 import BeautifulSoup
	if not html and file:
		U,T,N,F=py.importUTNF()
		if cache:
			bs=U.get(file)
			if bs:return bs
		html=F.read(file)	
	if not html:return html
	import bs4
	
	t=py.str(py.type(html) )
	if 'requests.models.Response' in t:
		html=html.text
	try:
		import lxml
		bs=bs4.BeautifulSoup(html,features='lxml' )	
	except:
		bs=bs4.BeautifulSoup(html,features="html5lib" )	
	if cache and file:
		return U.set(file,bs)
	return bs
bs=beautifulsoup=beautifulSoup=BeautifulSoup

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

RE_IP= '''(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))'''
def ip_location_text(text,location_format=' [{0}] ',reverse_ip=True,**ka):
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
readableIPLocationText=ipLocationText=ip_location=ip_location_text

	
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

	
	
	
def regex_count(a,regex,flags=0):
	return py.len(re.findall(regex, a,flags=flags))
countRegex=regexCount=count_regex=regex_count
	
def regex_replace(a,regex,str_or_func,flags=0):
	''' str_or_bytes_or_func
func( a: <_sre.SRE_Match object; span=(2388, 2396), match='21758465'>  ):

a.span()==(2388, 2396)

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
		p=re.compile(regex,flags=flags)
	else:
		p=regex
	return p.sub(func,a)#TypeError: 'flags' is an invalid keyword argument for sub()
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
		
def detect_and_decode(abytes,confidence=0.7,default=py.No('default encoding "" '),return_encoding=False  ):
	if abytes==b'':return ''
	if py.isunicode(abytes):return abytes
	if not py.isbyte(abytes):
		raise py.ArgumentError('is not bytes',abytes)
	encoding=detect(abytes=abytes,confidence=confidence,default=default)
	if not encoding:return encoding
	try:
		if return_encoding:
			return encoding,abytes.decode( encoding )
		else:
			return abytes.decode( encoding )
	except Exception as e:
		U,T,N,F=py.importUTNF()
		# py.importU().get_or_set('auto_decode.err.list',[]).append(e)
		# return py.No(*e.args)
		return py.No(e,abytes,msg=f'''{T.sub(py.str(e.__class__),"'","'")} {e.args[0]} [{e.args[2]}:{e.args[3]}] {e.args[4]} {py.len(abytes),py.len(e.args[1])}''',)
		
detect_decode=detectDecode=detectAndDecode=auto_decode=autoDecode=detect_and_decode

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
def get_url_netloc(url):
	''' return "ip:port" '''
	from six.moves.urllib.parse import urlsplit
	url=url.strip()
	if '://' not in url:
		url='http://'+url
	up=urlsplit(url=url)
	return up.netloc
hostname=host_name=get_domain_parts_by_url=get_domain_from_url=netloc=get_url_netloc

def get_url_full_path(url):
	netloc=get_url_netloc(url)
	return sub(url,netloc+'/')
get_url_netloc_right=get_url_path=get_url_full_path

def url_split(url):
	''' return SplitResult(scheme='ws', netloc='192.168.43.162:8080', path='/pty', query='', fragment='')
'''	
	from six.moves.urllib.parse import urlsplit
	return urlsplit(url=url)  # obj
urlsplit=url_split	

def urlEncode(a,safe='/:', encoding=None, errors=None,**ka):
	''' a : str_or_bytes
	#todo 	convert Non-string objects
#TODO 重复调用 会出现 "%252525252525...."	
	
quote real path	
 'C:\\QGB\\Anaconda3\\lib\\urllib\\parse.py',
 '-n 782'	
	'''
	U=py.importU()
	safe=U.get_duplicated_kargs(ka,'skip','ignore',default=safe)
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

def T_RE_preprocessor(regex,T_RE='T.RE'):
	if not T_RE:return regex
	if not py.istr(T_RE):T_RE='T.RE'
	if T_RE not in regex:return regex
	
	T=py.importT()	
	
	rd={}
	for i in T.regex_match_all(regex,T.regex_escape(T_RE)+r'[_\da-zA-Z]+'):
		v=py.getattr(T,i[2:])
		if not v:raise py.ArgumentError('%s not in T'%v,regex)
		if not py.istr(v):raise py.ArgumentError('T.%s not string'%v,regex)
		rd[i]=v
	return T.replacey(regex,rd)	

def regex_match_named_return_dict(a,*regexs,T_RE='T.RE'):
	''' #not    ,**defaults
re.search('(?P<name>.*) (?P<phone>.*)', 'John 123456').group('name')=='John'
#py3.7 ka的顺序与调用顺序一致	
'''
	U=py.importU()	
	if not regexs:raise py.ArgumentError(regexs)
	
	rd={}
	err=[]
	for regex in regexs:
		regex=T_RE_preprocessor(regex,T_RE)
		regex = re.compile(regex)
		if not regex.groupindex:
			raise py.ArgumentError(regex,'need (?P<name>regex) ... ')
		r= re.search(regex,a) # if not match return None
		if not r:
			err.append(regex)
			continue
		# 一组没匹配到 {'protocol': None} 与 匹配到空 {'aaa':''}  是不一样的
		# rd.update(r.groupdict())
		U.dict_update_dict_merge_value_list(rd,r.groupdict())
	# for name,v in r.items():
	if rd:return rd
	else :return py.No('NotMatch:',err,a)
	
	re.search(a,regex)
regex_groupdict=regex_named=named_regex_match=regex_match_named=match_regex_named=regex_match_named_return_dict
	
def regex_match_all(a,regex):
	if py.isinstance(a,re.Pattern) and py.istr(regex):
		U.log('#Warning# Args: a,regex  not  regex,a . but auto fixed')
		a,regex=regex,a
		
	return [i.group() for i in re.finditer(regex,a)]
matchRegex=matchRegexAll=regexMatchAll=regex_match_all
		
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
def bytes_to_base64(a,encoding='utf-8'):
	'''return str'''
	import base64
	if py.istr(a):
		a=a.encode(encoding)
	if py.is3():
		return base64.b64encode(a).decode('ascii')
	else:
		return base64.b64encode(a)
b64encode=base64_encode=bytesToBase64=bytes_to_base64
		
def base64_decode_return_string(a,return_bytes=py.No('avoid argument conflict'),return_str=True):
	import base64
	# if not (return_bytes^return_str): # a^b==False # a,b相等
		# raise py.ArgumentError('return_bytes==return_str')
	if not return_str:return_bytes=True
	
	if return_bytes :#or py.isbyte(a):
		if not py.isbyte(a):
			a=a.encode('ascii')
		return base64.b64decode(a) #type bytes
	else:	
	# if py.istr(a):
		return detectAndDecode(base64.b64decode(a))
b64decode=base64Decode=base64_decode=base64decode=b64_str=base64_to_str=base64_decode_return_str=base64_decode_return_string	

def base64_to_bytes(a):
	import base64
	if py.istr(a):
		return base64.b64decode(a)
	if py.isbyte(a):
		return base64.b64decode(a) #type bytes
b64_bytes=base64_decode_return_bytes=base64_to_bytes	

		
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
		for i,v in py.enumerate(a[::-1]):
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

load_js=loads_js=load_js_obj=load_js_object=js_load=js_loads=js_obj_loads=javascript_object_loads

def jsonToDict(a):
	'''py2: 不同于 json_loads ，不会自动转换 到unicode'''
	import ast
	return ast.literal_eval(a.replace('false','False').replace('true','True'))
js2py=jsonToDict
	
def json_load(astr='',file=None,comment=lambda s:re.sub("//.*","",s,flags=re.MULTILINE),**ka):
	import json
	if not (astr or file):
		return py.No('either astr or file, but not any',astr,file) #一个也没有 不用 both not
	if (astr and file):
		return py.No('either str or file, but not both',astr,file) # not all 可以吗
	
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
	if py.isbyte(astr):
		astr=detect_and_decode(astr,default='utf-8')
	
	if comment and py.callable(comment):
		astr=comment(astr)
		
	try:
		return json.loads(astr,**ka)
	except Exception as e:
		return py.No(e,astr)
json_loads=json_load

def json_dump_to_file(obj,file,**ka):
	'''json.dump(
    obj,
    fp,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    cls=None,
    indent=None,
    separators=None,
    default=None,
    sort_keys=False,
    **kw,
)
'''
	import json
	U,T,N,F=py.importUTNF()
	file=U.get_duplicated_kargs(ka,'file','f','fp',default=file)
	try:
		with F.open(file,'w') as f:
			return json.dump(obj ,fp=f )
	except Exception as e:
		return py.No(e)
		
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
subl=sublast=subt=sub_last=subLast=subr=sub_right=subRight=sub_tail
	
def del_sub(a,x,y,start=0,end=-1):
	return a[start:x]+a[y:end]
	
def replace_all_space(a,to='',target=r"\s+"):
	'''  多个连续空白字符会 缩减成 一个空格
	in char256 {' ', '\x0b', '\x1c', '\x1d', '\t', '\x0c', '\x1e', '\x85', '\xa0', '\x1f', '\r', '\n'}  removed'''
	import re
	return re.sub(target, to, a, flags=re.UNICODE)
del_space=del_spaces=remove_all_space=replace_all_spaces=delAllSpace=removeAllSpaces=removeAllSpace=replace_all_space

def replace_multi_target(a,olds,new='',case_sensitive=True):
	'''
olds could be dict	
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
replacey=replace_multi_target	
	
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
只有【'%02d'%4】这种用法 '%0-2d'%4 == '4 '	不会用0填充右边
	
 >  '%(a)s %(b)s'%(3,2)
TypeError: format requires a mapping  
##Solution##  '%(a)s %(b)s' % py.locals()

'%(1)s %("")s'%{'1':1,'""':54353}  # dict key必须为str，%()s支持任意字符串？，dict-key只能多，不能少

In [141]: f'{n:03} =='
Out[141]: '004 =='

In [139]: f'{n:>03} =='
Out[139]: '004 =='

In [140]: f'{n:>03d} =='
Out[140]: '004 =='

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

def filename_unlegalized(a,):
	''' '''
	r=''
	charset=[py.chr(py.ord(c)+0XFEE0) for c in NOT_FILE_NAME_WINDOWS]
	for c in a:
		if c in charset:
			r+=py.chr(py.ord(c)-0XFEE0)
		else:
			r+=c
	return r
unfilename=unlegalized_filename=filename_unlegalized

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

def pathname_legalized(a,reduce_space=True):
	''' Reduce 减少、Reuse 反复使用、Recycle 再循环
	
'''	
	if not py.istr(a):a=string(a)
	if reduce_space:
		a=replace_all_space(a.strip(),space)
	r=''
	for n,c in py.enumerate(a):
		if  (c in NOT_PATH_NAME) or (c==':' and n!=1):
			r+=py.chr(py.ord(c)+0XFEE0)
		else:r+=c
	r=replace_all(r,'//','/')	
	r=replace_all(r,chr(0x5C)+chr(0x5C),chr(0x5C))	
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
	
	
def max_wcswidth_return_int(*a):
	if py.len(a)==1 and not py.istr(a[0]) and py.iterable(a[0]):
		a=a[0]
	r=0
	for i in a:
		# i=string(i)
		n=wcswidth(i)
		if n>r:r=n
	return r
max_wcswidth=max_wcswidth_return_int

def select_max_len_str(*a):
	'''return max length string(a[i])'''
	r=''
	for i in a:
		i=string(i)
		if len(i)>len(r):r=i
	return r
get_max_len_str=select_max_len_str	
	
def allAscii(a):
	if not py.istr(a):return False
	for i in a:
		if ord(i)>127:return False
		# U.pln( ord(i);break
	return True
	
z09_finance=gzfn=zfn=zf09=gszFinancial='''零壹贰叁肆伍陆柒捌玖拾佰仟萬億'''
#亿的后面 ，大写小写都是同一个。
#参见https://zh.wikipedia.org/wiki/中文数字
gsz09=gsZ09=gz09=z09=znumber=gzn=gszn=zn='''〇一二三四五六七八九'''
gsz10=gsZ10=z10='''一二三四五六七八九十'''
gszi=gsZI='''个、十、百、千、万、十万、百万、千万、亿、十亿、百亿、千亿、兆、十兆、百兆、千兆、京、十京、百京、千京、垓、十垓、百垓、千垓、秭、十秭、百秭、千秭、穰、十穰、百穰、千穰、沟、十沟、百沟、千沟、涧、十涧、百涧、千涧、正、十正、百正、千正、载、十载、百载、千载、极、十极、百极、千极'''
gZi=gzi=glzi=gsZI.split('、')

def readNumber(a,split=4,p=True):
	'''
T.readNumber(2**172)
5986极3107载0650正7378涧3529沟6229穰3074秭8058垓9524京8510兆6996亿9602万9696

In [134]: T.readNumber 2**173
IndexError                                Traceback (most recent call last)
<ipython-input-134-e87d6523ae23> in <module>
----> 1 T.readNumber(2**173)

C:/QGB/babun/cygwin/bin\qgb\T.py in readNumber(a, split, p)
   1830                 if i%split==0:
   1831                         w=b[i:i+split]
-> 1832                         s=w[::-1]+zh[iz]+s
   1833                         iz+=1
   1834                         # U.pln(  i,

IndexError: list index out of range
'''	
	
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
	for i,k in py.enumerate(b):	
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
RE_VAR_BODY=RE_VAR_MIDDLE_UNICODE= '''[0-9A-Z_a-z\xaa\xb5\xb7\xba\xc0-\xd6\xd8-\xf6\xf8-\u02c1\u02c6-\u02d1\u02e0-\u02e4\u02ec\u02ee\u0300-\u0374\u0376-\u0377\u037b-\u037d\u037f\u0386-\u038a\u038c\u038e-\u03a1\u03a3-\u03f5\u03f7-\u0481\u0483-\u0487\u048a-\u052f\u0531-\u0556\u0559\u0560-\u0588\u0591-\u05bd\u05bf\u05c1-\u05c2\u05c4-\u05c5\u05c7\u05d0-\u05ea\u05ef-\u05f2\u0610-\u061a\u0620-\u0669\u066e-\u06d3\u06d5-\u06dc\u06df-\u06e8\u06ea-\u06fc\u06ff\u0710-\u074a\u074d-\u07b1\u07c0-\u07f5\u07fa\u07fd\u0800-\u082d\u0840-\u085b\u0860-\u086a\u08a0-\u08b4\u08b6-\u08bd\u08d3-\u08e1\u08e3-\u0963\u0966-\u096f\u0971-\u0983\u0985-\u098c\u098f-\u0990\u0993-\u09a8\u09aa-\u09b0\u09b2\u09b6-\u09b9\u09bc-\u09c4\u09c7-\u09c8\u09cb-\u09ce\u09d7\u09dc-\u09dd\u09df-\u09e3\u09e6-\u09f1\u09fc\u09fe\u0a01-\u0a03\u0a05-\u0a0a\u0a0f-\u0a10\u0a13-\u0a28\u0a2a-\u0a30\u0a32-\u0a33\u0a35-\u0a36\u0a38-\u0a39\u0a3c\u0a3e-\u0a42\u0a47-\u0a48\u0a4b-\u0a4d\u0a51\u0a59-\u0a5c\u0a5e\u0a66-\u0a75\u0a81-\u0a83\u0a85-\u0a8d\u0a8f-\u0a91\u0a93-\u0aa8\u0aaa-\u0ab0\u0ab2-\u0ab3\u0ab5-\u0ab9\u0abc-\u0ac5\u0ac7-\u0ac9\u0acb-\u0acd\u0ad0\u0ae0-\u0ae3\u0ae6-\u0aef\u0af9-\u0aff\u0b01-\u0b03\u0b05-\u0b0c\u0b0f-\u0b10\u0b13-\u0b28\u0b2a-\u0b30\u0b32-\u0b33\u0b35-\u0b39\u0b3c-\u0b44\u0b47-\u0b48\u0b4b-\u0b4d\u0b56-\u0b57\u0b5c-\u0b5d\u0b5f-\u0b63\u0b66-\u0b6f\u0b71\u0b82-\u0b83\u0b85-\u0b8a\u0b8e-\u0b90\u0b92-\u0b95\u0b99-\u0b9a\u0b9c\u0b9e-\u0b9f\u0ba3-\u0ba4\u0ba8-\u0baa\u0bae-\u0bb9\u0bbe-\u0bc2\u0bc6-\u0bc8\u0bca-\u0bcd\u0bd0\u0bd7\u0be6-\u0bef\u0c00-\u0c0c\u0c0e-\u0c10\u0c12-\u0c28\u0c2a-\u0c39\u0c3d-\u0c44\u0c46-\u0c48\u0c4a-\u0c4d\u0c55-\u0c56\u0c58-\u0c5a\u0c60-\u0c63\u0c66-\u0c6f\u0c80-\u0c83\u0c85-\u0c8c\u0c8e-\u0c90\u0c92-\u0ca8\u0caa-\u0cb3\u0cb5-\u0cb9\u0cbc-\u0cc4\u0cc6-\u0cc8\u0cca-\u0ccd\u0cd5-\u0cd6\u0cde\u0ce0-\u0ce3\u0ce6-\u0cef\u0cf1-\u0cf2\u0d00-\u0d03\u0d05-\u0d0c\u0d0e-\u0d10\u0d12-\u0d44\u0d46-\u0d48\u0d4a-\u0d4e\u0d54-\u0d57\u0d5f-\u0d63\u0d66-\u0d6f\u0d7a-\u0d7f\u0d82-\u0d83\u0d85-\u0d96\u0d9a-\u0db1\u0db3-\u0dbb\u0dbd\u0dc0-\u0dc6\u0dca\u0dcf-\u0dd4\u0dd6\u0dd8-\u0ddf\u0de6-\u0def\u0df2-\u0df3\u0e01-\u0e3a\u0e40-\u0e4e\u0e50-\u0e59\u0e81-\u0e82\u0e84\u0e87-\u0e88\u0e8a\u0e8d\u0e94-\u0e97\u0e99-\u0e9f\u0ea1-\u0ea3\u0ea5\u0ea7\u0eaa-\u0eab\u0ead-\u0eb9\u0ebb-\u0ebd\u0ec0-\u0ec4\u0ec6\u0ec8-\u0ecd\u0ed0-\u0ed9\u0edc-\u0edf\u0f00\u0f18-\u0f19\u0f20-\u0f29\u0f35\u0f37\u0f39\u0f3e-\u0f47\u0f49-\u0f6c\u0f71-\u0f84\u0f86-\u0f97\u0f99-\u0fbc\u0fc6\u1000-\u1049\u1050-\u109d\u10a0-\u10c5\u10c7\u10cd\u10d0-\u10fa\u10fc-\u1248\u124a-\u124d\u1250-\u1256\u1258\u125a-\u125d\u1260-\u1288\u128a-\u128d\u1290-\u12b0\u12b2-\u12b5\u12b8-\u12be\u12c0\u12c2-\u12c5\u12c8-\u12d6\u12d8-\u1310\u1312-\u1315\u1318-\u135a\u135d-\u135f\u1369-\u1371\u1380-\u138f\u13a0-\u13f5\u13f8-\u13fd\u1401-\u166c\u166f-\u167f\u1681-\u169a\u16a0-\u16ea\u16ee-\u16f8\u1700-\u170c\u170e-\u1714\u1720-\u1734\u1740-\u1753\u1760-\u176c\u176e-\u1770\u1772-\u1773\u1780-\u17d3\u17d7\u17dc-\u17dd\u17e0-\u17e9\u180b-\u180d\u1810-\u1819\u1820-\u1878\u1880-\u18aa\u18b0-\u18f5\u1900-\u191e\u1920-\u192b\u1930-\u193b\u1946-\u196d\u1970-\u1974\u1980-\u19ab\u19b0-\u19c9\u19d0-\u19da\u1a00-\u1a1b\u1a20-\u1a5e\u1a60-\u1a7c\u1a7f-\u1a89\u1a90-\u1a99\u1aa7\u1ab0-\u1abd\u1b00-\u1b4b\u1b50-\u1b59\u1b6b-\u1b73\u1b80-\u1bf3\u1c00-\u1c37\u1c40-\u1c49\u1c4d-\u1c7d\u1c80-\u1c88\u1c90-\u1cba\u1cbd-\u1cbf\u1cd0-\u1cd2\u1cd4-\u1cf9\u1d00-\u1df9\u1dfb-\u1f15\u1f18-\u1f1d\u1f20-\u1f45\u1f48-\u1f4d\u1f50-\u1f57\u1f59\u1f5b\u1f5d\u1f5f-\u1f7d\u1f80-\u1fb4\u1fb6-\u1fbc\u1fbe\u1fc2-\u1fc4\u1fc6-\u1fcc\u1fd0-\u1fd3\u1fd6-\u1fdb\u1fe0-\u1fec\u1ff2-\u1ff4\u1ff6-\u1ffc\u203f-\u2040\u2054\u2071\u207f\u2090-\u209c\u20d0-\u20dc\u20e1\u20e5-\u20f0\u2102\u2107\u210a-\u2113\u2115\u2118-\u211d\u2124\u2126\u2128\u212a-\u2139\u213c-\u213f\u2145-\u2149\u214e\u2160-\u2188\u2c00-\u2c2e\u2c30-\u2c5e\u2c60-\u2ce4\u2ceb-\u2cf3\u2d00-\u2d25\u2d27\u2d2d\u2d30-\u2d67\u2d6f\u2d7f-\u2d96\u2da0-\u2da6\u2da8-\u2dae\u2db0-\u2db6\u2db8-\u2dbe\u2dc0-\u2dc6\u2dc8-\u2dce\u2dd0-\u2dd6\u2dd8-\u2dde\u2de0-\u2dff\u3005-\u3007\u3021-\u302f\u3031-\u3035\u3038-\u303c\u3041-\u3096\u3099-\u309a\u309d-\u309f\u30a1-\u30fa\u30fc-\u30ff\u3105-\u312f\u3131-\u318e\u31a0-\u31ba\u31f0-\u31ff\u3400-\u4db5\u4e00-\u9fef\ua000-\ua48c\ua4d0-\ua4fd\ua500-\ua60c\ua610-\ua62b\ua640-\ua66f\ua674-\ua67d\ua67f-\ua6f1\ua717-\ua71f\ua722-\ua788\ua78b-\ua7b9\ua7f7-\ua827\ua840-\ua873\ua880-\ua8c5\ua8d0-\ua8d9\ua8e0-\ua8f7\ua8fb\ua8fd-\ua92d\ua930-\ua953\ua960-\ua97c\ua980-\ua9c0\ua9cf-\ua9d9\ua9e0-\ua9fe\uaa00-\uaa36\uaa40-\uaa4d\uaa50-\uaa59\uaa60-\uaa76\uaa7a-\uaac2\uaadb-\uaadd\uaae0-\uaaef\uaaf2-\uaaf6\uab01-\uab06\uab09-\uab0e\uab11-\uab16\uab20-\uab26\uab28-\uab2e\uab30-\uab5a\uab5c-\uab65\uab70-\uabea\uabec-\uabed\uabf0-\uabf9\uac00-\ud7a3\ud7b0-\ud7c6\ud7cb-\ud7fb\uf900-\ufa6d\ufa70-\ufad9\ufb00-\ufb06\ufb13-\ufb17\ufb1d-\ufb28\ufb2a-\ufb36\ufb38-\ufb3c\ufb3e\ufb40-\ufb41\ufb43-\ufb44\ufb46-\ufbb1\ufbd3-\ufc5d\ufc64-\ufd3d\ufd50-\ufd8f\ufd92-\ufdc7\ufdf0-\ufdf9\ufe00-\ufe0f\ufe20-\ufe2f\ufe33-\ufe34\ufe4d-\ufe4f\ufe71\ufe73\ufe77\ufe79\ufe7b\ufe7d\ufe7f-\ufefc\uff10-\uff19\uff21-\uff3a\uff3f\uff41-\uff5a\uff66-\uffbe\uffc2-\uffc7\uffca-\uffcf\uffd2-\uffd7\uffda-\uffdc\U00010000-\U0001000b\U0001000d-\U00010026\U00010028-\U0001003a\U0001003c-\U0001003d\U0001003f-\U0001004d\U00010050-\U0001005d\U00010080-\U000100fa\U00010140-\U00010174\U000101fd\U00010280-\U0001029c\U000102a0-\U000102d0\U000102e0\U00010300-\U0001031f\U0001032d-\U0001034a\U00010350-\U0001037a\U00010380-\U0001039d\U000103a0-\U000103c3\U000103c8-\U000103cf\U000103d1-\U000103d5\U00010400-\U0001049d\U000104a0-\U000104a9\U000104b0-\U000104d3\U000104d8-\U000104fb\U00010500-\U00010527\U00010530-\U00010563\U00010600-\U00010736\U00010740-\U00010755\U00010760-\U00010767\U00010800-\U00010805\U00010808\U0001080a-\U00010835\U00010837-\U00010838\U0001083c\U0001083f-\U00010855\U00010860-\U00010876\U00010880-\U0001089e\U000108e0-\U000108f2\U000108f4-\U000108f5\U00010900-\U00010915\U00010920-\U00010939\U00010980-\U000109b7\U000109be-\U000109bf\U00010a00-\U00010a03\U00010a05-\U00010a06\U00010a0c-\U00010a13\U00010a15-\U00010a17\U00010a19-\U00010a35\U00010a38-\U00010a3a\U00010a3f\U00010a60-\U00010a7c\U00010a80-\U00010a9c\U00010ac0-\U00010ac7\U00010ac9-\U00010ae6\U00010b00-\U00010b35\U00010b40-\U00010b55\U00010b60-\U00010b72\U00010b80-\U00010b91\U00010c00-\U00010c48\U00010c80-\U00010cb2\U00010cc0-\U00010cf2\U00010d00-\U00010d27\U00010d30-\U00010d39\U00010f00-\U00010f1c\U00010f27\U00010f30-\U00010f50\U00011000-\U00011046\U00011066-\U0001106f\U0001107f-\U000110ba\U000110d0-\U000110e8\U000110f0-\U000110f9\U00011100-\U00011134\U00011136-\U0001113f\U00011144-\U00011146\U00011150-\U00011173\U00011176\U00011180-\U000111c4\U000111c9-\U000111cc\U000111d0-\U000111da\U000111dc\U00011200-\U00011211\U00011213-\U00011237\U0001123e\U00011280-\U00011286\U00011288\U0001128a-\U0001128d\U0001128f-\U0001129d\U0001129f-\U000112a8\U000112b0-\U000112ea\U000112f0-\U000112f9\U00011300-\U00011303\U00011305-\U0001130c\U0001130f-\U00011310\U00011313-\U00011328\U0001132a-\U00011330\U00011332-\U00011333\U00011335-\U00011339\U0001133b-\U00011344\U00011347-\U00011348\U0001134b-\U0001134d\U00011350\U00011357\U0001135d-\U00011363\U00011366-\U0001136c\U00011370-\U00011374\U00011400-\U0001144a\U00011450-\U00011459\U0001145e\U00011480-\U000114c5\U000114c7\U000114d0-\U000114d9\U00011580-\U000115b5\U000115b8-\U000115c0\U000115d8-\U000115dd\U00011600-\U00011640\U00011644\U00011650-\U00011659\U00011680-\U000116b7\U000116c0-\U000116c9\U00011700-\U0001171a\U0001171d-\U0001172b\U00011730-\U00011739\U00011800-\U0001183a\U000118a0-\U000118e9\U000118ff\U00011a00-\U00011a3e\U00011a47\U00011a50-\U00011a83\U00011a86-\U00011a99\U00011a9d\U00011ac0-\U00011af8\U00011c00-\U00011c08\U00011c0a-\U00011c36\U00011c38-\U00011c40\U00011c50-\U00011c59\U00011c72-\U00011c8f\U00011c92-\U00011ca7\U00011ca9-\U00011cb6\U00011d00-\U00011d06\U00011d08-\U00011d09\U00011d0b-\U00011d36\U00011d3a\U00011d3c-\U00011d3d\U00011d3f-\U00011d47\U00011d50-\U00011d59\U00011d60-\U00011d65\U00011d67-\U00011d68\U00011d6a-\U00011d8e\U00011d90-\U00011d91\U00011d93-\U00011d98\U00011da0-\U00011da9\U00011ee0-\U00011ef6\U00012000-\U00012399\U00012400-\U0001246e\U00012480-\U00012543\U00013000-\U0001342e\U00014400-\U00014646\U00016800-\U00016a38\U00016a40-\U00016a5e\U00016a60-\U00016a69\U00016ad0-\U00016aed\U00016af0-\U00016af4\U00016b00-\U00016b36\U00016b40-\U00016b43\U00016b50-\U00016b59\U00016b63-\U00016b77\U00016b7d-\U00016b8f\U00016e40-\U00016e7f\U00016f00-\U00016f44\U00016f50-\U00016f7e\U00016f8f-\U00016f9f\U00016fe0-\U00016fe1\U00017000-\U000187f1\U00018800-\U00018af2\U0001b000-\U0001b11e\U0001b170-\U0001b2fb\U0001bc00-\U0001bc6a\U0001bc70-\U0001bc7c\U0001bc80-\U0001bc88\U0001bc90-\U0001bc99\U0001bc9d-\U0001bc9e\U0001d165-\U0001d169\U0001d16d-\U0001d172\U0001d17b-\U0001d182\U0001d185-\U0001d18b\U0001d1aa-\U0001d1ad\U0001d242-\U0001d244\U0001d400-\U0001d454\U0001d456-\U0001d49c\U0001d49e-\U0001d49f\U0001d4a2\U0001d4a5-\U0001d4a6\U0001d4a9-\U0001d4ac\U0001d4ae-\U0001d4b9\U0001d4bb\U0001d4bd-\U0001d4c3\U0001d4c5-\U0001d505\U0001d507-\U0001d50a\U0001d50d-\U0001d514\U0001d516-\U0001d51c\U0001d51e-\U0001d539\U0001d53b-\U0001d53e\U0001d540-\U0001d544\U0001d546\U0001d54a-\U0001d550\U0001d552-\U0001d6a5\U0001d6a8-\U0001d6c0\U0001d6c2-\U0001d6da\U0001d6dc-\U0001d6fa\U0001d6fc-\U0001d714\U0001d716-\U0001d734\U0001d736-\U0001d74e\U0001d750-\U0001d76e\U0001d770-\U0001d788\U0001d78a-\U0001d7a8\U0001d7aa-\U0001d7c2\U0001d7c4-\U0001d7cb\U0001d7ce-\U0001d7ff\U0001da00-\U0001da36\U0001da3b-\U0001da6c\U0001da75\U0001da84\U0001da9b-\U0001da9f\U0001daa1-\U0001daaf\U0001e000-\U0001e006\U0001e008-\U0001e018\U0001e01b-\U0001e021\U0001e023-\U0001e024\U0001e026-\U0001e02a\U0001e800-\U0001e8c4\U0001e8d0-\U0001e8d6\U0001e900-\U0001e94a\U0001e950-\U0001e959\U0001ee00-\U0001ee03\U0001ee05-\U0001ee1f\U0001ee21-\U0001ee22\U0001ee24\U0001ee27\U0001ee29-\U0001ee32\U0001ee34-\U0001ee37\U0001ee39\U0001ee3b\U0001ee42\U0001ee47\U0001ee49\U0001ee4b\U0001ee4d-\U0001ee4f\U0001ee51-\U0001ee52\U0001ee54\U0001ee57\U0001ee59\U0001ee5b\U0001ee5d\U0001ee5f\U0001ee61-\U0001ee62\U0001ee64\U0001ee67-\U0001ee6a\U0001ee6c-\U0001ee72\U0001ee74-\U0001ee77\U0001ee79-\U0001ee7c\U0001ee7e\U0001ee80-\U0001ee89\U0001ee8b-\U0001ee9b\U0001eea1-\U0001eea3\U0001eea5-\U0001eea9\U0001eeab-\U0001eebb\U00020000-\U0002a6d6\U0002a700-\U0002b734\U0002b740-\U0002b81d\U0002b820-\U0002cea1\U0002ceb0-\U0002ebe0\U0002f800-\U0002fa1d]'''# RE len 10419+2, 713 items

RE_VAR_NOT_HEAD='''[0-9\xb7\u0300-\u036f\u0387\u0483-\u0487\u0591-\u05bd\u05bf\u05c1-\u05c2\u05c4-\u05c5\u05c7\u0610-\u061a\u064b-\u0669\u0670\u06d6-\u06dc\u06df-\u06e4\u06e7-\u06e8\u06ea-\u06ed\u06f0-\u06f9\u0711\u0730-\u074a\u07a6-\u07b0\u07c0-\u07c9\u07eb-\u07f3\u07fd\u0816-\u0819\u081b-\u0823\u0825-\u0827\u0829-\u082d\u0859-\u085b\u08d3-\u08e1\u08e3-\u0903\u093a-\u093c\u093e-\u094f\u0951-\u0957\u0962-\u0963\u0966-\u096f\u0981-\u0983\u09bc\u09be-\u09c4\u09c7-\u09c8\u09cb-\u09cd\u09d7\u09e2-\u09e3\u09e6-\u09ef\u09fe\u0a01-\u0a03\u0a3c\u0a3e-\u0a42\u0a47-\u0a48\u0a4b-\u0a4d\u0a51\u0a66-\u0a71\u0a75\u0a81-\u0a83\u0abc\u0abe-\u0ac5\u0ac7-\u0ac9\u0acb-\u0acd\u0ae2-\u0ae3\u0ae6-\u0aef\u0afa-\u0aff\u0b01-\u0b03\u0b3c\u0b3e-\u0b44\u0b47-\u0b48\u0b4b-\u0b4d\u0b56-\u0b57\u0b62-\u0b63\u0b66-\u0b6f\u0b82\u0bbe-\u0bc2\u0bc6-\u0bc8\u0bca-\u0bcd\u0bd7\u0be6-\u0bef\u0c00-\u0c04\u0c3e-\u0c44\u0c46-\u0c48\u0c4a-\u0c4d\u0c55-\u0c56\u0c62-\u0c63\u0c66-\u0c6f\u0c81-\u0c83\u0cbc\u0cbe-\u0cc4\u0cc6-\u0cc8\u0cca-\u0ccd\u0cd5-\u0cd6\u0ce2-\u0ce3\u0ce6-\u0cef\u0d00-\u0d03\u0d3b-\u0d3c\u0d3e-\u0d44\u0d46-\u0d48\u0d4a-\u0d4d\u0d57\u0d62-\u0d63\u0d66-\u0d6f\u0d82-\u0d83\u0dca\u0dcf-\u0dd4\u0dd6\u0dd8-\u0ddf\u0de6-\u0def\u0df2-\u0df3\u0e31\u0e33-\u0e3a\u0e47-\u0e4e\u0e50-\u0e59\u0eb1\u0eb3-\u0eb9\u0ebb-\u0ebc\u0ec8-\u0ecd\u0ed0-\u0ed9\u0f18-\u0f19\u0f20-\u0f29\u0f35\u0f37\u0f39\u0f3e-\u0f3f\u0f71-\u0f84\u0f86-\u0f87\u0f8d-\u0f97\u0f99-\u0fbc\u0fc6\u102b-\u103e\u1040-\u1049\u1056-\u1059\u105e-\u1060\u1062-\u1064\u1067-\u106d\u1071-\u1074\u1082-\u108d\u108f-\u109d\u135d-\u135f\u1369-\u1371\u1712-\u1714\u1732-\u1734\u1752-\u1753\u1772-\u1773\u17b4-\u17d3\u17dd\u17e0-\u17e9\u180b-\u180d\u1810-\u1819\u18a9\u1920-\u192b\u1930-\u193b\u1946-\u194f\u19d0-\u19da\u1a17-\u1a1b\u1a55-\u1a5e\u1a60-\u1a7c\u1a7f-\u1a89\u1a90-\u1a99\u1ab0-\u1abd\u1b00-\u1b04\u1b34-\u1b44\u1b50-\u1b59\u1b6b-\u1b73\u1b80-\u1b82\u1ba1-\u1bad\u1bb0-\u1bb9\u1be6-\u1bf3\u1c24-\u1c37\u1c40-\u1c49\u1c50-\u1c59\u1cd0-\u1cd2\u1cd4-\u1ce8\u1ced\u1cf2-\u1cf4\u1cf7-\u1cf9\u1dc0-\u1df9\u1dfb-\u1dff\u203f-\u2040\u2054\u20d0-\u20dc\u20e1\u20e5-\u20f0\u2cef-\u2cf1\u2d7f\u2de0-\u2dff\u302a-\u302f\u3099-\u309a\ua620-\ua629\ua66f\ua674-\ua67d\ua69e-\ua69f\ua6f0-\ua6f1\ua802\ua806\ua80b\ua823-\ua827\ua880-\ua881\ua8b4-\ua8c5\ua8d0-\ua8d9\ua8e0-\ua8f1\ua8ff-\ua909\ua926-\ua92d\ua947-\ua953\ua980-\ua983\ua9b3-\ua9c0\ua9d0-\ua9d9\ua9e5\ua9f0-\ua9f9\uaa29-\uaa36\uaa43\uaa4c-\uaa4d\uaa50-\uaa59\uaa7b-\uaa7d\uaab0\uaab2-\uaab4\uaab7-\uaab8\uaabe-\uaabf\uaac1\uaaeb-\uaaef\uaaf5-\uaaf6\uabe3-\uabea\uabec-\uabed\uabf0-\uabf9\ufb1e\ufe00-\ufe0f\ufe20-\ufe2f\ufe33-\ufe34\ufe4d-\ufe4f\uff10-\uff19\uff3f\uff9e-\uff9f\U000101fd\U000102e0\U00010376-\U0001037a\U000104a0-\U000104a9\U00010a01-\U00010a03\U00010a05-\U00010a06\U00010a0c-\U00010a0f\U00010a38-\U00010a3a\U00010a3f\U00010ae5-\U00010ae6\U00010d24-\U00010d27\U00010d30-\U00010d39\U00010f46-\U00010f50\U00011000-\U00011002\U00011038-\U00011046\U00011066-\U0001106f\U0001107f-\U00011082\U000110b0-\U000110ba\U000110f0-\U000110f9\U00011100-\U00011102\U00011127-\U00011134\U00011136-\U0001113f\U00011145-\U00011146\U00011173\U00011180-\U00011182\U000111b3-\U000111c0\U000111c9-\U000111cc\U000111d0-\U000111d9\U0001122c-\U00011237\U0001123e\U000112df-\U000112ea\U000112f0-\U000112f9\U00011300-\U00011303\U0001133b-\U0001133c\U0001133e-\U00011344\U00011347-\U00011348\U0001134b-\U0001134d\U00011357\U00011362-\U00011363\U00011366-\U0001136c\U00011370-\U00011374\U00011435-\U00011446\U00011450-\U00011459\U0001145e\U000114b0-\U000114c3\U000114d0-\U000114d9\U000115af-\U000115b5\U000115b8-\U000115c0\U000115dc-\U000115dd\U00011630-\U00011640\U00011650-\U00011659\U000116ab-\U000116b7\U000116c0-\U000116c9\U0001171d-\U0001172b\U00011730-\U00011739\U0001182c-\U0001183a\U000118e0-\U000118e9\U00011a01-\U00011a0a\U00011a33-\U00011a39\U00011a3b-\U00011a3e\U00011a47\U00011a51-\U00011a5b\U00011a8a-\U00011a99\U00011c2f-\U00011c36\U00011c38-\U00011c3f\U00011c50-\U00011c59\U00011c92-\U00011ca7\U00011ca9-\U00011cb6\U00011d31-\U00011d36\U00011d3a\U00011d3c-\U00011d3d\U00011d3f-\U00011d45\U00011d47\U00011d50-\U00011d59\U00011d8a-\U00011d8e\U00011d90-\U00011d91\U00011d93-\U00011d97\U00011da0-\U00011da9\U00011ef3-\U00011ef6\U00016a60-\U00016a69\U00016af0-\U00016af4\U00016b30-\U00016b36\U00016b50-\U00016b59\U00016f51-\U00016f7e\U00016f8f-\U00016f92\U0001bc9d-\U0001bc9e\U0001d165-\U0001d169\U0001d16d-\U0001d172\U0001d17b-\U0001d182\U0001d185-\U0001d18b\U0001d1aa-\U0001d1ad\U0001d242-\U0001d244\U0001d7ce-\U0001d7ff\U0001da00-\U0001da36\U0001da3b-\U0001da6c\U0001da75\U0001da84\U0001da9b-\U0001da9f\U0001daa1-\U0001daaf\U0001e000-\U0001e006\U0001e008-\U0001e018\U0001e01b-\U0001e021\U0001e023-\U0001e024\U0001e026-\U0001e02a\U0001e8d0-\U0001e8d6\U0001e944-\U0001e94a\U0001e950-\U0001e959]'''#VAR_BODY_BUT_NOT_HEAD len 4766+2 , 335 items(171 in BODY, 164 NOT fully equal)

RE_VAR_EXACTLY = RE_VAR_PRECISELY =RE_VAR_UNICODE=r'(?:(?!{head}){body})+'.format(head=RE_VAR_NOT_HEAD,body=RE_VAR_BODY)


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