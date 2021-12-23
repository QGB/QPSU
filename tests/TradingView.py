#coding=utf-8   
import sys,pathlib # *.py  /tests /qgb   /[gsqp]
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

def getBars():
	from flask import request
	U.get_or_set('tv',[]).append(U.dir(request))
	a=N.geta()
	d=T.parse_url_arg(a)
	
	return a
	
	