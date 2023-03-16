#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import socket
import threading
import time

gd={}

def handle_client(conn, addr):
	t=threading.current_thread()
	gd[addr]=[]

	print(t,"starting")

	# recv message
	while True:
		message = conn.recv(1024)
		# message = message.decode()
		if not message:break

		gd[addr].append(message)
		m=len(gd[addr])
		if m%2000==1:
			print(U.stime(),t, addr, m)
	
	# simulate longer work
	# time.sleep(5)

	# send answer
	# message = "Bye!"
	# message = message.encode()
	# conn.send(message)
	# print("client:", addr, 'send:', message)
	
	conn.close()

	print(t,"ending")
   
# --- main ---

host = '0.0.0.0'
port = 3344

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # solution for "[Error 89] Address already in use". Use before bind()
s.bind((host, port))
s.listen(1)

all_threads = []

def run():

	try:
		while True:
			print("Waiting for client")
			conn, addr = s.accept()
		
			print("Client:", addr)
			
			t = threading.Thread(target=handle_client, args=(conn, addr))
			t.start()
		
			all_threads.append(t)
	except KeyboardInterrupt:
		print("Stopped by Ctrl+C")
	finally:
		if s:
			s.close()
		for t in all_threads:
			t.join()
		
		