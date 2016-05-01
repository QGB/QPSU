# coding=utf-8
filename="!#$%&'()+,-0123456789;=@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{}~"
pathname=filename+'/\\:'
character='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
number='0123456789'
a_z0_9=alphanumeric=character+number
hex='0123456789abcdef'
REURL='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
REYMD="(19|20)[0-9]{2}[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])"
sqlite='SELECT * FROM sqlite_master;'
asciiPrint=' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'#0x20-0x7E ,32-126,len=95

#########################################
import   re
	
def string(a):
	if type(a)==type(''):return a
	try:a=str(a)
	except:a=''
	return a

def stringToChars(a):
	'''TODO:flap'''
	a=string(a)

def inMutiChar(a,asc):
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
	return inMuti()
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
	return replacey(a,'_',':','.','\\','/','-','"',' ','\n','\r','\t')
	
def haszh(a):
	zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
	match = zhPattern.search(a)
	if match:return True
	return False
	
if __name__=='__main__':
	print inMutiChar('2/ewffew////',set())
	exit()
	import os
	os.chdir('cd')
	import U
	sf=''
	for i in filename:
		U.write(i,'123')
		if U.read(i)=='123':sf+=i
	print sf==filename	
			
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