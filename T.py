# coding=utf-8
#考虑qgb 位于另一个包内的情况
if __name__.endswith('qgb.T'):from . import py
else:#['T','__main__']
	import py
FILE_NAME=fileChars=FILE_CHARS="!#$%&'()+,-0123456789;=@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{}~"+' .'
PATH_NAME=pathChars=PATH_CHARS='/\\:'+FILE_NAME# include space, dot

az=a_z='abcdefghijklmnopqrstuvwxyz'
AZ=A_Z=a_z.upper()

azAZ=aZ=a_Z=a_z+A_Z
AZaz=Az=A_z=a_z+A_Z
character=azAZ###Do not Change

num=s09=_09=number='0123456789'

azAZ09=aZ09=a_Z0_9=alphanumeric=character+number#azAZ09, not gs09AZ
Az09=A_z0_9=A_Z+a_z+number

Hex=gshex='0123456789abcdef'
HEX=gshex.upper()

#0x20-0x7E ,32-126,len=95
visAscii=printAscii=asciiPrint=' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
char256=''.join([chr(i) for i in range(256)])
bytes256=byte256=b''.join( [py.byte(i) for i in range(256)  ] )

CR='\r'
LF=EOL=eol='\n'
###############
RE_IMG_URL=r'(((http://www)|(http://)|(www))[-a-zA-Z0-9@:%_\+.~#?&//=]+)\.(jpg|jpeg|gif|png|bmp|tiff|tga|svg)'
RE_URL=r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
RE_YMD=r"(19|20)[0-9]{2}[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])"
RE_WhiteSpace=r'\s'
###############
SQLITE='SELECT * FROM sqlite_master;'

#########################################
squote=quote="'"
dquote=dQuote='"'

import   re	

gError=None
try:
	from chardet import detect as _detect
	def detect(abytes,confidence=0.7,default=py.No('default encoding "" ')  ):
		r=_detect(abytes)
		if r['encoding'] in ['Windows-1254' ]:
			try:
				if abytes.decode('utf-8').encode('utf-8')==abytes:
					return 'utf-8'
			except Exception as e:
				pass
		if r['confidence']>confidence:return r['encoding']
		else:
			if default:return default
			raise Exception(
			'{0} encoding {1} confidence {2} less then {3}'.format(
			abytes[:99],r['encoding'],r['confidence'],confidence)  )
except Exception as ei:
	def detect(*a):
		raise Exception('#not install chardet Module')  # <no> is not callable ,see the source
	pass
try:
	from pprint import pprint,pformat
except:pass
####################################################
def encode(s,encoding):
	'''
	'''
	
	
def join(iterable,separator=','):
	if py.istr(iterable):return iterable
	return separator.join([string(i) for i in iterable] )
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


def getFLD(url_or_domain):
	"""Extract the first level domain.
	
	"""
	import tld
	try:
		return tld.get_fld(fix_protocol=True,url=url_or_domain)
	except Exception as e:
		return py.No(e)
		#TldDomainNotFound: Domain 网站域名 didn't match any existing TLD name!
get_fld=getFLD


def filterInt(a,digits=py.range(1,999)):
	digits=py.list(digits)
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
filter_sint_list=filter_sint=filter_int=filterInt

################### zh #############################
# u'([\u4e00-\u9fff]+)'  
RE_ZH_PATTERN = re.compile(u'[\u4e00-\u9fa5]+')

def filterZh(a,splitor=' '):
	return splitor.join(RE_ZH_PATTERN.findall(a ) )
filter_zh=filterZh
	
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
	
def readableTimeText(txt,browser=True):
	U=py.importU()
	def ref(a):
		a=a.group()
		it=py.int(a)
		if py.len(a)==13:
			it=it/1000
		return U.stime(a)

	r= regexReplace(_4 , r'\d{10,}',ref)
	if browser:
		U.browserObj(r)
	else:return r
	
