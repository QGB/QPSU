try:
	import win32clipboard as w
	import win32con
except Exception as err:
	print __file__+":",err

def get():
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return d

def set(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_TEXT, aString)
    w.CloseClipboard()
	
#set(get()[0:5])	



#print '123'[0:9]
#import T



#import U
#U.test()
