from microdot_asyncio import Microdot, send_file,Response
from microdot_asyncio_websocket import with_websocket
ismpy=True
try:
	import uasyncio as asyncio
	import M
	uart=M.uart(tx=3,rx=2)#6 18
	# uart=M.uart(tx=2,rx=3,baudrate=38400)#12 mt7688
	# uart=M.uart(tx=9,rx=8)#13 hdc
	
	swriter = asyncio.StreamWriter(uart, {})
	sreader = asyncio.StreamReader(uart)
	gport=80
	gp='/'
	U,T,N,F=0,0,0,0
except Exception as e:
	print(e)
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
					r=swriter.a
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
	ismpy=False
	print(f'Not in micropython.listen:{gport} pid:',U.pid)
#############################################
loop = asyncio.get_event_loop()

break_sleep=False
async def sleep(asec):
	global break_sleep
	if aisec<1:return await asyncio.sleep(asec)

	break_sleep=False
	n,y=divmod(asec,int(asec)) # ZeroDivisionError: divide by zero
	for i in range(n):
		if break_sleep:return
		asyncio.sleep(1)
	if break_sleep:return	
	asyncio.sleep(y)
	
gt_off,gt_on,gpin=9999,0,18
def set_blink(off,on,pin):
	global gt_off,gt_on,gpin

async def blink_loop():
	await asyncio.sleep(1)
loop.create_task(blink_loop())

# if not ismpy:
async def sleep_loop():#sleep_for_ctrl_c windows
	global res
	while True:
		dws=[]
		for ws in gws:
			if ws.closed:
				dws.append(ws)
		for ws in dws:
			gws.remove(ws)
		await asyncio.sleep(1)
loop.create_task(sleep_loop())		
# grn=1		
# res=''
async def receiver():
	global gws
	print('start uart receive...')
	res=''
	while True:
		if sreader:	
			res = await sreader.read(999)#空参数，write 换行也不回返回	
		if not ismpy:print('uart Recieved', res) # for debug
		
		if ismpy and res:res=b'0'+res # micropython
		for ws in gws:
			try:
				await ws.send(res)
			except Exception as e:
				ws.closed=True
				print(ws,e)
loop.create_task(receiver())

app = Microdot()

@app.route('/token')
def token(request):
	return Response(body='{"token": ""}', status_code=200,)

gws=[]
@app.route('/ws')
@with_websocket
async def echo(request, ws):
	'''
AuthToken
1{"columns":186,"rows":45}
<
	
# 30e4 b8ad e696 87   #F.b2h('中文'.encode('utf-8'))== 'E4B8AD E69687'		
'''
	# global gws
	gws.append(ws)
	while True:
		data = await ws.receive()
		print('ws receive',data)
		if data.startswith(b'0'):#len(data)==2 and 
			data=data[1:]
		else:
			for bs in [b'{"AuthToken":"","columns":',b'1{"columns":',]:
				if data.startswith(bs):
					print('ws skip',data)
					data=b''
					break
		if swriter:await swriter.awrite(data)
		# r=U.execResult(data,globals=globals(),locals=locals())
		# if swriter:await swriter.awrite(r)
		# await ws.send(data)
		# if swriter:await swriter.awrite(f'{U.stime()} {data}')
		# await swriter.awrite('Hello uart\n')
		
@app.route('/<re:-.*:code>')#[dynamic path component]只能用 / 分隔
# @app.route('/-/<path:path>')#像/-code这种就不会匹配 除非 /-/
def rpc(request,code=''):
	global response
	response=Response( status_code=200,)
	if U:r=U.execResult(T.url_decode(code[1:]),globals=globals(),locals=locals())
	else:
		code=M.url_decode(code[1:])
		print(request,code)
		M.gc()
		try:
			exec(code,globals(),locals())
			if 'r' in locals():
				r=locals()['r']
				if not isinstance(r,str):
					r=repr(r)
			else:
				r='can not found r in locals()'
		except Exception as e:
			r=repr(e)
			del e
		# print(code,r)
		del code
		# r=code
	if not response.body:
		# response.body=r.encode()
		response.body=r#.encode('utf-8')	
	return response

@app.route('/')
@app.route('/<path:path>')#路径匹配函数放在最后，不然后面的 ws，token也会被匹配
def static(request,path=''):
	if not path:path='index.html'
	path=gp+path
	if U:print(U.stime(),path)
	else:print(request,path)
	return send_file(path)
	

loop.create_task(app.run(port=gport))

loop.run_forever()