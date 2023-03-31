#coding=utf-8
# cs=charset={'cp864', 'rot-13', 'iso8859-14', 'mac-cyrillic', 'cp852', 'cp863', 'cp367', 'iso8859-5', 'iso8859-16', 'cp500', 'gbk', 'mac-iceland', 'cp869', 'mac-arabic', 'koi8-r', 'koi8-u', 'cp856', 'cp949', 'cp1258', 'cp874', 'iso8859-4', 'euc-kr', 'utf-32', 'cp037', 'cp1255', 'cp850', 'bz2-codec', 'palmos', 'utf-16-le', 'cp737', 'punycode', 'cp437', 'iso8859-15', 'iso8859-1', 'cp858', 'iso2022-jp-2004', 'utf-32-le', 'gb2312', 'ascii', 'latin-1', 'iso2022-jp-ext', 'hex-codec', 'mac-centeuro', 'unicode-escape', 'shift-jisx0213', 'raw-unicode-escape', 'iso8859-3', 'cp866', 'iso8859-7', 'mac-latin2', 'iso8859-2', 'big5hkscs', 'cp1254', 'hz', 'iso2022-jp-1', 'mac-romanian', 'iso2022-kr', 'utf-16-be', 'iso8859-11', 'iso8859-13', 'cp1361', 'cp819', 'charmap', 'cp860', 'cp950', 'cp1140', 'iso2022-jp', 'hp-roman8', 'euc-jis-2004', 'utf-16', 'cp1253', 'cp1256', 'cp936', 'big5', 'cp1026', 'cp855', 'cp1251', 'mac-greek', 'cp1250', 'cp932', 'mbcs', 'iso8859-9', 'uu-codec', 'shift-jis-2004', 'unicode-internal', 'zlib-codec', 'iso2022-jp-3', 'cp1252', 'cp775', 'quopri-codec', 'tis-620', 'johab', 'shift-jis', 'cp1006', 'iso8859-6', 'utf-7', 'utf-8-sig', 'cp861', 'iso8859-8', 'cp1257', 'iso2022-jp-2', 'gb18030', 'base64-codec', 'cp720', 'iso8859-10', 'cp862', 'euc-jp', 'ptcp154', 'cp865', 'utf-32-be', 'cp875', 'utf-8', 'idna', 'mac-farsi', 'mac-roman', 'mac-turkish', 'euc-jisx0213', 'cp857', 'mac-croatian', 'cp424'}

def t():
	import os
	l=[]
	for i in range(2):
		try:
			l.append(os.dupterm(None,i))
		except Exception as e:
			l.append(e)
		write(f'osd{len(l)}',repr(l))	
	return l	

def rename(a,b):
	import os
	return	os.rename(a,b)
mv=rename	

def run_forever():
	import uasyncio as asyncio
	loop = asyncio.get_event_loop()
	loop.run_forever()

def socket_send(file='',data='',ip='192.168.1.3',port=8000):
	import socket
	sock = socket.socket()
	addrinfos = socket.getaddrinfo(ip, port)
	# (host and port to connect to are in 5th element of the first tuple in the addrinfos list
	sock.connect(addrinfos[0][4])
	if data:sock.send(data)
	if file:
		isize=size(file)
		with open(file,'rb') as f:
			while f.tell()<isize:
				sock.write(f.read(4096))
	sock.close()

def _post_large_file(url,file,headers={}):
	'''   File "/lib/urequests.py", line 115, in post
TypeError: unexpected keyword argument 'files'
>>>
'''
	import urequests
	files = {file: open(file, 'rb')}
	return urequests.post(url,files=files)
	
