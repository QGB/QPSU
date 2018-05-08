#coding=utf-8
import sys,os
if __name__=='__main__':import U,T,F,py
else:from . import U,T,F,py#from .   Attempted relative import in non-package
gError=None
# U.pln U.gError
g=get=gipy=U.isipy()#不能直接引用U.ipy,环境不确定 动态判断避免识别错误
if not gipy:raise EnvironmentError
gipy.autocall=2
gIn=gipy.user_ns['In'];gOut=gipy.user_ns['Out']

# gipy.editor=U.npp()
def sycn():
	''' '''
	
def run(file):
	file=F.autof(file,ext='py')
	return g.magic(u'run -i '+file)

def input(fliter='',lenMin=-1,lenMax=U.IMAX):
	r=[i for i in  enumerate(gIn) if fliter in i[1]]
	return [i for i in  r if lenMin<=len(i[1])<=lenMax]
	
def outType(t=None):
	'''t is type to flit'''
	if t !=None:
		if type(t) is U.instance:
			t=t.__class__
		if type(t) is U.classType:#没有考虑 取出Class 类型的情况
			def m(a):return isinstance(a,t)
		else:
			if not isinstance(t,type):
				t=type(t)
			def m(a):return type(a) is t
	r={}
	for i in gOut:
		if t !=None:
			if not m(gOut[i]):continue
		r[i]=type(gOut[i]),U.len(gOut[i])
		
	return r
outype=outType

def outlen(min=-1,max='infinity',start=0,stop=U.IMAX,end=U.IMAX):
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

# U.cdt()
gsavePath=U.gst+'ipy/'

# U.cd('ipy')
# U.pln U.pwd()

date=U.getDate()
gshead='#coding=utf-8'
gspath=U.getModPath(qgb=False,endSlash=False)
gsTryExcept=u'''try:{1}
except Exception as _e{0}:U.pln {0},_e{0}'''
#用print >>输出会自动换行,format 的参数应该与文本标记一致，
#否则出现IndexError: tuple index out of range
gdTimeName={}
gIgnoreIn=[ u'from qgb import *',u'ipy.',u'get_ipython()']

def save(file=None,lines=-1,tryExcept=False,out=False,columns=70,overide=True):
	'''file is str or (mod a)
	在没有ipython实例时，不能get_ipython()
	当file被指定时，overide 参数无效'''
	try:
		if type(lines) in(int,long) and lines>0:
			lsta,lend=0,lines
		elif len(lines)==2:lsta,lend=lines
		else:raise Exception
	except:
		lsta,lend=0,gIn.__len__()
	if file:#当指定file 名时，总是 overide
		if T.istr(file):
			if not file.lower().endswith('.py'):
				file+='.py'
			F.new(file)
			file=open(file,'a')
		elif type(file) is py.file:
			if file.mode!='a':return False
			pass
		else:
			raise Exception('invalid argument file')
	else:
		if gdTimeName and overide:
			file=gdTimeName[gdTimeName.keys()[-1]]
			file=open(file,'w')
			# last=-1
			# for t in gdTimeName:
				# if t>last:file,last=name,d
			# last=gdTimeName.values()
			# last.sort()#从小到大排序,ACS正序, DESC倒序  Ascending and Descending 
			# file=[n for n,d in gdTimeName.items() if d==last[-1]][0]
		else:
			file='{0}{1}.py'.format(gsavePath,U.stime())
			file=open(file,'a')
	U.pln(gshead,file=file)
	U.pln(U.main(display=False),file=file  )
	# print >>file,'import sys;sys.path.append('{0}');from qgb import *'.format(gspath)
	#using single quote for cmd line
	#-4 为了去除 /qgb
	#ipython --InteractiveShellApp.exec_lines=['%qp%'] 不会改变In[0],始终为''?
	for i,v in enumerate(gIn):
		if i==0:continue
		if i in gOut.keys():
			v=u'_{0}={1}'.format(i,v)
			if out:
				U.pln('"""#{0}'.format(i),file=file )
				U.pln(gOut[i],file=file )
				U.pln('"""',file=file )
		if U.isSyntaxError(v) or U.multin(gIgnoreIn,v):
		# or u'from qgb import *' in v or sum(map(lambda a:v.startswith(a),gIgnoreStart) ):
			v=u'#'+v		
				
		if tryExcept:
			v='#########################\n\t'+v
			U.pln(gsTryExcept.format(i,v).encode('utf-8'),file=file )
		else:
			U.pln(v.encode('utf-8'),' '*(columns-len(v.splitlines()[-1])),'#',i,file=file )
		# if i in [14]:import pdb;pdb.set_trace()#U.repl()	
	# gipy.magic(u'save save.py 0-115')
	# U.pln(gIn
	# U.pln(gOut.keys()
	
	gdTimeName[U.time()]=file.name
	return '{0} {1} success!'.format(save.name,file.name)
