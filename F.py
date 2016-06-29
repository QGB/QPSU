def hexToBytes(a):
	if type(a)!=type('') or len(a)%2!=0:
		return None
	
	print bytes(1)+'99'
	# for i in range(len(a)/2):
	
	
s='''%3Ctextarea+stylew3equalsign%22width%3A100%25%3Bheight%3A100%25%22%3Epublic+class+Int%7B%0D%0A%0D%0A%09public+static+void+main%28String%5B%5D+ays%29%7B%0D%0A%09%09int+aw3equalsignays.lengthw3equalsignw3equalsign1%3FInteger.valueOf%28ays%5B0%5D%29%3A%0D%0A%09%09%2F**xjw++a**%2F++2%3B%0D%0A%09%09%0D%0A%09%09for%28int+iw3equalsign0%2Csw3equalsign0%2Ctw3equalsign0%3Bi%3Ca%3Bi%2B%2B%29%7B%0D%0A%09%09%09t%2Bw3equalsigna*new+Object%28%29%7B%0D%0A%09%09%09%09int+pow%28int+a%2Cint+n%29%7B%0D%0A%09%09%09%09%09if%28nw3equalsignw3equalsign0%29return+1%3B%0D%0A%09%09%09%09%09if%28nw3equalsignw3equalsign1%29return+a%3B%0D%0A%09%09%09%09%09return+pow%28a%2Cn-1%29*a%3B%0D%0A%09%09%09%09%7D%09%0D%0A%09%09%09%7D.pow%2810%2Ci%29%3B%0D%0A%09%09%09s%2Bw3equalsignt%3B%0D%0A%09%09%09if%28iw3equalsignw3equalsigna-1%29System.out.printf%28%22a+w3equalsign+%25s%5Cns+w3equalsign+%25s%5Cn%22%2Ca%2Cs%29%3B%09%09%0D%0A%09%09%7D%0D%0A%09%7D%0D%0A%0D%0A%7D%3C%2Ftextarea%3E%0D%0A'''
	
import T,N,U
su='http://www.w3school.com.cn/tiy/v.asp?code='
for i in T.HEX:
	for j in T.HEX:
		# su+='%'+i+j
		su+='%77'
		U.pln(i,j,N.http(su)[:8])
exit()
	
	
if __name__=='__main__':
	import binascii as ba
	
	s=ba.b2a_hex(s)
	t=''
	
	for i in xrange(len(s)):
		if i%2==0:t+='%'
		t+=s[i]
	print t	
	print hexToBytes('3334')