def post_large_file(url,file,headers={}):#, data=None, json=None,params=None
	import urequests,usocket
	try:
		proto, dummy, host, path = url.split("/", 3)
	except ValueError:
		proto, dummy, host = url.split("/", 2)
		path = ""
	if proto == "http:":
		port = 80
	elif proto == "https:":
		import ussl
		port = 443
	else:
		raise ValueError("Unsupported protocol: " + proto)

	if ":" in host:
		host, port = host.split(":", 1)
		port = int(port)
		
	# if params:
		# path = path + "?"
		# for k in params:
			# path = path + '&'+k+'='+params[k]

	ai = usocket.getaddrinfo(host, port)
	addr = ai[0][4]
	s = usocket.socket()
	s.connect(addr)
	if proto == "https:":
		s = ussl.wrap_socket(s)
	s.write(b"POST /%s HTTP/1.0\r\n" % path)
	if not "Host" in headers:
		s.write(b"Host: %s\r\n" % host)
	# Iterate over keys to avoid tuple alloc
	for k in headers:
		s.write(k)
		s.write(b": ")
		s.write(headers[k])
		s.write(b"\r\n")
	# if json is not None:
		# assert data is None
		# import ujson
		# data = ujson.dumps(json)
	
	# if data:
	isize=size(file)
	s.write(b"Content-Length: %d\r\n" % isize)
	s.write(b"\r\n")
	# if data:
	gc()

	with open(file,'rb') as f:
		while f.tell()<isize:
			s.write(f.read(256))

	l = s.readline()
	protover, status, msg = l.split(None, 2)
	status = int(status)
	#print(protover, status, msg)
	while True:
		l = s.readline()
		if not l or l == b"\r\n":
			break
				#print(l)
		if l.startswith(b"Transfer-Encoding:"):
			if b"chunked" in l:
				raise ValueError("Unsupported " + l)
		elif l.startswith(b"Location:") and not 200 <= status <= 299:
			raise NotImplementedError("Redirects not yet supported")

	resp = Response(s)
	resp.status_code = status
	resp.reason = msg.rstrip()
	return resp

def delete_file(f):
	import os
	return os.remove(f)
delete=delete_file

def size(f):
	'''
os.stat('boot.py')
st_mode
(32768, 0, 0, 0, 0, 0, 742, 0, 0, 0)
	
	'''
	import os
	st_mode,  st_ino,st_dev,st_nlink,  st_uid,st_gid,  st_size,  st_atime,st_mtime,st_ctime=os.stat(f)
	return st_size

def is_esp32c3():
	import os
	return 'ESP32C3' in os.uname().machine

def uname():
	'''
(sysname='esp32', nodename='esp32', release='1.19.1', version='v1.19.1 on 2022-08-29', machine='ESP32C3 module with ESP32C3')
'''	
	import os
	return os.uname()

def get_chip_id(return_hex=False):
	import machine
	b=machine.unique_id()
	if return_hex:
		return b2h(b)  # '6055f9776880'    
	return b	

def b2h(bs,split=''):
	return split.join(
	[('%02s'%(hex(b)[2:])).replace(' ','0') for b in	bs])
# str no rjust ,%02i不支持str类型

guart=gct={}
def count(a=0):
	if a not in gct:
		gct[a]=0
	else:
		gct[a]+=1
	return gct[a]
ct=count

def uart(tx=2,rx=3,index=1,w='',baudrate=115200,wsleep=0.1):
	global guart
	from machine import UART
	if not guart:guart={}
	k=(tx,rx,baudrate)
	if k in guart:
		uart1=guart[k]
	else:
		guart[k]=uart1 = UART(index, baudrate=baudrate, tx=tx, rx=rx)
	if w:
		uart1.write(w)
		sleep(wsleep)
		print(uart1.read())
	return uart1

def sha256(b=b'',f=''):
	hashlib.sha256
	h.update(b)
	return binascii.hexlify(h.digest())

def new_file(f,size,chunk=4096,b=b'\x00'):
	with open(f,'w') as _:
		_.write('')
	n=0	
	with open(f,'a') as _: # wa ValueError:
		if size>chunk:
			bc=b*chunk
			for i in range(0,size,chunk):
				_.write(bc)
				n+=chunk
				if i%20480==0:print(i,i/1024,'KB')
		_.write(b*(size-n))
	import os	
	return os.stat(f)
