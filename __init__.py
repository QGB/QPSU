
# try:
	# import U
	# U.tab()
# except:pass


__all__=['U','T','N','F']


# for i in F.list('./'):
	# print i
import sys
for i in __all__:
	if i in sys.modules:
		sys.modules['_'+i]=sys.modules.pop(i)
	try:exec('import '+i)
	except:__all__.remove(i)
	
# print __all__
try:
	f=sys._getframe()
	while f and f.f_globals and 'get_ipython' not in f.f_globals.keys():
		f=f.f_back
	ipy=f.f_globals['get_ipython']()
	ipy.autocall=2
except Exception as e:print e
