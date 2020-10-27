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
		loop.run_forever()
		print(U.stime(),'run_forever')
	except BaseException:
		# U.msgbox(U.stime())
		U.exit('KeyboardInterrupt')


