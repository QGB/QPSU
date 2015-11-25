REURL='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
REYMD="(19|20)[0-9]{2}[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])"
def sub(s,s1,s2=''):
	if(s==None):return None
	s=str(s)
	i1=s.find(s1)
	if(s2==''):
		i2=s.__len__()
	else:
		i2=s.find(s2)
	if(-1==i1 or -1==i2):
		return ''
	i1+=len(s1)
#	print i1,i2
	return s[i1:i2]
		

#print sub('12345678','1','')