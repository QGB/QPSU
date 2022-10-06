#!/usr/bin/env python3

import socket

# Read "distributed echo server" as "(distributed echo) server". The "server"
# is not "distributed" but the echos are "distributed" to every connected
# client.

# Connect to the server with `telnet $HOSTNAME 5000`.
host,port='0.0.0.0',5000
#host=socket.gethostname() ## W10-XXXX 计算机名

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind((host,port))
server.listen(5)
print('listen',host,port)
connections = []

async def sender():
	while True:
		try:
			connection, address = server.accept()
			connection.setblocking(False)
			connections.append(connection)
		except BlockingIOError:
			pass

		for connection in connections:
			try:
				message = connection.recv(4096)
				print('recv',message)
			except BlockingIOError:
				continue

			for connection in connections:
				connection.send(message)
			
loop = asyncio.get_event_loop()
# rs=loop.create_task(start())
rs=loop.create_task(sender())
# print(rs)
# loop.create_task(receiver())
loop.run_forever()			