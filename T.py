REURL='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
REYMD="(19|20)[0-9]{2}[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])"
def sub(s,s1,s2=''):
	if(s==None):return None
	s=str(s)
	i1=s.find(s1)
	if(s2==''):
		i2=s.__len__()
	else:
		i2=s.find(s2,i1+1)
	if(-1==i1 or -1==i2):
		return ''
	i1+=len(s1)
	# print i1,i2
	return s[i1:i2]
		
s='''
"D:\Program Files\goagent_3.1.0-0\local\proxy.ini"
"E:\software\net\tool\XX-Net-1.3.6\goagent\3.1.40\local\proxy.ini"
"E:\software\net\tool\XX-Net-2.5.1\gae_proxy\local\proxy.ini"
"E:\software\net\tool\XX-Net-2.5.1\php_proxy\local\proxy.ini"
"C:\Documents and Settings\Adminstrtor\Recent\proxy.ini.lnk"
'''
a=r'"'
# print sub(s,r'"',a)
# print s.find(a,)
# print s[:50]
# print s.find('1')