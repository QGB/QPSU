
# coding=utf-8
FILE_NAME="!#$%&'()+,-0123456789;=@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{}~"### NO space
PATH_NAME=FILE_NAME+'/\\:'

az=a_z='abcdefghijklmnopqrstuvwxyz'
AZ=A_Z=a_z.upper()

character=a_z+A_Z

s09=i09=_09=number='0123456789'

az09=a_z0_9=alphanumeric=character+number

hex='0123456789abcdef'
HEX=hex.upper()

#0x20-0x7E ,32-126,len=95
visAscii=printAscii=asciiPrint=' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

###############
REURL='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
REYMD="(19|20)[0-9]{2}[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])"
###############
sqlite='SELECT * FROM sqlite_master;'

#########################################
squote=quote="'"
dquote=dQuote='"'
import __builtin__ ;py=builtin=__builtin__
import   re	
try:
	from chardet import detect
except Exception as ei:
	pass
	
def matchHead(txt,regex):
	r=re.match(regex,txt)
	if r:return r.group()
	else:return ''
	
def string(a):
	if type(a) is str:return a
	try:a=str(a)
	except:a=''
	return a

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
		sr=sr+str(i)+','
	return '['+sr+']'
def ishex(a):
	if type('')!=type(a):return False
	if len(a)<1:return False
	for i in a.lower():
		if i not in hex:return False
	return True	
def sub(s,s1,s2=''):
	if(s==None):return None
	s=str(s)
	i1=s.find(s1)
	if(s2==''):
		i2=s.__len__()
	else:
		i2=s.find(s2,i1+len(s1))
	if(-1==i1 or -1==i2):
		return ''
	i1+=len(s1)
	# print i1,i2
	return s[i1:i2]
subLeft=subl=sub

def subRight(s,s1,s2=''):
	if(s==None):return None
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
	# print i1,i2
	return s[i1:i2]
subLast=subr=subRight
	
def replacey(a,c,*yc):
	if(a==None):raise Exception('a(string) == None')
	else:a=str(a)
	if(len(yc)<1):raise Exception('Target chars Null')
	if(c==None):raise Exception('c None')
	for i in yc:
		a=a.replace(i,c)
	return a
	print yc
	
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
# print varname(i09)
def filename(a):
	# if type(a) is not str:return ''
	r=''
	for i in range(len(a)):
		if a[i] in FILE_NAME:r+=a[i]
		else:r+='_'
	return r
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
		import U
		s.data=eval(U.read(fileName))['log']
		
	
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
	if type(a) not in (str,unicode):return False
	for i in a:
		if ord(i)>127:return False
		# print ord(i);break
	return True
	
gsZI='''个、十、百、千、万、十万、百万、千万、亿、十亿、百亿、千亿 、兆、十兆、百兆、千兆、京、十京、百京、千京、垓、十垓、百垓、千垓、秭、十秭、百秭、千秭、穰、十穰、百穰、千穰、沟、十沟、百沟、千沟、涧、十涧、百涧、千涧、正、十正、百正、千正、载、十载、百载、千载、极、十极、百极、千极'''
gZi=gsZI.split('、')

def readNumber(a,split=4,p=True):
	if split<1:return ''
	zh=gZi[::split]
	if a not in(str,unicode):a=str(a)
	import U
	a=''.join(U.one_in(list(a),number))
	while(a.startswith('0')):a=a[1:]

	s='';im=py.len(a);iz=0;zh[0]=''#忽略 个
	for i,k in enumerate(a):	
		if i%split==0:
			i=a[im-i-split:im-i]
			s=i+zh[iz]+s
			iz+=1
			print  i,
	s=a[0:im-((iz-1)*split)]+s
	# U.repl()
	# for i in zh:print i.decode('utf-8').encode(U.stdout.encoding)
	s=s.decode('utf-8')
	if p:print s.encode(U.stdout.encoding)		
	return s

gcszh=gZhEncodings=gcodingZh={'gb18030', 'gb2312', 'gbk', 'big5', 'big5hkscs', 'cp932', 'cp949', 'cp950', 'euc-jisx0213', 'euc-jis-2004', 'euc-jp', 'euc-kr', 'hz', 'idna', 'iso2022-jp', 'iso2022-jp-1', 'iso2022-jp-2', 'iso2022-jp-2004', 'iso2022-jp-3', 'iso2022-jp-ext', 'iso2022-kr', 'johab', 'mbcs', 'punycode', 'raw-unicode-escape', 'shift-jis','shift-jisx0213', 'shift-jis-2004', 'unicode-escape', 'unicode-internal', 'utf-16', 'utf-16-be', 'utf-16-le', 'utf-32', 'utf-32-be', 'utf-32-le', 'utf-7', 'utf-8', 'utf-8-sig'}
	
