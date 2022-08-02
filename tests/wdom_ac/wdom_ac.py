#coding=utf-8
import sys,pathlib				 # .py/wdom_ac/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

from qgb import pil
import tornado


from wdom.tag import H1
from wdom.document import set_app,get_document
from wdom.server import add_static_path
import wdom #不显示导入 wdom.server，会找不到

static_path=[i for i in sys.path if i.endswith('site-packages')][0]+'/streamlit/static/'

static_path=U.get_current_file_dir()
print(static_path)
add_static_path('static',static_path)


# w=sys.modules[__name__]
# doc._Document__html.outerHTML  .html  #这个无法更改
# doc._Document__html.innerHTML  #这个不能更改，否则就算你改回来，所有事件失效，元素无法控制，不能添加新元素。
						#你只能硬改_Document__html来显示
# h1.style.backgroundColor='red'  
# h1.style.color='red'  # 在IPY 中，我首先设置颜色无效，直到我设置textContent 才忽然变过来并可正常改变
#h1.style.backgroundColor='#112233'
# while True:
    # h1.style.backgroundColor='#'+''.join([U.random_choice(T.HEX) for i in range(6)])
    # U.sleep(0.02)
    # U.ct(_i)
######

doc=document=get_document()

app=wdom.server.get_app()
def set_extra_headers(self, path):
	self.set_header("Cache-control", "no-cache")
app.set_extra_headers=set_extra_headers



# picnic 蓝色按钮
from wdom.themes import bagpakk,baseguide,bijou,blaze,bootstrap3,bootstrap4,bulma,concise,default,foundation,furtive,groundwork,ink,kathamo,kube,mdl,milligram,mui,papier,picnic,pure,schema,semantic,siimple,skeleton,skyblue,spark,spectre,vital
###
# vital.css_files=['/static/vital.css']
# doc.register_theme(vital)

def set_temperature(event):
	t=event.target
	v=py.float(event.target.value)
	
	
	pt=doc.getElementById('pt')
	
	pt.textContent=f'{event.target.value}'
	
	bg=doc.body.style.backgroundColor
	inv=pil.get_max_distance_color_from_color10(bg)
	# print(bg,inv)
	pt.style['color']=inv
	
	N.HTML.xiaomi_air_conditioner_control(t=v)

def load_html():
	html=F.read(static_path+'index.html')
	doc.body.innerHTML=html
	# doc.register_theme(getattr(wdom.themes,U.parseArgs().str))
	# doc.body.style.backgroundColor='#0f0035F0'
	doc.body.style.backgroundColor='black'
	
	t=doc.getElementById('t')
	t.addEventListener('input',set_temperature)
	
	
	doc.getElementById('exit').addEventListener('click',lambda event:U.exit() ,)
	return
	
	getime	 =doc.getElementById('time')
	gefirst	 =doc.getElementById('first')
	geprev	 =doc.getElementById('prev')
	genext	 =doc.getElementById('next')
	gelast	 =doc.getElementById('last')
	gerealtime =doc.getElementById('realtime')
	gepageNum	 =doc.getElementById('pageNum')
	gepageCount=doc.getElementById('pageCount')
	getb  =doc.getElementById('mytable')
	
	globals().update(locals().copy())
	gefirst.addEventListener('click',first)
	geprev.addEventListener('click',prev)
	genext.addEventListener('click',next)
	gelast.addEventListener('click',last)
	gepageNum.addEventListener('input',onPageNum)
	
	update(gip)


giport=30000
girpcPort=23571
def start(port='auto',rpcPort='auto 23571'):
	global giport,girpcPort
	
	if not py.isint(port):
		port=giport
	if not py.isint(rpcPort):
		rpcPort=girpcPort
		# if U.iswin():
			# rpcPort=port+1
	print('port:',port)
	giport=port
	girpcPort=rpcPort
	
	from wdom.server import start_server
	start_server(address='0.0.0.0',port=port,autoreload=True)
	
	import asyncio
	loop=asyncio.get_event_loop()
	t=U.thread(target=loop.run_forever)
	t.start()
	
	N.rpcServer(port=rpcPort,locals=globals(),globals=globals())
	
if __name__ == '__main__':
	load_html()
	start(port=U.parseArgs(int=giport).int)
 