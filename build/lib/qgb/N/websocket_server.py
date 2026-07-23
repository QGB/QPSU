#coding=utf-8
import sys,pathlib
gsqp=pathlib.Path(__file__).absolute(
		).parent.parent.parent.__str__()
	#*.py /N     /qgb   /[gsqp]  
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()
# py.pdb()()
#下面这样不行，一直卡在'C:\\QGB\\babun\\cygwin\\bin\\qgb'，多加.parent也无效
# gsqp=Path(__file__).parent.parent.parent.parent.parent.absolute().__str__()
# print(gsqp,[],sys.path)
# import py

import asyncio,websockets
import signal

# signal.signal(signal.SIGINT,U.exit)
# signal.signal(signal.SIGTERM,U.exit)

async def hello(websocket, path):
	name = await websocket.recv()
	# py.pdb()()
	r="{ qgb }"
	if not U.get(websocket.transport._sock) and name=='trigger':
		r={"cmds":[{"cmd":"canvas","idx":0},{"lights":"empty_list","idx":0},{"cmd":"distant_light","idx":2,"direction":[0.22,0.44,0.88],"color":[0.8,0.8,0.8],"size":[1.0,1.0,1.0],"canvas":0},{"cmd":"distant_light","idx":3,"direction":[-0.88,-0.22,-0.44],"color":[0.3,0.3,0.3],"size":[1.0,1.0,1.0],"canvas":0},{"cmd":"box","idx":5,"size":[1.0,1.0,1.0],"canvas":0}]}
		r=U.get_set(0,r)
		r=T.json_dumps(r)
		U.set(websocket.transport._sock,[U.stime()])
	elif name=='trigger':
		U.get(websocket.transport._sock).append(U.stime())	
	else:
		r=U.exec_return_str(name,globals=globals(),locals=locals() )	
	await websocket.send(r)

	return
	print(f"< {name}")

	greeting = f"{path} {name} !"

	await websocket.send(greeting)
	print(f"> {greeting}")

start_server = websockets.serve(hello, 'localhost', 8765)

loop=asyncio.get_event_loop()
# loop.add_signal_handler(signal.SIGINT,U.exit)
# loop.add_signal_handler(signal.SIGTERM, U.exit)

loop.run_until_complete(start_server)
print(U.stime(),'run_until_complete done!')

def wakeup():
	loop.call_later(0.1, wakeup)


if '__main__' in __name__:
	try:
		loop.call_later(0.1, wakeup)
		print(U.stime(),'call_later')
		# loop.run_forever()
		t=U.Thread(target=loop.run_forever)
		t.start()
		print(U.stime(),'run_forever')
		U.ipy_embed()()
	except BaseException:
		# U.msgbox(U.stime())
		U.exit('KeyboardInterrupt')


