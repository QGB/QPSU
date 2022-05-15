#coding=utf-8
try:from . import py
except:import py
# 因为 Clipboard 在 qgb.U 中 较早加载，此时又引入其他模块 容易造成循环引用 引起 其他问题。

try:
	import win32clipboard as w
	import win32con
except Exception as err:
	gError=err

def get(p=False,edit=False,edit_prompt='',only_edit_firstline=True,**ka):
	'''win32con.
CF_DSPTEXT     ', 129],
CF_OEMTEXT     ', 7],
CF_RETEXTOBJ   ', 'RichEdit Text and Objects'],
CF_TEXT        ', 1],
CF_UNICODETEXT ', 13],
	
	in py3 win32con.CF_TEXT return b' '
prompt [präm(p)t 不发音p] 提示 ;
promte 提升
	'''
	U=py.importU()
	if U.istermux():return U.cmd('termux-clipboard-get') 
	p=U.get_duplicated_kargs(ka,'_print','print_','show','PRINT',default=p)
	edit=U.get_duplicated_kargs(ka,'e','E','input_edit','input','edit_clipboard',default=edit)
	
	w.OpenClipboard()
	d = w.GetClipboardData(win32con.CF_UNICODETEXT)
	w.CloseClipboard()
	if p:U.pln(d)
	if edit:
		type=U.get_duplicated_kargs(ka,'type','edit_type','t') 
		edit_prompt=U.get_duplicated_kargs(ka,'title','msg','edit_msg','edit_prompt','prompt','promte','promot','promote',default=edit_prompt)
		only_edit_firstline=U.get_duplicated_kargs(ka,'edit_firstline','firstline','fl',
		'line0','l0',default=only_edit_firstline)
		if not edit_prompt:
			if py.istr(edit):edit_prompt=edit
			else:edit_prompt=''
		if only_edit_firstline and py.len(d.splitlines())>0:
			d=d.splitlines()[0]
		d=U.input(edit_prompt,default=d,type=type)
	return d
# U.cbg=get
	
def set(aString,p=0,r=0):
	U=py.importU()
	if p:print("'''",aString,"'''")
	if U.istermux():return U.cmd('termux-clipboard-set',input=aString) 
	try:
		w.OpenClipboard()
		w.EmptyClipboard()
		# w.SetClipboardData(win32con.CF_TEXT, aString)
		w.SetClipboardText(aString)
	finally:
		w.CloseClipboard()
	if r:return U.StrRepr(aString)	
# U.cbs=set
		
def set_repr(a):
	return set(repr(a))
setr=setRepr=set_repr

def close():
	w.CloseClipboard()

gsdir=''
def get_image(file=None,format='png'):
	''' :param fp: A filename (string), pathlib.Path object or file object.

KeyError: '.PNG'  [format not contains . ]
	'''
	global gsdir
	U,T,N,F=py.importUTNF()
	if not gsdir:
		gsdir=U.get_or_set('clipboard.dir',lazy_default=lambda :F.md(U.gst+'clipboard'))
	
	from PIL import ImageGrab,Image
	im = ImageGrab.grabclipboard()
	if im and file:
		# if not im:
			# return 			
		if not F.isAbs(file):
			file=gsdir+file
		if not file.lower().endswith(format.lower()):
			file=file+'.'+format
		im.save(file,format)
		
		return file
	elif not im:
		return py.No('can not get clipboard image')
	return im
get_img=get_image
###############################	
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
