import uasyncio as asyncio
# from pyb import UART
# uart = UART(4, 9600)
import M
uart=M.uart(tx=2,rx=3)

swriter = asyncio.StreamWriter(uart, {})
# async def sender():
	# while True:
		# await swriter.awrite('Hello uart\n')
		# await asyncio.sleep(2)

sreader = asyncio.StreamReader(uart)
async def receiver():
	global gws
	print('start uart receive...')
	while True:
		res = await sreader.read(1)#空参数，write 换行也不回返回
		# print('uart Recieved', res)
		if gws:await gws.send(res)


from microdot_asyncio import Microdot, send_file,Response
from microdot_asyncio_websocket import with_websocket

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
		await swriter.awrite(data)
		# await swriter.awrite('Hello uart\n')
# 30e4 b8ad e696 87   #F.b2h('中文'.encode('utf-8'))== 'E4B8AD E69687'		
		
		
loop = asyncio.get_event_loop()
# rs=loop.create_task(sender())
# print(rs)
loop.create_task(receiver())
loop.create_task(app.run(port=80))

loop.run_forever()


# loop.run_forever()