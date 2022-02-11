import pebble # import ProcessPool
from concurrent.futures import TimeoutError
# from time import sleep 
# import psutil,os
import sys;'qgb.U' in sys.modules or sys.path.append('C:/QGB/babun/cygwin/bin/');from qgb import *

def function(foo, bar=0):
	# ppid=psutil.Process(os.getpid()).ppid()
	U.sleep(U.randomInt(1,9)/5)
	return U.ppid(),foo + bar
	
def target_wrap(function,*a,**ka):
	return a,ka,function(*a,**ka)

gt=U.get_or_set('gt',[])
ge=U.get_or_set('ge',[])
def task_done(future):
	global gt,ge
	try:
		result = future.result()  # blocks until results are ready
		print("success:" ,repr(result[2]))
		gt.append(future)
	except TimeoutError as error:
		print("Function took longer than %d seconds" % error.args[1])
		ge.append(error)
	except Exception as error:
		print("Function raised %s" % error)
		print(error.traceback)  # traceback of the function

if __name__ == '__main__':
	with pebble.ProcessPool(max_workers=5, max_tasks=0) as pool:
		for i in range(0, 10):
			future = pool.schedule(function, args=[i], timeout=1)
			future.add_done_callback(task_done)
			