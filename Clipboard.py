try:
	import win32clipboard as w
	import win32con
except Exception as err:
	gError=err

def get():
	'''win32con.
CF_DSPTEXT     ', 129],
CF_OEMTEXT     ', 7],
CF_RETEXTOBJ   ', 'RichEdit Text and Objects'],
CF_TEXT        ', 1],
CF_UNICODETEXT ', 13],
	
	in py3 win32con.CF_TEXT return b' '
	'''
	w.OpenClipboard()
	d = w.GetClipboardData(win32con.CF_UNICODETEXT)
	w.CloseClipboard()
	return d

def set(aString):
	w.OpenClipboard()
	w.EmptyClipboard()
	# w.SetClipboardData(win32con.CF_TEXT, aString)
	w.SetClipboardText(aString)
	w.CloseClipboard()
	
#set(get()[0:5])	


#import T



#import U
#U.test()
