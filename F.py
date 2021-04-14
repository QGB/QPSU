# coding=utf-8
import sys as _sys;from os import path as _p#endswith 是为了适配qgb处于另外一个包内的情况
if __name__.endswith('qgb.F'):from . import py
else:import py
T=py.importT()
import os as _os
try:from pathlib import Path
except:pass

gError=[]
def setErr(ae):
	global gError
	U=py.importU()
	if U.gbLogErr:# U.
		if type(gError) is list:gError.append(ae)
		elif gError:gError=[gError,ae]
		else:gError=[ae]
	else:
		gError=ae
	if U.gbPrintErr:U.pln('#Error ',ae)
###################
class IntSize(py.int):
	def __new__(cls, *a, **ka):
		return py.int.__new__(cls, *a, **ka)
	def __repr__(self):
		return '<{}>'.format(numToSize(self) )
		# return '<{}={}>'.format(super().__repr__(),F.ssize(self) )

def test_long_filename():
	'''
245
246
247
248
249 #FileNotFoundError     Windows 10                    

'''
	v='a234567890b234567890c234567890d234567890e234567890f234567890g234567890h234567890i234567890j234567890k234567890l234567890m234567890n234567890o234567890p234567890q234567890r234567890s234567890t234567890u234567890v234567890w234567890x234567890y234567890z23456789'# len(v)==259
	p=F.mkdir(U.gst+'fn')
	U.cd(p)
	for n in range(245,260):
		print(n)
		with open(v[:n],'w') as f:f.write(str(n))
		with open(p+v[:n],'w') as f:f.write(str(n))
		#249 两个同样  #FileNotFoundError 
		
	# for n in range(245,260):
		# print(n)
		
		
def replaceOnce(a,old,new):
	return a.replace(old, new,1) #count=1 #TypeError: replace() takes no keyword arguments 
	
def expandUser(file='',user=''):
	'''always return endswith / 
	
import os, pwd
pwd.getpwuid(os.getuid()).pw_dir	
	'''
	import os
	h=os.path.expanduser('~'+user)
	h=autoPath(h)
	# if not r.endswith('/'):r=r+'/'
	return replaceOnce(file,'~',h)
expand_user=expanduser=expandUser
	
def getHomeFromEnv():
	import os
	U=py.importU()
	if U.isLinux():
		name='HOME'
	elif U.isWin():
		name='USERPROFILE'
	else:
		raise EnvironmentError('#TODO system case')
	r=U.getEnv(name)
	r=autoPath(r)
	if not r.endswith('/'):r=r+'/'
	return r
home=gethome=get_home=getHome=getHomeFromEnv	
	
def include(file,keyword):
	if py.isbyte(keyword):mod='rb'
	else:mod='r'
	try:
		with py.open(file,mod) as f:
			for i in f:
				if keyword in i:return True
	except Exception as e:
		return py.No(e)
	return False
	
def stat(path, dir_fd=None, follow_symlinks=True):
	U=py.importU()
	IntSize,FloatTime,IntOct=U.IntSize,U.FloatTime,U.IntOct	
	import os
	try:
		if isinstance(path,os.stat_result):
			s=path
		else:
			s=os.stat(path=path, dir_fd=dir_fd, follow_symlinks=follow_symlinks)
		# return [
		# 		path,
		# 		IntSize(s.st_size),
		# 		FloatTime(s.st_atime),
		# 		FloatTime(s.st_mtime),
		# 		FloatTime(s.st_ctime),
		# 		IntOct (s.st_mode ),
		# 		]
		
	except Exception as e:
		return py.No(e)
	r={}
	for i in py.dir(s):
		if not i.startswith('st_'):continue
		v=getattr(s,i,py.No('Error getattr') )
		if i=='st_size':r[i]=IntSize(v);continue
		if i=='st_mode':r[i]=IntOct(v)      ;continue
		if i.endswith('time'):
			r[i]=FloatTime(v)
			continue
		r[i]=v
	return r
	
def repr_dill_load(obj):
	'''	不用考虑文件问题，以后要统一 序列化系列函数,
	但是这个函数序列化后是字符串，不能 autoArgs 是否是file参数
'''
	
def repr_dill_dump(obj):
	'''#TODO not dill basic type :  number,bytes,str,  ... (all ast.literal_eval) 
	'''
	
	return
	
def basic_dump(obj):
	return py.repr(obj)

def basic_load(sobj):
	T=py.importT()
	return T.unrepr(sobj)
	
def deSerialize(obj=None,file=None):
	'''The protocol version of the pickle is detected automatically, so no
protocol argument is needed.  Bytes past the pickled object's
representation are ignored.
'''
	if not py.isbyte(obj) and not file:raise py.ArgumentError('need bytes or file=str ')
	import pickle
	if py.istr(obj):
		file=obj
		obj=None
		U.log('autoArgs file=%s'%file)
	if py.isbyte(obj):
		return pickle.loads(obj)
	else:
		file=autoPath(file)
		with py.open(file,'rb') as f:
			return pickle.load(f)
ds=pickle_load=unSerialize=unserialize=deserialize=deSerialize
			
def serialize(obj,file=None,protocol=0):
	'''if not file: Return the pickled representation of the object as a bytes object.
	'''
	import pickle
	if file:
		file=autoPath(file)
		with py.open(file,'wb') as f:
			pickle.dump(obj=obj,file=f,protocol=protocol)
		return file
	else:
		return pickle.dumps(obj=obj,protocol=protocol)	
s=pickle_dump=serialize

def dill_load_file(file,dill_ext='.dill'):
	import dill
	dill.settings['ignore']=False #KeyError: 'ignore'
	
	file=auto_path(file,ext=dill_ext)
	try:
		with py.open(file,'rb') as f:
			return dill.load(f)
	except Exception as e:#TODO all  load save py.No
		return py.No(file,e)
