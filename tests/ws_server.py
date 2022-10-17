#!/usr/bin/env python
#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import asyncio
import signal
import websockets

async def echo(websocket,path):
	''' path:'/ws'
'''	
	try:
		requested_protocols = websocket.request_headers["Sec-WebSocket-Protocol"]
	except KeyError:
		print("Client hasn't requested any Subprotocol. Closing connection")
		return await websocket.close()
	print(requested_protocols)
	await asyncio.sleep(999)

	async for message in websocket:
		r=U.execResult(message,globals=globals(),locals=locals())
		await websocket.send(r)
		
async def sleep_for_ctrl_c():
	while True:
		await asyncio.sleep(1)
	
async def main():
	global stop
	# Set the stop condition when receiving SIGTERM.
	loop = asyncio.get_running_loop()
	loop.create_task(sleep_for_ctrl_c())
	# loop.add_signal_handler(signal.SIGINT, stop.set_result, None)
	# signal.signal(signal.SIGINT, stop.set_result)
	stop = loop.create_future()
	# async with websockets.serve(echo, '0.0.0.0', 1122,):#不加 asyncio.streams.IncompleteReadError: 0 bytes read on a total of 2 expected bytes
	serve=await websockets.serve(echo, '0.0.0.0', 1122,subprotocols=['tty'])
	# serve=await websockets.serve(echo, '0.0.0.0', 1122,subprotocols=[])
	# serve
	# async with :
	await stop



import logging
logger = logging.getLogger('websockets.server')
logger.setLevel(-1)


asyncio.run(main())