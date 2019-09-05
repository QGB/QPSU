#coding=utf8
import sys;'qgb.U' in sys.modules or sys.path.append('E:/QGB/babun/cygwin/bin/')
import sys;'qgb.U' in sys.modules or sys.path.append('./');
from qgb import *

from wdom.tag import H1
from wdom.document import set_app,get_document
from wdom.server import start
import wdom

q=F.dill_load(F.getHome()+'(sys.q) = [0 (102 )].dill')[0]

def iterQ():
	for p in q:
		for s in p:
			h=wdom.tag.Div()
			h.innerHTML=s
			yield h

# U.ipy_embed()()
if __name__ == '__main__':
	document = get_document()
	# for i in iterQ():
		# document.appendChild(i)
	div=wdom.tag.HTMLIFrameElement()
	div.innerHTML=N.HTTP.get('http://192.168.1.111:23571/r=sys.q[-1][-1]')
	document.appendChild(div)
	
	set_app(document) # equivalent to `wdom.document.get_document().body.appendChild(h1)`
	start()