RE_IP= re.compile('''(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))''')
def ipLocationText(text,location_format=' [{0}] ',reverse_ip=True,p=True):
	U=py.importU()
	N=py.importN()
	
	def fr(a):
		# i0,i=a.span()
		# a=py.int(text[i0:i] )
		a=a.group()
		location=N.ipLocation(a,reverse_ip=reverse_ip)
		return location

	r=regexReplace(text,RE_IP,fr)
	if p:U.pln(r)
	else:return r
	
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

def regexCount(a,regex):
	return py.len(re.findall(regex, a))
countRegex=regexCount
	
def regexReplace(a,regex,str_or_func):
	''' 
func( a: <_sre.SRE_Match object; span=(2388, 2396), match='21758465'>  ):
	match==a.group()	
	
	
\QGB\Anaconda3\Lib\site-packages\jedi\evaluate\compiled\fake\_sre.pym
    class SRE_Match():
            yield SRE_Match(self)	
	'''
	if py.istr(str_or_func):
		def func(_a):
			#   <_sre.SRE_Match object; span=(2388, 2396), match='21758465'>
			# match==a.group()	
			return str_or_func
	else:
		func=str_or_func
	if not py.callable(func):raise py.ArgumentError('str_or_func',str_or_func)
	
	if py.istr(regex):
		p=re.compile(regex)
	else:
		p=regex
	return p.sub(func,a)
##################  regex end  ############################
def autoDecode(abytes,confidence=0.7,default=py.No('default encoding "" ')  ):
	if py.isunicode(abytes):return abytes
	if not py.isbyte(abytes):
		raise py.ArgumentError('is not bytes',abytes)
	return abytes.decode( detect(abytes=abytes,confidence=confidence,default=default) )
detectDecode=detectAndDecode=autoDecode

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
def urlEncode(a):
	''' a : str_or_bytes
	#todo 	convert Non-string objects
	'''
	
	if py.is3():
		import urllib
		return urllib.parse.quote(a)
	raise NotImplementedError()
def urlDecode(a):
	''' a : str_or_bytes
	'''
	if py.is3():
		import urllib
		if isinstance(a, py.bytes):a=a.decode()
		# if not py.istr():
		return urllib.parse.unquote(a)
	raise NotImplementedError()
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

def matchWildcard(a,exp):
	'''Wildcard character'''
	import fnmatch
	exp=fnmatch.translate(exp)
	exp=re.compile(exp)
	try:
		return exp.match(a).group()	
	except:
		return ''

def regexMatchAll(a,regex):
	return [i.group() for i in re.finditer(regex,a)]
		
def regexMatchGroups(a,regex):
	''' return [list of re.search group [s]]
re.search(pattern, string, flags=0)
pattern	匹配的正则表达式
string	要匹配的字符串。
flags	标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。
	'''
	r= re.search(regex,a)
	if r:
		if r.groups():#返回一个包含所有小组字符串的元组，从 1 到 所含的小组号。
			r=[r.group()]+py.list(r.groups())
		else:r=[r.group()]
		return r
	else:
		return []
match_groups=matchGroups=regexMatchGroups

def regexMatch(a,regex):
	''' return :str  match_groups first
	'''
	r=regexMatchGroups(a,regex)
	if r:return r[0]
	else:return ''
matchRegex=regexMatch

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

def base64decode(a):
	import base64
	if py.istr(a):
		return detectAndDecode(base64.b64decode(a))
	if py.isbyte(a):
		return base64.b64decode(a) #type bytes
		
def strToBaseN(a,base=64,symbols=None):
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
	import ast
	return ast.literal_eval(str)
unrepr=ast_literal_eval=literal_eval

def jsonToDict(a):
	'''is2: 不同于 json_loads ，不会自动转换 到unicode'''
	import ast
	return ast.literal_eval(a.replace('false','False').replace('true','True'))
js2py=jsonToDict
	
def json_loads(astr):
	import json
	try:
		return json.loads(astr)
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
	
