#coding=utf-8
import sys,pathlib
gsqp=pathlib.Path(__file__).absolute(
		).parent.parent.__str__()
	#*.py /qgb   /[gsqp]  
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import asyncio

async def sleep(sec):
	return await asyncio.sleep(sec)
	
async def websocket_client_send(url,astr):
	import websockets
	url=N.auto_url(url,default_protocol='ws')
	
	async with websockets.connect(url) as ws:
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

