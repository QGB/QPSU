#coding=utf-8
import sys,pathlib
gsqp=pathlib.Path(__file__).absolute(
		).parent.parent.parent.__str__()
	#*.py /N     /qgb   /[gsqp]  
if gsqp not in sys.path:sys.path.append(gsqp)
from qgb import py
U,T,N,F=py.importUTNF()

def replace_ws_url(ws,netloc='127.0.0.1:8765'):
	return ws.replace(T.netloc(ws),netloc)
# py.pdb()()
import asyncio,websockets
import signal
async def proxy(websocket, path):
	global target_connect
	client_msg = await websocket.recv()
    # print(f"< {name}")

    # greeting = f"{path} {name} !"
	async with websockets.connect(f'ws://{target_netloc}{path}') as target_connect:
		await target_connect.send(client_msg)
		r = await target_connect.recv()
	
	await websocket.send(r)
	print(f"{U.stime()} {client_msg} > [{path}] > {r}")


def wakeup():
	loop.call_later(0.1, wakeup)


if '__main__' in __name__:
	listen_host=U.parse_cmd_duplicated_arg('host','listen_host','ip',default='0.0.0.0')
	listen_port=U.parse_cmd_duplicated_arg('port','listen_port','p',default=8765)
	target_url=U.parse_cmd_duplicated_arg('target','path','url','target_url','u',type=py.str)
	if not target_url:
		raise py.ArgumentError('cmd must provide target_url:-u[rl]')
	target_netloc=T.netloc(target_url)
	target_connect=U.get(target_url)

	print([U.stime(),listen_host,listen_port,target_url,target_connect])

	start_server = websockets.serve(proxy, listen_host,listen_port)

	loop=asyncio.get_event_loop()
	# loop.add_signal_handler(signal.SIGINT,U.exit)
	# loop.add_signal_handler(signal.SIGTERM, U.exit)

	loop.run_until_complete(start_server)
	print(U.stime(),'run_until_complete(start_server) done!')
	
	try:
		loop.call_later(0.1, wakeup)
		print(U.stime(),'call_later')
		loop.run_forever()
		print(U.stime(),'run_forever')
	except BaseException:
		# U.msgbox(U.stime())
		U.exit(msg='KeyboardInterrupt')


