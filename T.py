def sub(s,s1,s2):
	i1=s.find(s1)
	if(s2==''):
		i2=s.__len__()
	else:
		i2=s.find(s2)
	if(-1==i1 or -1==i2):
		return ''
#	print i1,i2
	return s[i1+1:i2]
		

#print sub('12345678','1','')