#coding=utf-8
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
	try:
		w.OpenClipboard()
		w.EmptyClipboard()
		# w.SetClipboardData(win32con.CF_TEXT, aString)
		w.SetClipboardText(aString)
	finally:
		w.CloseClipboard()

def set_repr(a):
	return set(repr(a))
setr=setRepr=set_repr

def close():
	w.CloseClipboard()
	
def getTypeList():
	'''cb.set('===============')
	for i in range(1,65536):
[[1, b'==============='],
 [7, b'==============='],
 [13, '==============='],
 [16, b'\x04\x08\x00\x00']]
 
 other:if d.args==('Specified clipboard format is not available',):continue
 TypeError('Specified clipboard format is not available')
 '''
	w.OpenClipboard()
	r={}
	i=0
	while True:
		i=w.EnumClipboardFormats(i)
		if not i:break
		try:
			d=w.GetClipboardData(i)
		except Exception as e:
			r[i]=e
		else:	
			r[i]=d
			# r.append([i,d])
	w.CloseClipboard()# 未close 会导致 clipboard 无法使用
	return r

#set(get()[0:5])	


#import T



#import U
#U.test()