dill_read=read_dill=dill_load=dill_load_file


def dill_load_bytes(bytes):
	import dill
	return dill.loads(bytes)
dill_loads=dill_load_byte=dill_load_bytes

def dill_dump_bytes(obj,file=None,protocol=None,dill_ext='.dill'):
	'''
	dill.dump(obj, file, protocol=None, byref=None, fmode=None, recurse=None)
	dill.dumps(obj, protocol=None, byref=None, fmode=None, recurse=None)

	ValueError: pickle protocol must be <= 4 
r=request.get ...
F.readableSize(len(F.dill_dump(protocol=None,obj=r)  ) )#'14.192 KiB'

F.readableSize(len(F.dill_dump(protocol=0,obj=r)  ) )   #'15.773 KiB'
F.readableSize(len(F.dill_dump(protocol=1,obj=r)  ) )   #'19.177 KiB'
F.readableSize(len(F.dill_dump(protocol=2,obj=r)  ) )   #'18.972 KiB'
F.readableSize(len(F.dill_dump(protocol=3,obj=r)  ) )   #'14.192 KiB'
F.readableSize(len(F.dill_dump(protocol=4,obj=r)  ) )   #'13.694 KiB'


	'''
	import dill
	if file:
		file=auto_path(file,ext=dill_ext)
		with py.open(file,'wb') as f:
			dill.dump(obj=obj,file=f,protocol=protocol)		
		return file
	else:
		return dill.dumps(obj=obj,protocol=protocol)
dill_write=write_dill=dill_dump=dill_dumps=dill_dump_bytes 

def dill_dump_string(obj,**ka):
	U=py.importU()
	encoding=U.get_duplicated_kargs(ka,'encoding','encode','coding')
	if not encoding:
		encoding=U.get_or_set('dill_string.encoding',default='latin')
	return dill_dump_bytes(obj).decode(encoding)	
dill_dump_str=dill_dump_string

def dill_load_string(s,**ka):
	U=py.importU()
	encoding=U.get_duplicated_kargs(ka,'encoding','encode','coding')
	if not encoding:
		encoding=U.get_or_set('dill_string.encoding',default='latin')
	return dill_load_bytes(s.encode(encoding) )
dill_load_str=dill_load_string

def load(file,):
	''' '''
	
def write(file,obj,):
	''' '''
	
		
def chmod777(file,mode=0o777,):
	import os
	os.chmod(file, mode) 
chmod=chmod777

def getMode(file):
	import os
	try:
		r= oct(os.stat(file).st_mode)
		if r[:5]!='0o100':raise Exception('不是100代表什么？',r)
		return r[-3:]
	except Exception as e:
		return py.No(e)
getmode=	getMode
	
def copy(src,dst):
	r''' src : sFilePath , list ,or \n strs
dst:sPath
	'''
	from shutil import copy as _copy
	if not py.istr(dst):raise py.ArgumentError('dst must be str')
	if py.istr(src):
		if '\n' in src:
			src=src.splitlines()
			return copy(src,dst)
		return _copy(src,dst)
	if py.iterable(src):
		fns=[]
		for i in src:
			fn=getName(i)
			if fn in fns:
				fn=T.fileName(i)
			fns.append(fn)
			_copy(i,getPath(dst)+fn)
		return fns
def modPathInSys(mod=None):
	if mod:
		if not py.istr(mod):mod=mod.__file__
	else:mod=__file__
	
	mod=mod.replace('\\','/')
	inPath=False
	if os.path.isabs(mod):
		for i in sys.path:
			i=i.replace('\\','/')
			if i and mod.startswith(i):
				if not i.endswith('/'):i+='/'
				i+='qgb'
				if mod.startswith(i):inPath=True
	else:
		raise NotImplementedError('__file__ not abs')
	return inPath
def lineCount(a):
	def blocks(files, size=65536):
		while True:
			b = files.read(size)
			if not b: break
			yield b

	with py.open(a, "r") as f:
		return sum(bl.count("\n") for bl in blocks(f))
		
def getPath(asp):
	asp=asp.replace('\\','/')
	if asp.endswith('/'):return asp
	else:
		if isDir(asp):return asp+'/'
		else:
			# _p.dirname('.../qgb/')# 'G:/QGB/babun/cygwin/lib/python2.7/qgb'
			# _p.dirname('.../qgb')# 'G:/QGB/babun/cygwin/lib/python2.7'
			return _p.dirname(asp)+'/'
def getPaths(a):
	r''' a:str 
	'''
	U=py.importU()
	if U.iswin():
		sp=a.replace('\\','/').split('/')
		rlist=[]
		def append(r):
			if r and r not in rlist:rlist.append(r)
		r=''
		for i,v in enumerate(sp):
			if len(v)>1 and v[-2] in T.AZ and v[-1]==':':
				append(r)
				r=v[-2:]+'/'
				continue

			for j in v:
				if j not in T.PATH_NAME:
					append(r)
					r=''
					continue

			if r and v:
				if isdir(r+v):r=r+v+'/'
				else:
					append(r)
					r=''
					continue
		return rlist
	else:
		raise NotImplementedError('*nux')
	
def get_filename_from_full_path(a):
	''' if a.endswith('/'):return ''
	'''
	a=a.replace('\\','/')
	if '/' not in a:return a
	else:
		# import T
		return T.subr(a,'/','')
get_name=getname=getName=getNameFromPath=getFilename=get_filename=get_filename_from_full_path
# filename=fileName=getname=getName=name
		
def getNameWithoutExt(a):
	''' see getNameFromPath
	'''
	
	a=getNameFromPath(a)
	if '.' in a:
		return T.subr(a,'','.')
	else:return a

