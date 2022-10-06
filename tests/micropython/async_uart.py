try:
	import uasyncio as asyncio
except:
	import asyncio
# from pyb import UART
# uart = UART(4, 9600)
try:
	import M
	uart=M.uart()

	swriter = asyncio.StreamWriter(uart, {})
	sreader = asyncio.StreamReader(uart)
except:
	import sys
	if 'qgb.U' not in sys.modules:
		sys.path.append('C:/QGB/babun/cygwin/bin/')
		sys.path.append('/mnt/c/QGB/babun/cygwin/bin/')
	from qgb import py,U,T,N,F
	swriter=None
	sreader=None
async def sender():
	while True:
		# b=last_client_socket.recv(1)
		if not last_client_socket:
			await asyncio.sleep(0.1)
			continue
		print('await socket.recv',dir(last_client_socket))
		last_client_socket.sendall(b'[3232]')
		b=await last_client_socket.recv(1) #no arg: TypeError: function takes 2 positional arguments but 1 were given
		print('socket.recv',b)
		await asyncio.sleep(1)	
		if not b:
			await asyncio.sleep(0.1)
			
		else:
			if swriter:await swriter.awrite(b)
		# 

async def receiver():
	while True:
		if sreader:res = await sreader.readline()
		else:
			res=U.btime()
			await asyncio.sleep(2)
		print('Recieved', res)
		last_client_socket.sendall(res)
		
last_client_socket=None		
def accept_telnet_connect(telnet_server):
	global last_client_socket
	

	
	if last_client_socket:
		# close any previous clients
		# uos.dupterm(None)
		last_client_socket.close()
	
	last_client_socket, remote_addr = telnet_server.accept()
	print(telnet_server,"Telnet connection from:",last_client_socket, remote_addr)
	last_client_socket.setblocking(False)
	# dupterm_notify() not available under MicroPython v1.1
	# last_client_socket.setsockopt(socket.SOL_SOCKET, 20, uos.dupterm_notify)
	
	last_client_socket.sendall(bytes([255, 252, 34])) # dont allow line mode
	last_client_socket.sendall(bytes([255, 251, 1])) # turn off local echo		
		
# async def start(port=23):
def start(port=23):
	import socket
	global server_socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	ai = socket.getaddrinfo("0.0.0.0", port)
	addr = ai[0][4]
	print('getaddrinfo',port,addr)

	server_socket.bind(addr)
	# print('server_socket.bind',addr,file=out)
	server_socket.listen(1)
	# py.pdb()()
	try:
		server_socket.setsockopt(socket.SOL_SOCKET, 20, accept_telnet_connect) #esp micropython 专用
	except:
		
start()
loop = asyncio.get_event_loop()
# rs=loop.create_task(start())
rs=loop.create_task(sender())
print(rs)
loop.create_task(receiver())
loop.run_forever()