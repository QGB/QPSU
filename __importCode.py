# Importing a dynamically generated module
print (23333333)
if __name__=='__main__':import py
else:from . import py

print(py)



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
		exec (code) in module.__dict__
	except Exception as e:
		U.pln( e,233)
		exit()
	if addToSys and sys and sysModule:
		sys.modules[name] = module

	return module

# Example
code = \
"""
def testFunc():
	U.pln( "spam!")

class testClass:
	def testMethod(self):
		U.pln( "eggs!")

"""

m = importCode(code,"test")
# m.testFunc()#is3 AttributeError: module 'test' has no attribute 'testFunc'
# m.testClass().testMethod()