def auto_find_file(head,ext='',r='Default auto accroding to the head'):
	'''r :recursion
	return str  
	# TODO # ext=?ext*     '''
	if not py.type(ext)==py.type(head)==py.str or head=='':
		return ''
	
	if len(ext)>0 and not ext.startswith('.'):ext='.'+ext
	head=head.lower();ext=ext.lower()
	head=head.replace('\\','/')
	if '/' in head:
		if py.type(r) is py.str:
			r=True
		else:
			r=False
	
	ap='.'
	if _p.isabs(head):
		ap=dir(head)
		if not isExist(ap):
			if head.endswith(ext):return head
			else:return head+ext
	
	# import F
	ls=[i.lower() for i in list(ap,r=r)]
	if head+ext in ls:return head+ext
	# import U
	# U.pprint(ls)
	for i in ls:		
		if i.startswith(head) and i.endswith(ext):return i
	
	for i in ls:
		if head in i and ext in i:return i
		
	# if inMuti(ext,'*?'):ext=ext.replace('*')
	
	if not head.endswith(ext):head+=ext
	
	return head
autof=auto_find_file
		
def new(a):
	'''will overwrite'''
	try:
		f=py.open(a,'w')
		f.write('')
		f.close()
		return f.name
	except Exception as e:
		setErr(e)
		return False
		
def isDir(ast):
	'''#TODO:
	
	'''	
	if not py.istr(ast):ast=py.str(ast)
	if not ast:return False
	ast=ast.replace('\\','/')
	if exist(ast):
		return _p.isdir(ast)
	else:
		if ast.endswith('/'):return True
		else:                return False
isPath=isdir=isDir
	# if not ast.replace('.','').strip():return True # （不是 点和空格 返回 T） 
	# return ('/' in ast) or ('\\' in ast)
	# return _p.sep in ast
# def is	
def bin(a,split=''):
	'''
bin(number, /)
F.bin(1.0)=='0b00111111100000000000000000000000'  # （大端）
'''
	import struct
	if py.isint(a):
		return py.bin(a)
	r='0b'
	if py.isfloat(a):
		r=r+split.join(py.bin(i).replace('0b', '').rjust(8, '0') for i in struct.pack('!f', a))
	elif py.isbytes(a):
		r=r+split.join(py.bin(i).replace('0b', '').rjust(8, '0') for i in a)
	else:
		raise py.ArgumentUnsupported('#TODO type',a)
	return r
def intToBytes(a):
	T=py.importU().T
	a=T.intToStr(a)
	return hexToBytes(a)
i2b=intToBytes

def bytesToHex(a,split=''):
	'''如果 len(split)是奇数，肯定返回 （奇数+偶数）=奇数
						偶=》偶
	'''
	if py.is3():
		# ord=lambda b:py.int.from_bytes(b,'big')
		ord=lambda i:i
	else:
		ord=py.ord
	r=split.join( [DIH[ord(i)] for i in a] )
	return r
b2h=bytesToHex
	
def hexToBytes(a,split='',ignoreNonHex=True):
	a=a.upper();r=b''
	if ignoreNonHex:a=''.join([i for i in a if i in '0123456789ABCDEF'])
	it=2
	if len(split)>0:it+=len(split)
	if it==2 and len(a) % it!=0:return ()
	if it>2:
		a=a.split(split)
		if len(a[-1]) == 0:a=a[:-1]
		for i in a:
			r+=py.byte(DHI[ i ])
		return r
		
	for i in range(py.int(py.len(a)/2 )):
		r+=py.byte(DHI[a[i*2:i*2+2]])
	return r
h2b=hexToBytes


def writeIterable(file,data,end='\n',overwrite=True,encoding=None):
	U=py.importU()
	if not encoding:encoding=U.encoding
	
	file=autoPath(file)
	if overwrite:new(file)
	
	if py.is2():f=py.open(file,'a')
	else:       f=py.open(file,'a',encoding=encoding)
	
	for i in data:
		f.write(py.str(i)+end)
	f.close()
	return f.name

def write(file,data,mod='w',encoding='',mkdir=False,autoArgs=True,pretty=True):
	'''py3  open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
	   py2  open(name[, mode[, buffering]])
pretty=True        Format a Python object into a pretty-printed representation.
	'''
	U=py.importU()
	try:
		if autoArgs:
			if py.istr(data) and py.len(file)>py.len(data)>0:
				if '.' in data and '.' not in file   and  isFileName(data):
					file,data=data,file
					U.warring('F.write fn,data but seems data,fn auto corrected（v 纠正')
	except:pass
	
	# try:
	file=autoPath(file)
	if not encoding:encoding=U.encoding
	
	if mkdir:makeDirs(file,isFile=True)
	
	if 'b' not in mod and isinstance(data,py.bytes):mod+='b'# 自动检测 data与 mod 是否匹配
	
	if 'b' not in mod:
		mod+='b'
	f=py.open(file,mod)
		#f.write(强制unicode) 本来只适用 py.is3() ，但 py2 中 有 from io import open
	# with open(file,mod) as f:
	if py.isbyte(data):#istr(data) or (py.is3() and py.isinstance(data,py.bytes) )	:
		f.write(data)
	elif (py.is2() and py.isinstance(data,py.unicode)) or (py.is3() and py.istr(data)):
		f.write(data.encode(encoding))
	else:
		# if py.is2():print >>f,data
		# else:
		if pretty:
			data=U.pformat(data)
		U.pln(data,file=f)
	f.close()
	return f.name
	# except Exception as e:
		# setErr(e)
		# return False
gb_write_auto_filename_len=True
def write_auto_filename(*a,**ka):
	all_args=py.importU().getArgsDict()
	return all_args
	U=py.importU()
	T=py.importT()
	sp=mkdir(U.gst+write_auto_filename.__name__)
	rf=[]
	for k,v in  all_args.items():
		fn='{}{}'.format(sp,T.filename_legalized(k))
		if gb_write_auto_filename_len:
			len=U.len(v)
			if py.isint(len):
				fn+='={}'.format(len)
		f=write(fn ,v,autoArgs=False)
		rf.append(f)
	return rf
