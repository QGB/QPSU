# Importing a dynamically generated module

def importCode(code,name,addToSys=True,sys=True,sysModule=True):
	"""
	Import dynamically generated code as a module. code is the
	object containing the code (a string, a file handle or an
	actual compiled code object, same types as accepted by an
	exec statement). The name is the name to give to the module,
	and the final argument says wheter to add it to sys.modules
	or not. If it is added, a subsequent import statement using
	name will return this module. If it is not added to sys.modules
	import will try to load it in the normal fashion.
	
	import foo

	is equivalent to

	foofile = open("/path/to/foo.py")
	foo = importCode(foofile,"foo",1)

	Returns a newly generated module.
	"""
	import sys,imp

	module = imp.new_module(name)

	try:
		exec code in module.__dict__
	except Exception as e:
		print e,233
		exit()
	if addToSys and sys and sysModule:
		sys.modules[name] = module

	return module

# Example
code = \
"""
def testFunc():
	print "spam!"

class testClass:
	def testMethod(self):
		print "eggs!"
def
"""

m = importCode(code,"test")
m.testFunc()
m.testClass().testMethod()
