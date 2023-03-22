import uasyncio as asyncio
import M
uart=M.uart(tx=18,rx=19,baudrate=57600)
# swriter = asyncio.StreamWriter(uart, {})
sreader = asyncio.StreamReader(uart)

uws="ws://192.168.1.11:3344/ws"
import async_websocket_client

async def receiver(u=uws):
	global ws
	ws = async_websocket_client.AsyncWebsocketClient(10)#数字越大，建立连接越慢
	await ws.handshake(u)
	o=await ws.open()

	print('start uart receive...',M.time(),ws)
	res=''
	n=0
	while True:
		if sreader:	
			res = await sreader.read(1024)#空参数，write 换行也不回返回	
		# if not ismpy:print('uart Recieved', res) # for debug
		
		if res:
			n+=1
			# res=b'0'+res # micropython
			if n%1000==0:
				print(n,M.time())
			await ws.send(res)
		else:
			continue
		# for ws in gws:
			# try:
				# await ws.send(res)
			# except Exception as e:
				# ws.closed=True
				# print(ws,e)

async def t():
	ft='tmp.txt'
	with open(ft,'w') as _:
		_.write('')
	f=open(ft,'a')	

	ws = async_websocket_client.AsyncWebsocketClient(10)#数字越大，建立连接越慢
	await ws.handshake(uws)
	o=await ws.open()
	print(M.get('http://192.168.1.11:3344/-r=ds.clear()'),ws,o)
	

	m=0x800000
	# z=0x2000
	#m=0x8000
	z=0x400
	for i in range(m//z):
		# M.gc()
		cmd=f'spi read {hex(z*i)} {hex(z*(i+1))} \n '
		uart.write(cmd)
		# print(cmd)
		w=0
		for j in range(z):
			# r=await sreader.read(256)
			r=uart.read(256)
			if r:
				f.write(r)
				try:
					await ws.open()
					await ws.send(r)	
				except:
					print(i,j)
				w=0
			else:
				w+=1
				await asyncio.sleep(0.001)
				if w>30:break
		# break

	return i,j,w,f.tell(),f.close()

	n=0
	m=0
	while 1:
		r=uart.read(256)
		if r:
			n=0
			m+=1

			await ws.open()
			await ws.send(r)	
		else:
			await asyncio.sleep(0.01)
			n+=1
			if n>300:return n,m


	return n,m
	# if o:
	# import time

	# uart.write('spi\n')

	t0=time.ticks_ms()
	r=uart.read(1024)
	while not r:
		await asyncio.sleep(0.01)
		r=uart.read(1024)
	tms=time.ticks_ms()-t0

	print(ws,o,r,tms)
	if r:await ws.send(r)

	uart.write('\n')
	uart.write('spi read 0x0 0x80 \n')
	r=uart.read(1024)
	while r:
		await ws.send(r)
		r=uart.read(1024)

	return 1

async def ws_send(m='SOS!',u=uws,):
	'''
M.download('http://192.168.1.3/C%3A/QGB/babun/cygwin/bin/qgb/tests/micropython/mdot/sp;spi_read=M.reload('spi_read')

spi_read.loop.run_until_complete(spi_read.ws_send())
	'''
	ws = async_websocket_client.AsyncWebsocketClient(10)#数字越大，建立连接越慢
	await ws.handshake(u)
	o=await ws.open()
	await ws.send(m)
	data = await ws.recv()
	# print(data)
	return o,data

loop = asyncio.get_event_loop()
def run():
	
	loop.create_task(receiver())
	# loop.create_task(ws())
	
	# uart.write('spi read 0x0 0x800000 \n')
	uart.write('spi read 0x0 0x80 \n')
	loop.run_forever()


def gpio_g(m=96,s=None):
	if not s:
		import socket
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect(('192.168.1.5', 3344))

	print(uart.read(256))

	for i in range(m):
		print(i)
		try:
			M.get(f'http://192.168.1.3:16084/r=U.speak({i})')
		except Exception as e:print(e)	
		M.gc()
		uart.write(f'gpio g {i} \n')
		w=0
		for j in range(99):
			# r=await sreader.read(256)
			r=uart.read(256)
			if r:
				# if b'malloc error' in r:
				# 	uart.write('reset \n')
				# 	M.sleep(0.5)
				# 	for i in range(55):
				# 		uart.write('4')
				# 		M.sleep(0.1)
				# 	return i,j,w,s
				try:
					s.sendall(r)	
				except:
					print(i,j)
				w=0
			else:
				w+=1
				M.sleep(0.001)
				if w>30:break
	s.close()			
	return i,w,s

def c(start=0x0,m=0x800000,z=0x1000,s=None):
	if not s:
		import socket
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect(('192.168.1.5', 3344))

	for i in range(start,m+z,z):
		# M.gc()
		cmd=f'spi read {hex(i)} {hex(z)} \n '
		uart.write(cmd)
		# print(cmd)
		w=0
		for j in range(z):
			# r=await sreader.read(256)
			r=uart.read(256)
			if r:
				if b'malloc error' in r:
					uart.write('reset \n')
					M.sleep(0.5)
					for i in range(55):
						uart.write('4')
						M.sleep(0.1)
					return i,j,w,s
				try:
					s.sendall(r)	
				except:
					print(i,j)
				w=0
			else:
				w+=1
				M.sleep(0.001)
				if w>30:break
		# break
	s.close()
	return i,j,w,s

