#coding=utf-8
import sys,os
if __name__.endswith('qgb.chrome'):from . import py
else:import py
U,T,N,F=py.importUTNF()

# import pychrome  
import pyppeteer  
import asyncio

def connect(ws):
	''' qgb
print(connection, browserContextIds, ignoreHTTPSErrors, defaultViewport)	
<pyppeteer.connection.Connection object at 0x0000016D1F3B2D88> [] False {'width': 800, 'height': 600}	
	'''
	


loop=asyncio.get_event_loop()
def windows_asyncio_KeyboardInterrupt_patch():
	loop.call_later(0.1, windows_asyncio_KeyboardInterrupt_patch)

if '__main__' in __name__:
	try:
		loop.call_later(0.1, wakeup)
		print(U.stime(),'call_later')
		loop.run_forever()
		print(U.stime(),'run_forever')
	except BaseException:
		# U.msgbox(U.stime())
		U.exit(msg='KeyboardInterrupt')