new=new_file	
	
def write(f,text):
	with open(f,'w') as _:
		return _.write(text)
def read(f,size=-1):
	if "'TextIOWrapper'" in repr(f):#<class 'TextIOWrapper'>
		f.seek(0)
		return f.read(size)

	with open(f) as _:
		return _.read(size)

def gv():
	print(sys_info())
	gc()
	print(sys_info())
	
def sleep(t=0.001):
	import time
	time.sleep(t)
	
def ls(p='/'):
	'''
icroPython v1.15-60-g28b5a71b1-dirty on 2021-05-01; win32 version
list(os.ilistdir())	
AttributeError: 'module' object has no attribute 'listdir'
AttributeError: 'module' object has no attribute 'statvfs'
ImportError: no module named 'upip'
	'''
	import os
	return os.listdir(p)
	
	
def sys_info(unit=1024):
	import gc
	F = gc.mem_free()
	A = gc.mem_alloc()
	T = F+A
	P = '{0:.2f}%'.format(F/T*100)
	return 'disk Total:{0} KB, Free:{1} KB. === '.format(*disk_usage(unit=unit))+'mem Total:{0} Free:{1} ({2})'.format(T,F,P)
mem=info=sys_info

def disk_usage(unit=1024): 
	'''1024 B = KB
(4096, 4096, 669, 0, 0, 0, 0, 0, 0, 255)	
	'''
	import os
	f_bsize, f_frsize, f_blocks, f_bfree, f_bavail, f_files, f_ffree, f_favail, f_flag, f_namemax=os.statvfs('/')
	return (f_bsize*f_blocks/unit,f_bsize*f_bavail/unit)
df=disk_usage

try:
	import network
except:pass

def ifconfig():
	'''network.STA_IF==0 
0 : ('0.0.0.0', '0.0.0.0', '0.0.0.0', '208.67.222.222')
1 : ('192.168.4.1', '255.255.255.0', '192.168.4.1', '208.67.222.222')
2 : TypeError: function missing 1 required positional arguments
3 : 重启 卡死	
	'''
	return __import__('network').WLAN(0).ifconfig(),__import__('network').WLAN(1).ifconfig()
	# import network;return network.WLAN(0).ifconfig(),network.WLAN(1).ifconfig()
	n=network.WLAN(network.STA_IF)
	return n.ifconfig()
ip=ipconfig=ifconfig

def wifi_scan(p=1,return_dict=False):
	import network
	n=network.WLAN(network.STA_IF)
	n.active(True)
	r=[]
# ' '.join([' '*8,'ssid',' '*6,'bssid',' '*4,'channel,RSSI,authmode,hidden'])
	if p:print('         ssid        bssid      channel,RSSI,authmode,hidden')
	for ssid, bssid, channel, RSSI, authmode, hidden in sorted(n.scan(),reverse=1,key=lambda a:a[3]):
		ssid=ssid.decode('utf-8')
		bssid=b2h(bssid,split='-')
		if p:
			print('%-20s'%ssid, bssid, '%-2s'%channel, RSSI, authmode, hidden )
		else:
			row=(ssid, bssid, channel, RSSI, authmode, hidden)
			# if r and RSSI>r[0][3]:
				# r.insert(0,row)
			# else:
			r.append(row)
	gc()
	if not p:return r
wl=lw=wifi_ls=ls_wifi=list_wifi=wifi_list=ws=get_wifi_list=scanw=scan_wifi=wifi_scan

def is_wifi_connected():
	global STA_IF
	if not STA_IF:
		STA_IF=network.WLAN(network.STA_IF)
	return STA_IF.isconnected()
isc=iswifi=iswific=is_wific=isconnected=is_wifi_connected
	
