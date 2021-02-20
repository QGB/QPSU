# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import network;
sta_if = network.WLAN(network.STA_IF); 
sta_if.active(True);
sta_if.connect('test',str(2*3*3*47*14593));


import webrepl
webrepl.start()

import M
import gc


r=sta_if.isconnected()
print('connected ',r)


gc.collect()

del network,webrepl,gc,sta_if