def string(a,decode=''):
	'''return unicode'''
	if py.is2():
		if py.type(a) is py.str and decode:return a.decode(decode)
		U=py.importU()
		if py.type(a) is py.unicode:return a#.encode(U.encoding)
		try:return py.str(a)
		except:return ''
	else:
		if isinstance(a,py.bytes) and decode:return a.decode(decode)
		try:return py.str(a)
		except:return ''
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

def sub(s,s1,s2=''):
	if(s==None):return ()
	if not istr(s):s=str(s)
	i1=s.find(s1)
	if(s2==''):
		i2=s.__len__()
	else:
		i2=s.find(s2,i1+len(s1))
	if(-1==i1 or -1==i2):
		return ''
	i1+=len(s1)
	# U.pln( i1,i2
	return s[i1:i2]
subLeft=subl=sub

def subRight(s,s1,s2=''):
	if(s==None):return ()
	s=str(s)
	i1=0
	if s1!='':i1=s.rfind(s1)
	if(s2==''):
		i2=s.__len__()
	else:
		i2=s.rfind(s2,i1+1)
	if(-1==i1 or -1==i2):
		return ''
	i1+=len(s1)
	# U.pln( i1,i2
	return s[i1:i2]
subLast=subr=subRight
	
def removeAllSpace(a):
	'''in char256 {' ', '\x0b', '\x1c', '\x1d', '\t', '\x0c', '\x1e', '\x85', '\xa0', '\x1f', '\r', '\n'}  removed'''
	import re
	return re.sub(r"\s+", "", a, flags=re.UNICODE)
delAllSpace=removeAllSpaces=removeAllSpace

def replacey(a,olds,new):
	if not py.istr(a):return py.No('a is not str',a)
	# else:a=str(a)
	if(len(olds)<1):raise Exception('Target chars Null')
	for i in olds:
		a=a.replace(i,new)
	return a
	
	
def replaceAll(a,old,new):
	''' S.replace(old, new[, count]) -> string'''
	while old in a:
		a=a.replace(old,new)
	return a
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
def fileNameLegalized(a,default='_'):
	if not py.istr(a):a=string(a)
	r=''
	for i in range(len(a.strip() )  ):
		if (a[i] in FILE_NAME) or hasZh(a[i] ):
			r+=a[i]
		else:r+=default
	return r
fileName=filename=fileNameLegalized
# filename.__str__=FILE_NAME	
	
def haszh(a):
	zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
	match = zhPattern.search(a)
	if match:return True
	return False
	
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
	
def min(*a):
	'''return min length string(a[i])'''
	r=''
	for i in a:
		i=string(i)
		if len(i)<len(r):r=i
	return r
	
	
def max(*a):
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
	
gszFinancial='''零壹贰叁肆伍陆柒捌玖拾佰仟萬億'''
#亿的后面 ，大写小写都是同一个。
#参见https://zh.wikipedia.org/wiki/中文数字
gsz09=gsZ09='''〇一二三四五六七八九'''
gszi=gsZI='''个、十、百、千、万、十万、百万、千万、亿、十亿、百亿、千亿 、兆、十兆、百兆、千兆、京、十京、百京、千京、垓、十垓、百垓、千垓、秭、十秭、百秭、千秭、穰、十穰、百穰、千穰、沟、十沟、百沟、千沟、涧、十涧、百涧、千涧、正、十正、百正、千正、载、十载、百载、千载、极、十极、百极、千极'''
gZi=gsZI.split('、')

def readNumber(a,split=4,p=True):
	if split<1:return ''
	zh=gZi[::split]
	if py.isnum(a):a=py.int(a)#py2 ok
	if not py.istr(a):a=str(a)
	U=py.importU()
	a=''.join(U.one_in(py.list(a),number))
	while(a.startswith('0')):a=a[1:]

	s='';im=py.len(a);iz=0;zh[0]=''#忽略 个
	for i,k in enumerate(a):	
		if i%split==0:
			i=a[im-i-split:im-i]
			s=i+zh[iz]+s
			iz+=1
			# U.pln(  i,
	s=a[0:im-((iz-1)*split)]+s
	# U.repl()
	# for i in zh:U.pln( i.decode('utf-8').encode(U.stdout.encoding) )
	if py.is2():s=s.decode('utf-8').encode(U.stdout.encoding)
	if p:U.pln(s)	
	return s

