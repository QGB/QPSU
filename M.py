#coding=utf-8
cs=charset={'cp864', 'rot-13', 'iso8859-14', 'mac-cyrillic', 'cp852', 'cp863', 'cp367', 'iso8859-5', 'iso8859-16', 'cp500', 'gbk', 'mac-iceland', 'cp869', 'mac-arabic', 'koi8-r', 'koi8-u', 'cp856', 'cp949', 'cp1258', 'cp874', 'iso8859-4', 'euc-kr', 'utf-32', 'cp037', 'cp1255', 'cp850', 'bz2-codec', 'palmos', 'utf-16-le', 'cp737', 'punycode', 'cp437', 'iso8859-15', 'iso8859-1', 'cp858', 'iso2022-jp-2004', 'utf-32-le', 'gb2312', 'ascii', 'latin-1', 'iso2022-jp-ext', 'hex-codec', 'mac-centeuro', 'unicode-escape', 'shift-jisx0213', 'raw-unicode-escape', 'iso8859-3', 'cp866', 'iso8859-7', 'mac-latin2', 'iso8859-2', 'big5hkscs', 'cp1254', 'hz', 'iso2022-jp-1', 'mac-romanian', 'iso2022-kr', 'utf-16-be', 'iso8859-11', 'iso8859-13', 'cp1361', 'cp819', 'charmap', 'cp860', 'cp950', 'cp1140', 'iso2022-jp', 'hp-roman8', 'euc-jis-2004', 'utf-16', 'cp1253', 'cp1256', 'cp936', 'big5', 'cp1026', 'cp855', 'cp1251', 'mac-greek', 'cp1250', 'cp932', 'mbcs', 'iso8859-9', 'uu-codec', 'shift-jis-2004', 'unicode-internal', 'zlib-codec', 'iso2022-jp-3', 'cp1252', 'cp775', 'quopri-codec', 'tis-620', 'johab', 'shift-jis', 'cp1006', 'iso8859-6', 'utf-7', 'utf-8-sig', 'cp861', 'iso8859-8', 'cp1257', 'iso2022-jp-2', 'gb18030', 'base64-codec', 'cp720', 'iso8859-10', 'cp862', 'euc-jp', 'ptcp154', 'cp865', 'utf-32-be', 'cp875', 'utf-8', 'idna', 'mac-farsi', 'mac-roman', 'mac-turkish', 'euc-jisx0213', 'cp857', 'mac-croatian', 'cp424'}

def b2h(bs,split=''):
	return split.join(
	[('%02s'%(hex(b)[2:])).replace(' ','0') for b in	bs])
# str no rjust ,%02i不支持str类型

gct={}
def count(a=0):
	if a not in gct:
		gct[a]=0
	else:
		gct[a]+=1
	return gct[a]
ct=count

def read(f):
	with open(f) as _:
		return _.read(-1)

import os,time
def gv():
	print(sys_info())
	gc()
	print(sys_info())
	
def sleep(t=0.001):
	time.sleep(t)
	
def ls(p='/'):
	return os.listdir(p)
	
def sys_info(unit=1024):
	import gc
	F = gc.mem_free()
	A = gc.mem_alloc()
	T = F+A
	P = '{0:.2f}%'.format(F/T*100)
	return 'disk Total:{0} KB, Free:{1} KB. === '.format(*disk_usage())+'mem Total:{0} Free:{1} ({2})'.format(T,F,P)
mem=info=sys_info

def disk_usage(unit=1024): 
	'''1024 B = KB
	'''
	f_bsize, f_frsize, f_blocks, f_bfree, f_bavail, f_files, f_ffree, f_favail, f_flag, f_namemax=os.statvfs('/')
	return (f_bsize*f_blocks/unit,f_bsize*f_bavail/unit)
df=disk_usage

try:
	import network
except:pass

def ip():
	n=network.WLAN(network.STA_IF)
	return n.ifconfig()
	
def wifi_scan(p=1):
	n=network.WLAN(network.STA_IF)
	n.active(True)
	r=[]
# ' '.join([' '*8,'ssid',' '*6,'bssid',' '*4,'channel,RSSI,authmode,hidden'])
	if p:print('         ssid        bssid      channel,RSSI,authmode,hidden')
	for ssid, bssid, channel, RSSI, authmode, hidden in sorted(n.scan(),reverse=1,key=lambda a:a[3]):
		ssid=ssid.decode('utf-8')
		bssid=b2h(bssid,split='-')
		if p:
			print('%-20s'%ssid, bssid, channel, RSSI, authmode, hidden )
		else:
			row=(ssid, bssid, channel, RSSI, authmode, hidden)
			# if r and RSSI>r[0][3]:
				# r.insert(0,row)
			# else:
			r.append(row)
	gc()
	if not p:return r
ws=wifi_scan

def wifi_connect(ssid,pw):
	n=network.WLAN(network.STA_IF)
	n.active(True)
	n.connect(ssid,pw)
	return n.isconnected()
wc=wific=wifi_connect

def wifi_ap(ssid,pw):
	# Change ssid/password of ESP8266's AP:
	n= network.WLAN(network.AP_IF)
	n.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=pw)
ap=wifi_ap

def setup():
	wifi_connect('TP-LINK_8CD652','12345678')

def gc():
	import gc
	return gc.collect()
	
def reload(m='M'):
	import sys
	sys.modules.pop(m)
	sys.modules[m]=__import__(m)
	return sys.modules[m]
r=reload
	
def reboot():
	import machine
	return machine.reset()

gdpin={}
def gpio(index=2,mod=1):
	'''import mac	hine;help(machine.Pin)
IN -- 0
  OUT -- 1
  OPEN_DRAIN -- 2
  PULL_UP -- 1
  IRQ_RISING -- 1
  IRQ_FALLING -- 2
'''
	import machine
	gdpin[(index,mod)]=machine.Pin(index,mod)
	return gdpin[(index,mod)]
led2=gpo=pin=Pin=gpio

def gpi(index=0):
	import machine
	gdpin[(index,0)]=machine.Pin(index, machine.Pin.IN, machine.Pin.PULL_UP)
	return gdpin[(index,0)]

def blink(a=0.2,b=0.47,index=2):
	from time import sleep
	p=Pin(index)
	while 1:
		p.off()
		sleep(a)
		p.on()
		sleep(b)
	

class V():
	# def __getattribute__(self, name):
	def __getattr__(self, name):
		print('===',self, name)
		return None
	def __call__(self, *a,**ka):
		print('CALL ',self,a,ka)
		
		
		
		
		