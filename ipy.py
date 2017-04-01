
#coding=utf-8
import sys,os,U,T,F
# print U.gError
g=get=gipy=U.isipy()#不能直接引用U.ipy,环境不确定 动态判断避免识别错误
if not gipy:raise EnvironmentError
gIn=gipy.user_ns['In'];gOut=gipy.user_ns['Out']
gt=None#thread

def outType():
	r={}
	for i in gOut:
		r[i]=type(gOut[i])
	return r
outype=outType

def outlen():
	r={}
	for i in gOut:
		r[i]=U.len(gOut[i])
	return r

# U.cdt()
gsavePath=U.gst+'ipy/'

# U.cd('ipy')
# print U.pwd()

date=U.getDate()
gshead='#coding=utf-8'
gsTryExcept=u'''try:{1}
except Exception as _e{0}:print {0},_e{0}'''
#用print >>输出会自动换行,format 的参数应该与文本标记一致，
#否则出现IndexError: tuple index out of range
gdTimeName={}
def save(file=None,lines=-1,tryExcept=False,Out=False,minSpace=70,overide=True):
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
	if file:
		if type(file) in (unicode,str):
			file=open(file,'a')
		elif type(file) is __builtin__.file:
			if file.mode!='a':return False
			pass
		else:
			raise Exception('invalid argument file')
	else:
		if gdTimeName and overide:
			file=gdTimeName[gdTimeName.keys()[-1]]
			# last=-1
			# for t in gdTimeName:
				# if t>last:file,last=name,d
			# last=gdTimeName.values()
			# last.sort()#从小到大排序,ACS正序, DESC倒序  Ascending and Descending 
			# file=[n for n,d in gdTimeName.items() if d==last[-1]][0]
		else:
			file='{0}{1}.py'.format(gsavePath,U.stime())
		file=open(file,'a')
	print >>file,gshead
	print >>file,'import sys;sys.path.append("{0}")'.format(U.getModPath(qgb=False,endSlash=False))
	#-4 为了去除 /qgb
	#ipython --InteractiveShellApp.exec_lines=['%qp%'] 不会改变In[0],始终为''?
	for i,v in enumerate(gIn):
		if i==0:continue
		if U.isSyntaxError(v):
			v=u'#'+v
		if i in gOut.keys():
			v=u'_{0}={1}'.format(i,v)
			if Out:
				print >>file,'"""#{0}'.format(i)
				print >>file,gOut[i]
				print >>file,'"""'
		if tryExcept:
			v='#########################\n\t'+v
			print >>file,gsTryExcept.format(i,v).encode('utf-8')
		else:
			print >>file,v.encode('utf-8'),' '*(minSpace-len(v)),'#',i
			
	# gipy.magic(u'save save.py 0-115')
	# print >>file,gIn
	# print >>file,gOut.keys()
	
	gdTimeName[U.time()]=file.name
	return '{0} {1} success!'.format(save.name,file.name)
save.name='{0}.{1}'.format(__name__,save.__name__)
F.md(gsavePath)
print gsavePath

def reset():
	gipy.execution_count=0


gError=None
def recorder():
	while True:
		try:
			save(overide=True)
			U.sleep(9)
		except Exception as e:
			if U.printError:print e
			global gError
			gError=e
	from copy import deepcopy
	F.md(date);U.cd(date)
	fi=None;li=[]
	def new():
		print globals().keys()
		print '*'*66
		print dir(recorder)
		print recorder.__dict__	
		fi=open(U.stime()+'.In','a')
		li=[]
		# print fi
	def write():
		F.new(fi.name)
		print >>fi,li
	new()
	while True:
		print fi
		if len(gi)>len(li):
			li=deepcopy(gi)
			write()
		else:
			if li!=gi:
				fi.close()
				new()
			else:pass#Not Change
			
		U.sleep(9)#second
def startRecord():
	global gt
	gt=U.thread(target=recorder)
	gt.setName(save.name)
	gt.setDaemon(True)
#	setDaemon：主线程A启动了子线程B，调用b.setDaemaon(True)，则主线程结束时，会把子线程B也杀死，与C/C++中得默认效果是一样的。
	gt.start()
#
############以下暂时未用
#
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
		print 'gab',a,ka
		return a[0]
	def __getattr__(s,*a,**ka):
		print 'ga',a,ka
		if a[0].startswith('__'):
			def ta(*at,**kat):return '%s %s %s'%(a[0],len(at),len(kat))
			return ta
		return a[0]
		# if a[0] in s.__dir__():return eval('{0}'.format(a[0]))
	def rewrite(*a,**ka):
		print 'rewrite',type(a[0]),a[1:],ka	

# print repr(F.md),U.getMod('qgb.ipy')

gi=IPy()
# if U.getMod('qgb.ipy'):
	# U.replaceModule('ipy',gi,package='qgb',backup=False)


# U.msgbox()
# F.writeIterable('ipy/fwi.txt',sys.modules)

# U.repl()
# U.thread(target=recorder).start()
# print 233