writeA=write_auto_args=write_args=write_auto_filename


def append(file,data):
	'''builtin afile.write() No breakLine'''
	write(file,data,mod='a')
	
def detect_file_encoding(file,confidence=0.7,default=py.No('not have default encoding'),buffer_size=9999,p=True):
	if py.istr(file):
		with py.open(file,'rb') as f:
			b=f.read(buffer_size)
	elif py.isfile(file):
		if 'b' not in file.mode:raise py.ArgumentError("'b' not in file.mode",file)
		i=file.tell()
		b=file.read(buffer_size)
		file.seek(i)
		
	else:raise py.ArgumentError('need str or file')

	c= T.detect(b,confidence=confidence,default=default)
	if p:print(file,c) #TODO U.get_or_set('detect_file_encoding.p',True)
	return c
detect=detectEncoding=detect_encoding=detect_file_encoding
	
def read(file,encoding='',mod='r',return_filename=False,print_detect_encoding=True,**ka):
	'''if return_filename:
			return content,f.name
			'''
	file=autoPath(file)
	if not encoding and print_detect_encoding:
		U=py.importU()
		_pde=U.get_duplicated_kargs(ka,'p_encoding','p','pde','pEncoding','p_decode')
		if _pde!=U.GET_DUPLICATED_KARGS_DEFAULT:
			print_detect_encoding=_pde
	if not return_filename:
		U=py.importU()
		return_filename=U.get_duplicated_kargs(ka,'returnFile','rf','rfn','return_file','return_name',)
		
	if py.is2():f=py.open(file,mod)
	else:#is3
		encoding=encoding or detectEncoding(file,confidence=0.9,default='utf-8',p=print_detect_encoding)
		#utf-8 /site-packages/astropy/coordinates/builtin_frames/__init__.py  {'confidence': 0.73, 'encoding': 'Windows-1252'
		f=py.open(file,mod,encoding=encoding)
	s=f.read()
	f.close()
	if return_filename:
		return s,f.name
	else:
		return s
	# except Exception as e:
		# return f,e
		# if 'f' in py.dir() and f:f.close()
		# return ()
def read_bytes(file,size=-1,):
	'''is2 rb return str
f.read(size=-1, /)
Read and return up to n bytes.
	
	'''
	file=autoPath(file)
	try:
		with py.open(file,'rb') as f:
			return f.read(size)
	except Exception as e:
		return py.No(e,file)
readb=readByte=readBytes=read_byte=read_bytes	


def read_bytes_chunks(path,start=0,size = 8192):
	'''try this func
except : StopIteration((PermissionError(13, 'Permission denied'), 'D:/',8192)
	'''
	path=auto_file_path(path)
	try:
		with open(path, 'rb') as fd:
			yield fd.read(0) # 让错误提前暴露。不会造成 500 Internal Server error
			fd.seek(start)
			while 1:
				buf = fd.read(size)
				if buf:
					yield buf
				else:
					break
	except Exception as e:
		# py.importU().print_tb_stack(path,size,e)
		return (e,path,size)          #               
		# return py.No(e,path,size)                         
		# raise StopIteration(e)
rbc=read_bytes_stream=read_as_stream=read_file_chunks=readBytesChunks=read_bytes_chunks
			
def read_json(file,encoding=None):
	''' '''
	import json
	file=autoPath(file)
	if not encoding:encoding=detectEncoding(file)
	with py.open(file,encoding=encoding) as f:
		return json.load(f)
readjson=readJSON=json_load=read_json

def write_json(file,obj):
	import json
	with py.open(file,'w') as f: #not bytes,json write str
		json.dump(obj=obj,fp=f)
	return file

writeJSON=json_dump=write_json

def read_csv(file,encoding=None):
	file=autoPath(file)
	if not encoding:encoding=detectEncoding(file)
	import pandas as pd
	df = pd.read_csv(file, delimiter=',',encoding=encoding)
	r=[]
	is1=False
	if py.len(df.columns)==1:is1=True
	for i in df.values:
		if is1:
			r.append(i[0])
		else:
			r.append(tuple(i))
	return r
	# or export it as a list of dicts
	# dicts = df.to_dict().values()
readCSV=read_csv

def read_qpsu_file(file,prefix='file/'):
	U=py.importU()
	# 'E:/QGB/babun/cygwin/bin/qgb/'
	return read(U.getModPath()+prefix+file)
qpsufile=qpsuFile=readqp=readqpsu=readQPSU=read_qpsu=read_qpsu_file

def write_xlsx(file,a):
	import openpyxl
	file=autoPath(file)
	if file.lower().endswith('.xls'):file=file[:-4]+'.xlsx'
	if not file.lower().endswith('.xlsx'):file=file+'.xlsx'
	
	outwb = openpyxl.Workbook()  # 打开一个将写的文件
	sheet = outwb.create_sheet(index=0)  # 在将写的文件创建sheet
	for i, row in py.enumerate(a):
		for j, col in py.enumerate(row):
			sheet.cell(row=i+1, column=j+1).value=col
			# i,j=i+1,j+1 #我知道原因了，这是因为i+1 只应该每行执行一次，把它提到col循环外就行了
			# try:
				# sheet.cell(row=i, column=j).value=col #这样出现错误表格格式 ，原因？
			# except Exception as e:
				# return e,sheet,i,j,col
	outwb.save(file)  # 一定要记得保存
	return file
	
