#coding=utf-8
TMUX_NOTE='''
 I discovered that the -t and -s switches seem to accept [session]:window and not [session:]window. That is to say that specifying the session is optional, but including the : is mandatory. (I am using tmux 1.5)
 
:join-pane -s :1  把第 1 个window 加入到当前 pane
:break-pane -t [session]:[window]  分离当前 pane	到独立的 window ,不指定默认当前 session

:break-pane -t 1:0  # 当 session1存在window0时，命令没有成功执行。改成 1:1 成功

'''	


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
	import pexpect
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
	
	wds=[31,43]
	i=0
	while 1:
		i+=1
		gateway='192.168.%s.1' % wds[i%len(wds)]
		ip='%s62'%gateway
		if N.ping(ip,p=1):
			F.write('/etc/resolv.conf','nameserver '+gateway)
			c=ssh_trans(ip)
			while c.isalive():
				if not N.ping(ip,9,p=1):
					c.terminate()
				U.sleep(0.9)
		U.sleep(1)

def set_dns_server(ip):
	ip=N.auto_ip(ip)
	return F.write('/etc/resolv.conf','nameserver '+ip)
dns=set_dns=set_dns_server	


def change_user(uid, gid=None):
	'''
check_output(['id'], preexec_fn=change_user(pwd.getpwnam('u0_a131').pw_uid), env={})	

android 必须 3003 才能访问 网络 
	'''
	import os
	if gid is None:
		gid = uid
	def preexec_fn():
		os.setgid(gid)
		os.setgroups([gid,3003]) 
		os.setuid(uid)
	return preexec_fn
# from subprocess import check_output	
# print(check_output(['id']))
# print()
# print(check_output(['id']))


def bootargs_to_xml(s,f='',p=0):
	'''
bootargs=console=ttyAMA0,115200 blkdevparts=mmcblk0:1M(fastboot),1M(bootargs),10M(recovery),2M(deviceinfo),8M(loader),8M(loaderbak),1M(loaderdb),1M(loaderdbbak),8M(baseparam),8M(pqparam),20M(logo),20M(logobak),40M(fastplay),40M(fastplaybak),40M(kernel),20M(misc),8M(userapi),8M(hibdrv),8M(qbflag),300M(qbdata),500M(cache),50M(private),800M(system),-(userdata)
	
	'''
	m=0
	r=[]
	
	rs=[]
	ss=T.sub(s,':').split(',')
	mss=py.len(ss)-1
	for index,i in py.enumerate(ss):
		if i.startswith('-') and index==mss:
			print(index,i)
			name=T.sub(i,'(',')')
			n=0
			sn='"-"   '
			# break
		else:
			d=T.regex_match_named(i,r'(?P<n>\d+)(?P<unit>\w)\((?P<name>\w+)\)')
			if d['unit']!='M':return py.No(i,d,s)
			n=py.int(d['n'])
			name=d['name']
			sn=f'"{n}M"'
		sname=f'"{name}"'
		sm=f'"{m}M"'
		si=fr'''
<Part Sel="0" PartitionName={T.padding(sname,size=13)} FlashType="emmc" FileSystem="none" Start={T.padding(sm,size=7)} Length={T.padding(sn,size=6)} SelectFile="{name}.bin" />		
'''		
		m+=n
		rs.append('\t'+si.strip())
		r.append((n,name))
	xml= fr'''<?xml version="1.0" encoding="UTF-8"?>
<Partition_Info>
{T.eol.join(rs)}
</Partition_Info>	
'''	
	if p:print(xml)
	if f:
		if not f.lower().endswith('.xml'):
			f+='.xml'
		return F.write(f,xml)
	return r
	
	