STA_IF=0
def wifi_connect(ssid='test',pw=''.join(str(i) for i in range(1,9))):
	'''mpfshell -c open ws:192.168.43.145,1234
	'''
	global STA_IF
	if not STA_IF:
		STA_IF=network.WLAN(network.STA_IF)
	STA_IF.active(True)
	try:
		STA_IF.connect(ssid,pw)
	except Exception as e:
		print(e)
		STA_IF.disconnect()
	return STA_IF.isconnected()
c=jap=wc=wific=wifi_connect

def wifi_ap(ssid,pw):
	# Change ssid/password of ESP8266's AP:
	n= network.WLAN(network.AP_IF)
	n.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=pw)
ap=new_ap=wifi_ap

def setup():
	import webrepl_setup
	return wifi_connect('TP-LINK_8CD652*','12345678')
	
	
	wifi_connect ('TP-LINK_8CD652','1234567810')
	wifi_connect ('TP-LINK_516',str(112109389836//6))

def gc():
	import gc
	return gc.collect()
		
def reload(m='M'):
	import sys
	if m in sys.modules:
		sys.modules.pop(m)
	sys.modules[m]=__import__(m)
	return sys.modules[m]
r=reload
	
def reboot():
	''' 重启串口卡住： Advanced Seral setings > Flow control 改成 None'''
	return __import__('machine').reset()
	import machine
	return machine.reset()
reset=restart=reboot

gdpin={}
def gpio(index=2,mod=3):
	'''import mac	hine;help(machine.Pin)
IN -- 0
  OUT -- 1
  OPEN_DRAIN -- 2
  PULL_UP -- 1
  IRQ_RISING -- 1
  IRQ_FALLING -- 2
  
  machine.Pin.OUT == 3
'''
	import machine
	gdpin[(index,mod)]=machine.Pin(index,mod)
	return gdpin[(index,mod)]
led2=gpo=pin=Pin=gpio

def gpi(index=0,mod=None):
	import machine
	if mod==None:mod=machine.Pin.PULL_UP
	gdpin[(index,0)]=machine.Pin(index, machine.Pin.IN, mod)
	return gdpin[(index,0)]


def blink(a=0.2,b=0.47,index=None):
	if index==None:index=2
	if 'gop' in globals():
		p=gop
	else:
		from machine import Pin
		p=Pin(index,Pin.OUT)
	from time import sleep
	while 1:
		p.off()
		sleep(a)
		p.on()
		sleep(b)

def go(*a):
	o=gpo_3()
	try:
		blink(*a)
	except KeyboardInterrupt as e:
		o.off()
		return e

def gpo_3():
	global gop # RX 
	from machine import Pin
	gop=Pin(3,Pin.OUT)
	return gop
o3=gpo3=gpo_3

class V():
	# def __getattribute__(self, name):
	def __getattr__(self, name):
		print('===',self, name)
		return None
	def __call__(self, *a,**ka):
		print('CALL ',self,a,ka)
		
		
def print_time_ms(sleep=0.3):
	import time
	while 1:
		print(time.ticks_ms())
		time.sleep(sleep)
	return
pt=pms=print_ms=print_time_ms


def lp(mode=None,max_len=44,skip_pin=[6,7,8,9,10,11,12]):
	global f
	import machine
	if mode==None:mode=machine.Pin.PULL_UP
	f=open('data.txt','w')
	for index in range(max_len):
		print(index)
		# if index in [6,7,8,9,10,11,12]:continue
		# continue

		if (index,mode) in gdpin or index in skip_pin:
			print('skip0-',index)
			f.write('=='+str(index)+'\n')
			f.flush()			
			continue
		
		f.write(str(index)+'\n')
		f.flush()
	
		try:
			gdpin[(index,mode)]=machine.Pin(index, machine.Pin.IN, mode)
		except Exception as e:
			print(index,e)
	for k,p in gdpin.items():
		print(p.value(),k,p)

import machine,time
		
def off(*a,t=0.001):
	time.sleep(t)
	for i in a:
		i.off()
		
def step(t=0.001,a=1,b=2,c=0,d=3):
	
	a=gpo(a,)
	b=gpo(b,)
	c=gpo(c,)
	d=gpo(d,)

	off(a,b,c,d)
	while 1:
		a.on()
		off(a,b,c,d,t=t)
				
		b.on()
		off(a,b,c,d,t=t)		
		c.on()
		off(a,b,c,d,t=t)		
		d.on()
		off(a,b,c,d,t=t)
	# machine.Pin(index, machine.Pin.IN, machine.Pin.PULL_UP)h
	
def http_get(url):
	if '://' not in url:url='http://'+url
	import urequests
	return urequests.get(url)
get=http_get

def http_post(url,data):
	import urequests
	return urequests.post(url)
post=http_post

def http_download_file(url,filename=''):
	import mrequests
	r=mrequests.get(url)
	print('open...',r)
	if not filename:filename=sub_last(url,'/')
	print('save...',filename)
	r.save(filename)
	print('done !',filename)
	return filename
	
down_file=download=download_file=http_download=http_download_file	

def sub_tail(s,s1,s2=''):
	'''

'''	
	if not s:return s
	if isinstance(b'',bytes):
		null=b''
	else:
		s= str(s)
		null=''
	i1=0
	if s2:
		i2=s.rfind(s2)
		if i2==-1:return null
		if s1:
			i1=s[:i2].rfind(s1)
			if i1==-1:return null
			i1+=len(s1)
		else:
			i1=0
	else:
		i1=s.rfind(s1)
		if i1==-1:return null
		i1+=len(s1)
		i2=len(s)
	return s[i1:i2] 
sub_last=sub_tail

def sub_head(s,s1,s2=''):
	if not s:return s
	if isinstance(b'',bytes):
		null=b''
	else:
		s= str(s)
		null=''	
	i1=s.find(s1)
	if not s2:
		i2=len(s)
	else:
		i2=s.find(s2,i1+len(s1))
	if(-1==i1 or -1==i2):
		return null
	i1+=len(s1)
	return s[i1:i2]
sub=sub_head


def url_decode(str):
	dic = {"%21":"!","%22":'"',"%23":"#","%24":"$","%26":"&","%27":"'","%28":"(","%29":")","%2A":"*","%2B":"+","%2C":",","%2F":"/","%3A":":","%3B":";","%3D":"=","%3F":"?","%40":"@","%5B":"[","%5D":"]","%7B":"{","%7D":"}"}
	for k,v in dic.items(): str=str.replace(k,v)
	return str
urldecode=url_decode

def localtime():
	import utime
	return utime.localtime()
time=localtime	

# upip=0
def upip_install(pkg_name):
	# global upip
	# if not upip:
	import upip
	return upip.install(pkg_name)
pip=upip=pip_install=upip_install	

def pwm(pin=17,freq=1,duty=1023):
	''' machine.Pin.OUT == 3

p=M.pwm()
from time import sleep as s
f=p.freq
	
	'''
	from machine import Pin,PWM
	if duty<1:
		duty=round(duty*1024) #1023
	try:	
		pin=Pin(pin,Pin.OUT)
		p=PWM(pin, freq=freq, duty=duty)
		return p
	except Exception as e:
		return pin,e

def lpwm(p,):
	import M
	d={}
	for i in range(1024):         
		p.duty(i);
		p.duty(i);
		p.duty(i);
		p.duty(i);
		p.duty(i);
		
		s=repr(p);
		n=int(s[s.index('duty=')+5:s.index(',',24)])           
		if n in d:d[n].append(i)
		else:d[n]=[i]   
		if i%200==0:M.gc();print(i,M.info())
	with open('d.txt','w') as f:
		return f.write(repr(d))
		
# def fs()	