def write_xls(file,a):
	'''ValueError: row index was 65536, not allowed by .xls format'''
	import xlwt
	file=autoPath(file,ext='xls')
	
	xldoc = xlwt.Workbook()
	sheet = xldoc.add_sheet("Sheet1", cell_overwrite_ok=True)
	for i, row in py.enumerate(a):
		for j, col in py.enumerate(row):
			sheet.write(i, j, col)
	xldoc.save(file)
	return file
	
def read_xls(file,sheetIndex=0):
	''' return [ [colValue...]  .. ]  #No type description
	'''
	import xlrd                         
	w=xlrd.open_workbook(file)           
	sh=w.sheets()[sheetIndex]
	return sh._cell_values
	
def read_xls_sheets_name(file):
	import xlrd                         
	w=xlrd.open_workbook(file)           
	return py.list(py.enumerate( w.sheet_names() )  )
get_xls_sheets_name=read_xls_sheets_name
	
def read_sqlite(file,table='',sql="SELECT * FROM {};"):
	file=autoPath(file)
	if table:sql=sql.format(table)
	import sqlite3
	with sqlite3.connect(file) as con:
		cursor = con.cursor()
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
		#[('sessions',), ('sqlite_sequence',), ('history',), ('output_history',)]
		tables=[i[0] for i in cursor.fetchall()]
		if table:
			if not (table in tables):return py.No('no table',table,'found in',file)
			cursor.execute(sql )
			return cursor.fetchall()
		else:
			r={}
			for i in tables:
				r[i]=read_sqlite(file=file,table=i)
			return r
readSqlite=read_sqlite

def readYaml(file):
	import yaml
	with py.open(file) as f:
		return yaml.safe_load(f)

def writeYaml(file,obj):
	import yaml
	try:
		with py.open(file,'w') as f:
			yaml.dump(obj,f,default_flow_style=False)#default_flow_style=False parameter is necessary to produce the format you want (flow style), otherwise for nested collections it produces block style:
			return file
	except Exception as e:
		return py.No(e,file,obj)
		
def isDir(file):
	return _p.isdir(file)
is_folder=isFolder=is_dir=isdir=isDir
	
def exist(fn,zero=False):
	''': path.exist('c:')
Out[57]: False

In [58]: path.exist('o:')#这是因为当前目录下存在 'o:'，但是只能用ls完整查看
Out[58]: True
## 在cygwin中 只能判断 c:\ 或 c:/ ,单独 c: 总为False
#############
>>> path.exists('c:')
True
>>> path.exists('o:')
True
'''
	if not fn:return fn
	U=py.importU()
	if U.iscyg():
		if len(fn)==2 and fn[-1]==':':fn+='/'
		# raise NotImplementedError
	if _p.exists(fn):
		if _p.isdir(fn):return True
		if _p.getsize(fn)<1 and not zero:
			return False
		return True
	else:
		return False
isExist=exists=exist

def glob(path, pattern='**/*'):
	'''pattern='**/*'   : all files
	'**/*.txt'   : all txt files'''
	import pathlib
	return py.list(pathlib.Path('./').glob(pattern))

def walk(ap):
	'''
return tuple(ap,dir_list,file_list )
	2&3 : os.walk(top, topdown=True, onerror=None, followlinks=False)
	'''
	if py.is2():
		return _os.walk(ap).next()
	else:
		return _os.walk(ap).__next__()
		
def list(ap='.',type='',t='',r=False,d=False,dir=False,f=False,file=False):
	'''Parms:bool r recursion
			 str (type,t) '(d,f,a,r)'
	default return all'''
	U=py.importU()
	if dir:d=True
	if file:f=True
	if t and not type:type=t
	
	if 'd' in type:d=True
	if 'f' in type:f=True
	if 'a' in type:d=True;f=True
	if 'r' in type:r=True
	
	if d or dir or f or file:pass
	else:d=f=True		#default return all
	
	if not py.istr(ap) or py.len(ap)<1:
		setErr('F.list arguments ap error')
		ap='.'
	# if len(ap)==2 and ap.endswith(':'):ap+='/'	
	ap=ap.replace('\\','/')
	if not ap.endswith('/'):#U.inMuti(ap,'/','\\',f=str.endswith):
		if isDir(ap):
			ap+='/'
		else:
			return [abs(ap)]
		# if not ap.endswith('/'):ap+='/'
		# else:ap+='\\'
	
	# U.repl()
	########## below r is result
	rls=[]
	try:r3=py.list(walk(ap))
	except Exception as ew:
		# pln ap;raise ew
		return py.No(ew)
	
	if ap=='./':ap=''
	# U.repl()
	r3[1]=[ap+i+'/' for i in r3[1]] #dirs
	r3[2]=[ap+i for i in r3[2]] #files
	
	
	if d:rls.extend(r3[1])
 
	# 
	if r:
		for i in r3[1]:rls.extend(list(i,r=r,d=d,f=f))
			
	if f:rls.extend(r3[2])
	
	return rls
	# else:return r3[1]+r3[2]
ls=list

def ll(ap='.',readable=True,type='',t='',r=False,d=False,dir=False,f=False,file=False,return_dict=True,**ka):
	'''return {file : [size,atime,mtime,ctime,st_mode]}
	readable is True: Size,Stime,..
	linux struct stat: http://pubs.opengroup.org/onlinepubs/009695399/basedefs/sys/stat.h.html'''
	dr={}
	
	for i in list(ap,type=type,t=t,r=r,d=d,dir=dir,f=f,file=file):#ls 肯定返回 list类型！
		# importU;if U.DEBUG:U.pln ap,repr(i)
		try:
			s=_os.stat(i)
		except:
			continue
		if readable:
			U=py.importU()
			IntSize,FloatTime,IntOct=U.IntSize,U.FloatTime,U.IntOct
			dr[i]=[ IntSize(size(i)),
					FloatTime(s.st_atime),
					FloatTime(s.st_mtime),
					FloatTime(s.st_ctime),
					IntOct (s.st_mode ),
				]
		else:
			dr[i]=[size(i),s.st_atime,s.st_mtime,s.st_ctime,s.st_mode]
	if return_dict:
		return dr
	else:
		return [[k,*v] for k,v in dr.items()]

SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
			1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}
def numToSize(size, b1024=True):
	'''Convert a file size to human-readable form.
	Keyword arguments:
	size -- file size in bytes
	b1024 -- if True (default), use multiples of 1024
	if False, use multiples of 1000
	Returns: string
	test git
	'''
	U,T,N,F=py.importUTNF()	
	if py.istr(size) or py.isbyte(size):
		size=U.len(size)
	size=py.int(size)
	if size <= 0:
		return size
		# raise ValueError('number must be non-negative')

	multiple = 1024.0 if b1024 else 1000.0 #another if statement style
	
	if size<=multiple:return py.str(size)+' B'
	
	for suffix in SUFFIXES[multiple]:
		size /= multiple
		if size < multiple:
			return '{0:.3f} {1}'.format(size, suffix)
	raise ValueError('number too large')
ssize=readable_size=readableSize=numToSize

def size(asf,int=py.No('ipython auto readable')): 
	'''file or path return byte count
	not exist return -1'''
	asf=nt_path(asf)#if linux etc ,will auto ignored
	# asf=autoPath(asf)#in there,can't use gst
	size =0 #0L  SyntaxError in 3
	if not _p.exists(asf):
		return py.No('{} NOT EXISTS!'.format(asf))
	if not _p.isdir(asf):
		size= _p.getsize(asf)
		if size<=0:
			try:size=len(read(asf))
			except Exception as e:
				return py.No('unexcept err',e,asf)
		# return size
	else:# is dir
		for root, dirs, files in _os.walk(asf):  
			size += sum([_p.getsize(_p.join(root, name)) for name in files])  	
	U=py.importU()
	# U.msgbox(U.is_ipy_cell())
	if not int :#and U.is_ipy_cell():
		size=U.IntSize(size)
	return size 
	
# U.pln size(U.gst)
# exit()
	
def csvAsList(fn):
	import csv
	with py.open(fn, 'rb') as f:
		reader = csv.reader(f)
		return py.list(reader)

def getSourcePath():
	f=_sys._getframe().f_back
	def back(af,ai=0):
		if af is None:return ''
		if '__file__' in af.f_globals:return af.f_globals['__file__']
		else:return back(af.f_back,ai+1)
		
	return back(f)
	
	# U.pln globals().keys()
	# U.pln __file__, __name__ , __package__
	
def deleteFile(file):
	file=autoPath(file)
	sp=getSplitor(file)
	# for i in a.split(ap):
	U=py.importU()
	def Error():
		#Error()  返回None时   
		#TypeError: catching classes that do not inherit from BaseException is not allowed
		return FileNotFoundError
		#issubclass(FileNotFoundError,WindowsError) == True
		if U.iswin():	return WindowsError 
	
	try:
		if isDir(file):
			import shutil
			shutil.rmtree(file, ignore_errors=True)#这里不发出 异常 
			return file	
		_os.remove(file)#异常 是从这里产生的
		return file
	except FileNotFoundError as e:
		if isDir(file):
			raise Exception('#TODO')
		return py.No(file,e,'Not exists?')
	#Error  {'G:\\test\\npp': WindowsError(5, '')}
	# Docstring: MS-Windows OS system call failed.  
	#*nix NameError: name 'WindowsError' is not defined  '''
	except Exception as e:
		# setErr({file:e})
		return py.No(file,e)
	return False
rm=delete=deleteFile
	
def getSplitor(ap):
	if '/' in ap:return '/'
	if '\\' in ap:return '\\'		
	return '/'#default	
getsp=getSp=getSplitor		
		
def join_path(a,*p):
	'''os.path.join(a, *p)
Docstring:
Join two or more pathname components, inserting '/' as needed.
If any component is an absolute path, all previous path components
will be discarded.  An empty last part will result in a path that
ends with a separator.
File:      /root/anaconda3/lib/python3.7/posixpath.py
'''
	import os
	return os.path.join(a, *p)
join=joinPath=path_join=join_path

def mdcd(ap):
	return py.importU().cd(makeDirs(ap))

def move(source,target):
	F=py.importF()
	source=F.autoPath(source)
	target=F.autoPath(target)
	if target.endswith('/'):
		n=F.getName(source)
		target+=n
	import os
	try:
		os.rename(source, target)
		if not target.endswith('/') and F.isDir(target):
			target=target+'/'
		return target
	except (FileNotFoundError,FileExistsError) as e: # parentheses required, otherwise invalid syntax
		return py.No(e,source,target)

	# if not F.exist(target):
	# 	return py.No('moved to '+ target+' ,But not exist',source)
	# import shutil
	# shutil.move(source, target)
	# os.replace(source, target)
mv=move

