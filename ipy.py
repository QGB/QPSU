#coding=utf-8
import sys,os,IPython
if __name__.endswith('qgb.ipy'):from . import py#from .   Attempted relative import in non-package
else:import py
U,T,N,F=py.importUTNF()
gError=None
# U.pln U.gError
def main():
	'''不行，还是出现 sqlite3 缺少，
只能在bat里设置PATH启动
'''	
	ps=['',
 'Library\\mingw-w64\\bin',
 'Library\\usr\\bin',
 'Library\\bin',
 'Scripts',
 'lib\\site-packages\\numpy\\.libs']
 
	if U.iswin() and sys.executable.startswith(r'\\') and 'Anaconda3' in sys.executable:
		prefix=sys.executable[:sys.executable.index('Anaconda3')+9+1]
		print(U.set_env_path(append=[prefix+i for i in ps]))	
		
		from _ctypes import LoadLibrary as _dlopen
		h=_dlopen(r'\\192.168.1.3\c\QGB\Anaconda3\DLLs\_sqlite3.pyd',0)
		import sqlite3
		print(h,sqlite3)
	IPython.start_ipython()
	
if __name__ == '__main__':main()	


if not U.isipy():raise EnvironmentError
g=get=gipy=U.isipy()#不能直接引用U.ipy,环境不确定 动态判断避免识别错误 g.
if IPython.version_info[0]>=8 and IPython.version_info[1]>=27:
	gipy.autocall=1
else:	
	gipy.autocall=2

try:
    if gipy.history_load_length<2000:# 2025年12月27日 
        print('gipy.history_load_length :',gipy.history_load_length )
        gipy.history_load_length=99999
        
except:pass
   
if U.isWin():
	try:
		gipy.editor='cmd /k start "" %s' % U.npp(get_cmd=True)
	except Exception as e:
		print(e)
	try:
		from IPython.utils import py3compat # python 3.7
	except:pass
	try:
		from IPython.utils.process import py3compat # python 3.5
	except:pass
	py3compat.DEFAULT_ENCODING='gb18030' # default utf-8
if U.isLinux():
	vim=U.where('vim')
	if vim:
		gipy.editor=vim
	else:
		gipy.editor=U.where('vi')

In=gIn=gipy.user_ns['In'];Out=gOut=gipy.user_ns['Out']
# version='.'.join([str(i) for i in IPython.version_info if py.isnum(i)])  #(5, 1, 0, '') 5.1.0
version=py.float('{0}.{1}{2}\n{3}'.format(*IPython.version_info).splitlines()[0])
try:
	import asyncio
	gMainThread_async_event_loop=U.get_or_set('asyncio.get_event_loop()',lazy_default=lambda:asyncio.get_event_loop(),)
except:pass	
# gipy.editor=U.npp()

def get_var(name):
	return gipy.user_ns.get(name,py.No('not found',name))

gd_undo_save_In=U.get_or_set('ipy.undo_save_In',{})
def undo_save(*indexs):
	if not indexs:
		for n,i in U.enumerate_reversed(In):
			if i and i.startswith('ipy.save('):
				index=n
				break
		#没找到 index 就不会被定义，自动抛出异常	#TODO 待改进，出错很突兀，有点搞不懂
		index=U.input('undo last ipy.save:',type=py.int,default=index)
		indexs=[index]
	r=[]
	for index in indexs:
		if gIn[index] and gIn[index].startswith('ipy.save('):
			gd_undo_save_In[index]=gIn[index]
			gIn[index]=''#py.No(gIn[index])
		if not index in gOut:raise py.ArgumentError('index not in Out')
		sf=gOut[index]
		if 'ipy.save' not in sf:raise py.ArgumentError('not ipy.save,But In[index] cleaned')
		
		f=U.get_obj_file_lineno(sf)[0]
		row=F.delete(f),gIn[index]
		r.append(row)
	if py.len(r)==1:
		return r[0]
	else:	
		return r
save_undo=undo_save
	
def jupyter_password(passphrase='',salt='0'*12,algorithm='sha1'):
	import hashlib
	from ipython_genutils.py3compat import cast_bytes,str_to_bytes
	if py.isbytes(salt):
		bsalt=salt
		salt=bsalt.decode('ascii')
	elif py.istr(salt):
		bsalt=str_to_bytes(salt, 'ascii')
	else:
		raise py.ArgumentError(salt)
	
	h=hashlib.new(algorithm)
	h.update(cast_bytes(passphrase, 'utf-8') + bsalt)

	return ':'.join((algorithm, salt, h.hexdigest()))
