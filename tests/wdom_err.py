#coding=utf-8
import sys,pathlib				 # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()


from wdom.tag import H1
from wdom.document import set_app,get_document
from wdom.server import start
import wdom

# q=F.dill_load(F.getHome()+'(sys.q) = [0 (102 )].dill')[0]

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
	div.innerHTML='<a href>23333333</a>'
	# div.innerHTML=N.HTTP.get('http://192.168.1.111:23571/r=sys.q[-1][-1]')
	document.appendChild(div)
	
	set_app(document) # equivalent to `wdom.document.get_document().body.appendChild(h1)`
	start()