def makeDirs(ap,isFile=False,cd=0):
	ap=autoPath(ap)
	if not py.isbool(isFile) and not py.isint(isFile):
		py.importU().log('F.md(str,isFile={})'.format(repr(isFile)))
	if py.is3():
		from pathlib import Path
		p=Path(ap)
		
		if isFile:
			return makeDirs(p.parent,isFile=False)
		if p.is_file():#if not exists, is_dir() is_file() both return False
			return py.No(ap+' exists , and it is a file')
		r=py.No('unexpected err')
		try:
			p.mkdir()
		except (FileNotFoundError,):
			r=makeDirs(p.parent,isFile=False)
			if r:p.mkdir() # 建立父目录后，再次尝试创建本目录 
			# else:return r
			#但是如果父目录本来是个文件，再mkdir则FileNotFoundError: [WinError 3] 系统找不到指定的路径。
		except FileExistsError:
			pass
		except Exception as e:
			r=e
		if p.exists():
			sp=autoPath(p)
			if p.is_dir() and not sp.endswith('/'):
				sp+='/'
			r=sp
		else:
			r=py.No(r,p)
		if r and cd:py.importU().cd(r)
		return r

	# if py.is2():		#########################################	
	U=py.importU()
	sp=getSplitor(ap)
	ap=ap.split(sp)
	if isFile:ap=ap[:-1]
	# if not isabs(ap):
		# if not ap.startswith('.'):
			# if ap.startswith(sp):ap=U.gst[:-1]+ap
			# else:ap=U.gst+ap
	# else:
	base=''
	
	for i in ap:
		base+=(i+sp)
		#TODO 2019-1-19  未处理存在的是文件  而不是 文件夹的情况
		if exist(base):continue
		else:
			try:
				_os.mkdir(base)
			
			except Exception as e:
				if U.iswin():
					if e.winerror==5:continue#WindowsError(5, '') 拒绝访问
					if e.winerror==183:continue#WindowsError 183 当文件已存在时，无法创建该文件。
				if 'exists' in e.args[1]:#(17, 'File exists') cygwin;
					continue
				# U.repl(printCount=True)
				setErr(e)
				return False
	return True	
	
	# if U.iswin():
		
		# _os.system('md "{0}"'.format(ap))
md=mkdir=makeDirs		

gbAutoPath=True
def autoPath(fn,ext='',default='',dir=False):
	''' default is U.gst 
if fn.startswith("."): 如果路径中所有文件夹存在，则可以写入读取。否则无法写入读取。file io 都是这个规则吧
FileNotFoundError: [Errno 2] No such file or directory: '.

	'''
	U=py.importU()
	if not gbAutoPath:return fn
	if default:
		default=default.replace('\\','/')
		if not default.endswith('/'):default+='/'
	else:
		default=U.set_test_path(U.gst) # 防止 U.gst 被改变没被保存
	fn=str(fn)
	fn=fn.replace('\\','/')
	if ext and not ext.startswith('.'):ext='.'+ext
	if not fn.lower().endswith(ext.lower()):fn+=ext
	if fn.startswith("~/"):
		import os
		if U.isnix():
			home=os.getenv('HOME')
		else:
			home=os.getenv('USERPROFILE')# 'C:/Users/Administrator'  not  cyg home os.getenv('HOME')
		# else:		home=os.getenv('HOMEPATH')#  HOMEPATH=\Users\Administrator
		fn= home+fn[1:];

	#TODO to avoid dos max_path ,  must \ full path 2019年12月19日 不记得什么意思？ 
	if (not fn.startswith(".")) and (not isAbs(fn)) :
		while fn.startswith('/'):fn=fn[1:]
		fn= default + fn
	
	if py.len(fn)>=260 and U.iswin():
		fn=nt_path(fn)
	if(dir and not fn.endswith('/')):fn+='/'
	return fn
autofn=auto_filename=autoFileName=auto_file_path=auto_path=autoPath


def get_nt_short_path_name(long_name):
	import win32api
	if py.len(long_name)<250:return long_name
	if not long_name.startswith( u"\\\\?\\"):
		long_name=u"\\\\?\\"+long_name
	return win32api.GetShortPathName(long_name)
shortPath=short_path=get_win_short_path=win_short_path=get_windows_short_path=windows_short_path=nt_short_path=get_short_path=GetShortPath=GetShortPathName=get_nt_short_path_name

def nt_path(fn):
	'''if linux etc ,will auto ignored
write success, read failed ?	
	'''
	U=py.importU()
	fn=_p.abspath(fn)
	if  U.iswin():#or cyg?
		if not py.isunicode(fn):fn=fn.decode(U.T.detect(fn))#暂时没想到更好方法，头晕
		fn=fn.replace(u'/',u'\\')
		if u"\\\\?\\" in fn:
			pass
		elif fn.startswith(u"\\\\"):
			fn=u"\\\\?\\UNC\\" + fn[2:]
		else:
			fn=u"\\\\?\\" + fn    
	return fn
	
def abs(file):
	'''In [165]: gs ###notice Users/Admin
Out[165]: '\\\\?\\C:\\Users/Administrator\\.gradle\\caches\\3.3\\scripts-remappe
d\\sync_local_repo10406_a5s4kku7mncoj5pzsbgck2y4v\\6oxfw7eb7mpz692y3xnywccj1\\in
it1efd45104ffa2d33563b85b9edda76e3\\classes\\sync_local_repo10406_a5s4kku7mncoj5
pzsbgck2y4v$_run_closure1$_closure2$_closure4$_closure5.class'

In [166]: F._p.abspath gs
--------> F._p.abspath(gs)
Out[166]: '\\\\?\\C:\\Users\\Administrator\\.gradle\\caches\\3.3\\scripts-remapp
ed\\sync_local_repo10406_a5s4kku7mncoj5pzsbgck2y4v\\6oxfw7eb7mpz692y3xnywccj1\\i
nit1efd45104ffa2d33563b85b9edda76e3\\classes\\sync_local_repo10406_a5s4kku7mncoj
5pzsbgck2y4v$_run_closure1$_closure2$_closure4$_closure5.class'''
	return _p.abspath(file).replace('\\','/')
		
def isAbs(file):
	'''in cygwin:
In [43]: U.path.isabs( 'M:/Program Files/.babun/cygwin/lib/python2.7/qgb/file/attr.html')
Out[43]: False

In [45]: U.path	.isabs('M:\\Program Files\\.babun\\cygwin\\lib\\python2.7\\qgb\\file\\attr.html' )
Out[45]: False
##### win py3.6    fixed
--------> F.isabs('2d:\1\2')# False
--------> F.isabs('d:\1\2')# False
--------> F.isabs('/babun/cygwin/lib/python2.7\\qgb\\F.py')# True
#TODO 更加精细判断，文件名不合法 return None?
'''	
	U=py.importU()
	if U.iscyg() or U.iswin():
		if ':' in file:return True
		else:return False
	return _p.isabs(file)
