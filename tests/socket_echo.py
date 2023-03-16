#coding=utf-8
import sys,pathlib               # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0',3344))
s.listen(1)
conn, addr = s.accept()
while 1:
	data = conn.recv(1024)
	if not data:
		break
	conn.sendall(data)
	print(U.stime(),data)
conn.close()

