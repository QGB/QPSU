import multiprocessing
from os import getpid
from time import sleep 

def worker(procnum):

    print('I am number %d in process %d' % (procnum, getpid()))
	for i in range(5):
		sleep(1)
	os._exit(procnum)	
    return getpid()

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = 3)
    print(pool.map(worker, range(5)))
	