isabs=isAbs
		
def name(a):
	'''Anti abs
	得到 单独文件（夹）名字
	'''
	U=py.importU()
	if not U.T.istr(a):return ''
	if U.inMuti(a,'/','\\',f=str.endswith):a=a[:-1]
	if not isAbs(a):return a
	else:
		
		a=T.sub(a,dir(a))
		# U.repl()
		if U.inMuti(a,'/','\\',f=str.startswith):return a[1:]
		else:return a
		
def dir(a):
	#TODO a 为文件夹 应该直接返回
	return _p.dirname(a)
	# exit()

# def open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
	'''py2 from io import open
----> 1 open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)

TypeError: open() takes at most 7 arguments (8 given)
	TypeError: 'opener' is an invalid keyword argument for this function
	
'''


def readlines(a,EOL=True,encoding=None):
	a=autoPath(a)
	if not encoding:
		encoding=detectEncoding(a)
	r=[]
	try:
		if EOL:
			for i in py.open(a,encoding=encoding):r.append(i)
			return r
		else:
			return read(a,encoding=encoding).splitlines()
	except Exception as e:
		return py.No(e)
# F.isFileName('g:/a')
# []
def isFileName(a):
	'''a:str'''
	# from . import U #ValueError: Attempted relative import in non-package
	U=py.importU()
	for i in a:
		if i not in T.PATH_NAME:return py.No(i,a)
		
	return a
	

DIH=DINT_HEX=INT_HEX={0:'00',1:'01',2:'02',3:'03',4:'04',5:'05',6:'06',7:'07',8:'08',9:'09',10:'0A',11:'0B',12:'0C',13:'0D',14:'0E',15:'0F',16:'10',17:'11',18:'12',19:'13',20:'14',21:'15',22:'16',23:'17',24:'18',25:'19',26:'1A',27:'1B',28:'1C',29:'1D',30:'1E',31:'1F',32:'20',33:'21',34:'22',35:'23',36:'24',37:'25',38:'26',39:'27',40:'28',41:'29',42:'2A',43:'2B',44:'2C',45:'2D',46:'2E',47:'2F',48:'30',49:'31',50:'32',51:'33',52:'34',53:'35',54:'36',55:'37',56:'38',57:'39',58:'3A',59:'3B',60:'3C',61:'3D',62:'3E',63:'3F',64:'40',65:'41',66:'42',67:'43',68:'44',69:'45',70:'46',71:'47',72:'48',73:'49',74:'4A',75:'4B',76:'4C',77:'4D',78:'4E',79:'4F',80:'50',81:'51',82:'52',83:'53',84:'54',85:'55',86:'56',87:'57',88:'58',89:'59',90:'5A',91:'5B',92:'5C',93:'5D',94:'5E',95:'5F',96:'60',97:'61',98:'62',99:'63',100:'64',101:'65',102:'66',103:'67',104:'68',105:'69',106:'6A',107:'6B',108:'6C',109:'6D',110:'6E',111:'6F',112:'70',113:'71',114:'72',115:'73',116:'74',117:'75',118:'76',119:'77',120:'78',121:'79',122:'7A',123:'7B',124:'7C',125:'7D',126:'7E',127:'7F',128:'80',129:'81',130:'82',131:'83',132:'84',133:'85',134:'86',135:'87',136:'88',137:'89',138:'8A',139:'8B',140:'8C',141:'8D',142:'8E',143:'8F',144:'90',145:'91',146:'92',147:'93',148:'94',149:'95',150:'96',151:'97',152:'98',153:'99',154:'9A',155:'9B',156:'9C',157:'9D',158:'9E',159:'9F',160:'A0',161:'A1',162:'A2',163:'A3',164:'A4',165:'A5',166:'A6',167:'A7',168:'A8',169:'A9',170:'AA',171:'AB',172:'AC',173:'AD',174:'AE',175:'AF',176:'B0',177:'B1',178:'B2',179:'B3',180:'B4',181:'B5',182:'B6',183:'B7',184:'B8',185:'B9',186:'BA',187:'BB',188:'BC',189:'BD',190:'BE',191:'BF',192:'C0',193:'C1',194:'C2',195:'C3',196:'C4',197:'C5',198:'C6',199:'C7',200:'C8',201:'C9',202:'CA',203:'CB',204:'CC',205:'CD',206:'CE',207:'CF',208:'D0',209:'D1',210:'D2',211:'D3',212:'D4',213:'D5',214:'D6',215:'D7',216:'D8',217:'D9',218:'DA',219:'DB',220:'DC',221:'DD',222:'DE',223:'DF',224:'E0',225:'E1',226:'E2',227:'E3',228:'E4',229:'E5',230:'E6',231:'E7',232:'E8',233:'E9',234:'EA',235:'EB',236:'EC',237:'ED',238:'EE',239:'EF',240:'F0',241:'F1',242:'F2',243:'F3',244:'F4',245:'F5',246:'F6',247:'F7',248:'F8',249:'F9',250:'FA',251:'FB',252:'FC',253:'FD',254:'FE',255:'FF'}
DHI=DHEX_INT=HEX_INT={y:x for x,y in DIH.items()}




if __name__=='__main__':
	import T,U
	# l=csvAsList('process.csv')
	# U.shtml(l)
	# U.pln getSourcePath()
	# U.repl()
	exit()	
	r=hexToBytes(T.HEX.lower())
	# U.write('h.r',r)
	