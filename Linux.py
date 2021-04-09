import sys,pathlib				# *.py  /qgb   /[gsqp]
gsqp=pathlib.Path(__file__).absolute().parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

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



def ssh(host, cmd, user, password, timeout=30, bg_run=False):                                                                                                 
	"""SSH'es to a host using the supplied credentials and executes a command.                                                                                                 
	Throws an exception if the command doesn't return 0.                                                                                                                       
	bgrun: run command in the background"""                                                                                                                                    
	import pexpect

	# fname = tempfile.mktemp()                                                                                                                                                  
	# fout = open(fname, 'w')                                                                                                                                                    

	# options = '-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -oPubkeyAuthentication=no'                                                                         
	# if bg_run:                                                                                                                                                         
	# 	options += ' -f'                                                                                                                                                       
	# ssh_cmd = 'ssh %s@%s %s "%s"' % (user, host, options, cmd)                                                                                                                 
	ssh_cmd = 'ssh '
	child = pexpect.spawn(ssh_cmd, timeout=timeout)  #spawnu for Python 3                                                                                                                          
	child.expect(['[pP]assword: '])                                                                                                                                                                                                                                                                                               
	child.sendline(password)                                                                                                                                                   
	# child.logfile = fout                                                                                                                                                       
	child.expect(pexpect.EOF)                                                                                                                                                  
	child.close()                                                                                                                                                              
	# fout.close()                                                                                                                                                               

	fin = open(fname, 'r')                                                                                                                                                     
	stdout = fin.read()                                                                                                                                                        
	fin.close()                                                                                                                                                                

	if 0 != child.exitstatus:                                                                                                                                                  
		raise Exception(stdout)                                                                                                                                                

	return stdout	