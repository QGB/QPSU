# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import network;
sta_if = network.WLAN(network.STA_IF); 
sta_if.active(True);
# sta_if.connect('test',str(2*3*3*47*14593));


import M
try:
	import ble
	ble.sta_if=sta_if
	ble.main()
except Exception as e:
	print(e)



f='webrepl_cfg.py' 
if f not in M.ls():
	M.write(f,"PASS = '1234'\n")

import webrepl
webrepl.start()

r=sta_if.isconnected()
# print('try connect test',r)
gnw=0
if not r:
	import webrepl_cfg
	dsp=getattr(webrepl_cfg,'dsp',{})
	if dsp:
		while not sta_if.isconnected():
			ds=M.wifi_scan(p=0,return_dict=1)
			if not ds:continue
			else:gnw+=1
			if gnw>9:break
			for ssid,pw in dsp.items():
				if isinstance(ds,dict) and ssid not in ds:continue
				sta_if.disconnect()
				print('try connect ',ssid,pw)
				sta_if.connect(ssid,pw);
				for i in range(29):
					print('wait connect',ssid,i)
					M.sleep(1)
					if sta_if.isconnected():break
				if sta_if.isconnected():break
				
		del ssid,pw
		# del ds,sta_if
	del webrepl_cfg,dsp


del network,webrepl,f
import gc
gc.collect()
del gc

try:
	import mdot
except Exception as e:
	print(e)

