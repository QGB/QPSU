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


def ssh_trans(ip):
	c=pexpect.spawn('ssh -CNR *:8206:127.0.0.1:22 qgb@'+ip)
	try:
		c.expect(['[Pp]assword:'],timeout=3)     
		c.sendline('0')
	except Exception as e:
		c.terminate() 
		U.sleep(0.5)
		return ssh_trans(ip)
	return c
def auto_switch_network(bg_run=False):                                                                                                 
	"""SSH'es to a host using the supplied credentials and executes a command.                                                                                                 
	Throws an exception if the command doesn't return 0.                                                                                                                       
	bgrun: run command in the background
pip install dulwich paramiko ping3 pexpect	
	"""                                                                                                                                    
	import pexpect
	wds=[31,43]
	i=0
	while 1:
		i+=1
		gateway='192.168.%s.1' % wds[i%len(wds)]
		if N.ping(gateway,p=1):
			F.write('/etc/resolv.conf','nameserver '+gateway)
			c=ssh_trans('%s62'%gateway)

			while c.isalive():
				if not N.ping(gateway,9,p=1):
					c.terminate()
				U.sleep(0.9)
		U.sleep(1)
