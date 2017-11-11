# coding=utf-8
import __builtin__ as py
import os as _os;import sys as _sys;from os import path as _p
import T,U
gError=[]
def setErr(ae):
	global gError
	if U.gbLogErr:# U.
		if type(gError) is list:gError.append(ae)
		elif gError:gError=[gError,ae]
		else:gError=[ae]
	else:
		gError=ae
	if U.gbPrintErr:print '#Error ',ae# U.
	
def autof(head,ext=''):
	'''return str  
	# TODO # ext=?ext*     '''
	if not py.type(ext)==py.type(head)==py.str or head=='':
		return ''
	
	if len(ext)>0 and not ext.startswith('.'):ext='.'+ext
	head=head.lower();ext=ext.lower()
	
	ap='.'
	if _p.isabs(head):
		ap=dir(head)
		if not isExist(ap):
			if head.endswith(ext):return head
			else:return head+ext
	
	# import F
	ls=[i.lower() for i in list(ap)]
	if head+ext in ls:return head+ext
	
	for i in ls:		
		if i.startswith(head) and i.endswith(ext):return i
	
	for i in ls:
		if head in i and ext in i:return i
		
	# if inMuti(ext,'*?'):ext=ext.replace('*')
	
	if not head.endswith(ext):head+=ext
	
	return head
autoFileName=autof
		
def new(a):
	'''will overwrite'''
	try:
		f=open(a,'w')
		f.write('')
		f.close()
		return f.name
	except Exception as e:
		setErr(e)
		return False
def isPath(ast):
	if type(ast) not in (str,unicode):ast=py.str(ast)
	if not ast:return None
	if not ast.replace('.','').strip():return True
	return ('/' in ast) or ('\\' in ast)
	# return _p.sep in ast

def bytesToHex(a,split=''):
	r=''
	for i in a:
		r+=DIH[ord(i)]+split
	return r
b2h=bytesToHex
	
def hexToBytes(a,split=''):
	it=2
	if len(split)>0:it+=len(split)
	if it==2 and len(a) % it!=0:return None
	
	a=a.upper();r=''
	
	if it>2:
		a=a.split(split)
		if len(a[-1]) == 0:a=a[:-1]
		for i in a:
			r+=chr(DHI[ i ])
		return r
		
	for i in xrange(len(a)/2):
		r+=chr(DHI[a[i*2:i*2+2]])
	return r
h2b=hexToBytes

def writeIterable(a,data,end='\n',overwrite=True):
	if overwrite:new(a)	
	f=open(a,'a')
	for i in data:
		f.write(py.str(i)+end)

def write(a,data,mod='wb',mkdir=False,autoArgs=True):
	try:
		if autoArgs:
			if py.len(a)>py.len(data)>0:
				a,data=data,a
				U.warring('write fn,data')
	except:pass		
	
	try:
		a=autoPath(a)
		if mkdir:makeDirs(a,isFile=True)
		
		with open(a,mod) as f:
			if type(data) is py.str:
				f.write(data)
			elif type(data) is py.unicode:
				f.write(data.encode(U.encoding))
			else:
				print >>f,data
			return True
	except Exception as e:
		setErr(e)
		return False

def append(a,data):
	'''builtin afile.write() No breakLine'''
	write(a,data,mod='a')
	
def read(a,mod='r'):
	try:
		f=open(autoPath(a),mod)
		s=f.read()
		f.close()
		return s
	except:
		if 'f' in py.dir() and f:f.close()
		return None
	
def isdir(a):
	return _p.isdir(a)
	
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
def list(ap='.',type='',t='',r=False,d=False,dir=False,f=False,file=False):
	'''Parms:boll r recursion
			 str (type,t) '(d,f,a,r)'
	default return all'''
	# print ap
	if dir:d=True
	if file:f=True
	if t and not type:type=t
	
	if 'd' in type:d=True
	if 'f' in type:f=True
	if 'a' in type:d=True;f=True
	if 'r' in type:r=True
	
	if d or dir or f or file:pass
	else:d=f=True		#default return all
	
	if py.type(ap)!=py.type('') or py.len(ap)<1:
		setErr('F.list arguments ap error')
		ap='.'
	# if len(ap)==2 and ap.endswith(':'):ap+='/'	
	if not U.inMuti(ap,'/','\\',f=str.endswith):ap+='/'
	
	# print ap
	# U.repl()
	########## below r is result
	rls=[]
	try:r3=py.list(_os.walk(ap).next())
	except Exception as ew:
		# print ap;raise ew
		return []
	
	if ap=='./':ap=''
	# U.repl()
	r3[1]=[ap+i for i in r3[1]]
	r3[2]=[ap+i for i in r3[2]]
	
	
	if d:rls.extend(r3[1])
 
	# 
	if r:
		for i in r3[1]:rls.extend(list(i,r=r,d=d,f=f))
			
	if f:rls.extend(r3[2])
	
	return rls
	# else:return r3[1]+r3[2]
