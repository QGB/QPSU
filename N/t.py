from HTTPServer import *
# print dir()

@route()
def a(h):
	print dir()
	return [1,2,3]
def main():
	from threading import Thread
	Thread(target=serve).start()
# serve()	
if __name__=='__main__':
	main()
	