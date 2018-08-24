import pywinauto
import win32api  

if __name__.endswith('qgb.Win'):
	from .. import py
else:
	import py
py.importU()

def getWindowCur(w):
    import win32api
    x,y=win32api.GetCursorPos()
    r=w.rectangle()
    return [x-r.left,y-r.top]                                       
	
def printWindowCur(w)
	while 1:
		print (getWindowCur(w))
		U.sleep(1)           
		

def keySend(w,askey)
	r'''
 !"#$'*<-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]`abcdefghijklmnopqrstuvwxyz|
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
	'''
	
	w.send_keystrokes(askey)
	return askey