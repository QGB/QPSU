from ctypes import windll#.user32.MessageBoxA as m
u=windll.user32
msgbox=windll.user32.MessageBoxA
import  os,sys
#m(0, 'rtegwf', 'hi', 0)
#print 

def msgbox(s='pause',st='title'):
	u.MessageBoxA(0, s, st, 0)
	
def p(*a):
	print a
	sys.stdout.flush()

def x():
	exit(235)
	
def exit(i=2357):
	os._exit(i)


def test(a='mmmmmmmmm'):
	i=0
	s='''
print 1122
print dir()
print a
print s
i+=1
print '-'*6*5+str(i)
if(i<4):
	exec(s) 
	'''
	exec(s)
	exit()
	
#test()

#msgbox('1111')
'''
test('76543')


#
t=test()x

print id(test),id(t)
os._exit(3)
print type(t),type(test)
try:t()
except Exception as e:print str(e)
'''
#print type(t)