# coding=utf-8
hex='0123456789abcdef'
import   re
REURL='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
REYMD="(19|20)[0-9]{2}[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])"
sqlite='SELECT * FROM sqlite_master;'
def listToStr(a):
	if type(a)!=type([]):return ''
	sr=''
	for i in a:
		sr=sr+str(i)+','
	return '['+sr+']'
def ishex(a):
	if type('')!=type(a):return False
	if len(a)<1:return False
	for i in a:
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
	return replacey(a,'_',':','.','\\','/','-','"',' ','\n','\r','\t')
	
def haszh(a):
	zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
	match = zhPattern.search(a)
	if match:return True
	return False
	
if __name__=='__main__':	
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