jpw=jupyter_passwd=jupyter_password
	
def set_autocall(level=2):
	gipy.autocall=level
	return level
	
def sycn():
	'''  #TODO  '''
# __frame=sys._getframe().f_back	

def format(obj,width=79,max_seq_length=py.No("auto get-set 'ipy.pformat.max_seq_length' ",no_raise=1)):
	'''
IPython.lib.pretty.pretty(
    obj,
    verbose=False,
    max_width=79,
    newline='\n',
    max_seq_length=1000,
)	
	
	
	
/IPython/core/formatters.py: format(obj, include=None, exclude=None)
Docstring:
Return a format data dict for an object.

By default all format types will be computed.

The following MIME types are usually implemented:

* text/plain
* text/html
* text/markdown
* text/latex
* application/json
* application/javascript
* application/pdf
* image/png
* image/jpeg
* image/svg+xml

Parameters
----------
obj : object
    The Python object whose format data will be computed.
include : list, tuple or set; optional
    A list of format type strings (MIME types) to include in the
    format data dict. If this is set *only* the format types included
    in this list will be computed.
exclude : list, tuple or set; optional
    A list of format type string (MIME types) to exclude in the format
	
C:\QGB\Anaconda3\lib\site-packages\IPython\core\formatters.py :89  '''
	import IPython.lib.pretty
	if not max_seq_length:
		max_seq_length=U.get_or_set('ipy.pformat.max_seq_length',2000)
	else:
		U.set('ipy.pformat.max_seq_length',max_seq_length)
	try:
		return IPython.lib.pretty.pretty(obj,max_width=width,max_seq_length=max_seq_length)
	except Exception as e:
		return py.repr(e)
	
	from IPython.core.interactiveshell import InteractiveShell
	r= InteractiveShell.instance().display_formatter.format(obj)
	if py.len(r)!=2 or py.len(r[1])!=0 or not py.isdict(r[0]):raise EnvironmentError()
	return U.get_dict_value(r[0])
pformat=format

def trace_variable(code):
	import _ast
	if py.istr(code):a=U.parse_code(code ) # one line return <_ast.Expr,_ast.For...,multi return [Assign,Expr,For..]
	if getattr(code,'value',0):a=code
	if isinstance(a,_ast.Expr):
		a=a.value
	if isinstance(a,_ast.Call):
		a.args
		a.keywords	
trace_code=trace_var=trace_variable

def get_sqlite_history(filter='',file='~/.ipython/profile_default/history.sqlite',limit=2000,offset=0,StrRepr=True,**ka):
	'''   CREATE TABLE history (session integer, line integer, source text, source_raw text, PRIMARY KEY (session, line))
	ipy console default output max len 500
rpc_server : 2000  ,2001 有省略号 ...
'''	
	limit=U.get_duplicated_kargs(ka,'limit','limits','limites','count','n','max',default=limit)
	file=F.expanduser(file)
	
	if filter:
		if not filter.upper().startswith('WHERE SOURCE LIKE '):
			filter=f"WHERE source LIKE '%{filter}%' "
	else:
		filter=''
	his=F.read_sqlite(file,sql=f'SELECT * FROM history {filter} ORDER BY session DESC,line DESC  limit {limit} offset {offset} ')
	
	if filter:return his
	# his=his['history'] 
#    (44, 614, 'U.unique(_)', 'U.unique _')  
# session,line,  autocall ,    raw_input
	if StrRepr:
		return [ U.StrRepr(i[2]) for i in his ]
	return [ i[2] for i in his ]
his=history=getIpyHistory=get_history=get_sqlite_history
	
def dill_load(filename,return_value=False,set_user_ns=True):
	# F=py.importF()
	if filename.lower()[-5:] not in ['.dill','ickle']:
		for f in F.ls(U.gst,f=1,d=0):
			if filename in f:
				filename=U.input('edit or ctrl+c using: ',default=f)
				break
	vars=[]
	dnv={}
	if U.all_in([',','='],filename):
		vars=T.regex_match_all(F.getNameWithoutExt(filename),T.RE_vars_separated_by_commas)[0].split(',')
	if vars:
		for n,v in py.enumerate(F.dill_load(filename,dill_ext='')):
			dnv[vars[n]]=v
	else:
		varname=''
		for c in F.getNameWithoutExt(filename):
			if c not in T.alphanumeric_:break
			varname+=c
		dnv[varname]=F.dill_load(filename,dill_ext='')
	if py.len(dnv)==1:	
		r=[py.list(dnv)[0],filename]
	else:
		r=[py.list(dnv),filename]
	U.pln(r)
	if set_user_ns:
		for name,v in dnv.items():
			gipy.user_ns[name]=v
	if return_value:
		return r
	return filename	