gcscp={'cp819', 'cp1026', 'cp1252', 'cp1140', 'cp1006', 'cp1361', 'cp932', 'cp424', 'cp154', 'cp720', 'cp936', 'cp500', 'cp869', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp1255', 'cp1254', 'cp1257', 'cp1256', 'cp1251','cp1250', 'cp1253', 'cp858', 'cp437', 'cp949', 'cp1258', 'cp737', 'cp367', 'cp850', 'cp852', 'cp855', 'cp857', 'cp856', 'cp775', 'cp875','cp874', 'cp950'}
gcharset=charset=gcs=gencodings=gcoding={'ascii', 'base64-codec', 'big5', 'big5hkscs', 'bz2-codec', 'charmap', 'cp037', 'cp1006', 'cp1026', 'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'cp1361', 'cp367', 'cp424', 'cp437', 'cp500', 'cp720', 'cp737', 'cp775', 'cp819', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp858', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp936', 'cp949', 'cp950', 'euc-jis-2004', 'euc-jisx0213', 'euc-jp', 'euc-kr', 'gb18030', 'gb2312', 'gbk', 'hex-codec', 'hp-roman8', 'hz', 'idna', 'iso2022-jp', 'iso2022-jp-1', 'iso2022-jp-2', 'iso2022-jp-2004', 'iso2022-jp-3', 'iso2022-jp-ext', 'iso2022-kr', 'iso8859-1', 'iso8859-10', 'iso8859-11', 'iso8859-13', 'iso8859-14', 'iso8859-15', 'iso8859-16', 'iso8859-2', 'iso8859-3', 'iso8859-4', 'iso8859-5', 'iso8859-6', 'iso8859-7', 'iso8859-8', 'iso8859-9', 'johab', 'koi8-r', 'koi8-u', 'latin-1', 'mac-arabic', 'mac-centeuro', 'mac-croatian', 'mac-cyrillic', 'mac-farsi', 'mac-greek', 'mac-iceland', 'mac-latin2', 'mac-roman', 'mac-romanian', 'mac-turkish', 'mbcs', 'palmos', 'ptcp154', 'punycode', 'quopri-codec', 'raw-unicode-escape', 'rot-13', 'shift-jis', 'shift-jis-2004', 'shift-jisx0213', 'tis-620', 'unicode-escape', 'unicode-internal', 'utf-16', 'utf-16-be', 'utf-16-le', 'utf-32', 'utf-32-be', 'utf-32-le', 'utf-7', 'utf-8', 'utf-8-sig', 'uu-codec', 'zlib-codec'}	
if __name__=='__main__':
	import sys,os;sys.path.append('E:\sourceCode\shell\py');from qgb import *
	print U
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
			print i
		except:pass
	# print c
	exit()
	
	gcs=sorted(gcs)
	U.txt(str(gcs)) 
		
	exit()
	f=U.read(__file__)

	for i in gsZI.split('、'):
		print '%-2s %s'%(U.ct(),i.decode('utf-8').encode('gb18030'))
	exit()
	
	print detect(s)
	s=s.decode('utf-8')
	print haszh(s),len(s)
	exit()
	print max()
	exit()
	import os
	os.chdir('cd')
	sf=''
	for i in FILE_NAME:
		U.write(i,'123')
		if U.read(i)=='123':sf+=i
	print sf==FILE_NAME	
			
	# print U.inMuti('123456.9.9','18','1','',f=inMutiChar)
	# print len(asciiPrint)
	exit()
	# import urllib2,re
	# url='http://svn.kcn.cn/repos/kbs/'
	# r=urllib2.urlopen(url)
	# s=r.read()
	s='''<html><head><title>kbs - Revision 11899: /</title></head>
	<body>
	 <h2>kbs - Revision 11899: /</h2>
	 <ul>
	  <li><a href="branches/">branches/</a></li>
	  <li><a href="tags/">tags/</a></li>
	  <li><a href="trunk/">trunk/</a></li>
	 </ul>
	 <hr noshade><em>Powered by <a href="http://subversion.tigris.org/">Subversion</a> version 1.6.11 (r934486).</em>
	</body></html>'''
	# print "s='''{0}'''".format(s)
	print sub(s,'h','r')

	# print haszh(s)
	# s='44444.py.py'
	# print subr(s,'','.py')
	# print s.find(a,)
	# print s[:50]
	# print s.find('1')