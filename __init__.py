
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
	except:__all__.remove(i)


try:
	if U.isipy():
		__all__.append('ipy')
		U.ipy.autocall=2
		import ipy
		# ipy.startRecord()
		# M:\Program Files\.babun\cygwin\home\qgb\.ipython\profile_default\history.sqlite
	if U.iswin() or U.iscyg():
		__all__.append('Win')
	# print __all__	
except Exception as e:
	gError=e
	pass

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