load=dill_load	
def dill_dump(*vars,len=True,dump_path=''):
	'''
pip install astor
	'''
	T=py.importT()
	import ast
	co=sys._getframe().f_back.f_code
	dvars={}
	for index_a,e in  enumerate(ast.walk(U.getAST(co) )  ):
		da={i:py.getattr(e,i) for i in dir(e) if not i.startswith('_') } 
		
		# if index==1:break
		if ('value' in da) and py.isinstance( e.value,ast.Call):
			#ipy.*dump*()
			if U.getattr_multi_name(e.value,'func','value','id')=='ipy' and \
				('dump' in U.getattr_multi_name(e.value,'func','attr').lower() ):
				# print(index_a, da,'\n================\n')
				# U.set(e.value.args)
				for i,var in py.enumerate(e.value.args):
					# if py.isinstance( var,(ast.Name,ast.Subscript) ):# var : Name(lineno=1, col_offset=12, id='In', ctx=Load()),
					dvars[U.ast_to_code(var,EOL=False) ]=vars[i]
	if py.len(vars)==1 and not len:
		return F.dill_dump(obj=vars[0],file=py.list(dvars)[0])
	r=[]
	for n,i in py.enumerate(dvars):
		il=U.len(dvars[i])
		if il:
			if py.len(dvars)> 1:il='%-2s:%s'%(n,il)
			if py.len(dvars)==1:il='%-4s'%(il)
		else:
			il='%-2s'%n
		r.append( [ i, il ] )
	if py.len(r)> 1:f='(%s) = {%s}'
	if py.len(r)==1:
		f='%s-%s'
		vars=vars[0]
	#第一次调用 UnboundLocalError: local variable 'f' referenced before assignment ? 再次 ipy.dump 正常？
	f=f % ( ','.join([i[0] for i in r]) ,','.join([i[1] for i in r]))
	f=f.replace('"""',"'")
	f=T.fileName(f)
	if dump_path:
		dump_path=F.auto_path(dump_path)
		if not dump_path.endswith('/'):
			# raise py.ArgumentError(dump_path)
			dump_path+='/'
		f=dump_path+f
	return F.dill_dump(obj=vars,file=f)
	
dump=dill_dump
	
def run(file):
	file=F.autof(file,ext='py')
	return gipy.magic(u'run -i '+file)

def input(fliter='',lenMin=-1,lenMax=U.IMAX):
	r=[i for i in  enumerate(gIn) if fliter in i[1]]
	return [i for i in  r if lenMin<=len(i[1])<=lenMax]
	
def outType(t=None,start=0,stop=U.IMAX,len=py.range(U.IMAX)):
	'''t is type to flit
	is3:range(start, stop[, step]) -> range object
	'''
	if t !=None:
		# if type(t) is U.instance: # 这个什么意思来着
			# t=t.__class__
		if py.istr(t):
			def m(a):return t in py.repr(a)
		elif type(t) is U.classType:#没有考虑 取出Class 类型的情况
			def m(a):return isinstance(a,t)
		else:
			if not isinstance(t,type):
				t=type(t)
			def m(a):return type(a) is t
	r={}
	for index,i in py.enumerate(gOut):
		if index<start or index>stop:continue
		if t !=None:
			if not m(gOut[i]):continue
		r[i]=type(gOut[i]),U.len(gOut[i]),U.sizeof(gOut[i])
		
	return r
outype=outType

def outLen(min=-1,max='infinity',start=0,stop=U.IMAX,end=U.IMAX):
	'''min<=out[i].len<=max
	'''
	if end!=U.IMAX:stop=end
	r={}
	for i,k in enumerate(gOut):
		if i<start or i>stop:continue
		n=U.len(gOut[k])
		if type(max) is str:
			pass
		else:
			if n>max:continue
		if n<min:continue
		r[k]=n
	return r
outlen=outLen

date=U.getDateStr()
gshead='#coding=utf-8'
gspath=U.getModPath(qgb=False,endSlash=False)
gsTryExcept=u'''try:{1}
except Exception as _e{0}:U.pln({0},_e{0})'''
#用print >>输出会自动换行,format 的参数应该与文本标记一致，
#否则出现IndexError: tuple index out of range
# gs_ipy_save_file_list_name=
gsavelist=gsave_dict=gsave_list=gdTimeName=U.get_or_set(__name__+'.save_file_list',{})
gIgnoreIn=[ u'from qgb import *',u'ipy.',u'get_ipython()']
# U.cdt()
gsavePath=U.get_or_set('ipy.save_path',U.gst+'ipy/')
# U.cd('ipy')
# U.pln U.pwd()
F.md(gsavePath)
gstitle='{pid} ipy:{1} py:{0} at[{2}] {3}'.format(
	U.getPyVersion(),version,U.stime(format='%Y-%m-%d %H:%M:%S'),gsavePath,pid=U.pid
	)
