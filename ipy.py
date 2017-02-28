import sys,os,U,T,F

# print U.gError
gipy=U.ipy
gt=None

U.cdt()

os.mkdir('ipy')

# print 
def recorder():
	while True:
		gipy.user_ns['In']

def startRecord():
	global gt
	gt=U.thread(target=recorder)
	gt.start()



class IPy():

	def __call__(s):
		print 233
	
# sys.modules['qgb.ipy'] = IPy()
# U.msgbox()
F.writeIterable('ipy/fwi.txt',sys.modules)

U.repl()
# U.thread(target=recorder).start()
print 233