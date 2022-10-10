from microdot_asyncio import Microdot, send_file,Response
from microdot_asyncio_websocket import with_websocket

try:
	import uasyncio as asyncio
	import M
	uart=M.uart(tx=2,rx=3)

	swriter = asyncio.StreamWriter(uart, {})
	sreader = asyncio.StreamReader(uart)
	gport=80
except:
	import sys;'qgb.U' in sys.modules or sys.path.append('C:/QGB/babun/cygwin/bin/');from qgb import py,U,T,N,F
	import asyncio	
	class StreamReader:
		async def read(self,n):
			while True:
				if swriter.a:
					r=f'{U.stime()} {swriter.a}'
					swriter.a=None
					return r
				await asyncio.sleep(0.01)# 不加占满cpu
	sreader=StreamReader()
	class StreamWriter:
		def __init__(self):
			self.a=None
		async def awrite(self,a):
			self.a=a
	swriter=StreamWriter()
	gport=1122
	print('Not in micropython. pid:',U.pid)
async def receiver():
	global gws
	print('start uart receive...')
	while True:
		if sreader:res = await sreader.read(1)#空参数，write 换行也不回返回
		
		# print('uart Recieved', res)
		if gws:await gws.send(res)
#############################################

app = Microdot()


@app.route('/')
def index(request):
	return send_file('index.html')
	
import io
@app.route('/token')
def index(request):
	return Response(body=io.StringIO('{"token": ""}'), status_code=200,)

gws=None
@app.route('/ws')
@with_websocket
async def echo(request, ws):
	global gws
	gws=ws
	while True:
		data = await ws.receive()
		print('ws receive',data)
		# await ws.send(data)
		if swriter:await swriter.awrite(data)
		# await swriter.awrite('Hello uart\n')
# 30e4 b8ad e696 87   #F.b2h('中文'.encode('utf-8'))== 'E4B8AD E69687'		
		
		
loop = asyncio.get_event_loop()
# rs=loop.create_task(sender())
# print(rs)
loop.create_task(receiver())
loop.create_task(app.run(port=gport))

loop.run_forever()


# loop.run_forever()