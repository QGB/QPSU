from HTTPServer import *
# print dir()

@route()
def a(h):
	print dir()
	return [1,2,3]
	
from threading import Thread
Thread(target=serve).start()
# serve()	