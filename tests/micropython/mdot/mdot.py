from microdot_asyncio import Microdot, send_file,Response
from microdot_asyncio_websocket import with_websocket

try:
	import uasyncio as asyncio
	import M
	uart=M.uart(tx=2,rx=3)

	swriter = asyncio.StreamWriter(uart, {})
	sreader = asyncio.StreamReader(uart)
	gport=80
	gp='/'
	U,T,N,F=0,0,0,0
except:
	import requests,os,sys,pathlib   # .py/mdot  /micropy/test  /qgb   / 
	gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
	U,T,N,F=py.importUTNF()
	
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
	gp=r'\\192.168.1.10\qgb\github\ttyd\html\dist\\'
	# gp=r'\\192.168.1.10\qgb\github\ttyd\ttyd_html\dist/'
	gp=gsqp+'/qgb/tests/micropython/mdot/'
	print(f'Not in micropython.listen:{gport} pid:',U.pid)
#############################################
async def receiver():
	global gws
	print('start uart receive...')
	while True:
		if sreader:res = await sreader.read(1)#空参数，write 换行也不回返回
		
		# print('uart Recieved', res)
		if gws:await gws.send(res)

app = Microdot()

import io
@app.route('/token')
def index(request):
	return Response(body=io.StringIO('{"token": ""}'), status_code=200,)

gws=None
@app.route('/ws')
@with_websocket
async def echo(request, ws):
	'''
AuthToken
1{"columns":186,"rows":45}
<
	
# 30e4 b8ad e696 87   #F.b2h('中文'.encode('utf-8'))== 'E4B8AD E69687'		
'''
	global gws
	gws=ws
	while True:
		data = await ws.receive()
		print('ws receive',data)
		# await ws.send(data)
		if swriter:await swriter.awrite(data)
		# await swriter.awrite('Hello uart\n')
		
@app.route('/<re:-.*:code>')#[dynamic path component]只能用 / 分隔
# @app.route('/-<path:code>')#像这种就不会匹配 除非 /-/
def index(request,code):
	r=U.execResult(T.url_decode(code[1:]),globals=globals(),locals=locals())
	return Response(body=io.StringIO(r), status_code=200,)

@app.route('/')
@app.route('/<path:path>')#路径匹配函数放在最后，不然后面的 ws，token也会被匹配
def index(request,path=''):
	if not path:path='index.html'
	path=gp+path
	# if U:print(U.stime(),path)
	return send_file(path)
	

loop = asyncio.get_event_loop()
# rs=loop.create_task(sender())
# print(rs)
loop.create_task(receiver())
loop.create_task(app.run(port=gport))

loop.run_forever()