U.pln(gstitle)
if getattr(U,'Win',0):
	U.Win.setitle(gstitle)
#is2 py:2.713 ipy:5.1 at[2018-05-13 10:26:35.049] G:/test/ipy/   #len 57
#is3 py:3.63 ipy:6.1 at[2018-05-13 10:32:01.078] G:/test/ipy/    #56

def save(file=None,lines=-1,tryExcept=False,out=False,columns=70,overide=True,del_other=False,out_max=9999,In_index_delta=0,**ka):
	'''
U.set('ipy.save_path',U.gst+'ipy/')
	
file is str or (mod a)
	在没有ipython实例时，不能get_ipython()
	当file被指定时，overide 参数无效
#BUG #TODO
出现输入记录不同步的现象，应该添加一个报警
In [302]: _i265
Out[302]: '[i for i in sku if i[0] in [0.03, 0.04, 0.05, 0.06, 0.07, 0.18] ]'

In [303]: In[265]
Out[303]: 'page=pa=await tb.get_or_new_page(U.cbg(e=1))'
	
	
In_index_delta=1  # In[268]==_i269	  , Out[269]
	'''
	global gsavePath
	gsavePath=U.get('ipy.save_path')
	del_other=U.get_duplicated_kargs(ka,'delOther','delete','delattr',default=del_other)
	In_index_delta=U.get_duplicated_kargs(ka,'In_index_delta','in_index_delta','index_delta','in_delta','delta_in',default=In_index_delta)
	if ka:raise py.ArgumentError('没有处理这个ka，是不是多传了参数',ka)
	
	try:
		if py.isint(lines) and lines>0:
			# lsta,lend=0,lines 
			lsta,lend=lines,-1
		elif len(lines)==2:
			lsta,lend=lines
			if lsta and py.istr(lsta):
				for nls in py.range(py.len(gIn)-2,0-1,-1):
					if lsta in gIn[nls]:
						lsta=nls
						break
				else:# if break  else不会执行
					raise py.ArgumentError('lines index str not found in In',lsta)
			
			lsta=lsta if lsta>0 else 0
		else:raise Exception
	except:
		lsta,lend=0,gIn.__len__()
	if file:#当指定file 名时，总是 overide
		if T.istr(file):
			file=T.filename(file)[:255-3]# 如果用 pathname 不好处理 含有 /斜杠的问题
			if U.is_linux():
				while py.len(file.encode('utf-8'))> 255-3: # 256-3 too long !
					file=file[:-1]
			if U.iswin() and U.gst.startswith('\\'):
				while T.wcswidth(file) >= (255-3-4):
					file=file[:-1]
			file=F.autoPath(file,ext='.py',default=gsavePath)
#255-3(.py)  防止文件名过长 OSError: [Errno 22] Invalid argument: "\\\\?\	\C:\\test			
			F.new(file)
			if py.is2():file=open(file,'a')
			else:file=open(file,'a',encoding="utf8")
		elif py.isfile(file):
			if file.mode!='a':raise Exception('file mode should be "a" ')
		else:
			raise Exception('invalid argument file')
	else:
		if gdTimeName and overide:
			file=gdTimeName[py.list(gdTimeName.keys() )[-1]]#is3:TypeError: 'dict_keys' object does not support indexing
			file=F.autoPath(file,ext='.py',default=gsavePath)
			if py.is2():file=open(file,'w')
			else:file=open(file,'w',encoding="utf8")
			# last=-1
			# for t in gdTimeName:
				# if t>last:file,last=name,d
			# last=gdTimeName.values()
			# last.sort()#从小到大排序,ACS正序, DESC倒序  Ascending and Descending 
			# file=[n for n,d in gdTimeName.items() if d==last[-1]][0]
		else:
			file='{0}{1}.py'.format(gsavePath,U.stime())
			if py.is2():file=open(file,'a')
			else:file=open(file,'a',encoding="utf8")
	U.pln(gshead,file=file)
	#######  get exec_lines to gsqgb
	gsqgb=U.main(display=False)
