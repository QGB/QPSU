#coding=utf-8
# try:
	# import U
	# U.tab()
# except:pass
__all__=['U','T','N','F']

import sys
for i in __all__:
	if i in sys.modules:
		sys.modules['_'+i]=sys.modules.pop(i)
	try:exec('import '+i)
	except Exception as ei:
		if 'gError' in dir():gError.append(ei)
		else:gError=[ei]
		__all__.remove(i)

try:
	if U.isipy():
		__all__.append('ipy')
		import ipy
		ipy.gipy.autocall=2
		# ipy.gi.setModule()
		# U.replaceModule('ipy',ipy.gi,package='qgb',backup=False)
		# ipy=ipy.gi#少了这个，ipy在sys.modules 中虽然已经替换，但是实际使用却还是原来module ，？
		# ipy.startRecord()
		# M:\Program Files\.babun\cygwin\home\qgb\.ipython\profile_default\history.sqlite
	if U.iswin() or U.iscyg():
		__all__.append('Win')
	# print __all__	
except Exception as e:
	if 'gError' in dir():gError.append(ei)
	else:gError=[ei]

# print __all__
# try:
	# f=sys._getframe()
	# while f and f.f_globals and 'get_ipython' not in f.f_globals.keys():
		# f=f.f_back
	# ipy=f.f_globals['get_ipython']()
	# ipy.autocall=2
# except Exception as e:
	# pass
	# print e