gcszh=gZhEncodings=gcodingZh={'gb18030', 'gb2312', 'gbk', 'big5', 'big5hkscs', 'cp932', 'cp949', 'cp950', 'euc-jisx0213', 'euc-jis-2004', 'euc-jp', 'euc-kr', 'hz', 'idna', 'iso2022-jp', 'iso2022-jp-1', 'iso2022-jp-2', 'iso2022-jp-2004', 'iso2022-jp-3', 'iso2022-jp-ext', 'iso2022-kr', 'johab', 'mbcs', 'punycode', 'raw-unicode-escape', 'shift-jis','shift-jisx0213', 'shift-jis-2004', 'unicode-escape', 'unicode-internal', 'utf-16', 'utf-16-be', 'utf-16-le', 'utf-32', 'utf-32-be', 'utf-32-le', 'utf-7', 'utf-8', 'utf-8-sig'}
	
gcscp={'cp819', 'cp1026', 'cp1252', 'cp1140', 'cp1006', 'cp1361', 'cp932', 'cp424', 'cp154', 'cp720', 'cp936', 'cp500', 'cp869', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp1255', 'cp1254', 'cp1257', 'cp1256', 'cp1251','cp1250', 'cp1253', 'cp858', 'cp437', 'cp949', 'cp1258', 'cp737', 'cp367', 'cp850', 'cp852', 'cp855', 'cp857', 'cp856', 'cp775', 'cp875','cp874', 'cp950'}
gcharset=charset=gcs=gencodings=gcoding={'ascii', 'base64-codec', 'big5', 'big5hkscs', 'bz2-codec', 'charmap', 'cp037', 'cp1006', 'cp1026', 'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'cp1361', 'cp367', 'cp424', 'cp437', 'cp500', 'cp720', 'cp737', 'cp775', 'cp819', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp858', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp936', 'cp949', 'cp950', 'euc-jis-2004', 'euc-jisx0213', 'euc-jp', 'euc-kr', 'gb18030', 'gb2312', 'gbk', 'hex-codec', 'hp-roman8', 'hz', 'idna', 'iso2022-jp', 'iso2022-jp-1', 'iso2022-jp-2', 'iso2022-jp-2004', 'iso2022-jp-3', 'iso2022-jp-ext', 'iso2022-kr', 'iso8859-1', 'iso8859-10', 'iso8859-11', 'iso8859-13', 'iso8859-14', 'iso8859-15', 'iso8859-16', 'iso8859-2', 'iso8859-3', 'iso8859-4', 'iso8859-5', 'iso8859-6', 'iso8859-7', 'iso8859-8', 'iso8859-9', 'johab', 'koi8-r', 'koi8-u', 'latin-1', 'mac-arabic', 'mac-centeuro', 'mac-croatian', 'mac-cyrillic', 'mac-farsi', 'mac-greek', 'mac-iceland', 'mac-latin2', 'mac-roman', 'mac-romanian', 'mac-turkish', 'mbcs', 'palmos', 'ptcp154', 'punycode', 'quopri-codec', 'raw-unicode-escape', 'rot-13', 'shift-jis', 'shift-jis-2004', 'shift-jisx0213', 'tis-620', 'unicode-escape', 'unicode-internal', 'utf-16', 'utf-16-be', 'utf-16-le', 'utf-32', 'utf-32-be', 'utf-32-le', 'utf-7', 'utf-8', 'utf-8-sig', 'uu-codec', 'zlib-codec'}	
#https://docs.python.org/2/library/codecs.html#standard-encodings        https://docs.python.org/3/library/codecs.html#standard-encodings
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