ls=list

def ll(ap='.',readable=True,type='',t='',r=False,d=False,dir=False,f=False,file=False):
	'''return {file : [size,atime,mtime,ctime,st_mode]}
	readable is True: Size,Stime,..
	linux struct stat: http://pubs.opengroup.org/onlinepubs/009695399/basedefs/sys/stat.h.html'''
	dr={}
	for i in list(ap,type=type,t=t,r=r,d=d,dir=dir,f=f,file=file):
		s=_os.stat(i)
		dr[i]=[size(i),s.st_atime,s.st_mtime,s.st_ctime,s.st_mode]
		if readable:
			# import U
			for j in py.range(len(dr[i])):
				# print i,j,repr(dr[i][j])
				if py.type(dr[i][j]) is py.float:dr[i][j]=U.stime(time=dr[i][j])
				if py.type(dr[i][j]) is py.long:dr[i][j]=readableSize(dr[i][j])
	return dr

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
	if size < 0:
		return size
		# raise ValueError('number must be non-negative')

	multiple = 1024.0 if b1024 else 1000.0 #another if statement style
	for suffix in SUFFIXES[multiple]:
		size /= multiple
		if size < multiple:
			return '{0:.3f} {1}'.format(size, suffix)
	raise ValueError('number too large')
readableSize=numToSize
def size(asf): 
	'''file or path return byte count
	not exist return -1'''
	size = 0L
	if not _p.exists(asf):
		return -1L
	if not _p.isdir(asf):
		size= _p.getsize(asf)
		if size<=0:
			try:size=len(read(asf))
			except:return -1L
		return size
	for root, dirs, files in _os.walk(asf):  
		size += sum([_p.getsize(_p.join(root, name)) for name in files])  	
	return size 
	
# print size(U.gst)
# exit()
	
def csvAsList(fn):
	import csv
	with open(fn, 'rb') as f:
		reader = csv.reader(f)
		return py.list(reader)
		
def getSourcePath():
	f=_sys._getframe().f_back
	def back(af,ai=0):
		if af is None:return ''
		if '__file__' in af.f_globals:return af.f_globals['__file__']
		else:return back(af.f_back,ai+1)
		
	return back(f)
	
	# print globals().keys()
	# print __file__, __name__ , __package__
	
def delFile(a):
	a=autoPath(a)
	sp=getSplitor(a)
	# for i in a.split(ap):
	try:
		_os.remove(a)
		return True
	except Exception as e:
		setErr({a:e})
		return False
	
rm=delFile
	
def getSplitor(ap):
	if '/' in ap:return '/'
	if '\\' in ap:return '\\'		
	return '/'#default	
getsp=getSp=getSplitor		
		
		
def makeDirs(ap,isFile=False):
	ap=autoPath(ap)
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
				if U.gbPrintErr:print e
				return False
	return True	
	
	# if U.iswin():
		
		# _os.system('md "{0}"'.format(ap))
md=mkdir=makeDirs		

gbAutoPath=True
def autoPath(fn):
	if not gbAutoPath:return fn
	fn=str(fn)
	if (fn.startswith(".")):
		return fn;
	
	if isAbs(fn):
		return fn;
	else:
		if _p.exists(fn):return abs(fn)
		return (U.gst + fn);
def abs(a):
	return _p.abspath(a)
		
def isAbs(a):
	'''in cygwin:
In [42]: _28
Out[42]: 'M:/Program Files/.babun/cygwin/lib/python2.7/qgb/file/attr.html'

In [43]: U.path.isabs(_28)
Out[43]: False

In [44]: a
Out[44]: 'M:\\Program Files\\.babun\\cygwin\\lib\\python2.7\\qgb\\file\\attr.html'

In [45]: U.path	.isabs(a)
Out[45]: False
'''	
	if U.iscyg():
		if ':' in a:return True
	return _p.isabs(a)
isabs=isAbs
		
def name(a):
	'''Anti abs'''
	if type(a) not in (str,unicode):return ''
	if U.inMuti(a,'/','\\',f=str.endswith):a=a[:-1]
	if not isAbs(a):return a
	else:
		
		a=T.sub(a,dir(a))
		# U.repl()
		if U.inMuti(a,'/','\\',f=str.startswith):return a[1:]
		else:return a
		
