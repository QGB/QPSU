#coding=utf-8
# try:
	# import U
	# U.tab()
# except:pass
__all__=['U','T','N','F']

# import sys
# for i in __all__:
	# if i in sys.modules:
		# sys.modules['_'+i]=sys.modules.pop(i)
	# try:exec('import '+i)
	# except Exception as ei:
		# if 'gError' in dir():gError.append(ei)
		# else:gError=[ei]
		# __all__.remove(i)

try:
	try:from . import py
	except:import py
	U=py.importU()
	if U.isipy():
		__all__.append('ipy')
		# import ipy
		# ipy.gipy.autocall=2# 放到 qgb.ipy中
		# ipy.gi.setModule()
		# U.replaceModule('ipy',ipy.gi,package='qgb',backup=False)
		# ipy=ipy.gi#少了这个，ipy在sys.modules 中虽然已经替换，但是实际使用却还是原来module ，？
		# ipy.startRecord()
		# M:\Program Files\.babun\cygwin\home\qgb\.ipython\profile_default\history.sqlite
	if U.iswin() or (py.is2() and U.iscyg() ):
		__all__.append('Win')
	# U.pln( __all__	
except Exception as e:
	if 'gError' in dir():gError.append(e)
	else:gError=[e]

# U.pln( __name__
# sys.argv==['-c']
# U.repl()
# if __name__=='__main__': #此句在 python -m qgb中不会执行，始终为'qgb',  why? #TODO #TOKNOW
	
# U.pln( __all__
# try:
	# f=sys._getframe()
	# while f and f.f_globals and 'get_ipython' not in f.f_globals.keys():
		# f=f.f_back
	# ipy=f.f_globals['get_ipython']()
	# ipy.autocall=2
# except Exception as e:
	# pass
	# U.pln( e
