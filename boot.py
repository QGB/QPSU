# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import network;
sta_if = network.WLAN(network.STA_IF); 
sta_if.active(True);
sta_if.connect('test',str(2*3*3*47*14593));


import M
f='webrepl_cfg.py' 
if f not in M.ls():
	M.write(f,"PASS = '1234'\n")

import webrepl
webrepl.start()

r=sta_if.isconnected()
print('try connect test',r)
if not r:
	import webrepl_cfg
	lsp=getattr(webrepl_cfg,'lsp')
	if lsp:
		ds=M.ls_wifi(p=0,return_dict=1)
		for ssid,pw in lsp:
			if isinstance(ds,dict) and ssid not in ds:continue
			sta_if.disconnect()
			print('try connect ',ssid,pw)
			sta_if.connect(ssid,pw);
		del ds,ssid,pw
	del webrepl_cfg,lsp


del network,webrepl,sta_if,f
import gc
gc.collect()
del gc

try:
	import mdot
except Exception as e:
	print(e)