def dir(a):
	return _p.dirname(a)
	# exit()
	
# dir('d:/test/t.py')	


DIH=DINT_HEX=INT_HEX={0:'00',1:'01',2:'02',3:'03',4:'04',5:'05',6:'06',7:'07',8:'08',9:'09',10:'0A',11:'0B',12:'0C',13:'0D',14:'0E',15:'0F',16:'10',17:'11',18:'12',19:'13',20:'14',21:'15',22:'16',23:'17',24:'18',25:'19',26:'1A',27:'1B',28:'1C',29:'1D',30:'1E',31:'1F',32:'20',33:'21',34:'22',35:'23',36:'24',37:'25',38:'26',39:'27',40:'28',41:'29',42:'2A',43:'2B',44:'2C',45:'2D',46:'2E',47:'2F',48:'30',49:'31',50:'32',51:'33',52:'34',53:'35',54:'36',55:'37',56:'38',57:'39',58:'3A',59:'3B',60:'3C',61:'3D',62:'3E',63:'3F',64:'40',65:'41',66:'42',67:'43',68:'44',69:'45',70:'46',71:'47',72:'48',73:'49',74:'4A',75:'4B',76:'4C',77:'4D',78:'4E',79:'4F',80:'50',81:'51',82:'52',83:'53',84:'54',85:'55',86:'56',87:'57',88:'58',89:'59',90:'5A',91:'5B',92:'5C',93:'5D',94:'5E',95:'5F',96:'60',97:'61',98:'62',99:'63',100:'64',101:'65',102:'66',103:'67',104:'68',105:'69',106:'6A',107:'6B',108:'6C',109:'6D',110:'6E',111:'6F',112:'70',113:'71',114:'72',115:'73',116:'74',117:'75',118:'76',119:'77',120:'78',121:'79',122:'7A',123:'7B',124:'7C',125:'7D',126:'7E',127:'7F',128:'80',129:'81',130:'82',131:'83',132:'84',133:'85',134:'86',135:'87',136:'88',137:'89',138:'8A',139:'8B',140:'8C',141:'8D',142:'8E',143:'8F',144:'90',145:'91',146:'92',147:'93',148:'94',149:'95',150:'96',151:'97',152:'98',153:'99',154:'9A',155:'9B',156:'9C',157:'9D',158:'9E',159:'9F',160:'A0',161:'A1',162:'A2',163:'A3',164:'A4',165:'A5',166:'A6',167:'A7',168:'A8',169:'A9',170:'AA',171:'AB',172:'AC',173:'AD',174:'AE',175:'AF',176:'B0',177:'B1',178:'B2',179:'B3',180:'B4',181:'B5',182:'B6',183:'B7',184:'B8',185:'B9',186:'BA',187:'BB',188:'BC',189:'BD',190:'BE',191:'BF',192:'C0',193:'C1',194:'C2',195:'C3',196:'C4',197:'C5',198:'C6',199:'C7',200:'C8',201:'C9',202:'CA',203:'CB',204:'CC',205:'CD',206:'CE',207:'CF',208:'D0',209:'D1',210:'D2',211:'D3',212:'D4',213:'D5',214:'D6',215:'D7',216:'D8',217:'D9',218:'DA',219:'DB',220:'DC',221:'DD',222:'DE',223:'DF',224:'E0',225:'E1',226:'E2',227:'E3',228:'E4',229:'E5',230:'E6',231:'E7',232:'E8',233:'E9',234:'EA',235:'EB',236:'EC',237:'ED',238:'EE',239:'EF',240:'F0',241:'F1',242:'F2',243:'F3',244:'F4',245:'F5',246:'F6',247:'F7',248:'F8',249:'F9',250:'FA',251:'FB',252:'FC',253:'FD',254:'FE',255:'FF'}
DHI=DHEX_INT=HEX_INT={y:x for x,y in DIH.iteritems()}

def readlines(a):
	r=[]
	for i in py.open(autoPath(a)):r.append(i)
	return r




if __name__=='__main__':
	# import T,U
	print U.pwd()
	
	print exist('M:\\Program Files\\Notepad++\\notepad++.exe')
	# l=csvAsList('process.csv')
	# U.shtml(l)
	# print getSourcePath()
	U.repl()
	exit()	
	r=hexToBytes(T.HEX.lower())
	# U.write('h.r',r)
	print bytesToHex(r)	