#join(  <traitlets.config.loader.LazyConfigValue at 0x20066295400>  )  ###  TypeError: can only join an iterable
	gsexec_lines=U.getNestedValue(gipy.config,'InteractiveShellApp','exec_lines') #_class%20'traitlets.config.loader.LazyConfigValue'_.html
	if not py.iterable(gsexec_lines):
		gsexec_lines=[]
	gsexec_lines='	;'.join(gsexec_lines)
	if gsexec_lines:
		if not 'from qgb import' in gsexec_lines:
			gsqgb='{0}\n{1}'.format(gsqgb,gsexec_lines)
		else:gsqgb=gsexec_lines
	U.pln(gsqgb+'\n',file=file  )
	# print >>file,'import sys;sys.path.append('{0}');from qgb import *'.format(gspath)
	#using single quote for cmd line
	#-4 为了去除 /qgb
	#ipython --InteractiveShellApp.exec_lines=['%qp%'] 不会改变In[0],始终为''
	for i,v in enumerate(gIn[lsta:lend]):
		skip=False
		if i==0 and lsta==0:continue
		i=lsta+i+In_index_delta
		if not v:v=''
		v=v.strip()
			# U.isSyntaxError(u'_{0}={1}'.format(i,v) ) :
				# pass
		if i in gOut:
			if i==1 and py.istr(gOut[1]) and gOut[1].endswith(':/QGB/babun/cygwin/lib/python2.7/'):
				pass
			else:
				v=u'_{0}={1}'.format(i,v)
	
		if U.isSyntaxError(v) or U.multin(gIgnoreIn,v):
		# or u'from qgb import *' in v or sum(map(lambda a:v.startswith(a),gIgnoreStart) ):
			v=u'#'+v		
			skip=True
				
		if tryExcept and (not skip):
			v='#########################\n\t'+v
			if py.is2():v=gsTryExcept.format(i,v).encode('utf-8')
			else:v=gsTryExcept.format(i,v)
			U.p(v,file=file )
		else:
			if py.is2():v=v.encode('utf-8')
			else:pass
			if v:# IndexError: list index out of range
				U.p(v,' '*(columns-len(v.splitlines()[-1])),file=file )
			
		if out and (i in gOut) and (not skip):
			pout=pformat(gOut[i])
			if py.len(pout) > out_max:
				pout='#Warning#  len(pout)={} > out_max'.format(py.len(pout))
				print( '#ipy.save In[{}]{}# len(pout)={} > out_max'.format(i,gIn[i],py.len(pout)) )
			if '#' in v.splitlines()[-1].strip():
				out_head_char=T.eol
			else:out_head_char=';'
				
			U.pln(out_head_char+'"""#{0}'.format(i),file=file )
			# U.pln('"""',file=file )
			U.pln(pout.replace('"""','"qgb""'),file=file )
			U.pln('"""',file=file )	
		else:
			U.pln('#',i,file=file )
		# if i in [14]:import pdb;pdb.set_trace()#U.repl()	
	# gipy.magic(u'save save.py 0-115')
	# U.pln(gIn
	# U.pln(gOut.keys()
	file.close()
	gdTimeName[U.time()]=file.name
	
	
	if del_other:
		for t,f in gdTimeName.items():			
			if f == file.name:continue
			print('del:',U.stime(t),F.delete(f) or [f,False])
			
	return '{0} {1} success!'.format(save.name,file.name)
save.name='{0}.{1}'.format(__name__,save.__name__)

def reset_execution_count():
	gipy.execution_count=0

def ipyStart(*a):
	import IPython
	
	IPython.start_ipython()


def _seq_pprinter_factory(start, end, basetype):
	"""
	Factory that returns a pprint function useful for sequences.  Used by
	the default pprint for tuples, dicts, and lists.
	"""
	def inner(obj, p, cycle):
		typ = type(obj)
		if basetype is not None and typ is not basetype and typ.__repr__ != basetype.__repr__:
			# If the subclass provides its own repr, use it instead.
			return p.text(typ.__repr__(obj))

		if cycle:
			return p.text(start + '...' + end)
		step = len(start)
		p.begin_group(step, start)
		rows = columnize([repr(l) for l in obj], separator=", ",
						 displaywidth=p.max_width).split("\n")
		rows.remove('')
		for idx, x in p._enumerate(rows):
			if idx:
				p.breakable()
			p.text(x)
		if len(obj) == 1 and type(obj) is tuple:
			# Special case for 1-item tuples.
			p.text(',')
		p.end_group(step, end)

	return inner


def test(*a,**ka):
	co=sys._getframe().f_back.f_code
	return co
	
