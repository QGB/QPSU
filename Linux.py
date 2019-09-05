def set_ulimit_max():
	import resource
	soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
	resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
	return soft,hard
	
def get_all_fd():
	F.ls
	
def get_tty_size():
	import os
	rows, columns = os.popen('stty size', 'r').read().split()
	return rows,columns
	
def get_tty_width():
	return get_tty_size()[1]
	
def get_tty_height():
	return get_tty_size()[0]


	