save.name='{0}.{1}'.format(__name__,save.__name__)
F.md(gsavePath)
U.pln(gsavePath)

def reset():
	gipy.execution_count=0


def ipyStart(*a):
	import IPython
	IPython.start_IPython()
def ipyOutLast(i=None):
	'''废弃不用  desperated绝望  @deprecated不建议
	use _  ,  __ ,  ___ 
	ORZ'''
	# f=sys._getframe()
	# while f and f.f_globals and 'get_ipython' not in f.f_globals.keys():
		# f=f.f_back
	# Out=f.f_globals['Out']
	Out=gOut
	# globals()['gipy']=5
	
	def length():return len(Out)

	ipyOutLast.size=ipyOutLast.len=ipyOutLast.__len__=length
	# U.pln( ipyOutLast.size
	if i is None:
		if Out:
			# p("Out.keys ")
			im=len(Out.keys())
			if im<10:return Out.keys()
			elif 9<im<21:return [(k,ct(Out)) for k in Out.keys()] 
			else:
				# repl()
				r=[[]]
				for i,k in py.enumerate(Out):#index ,key
					# U.pln( i
					r[-1].append((k,i))
					if i%5==0:
						r.append([])
				return r
		else:
			U.pln( "##### IPy No Out #####")
			return
	
	if Out:
		try:
			return Out[i]
		except:return Out[Out.keys()[i]]
	return Out
	
	
#
############以下暂时未用
#
def recorder():
	while True:
		try:
			save(overide=True)
			U.sleep(9)
		except Exception as e:
			if U.gbPrintErr:U.pln(e)
			global gError
			gError=e
	from copy import deepcopy
	F.md(date);U.cd(date)
	fi=None;li=[]
	def new():
		U.pln(globals().keys()) 
		U.pln( '*'*66)
		U.pln( dir(recorder))
		U.pln( recorder.__dict__)	
		fi=open(U.stime()+'.In','a')
		li=[]
		# U.pln( fi
	def write():
		F.new(fi.name)
		U.pln(li,file=fi)
	new()
	while True:
		U.pln(fi) 
		if len(gi)>len(li):
			li=deepcopy(gi)
			write()
		else:
			if li!=gi:
				fi.close()
				new()
			else:pass#Not Change
			
		U.sleep(9)#second
		
		
gt=None#thread
def startRecord():
	global gt
	gt=U.thread(target=recorder)
	gt.setName(save.name)
	gt.setDaemon(True)
#	setDaemon：主线程A启动了子线程B，调用b.setDaemaon(True)，则主线程结束时，会把子线程B也杀死，与C/C++中得默认效果是一样的。
	gt.start()
class IPy():
	def __init__(s,mod=None):
		pass
		# if not mod:
			# U.getMod(
			# s._module=mod
	def setModule(s,mod=None):
		import sys
		if not mod:
			if 'qgb.ipy' in sys.modules:
				mod=sys.modules['qgb.ipy']
				if mod:
					if type(mod)!=type(sys):mod=mod._module
					#如果是module 直接往下执行
	
		if type(mod)==type(sys):
			s._module=mod
			return True
		else:raise Exception('need module qgb.ipy')
	def __nonzero__(s):
		return True
		
	def __dir__(s):
		return ['_module']
	
	def __call__(s):
		return gipy
	# def __repr__(s):
		# return '444'
	def __getattribute__ (*a,**ka):
		U.pln('gab',a,ka) 
		return a[0]
	def __getattr__(s,*a,**ka):
		U.pln('ga',a,ka) 
		if a[0].startswith('__'):
			def ta(*at,**kat):return '%s %s %s'%(a[0],len(at),len(kat))
			return ta
		return a[0]
		# if a[0] in s.__dir__():return eval('{0}'.format(a[0]))
	def rewrite(*a,**ka):
		U.pln( 'rewrite',type(a[0]),a[1:],ka	)

# U.pln( repr(F.md),U.getMod('qgb.ipy')

gi=IPy()
# if U.getMod('qgb.ipy'):
	# U.replaceModule('ipy',gi,package='qgb',backup=False)


# U.msgbox()
# F.writeIterable('ipy/fwi.txt',sys.modules)

# U.repl()
# U.thread(target=recorder).start()
# U.pln( 233