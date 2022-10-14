#coding=utf-8
import sys,pathlib
gsqp=pathlib.Path(__file__).absolute(
		).parent.parent.__str__()
	#*.py /qgb   /[gsqp]  
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import asyncio

def patch_nest_asyncio():
	import nest_asyncio
	return nest_asyncio.apply()
nest=nest_asyncio=patch_nest_asyncio
	
async def sleep(sec):
	return await asyncio.sleep(sec)
	
	
async def websocket_client_send(url,astr,subprotocols=None):
	import websockets
	url=N.auto_url(url,default_protocol='ws')
	# py.pdb()()
	if py.istr(subprotocols):subprotocols=[subprotocols]
	async with websockets.connect(url, subprotocols=subprotocols) as ws:
		await ws.send(astr)
		r = await ws.recv()
		return r
ws_send=websocket_client_send		

async def chrome_devtools_protocol_send(url,astr,params={},id=0):
	astr=astr.strip()
	if not id:id=U.ct()
	if py.istr(astr) and not (astr.startswith('{') and astr.endswith('}')):
		astr=py.dict(id=id,method=astr,params=params,)
	if py.isdict(astr):
		astr=T.json_dumps(astr)
	return astr,await websocket_client_send(url,astr)
csend=cws_send=c_ws_send=chrome_devtools_protocol_send

def async_to_sync(callable):
	''' (Pdb) A.a2s(connection.send)
*** TypeError: Called with unsupported argument: <bound method Connection.send of <pyppeteer.connection.Connection objec
t at 0x0000026A719AD108>>
'''
	import syncer
	return syncer.sync_fu(callable)
a2s=async_to_sync
# async def t(a):
	