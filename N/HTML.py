#coding=utf-8
import sys #endswith 是为了适配qgb处于另外一个包内的情况
if __name__.endswith('qgb.N.HTML'):from .. import py
else:
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
U,T,N,F=py.importUTNF()

def get_or_input_html(response,*name):
	v= U.get(name[0],)
	# if not v:
		# raise v
	# print(v)	
	return v	
def xiaomi_air_conditioner_control(response=None,token=py.No('auto get'),t=0):
	if not token:token=get_or_input_html(response,'miio.token')
	if not token:return
	
	import miio
	d=U.get_or_set(token,
			lazy_default=lambda:miio.device.Device(ip='192.168.1.4',token=token),
		)	
		
	if not t:t=261
		
	if t<16:t=16
	if t<33:t=t*10
		
	if t<160:t=160
	if t>320:t=320
	
	d.send("set_temperature", [t] )	
	return d
ac=xiaomi_air_conditioner_control	

# def list_2d_txt_href(response,a,file_column=None,**ka):
def google_search_result_zhihu(response,hs,u_size=36+4,**ka):
	l2=[[T.sub(a,'href="','"'),T.html2txt(a)] for a in hs]     
	
	zhihu_mark='.zhihu.com/'
	dr={}
	lr=[]
	for n,(u,t) in py.enumerate(l2):
		if zhihu_mark not in u:continue
		u=T.sub(u,zhihu_mark)
		
		t=T.replacey(t,['https://www.zhihu.com ›','https://www2.zhihu.com ›','http://www2.zhihu.com ›','http://www-quic.zhihu.com ›','https://zhuanlan.zhihu.com › ...','...  更多','question','answer'
			],'').strip()
		
		iq=u.find('?')
		if iq!=-1:
			if not U.one_in(['?page='],u):
				u=u[:iq]
		if u in dr:
			if '查看所有帖子'==t:continue
			
		U.set_dict_value_list(dr,u,t)
		
		t=T.replace_all_spaces(t,' ')
		
		lr.append([U.IntRepr(n,size=4),U.StrRepr(u,size=u_size),t])
		
	# lr=U.sort(lr,c=1)	
	lr.sort(key=lambda x:x[1])
	U.set('dr',dr)
	if not response:
		return lr
	
	def html_callback(html,head):
		bs=T.BeautifulSoup(html)
		es=bs.select(f'body > table > tbody > tr > td:nth-of-type({1+1})')
		
		t=''
		for ne,e in py.enumerate(es):
			u=e.text
			ea=bs.new_tag('a')
			ea.attrs["target"]='_blank'
			t=T.eol.join(dr[u])
			ea.append(t+u)
			if '/answer/' in u:
				u='answer/'+T.sub(u,'/answer/')
			ea.attrs['href'  ]=f"zhihu://{u}"
			e.clear()
			e.append(ea)		
			
			
		html=py.str(bs)
		return html
		
		
	return list_2d(response,U.col(lr,0,1),html_callback=html_callback,**ka)
	
	# return lr	
zhihu=google_search_result_zhihu		

def fullscreen_img(response,img):
	if py.istr(img) and '://' in img:
		u=img
	else:
		k='img-%s'%py.id(img)
		U.set(k,img)
		u=U.get('rpc.server.base')+f"N.img(p,U.get({repr(k)}))"

	html='''
<!doctype html>
<html lang="en"><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>HTML5 Fullscreen API
</title>

<style type="text/css">
body {
	background-color: #f3f3f3;
	margin: 0; /* 修复 左上 白边  【user agent stylesheet 8px】无效 */
}

.html5-fullscreen-api {
	position: relative;
}
.html5-fullscreen-api img {
	max-width: 100%;
	border: 0px solid #fff;
	box-shadow: 0px 0px 50px #ccc;
}
.html5-fullscreen-api .fs-button {
	z-index: 100;
	display: inline-block;
	position: absolute;
	top: 0px;
	right: 0px;
	cursor: pointer;
}
.html5-fullscreen-api .fs-button:after {
	display: inline-block;
	width: 100%;
	height: 100%;
	font-size: 32px;
	font-family: 'ModernPictogramsNormal';
	color: rgba(255,255,255,.5);
	cursor: pointer;
	content: "v";
}
.html5-fullscreen-api .fs-button:hover:after {
	color: rgb(255,255,255);
}
#fullscreen:-webkit-full-screen .fs-button:after {
	content: "X";
}
#fullscreen:-webkit-full-screen {
	width: 100%;
}
#fullscreen:-webkit-full-screen img {
	display: block;
	height: 100%;
	margin-left: auto;
	margin-right: auto
}

#fullscreen:-moz-full-screen .fs-button:after {
	content: "X";
}
#fullscreen:-moz-full-screen {
	width: 100%;
}
#fullscreen:-moz-full-screen img {
	display: block;
	height: 100%;
	margin-left: auto;
	margin-right: auto;
}

img{
		width:100%;
		padding: 0 0 0 0;		
		margin: 0 0 0 0;
		
}

</style> 

<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

<script>
$(document).ready(function(){
	$('.fs-button').on('click', function(){
		var elem = document.getElementById('fullscreen');

        if (
            document.fullscreenEnabled ||
            document.webkitFullscreenEnabled ||
            document.mozFullScreenEnabled ||
            document.msFullscreenEnabled
        ) {
            if (
                document.fullscreenElement ||
                document.webkitFullscreenElement ||
                document.mozFullScreenElement ||
                document.msFullscreenElement
            ) {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                } else if (document.mozCancelFullScreen) {
                    document.mozCancelFullScreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
            } else {
                if (elem.requestFullscreen) {
                    elem.requestFullscreen();
                } else if (elem.webkitRequestFullscreen) {
                    elem.webkitRequestFullscreen();
                } else if (elem.mozRequestFullScreen) {
                    elem.mozRequestFullScreen();
                } else if (elem.msRequestFullscreen) {
                    elem.msRequestFullscreen();
                }
            }
        } else {
            alert('Fullscreen is not supported on your browser.');
        }
	});
});

setTimeout(function(){
	// $('.fs-button').click()
},666)
</script>
</head>

<body>

<div id="fullscreen" class="html5-fullscreen-api">
	<img src="img_url">
	<span class="fs-button"></span>
</div>


</body>
</html>

'''.replace('img_url',u) # %py.locals()
	response.headers['Content-Type']='text/html;charset=utf-8';
	response.set_data(html)
	return 	html
fsimg=imgfs=fullscreen_img

def a_href(response,u=''):
	if not u:
		u=U.cbg()
	u=N.auto_url(u)
	html=f"""
<a href="{u}">{u}</a>	
	"""
	response.headers['Content-Type']='text/html;charset=utf-8';
	response.set_data(html)
	return 
HREF=URL=href=a_href	




def list_2d_txt_href(response,a,file_column=None,**ka):
	file_column=U.get_duplicated_kargs(ka,'file_column','cf','fc','f_col','fcol','fcolumn',default=file_column)
	def file_column_callback(html,head):
		nonlocal file_column,a
		if not py.isint(file_column):return html
		
		if file_column <0:file_column=py.len(a[0])+file_column
		from bs4 import BeautifulSoup
		
		from flask import request
		rpc_base=request.url_root[:-1]+U.get_or_set('rpc.server.base','/')
		url_read='a=N.geta();r=F.read(a)%23-'
		url_read='a=N.geta();N.flask_text_response(p,F.read(a))%23-'#fix 有些txt文件会变下载框
		# url_read='a=N.geta();N.html(p,F.read(a))%23-'
		
		bs=T.BeautifulSoup(html)
		# if debug:
			# U.set('html',html)
			# U.set('bs',bs)
		es=bs.select(f'body > table > tbody > tr > td:nth-of-type({1+file_column})')
		for ne,e in py.enumerate(es):
			f=a[ne][file_column]
			# if e.text!=f:
				# print('#error a[',ne,file_column,'!= e.text')
				# continue
				
			# e.string.replace_with(f'<a href="http://{request.remote_addr}/{f}">{f}</a>' )	
			# U.get_or_set('es.list',[]).append(e)
			# ea=BeautifulSoup(f'<a href=>{f}</a>'			
			ea=bs.new_tag('a')
			# ea.attrs['href']=f"http://{request.remote_addr}/{f}"
			# ea.attrs['href'  ]=f"{rpc_base+url_read}{f}"
			ea.attrs['href'  ]=f"{U.get_or_set('rpc.server.base','/')}{url_read}{f}"
			ea.attrs["target"]='_blank'
			ea.append(f)
			
			e.clear()
			e.append(ea)		
			
			
		html=py.str(bs)
		return html
	
		# def file_column_callback():pass
	return list_2d(response,a,html_callback=file_column_callback,**ka)
		
list_2d_txt=list_2d_txt_href

list_2d_CSS_MARK='/*css*/'
def list_2d(response,a,html_callback=None,index=False,sort_kw=U.SORT_KW_SKIP,debug=False,**ka):
	index=U.get_duplicated_kargs(ka,'index','n','enu','add_index','enumerate',default=index)
	sort_kw=U.get_duplicated_kargs(ka,'skw','sort','s',default=sort_kw)
	a=U.sort(a,sort_kw=sort_kw)
	# return a

	# request,ucode,urla=N.geta(return_other_url={'url_decode':1,
	# '%23-':1
	# },return_request=True)
	
	import pandas as pd
	df = pd.DataFrame(data=a)
	html=df.to_html(index=index) 
	
# <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
	head='''
<head>
<style type="text/css">
	table,th,td,textarea{
		padding:0px;
		margin:0px;
		border:1px solid green;/*没有solid 导致分割线消失*/
		border-spacing: 0px;
	}
	/*css*/
</style> 
</head>
'''	
	html=head+html
	if py.callable(html_callback):
		html=html_callback(html=html,head=head)

	if debug:return html
	
	response.headers['Content-Type']='text/html;charset=utf-8';
	response.set_data(html)
	return a
list=table=l2d=_2d_list=list2d=list_2d

def everything_search_image(response,add_offset=32,**ka):
	U.r(py,U,T,N,F,N.HTTP,N.HTML,)
	add_offset=U.get_duplicated_kargs(ka,'add_offset','offset','oa','ao','add',default=add_offset)
	# py.pdb()()
	# ucode=T.url_decode(ucode)
	# if not ucode.endswith('%23-'):
		# ucode+='%23-'
	request,ucode,a=N.geta(return_other_url={'url_decode':1,'%23-':1},return_request=True)
	
	U.set('rf',request.form )
	if request.form.get('a',''):	
		a=request.form.get('a','')

	
	if a:a=U.set('esimg.a',a)
	else:a=U.get('esimg.a')
	
	dua=T.parse_url_arg(a)     
	offset=py.int(dua.get('offset',0))
	search=dua['search']#,'')
	
	def offset_url(previous=False):
		if add_offset:
			if previous:
				return T.replace_url_arg(a,'offset',offset-add_offset)
			else:	
				return T.replace_url_arg(a,'offset',offset+add_offset)
		else:	
			return a
		# U.print_repr(add_offset,request.form,ucode,a,newa)	
		
		
	es_base='http://'+T.get_url_netloc(a)
	h=N.HTTP.get(a,proxy=0)
	bs=T.BeautifulSoup(h)
	efs=bs.select('td[class=file]  a')
	# U.set('es',[h,bs,fs])
	r=r"""
<meta name="viewport" content="width=device-width, initial-scale=0.3, minimum-scale=0.3, maximum-scale=1.0,user-scalable=0" cmt=禁止缩放/> 
	
<style type="text/css">
html,body{margin:0;pading:0;}/*不然两侧有空白*/	
img{
		width:100%;
		padding: 0 0 0 0;		
		margin: 0 0 0 0;
	}
/*

height: 25px;
*/	

	input,div{
border:1px solid #000000;
width: 99%;/*不然桌面会有下侧滚动条*/
overflow-x: auto;
white-space: nowrap;
overflow-y: hidden;
}
textarea.img_path{
	font-size:1.5vh; /*相对 屏幕高度*/
	direction: rtl; /*
		text-align: right;
		
		从右向左超出*/
	width:100%;
	padding:0px;
	margin:0px;
	border:1px solid #00000022; /*修复调整 textarea大小导致下分割线消失的问题*/
	border-spacing: 0px;
	resize: none; /*禁用 调整大小*/
	white-space: pre;/*以下3行，禁用 自动换行 */
	overflow-wrap: normal;
	overflow-x: scroll;
	
	height:2.3vh; /*隐藏滚动条 后，下方很多空白*/
}



textarea.img_path::-webkit-scrollbar,div::-webkit-scrollbar {
	display: none;    /* 隐藏滚动条 */
} 

div.scroll{
	height:15%;
	font-size:3vh;
	background:grey;
}

br {
   display: block;
   margin: 10px 0;
}

.submit{
	font-size:3vh;
	height:31%;
	width:99%;/*不然桌面会有下侧滚动条*/
	background:green;	
	text-align: left;
}

div.submit{
	height:15%;
}
input[type="text"]{
	font-size:1.8vh;
	
}

/*
	# height:555;
	# background:grey;

*/

</style> 

<script src="http://libs.baidu.com/jquery/2.1.4/jquery.min.js"></script>
<script>

 
</script>
	
"""+f"""
<form method="post" enctype="multipart/form-data" action="{ucode+offset_url(previous=True)}">
	<input type="text" name="a" value="{T.url_decode(offset_url(previous=True))}"/>
	<button type="submit" class="submit" id="previous" value="">
		↑ input[type="text"] added (previous=True)<br>
		current offset {offset} see browser url bar!<br>
		previous offset - {add_offset}
	</button>
</form>	

<div class="scroll" onclick="window.scrollTo(0, document.body.scrollHeight);">scroll to bottom</div>		

<div class="submit" onclick="document.getElementById('next').click()">next offset + {add_offset}</div>		

<!-- 

-->	
"""	

	for n,e in py.enumerate(efs):
		u=es_base+e.get('href')
		se=f''' <img src={u}>	
<textarea class="img_path">{n}{T.url_decode(u)}</textarea>		
		'''
		#RTL 文字从右至左  注意使用 f-string 执行顺序问题
#很奇怪 加空格显示 n总是在u的后面		
#>=={'77{} {} 99'.format(n,u)}++ 显示 ++http://192.168.1.3/C%3A/test/xsnvshen_a/24936/33978-8.jpg 99 772
#复制出来不是
		r+=se
	r=r+f'''	
<div class="scroll" onclick="window.scrollTo(0,0);">scroll to head</div>		
	
<div class="submit" onclick="document.getElementById('previous').click()"> previous offset - {add_offset}</div>			
	
<form method="post" enctype="multipart/form-data" action="{ucode+offset_url(previous=False)}">
	<input type="text" name="a" value="{T.url_decode(offset_url(previous=False))}"/>
	<button type="submit" class="submit" id="next" value="">
		↑ input[type="text"] added (previous=False)<br>
		current offset {offset} see browser url bar!<br>
		next offset + {add_offset}
	</button>
</form>		
'''	
	# response.set_data( h)
	response.headers['Content-Type']='text/html;charset=utf-8';
	response.set_data(r)
	return efs
esimg=everything_search_image

def format(s,**ka):
	ka={'{%s}'%k:v for k,v in ka.items()}
	return T.replacey(s,ka)

def eng_audio(response,word):
	f='google_translate_tts/%s.dill'%word
	F.mkdir(U.gst+F.dir(f))
	q=F.dill_load(f)
	if not q:
		q=F.dill_load('google_translate_tts/%s.dill'%U.StrRepr(word,size=15) )
	if not q:
	
		if N.check_port(21080):
			proxy='socks5://127.0.0.1:21080'
		else:	
			proxy=None
	
		try:
			u='https://translate.googleapis.com/translate_tts?client=gtx&ie=UTF-8&tl=en&tk=775040.775040&q='+T.url_encode(word)
			q=N.HTTP.request(u,proxy=proxy,timeout=6)
			b=q.content
			F.dill_dump(file=f,obj=q)
		except Exception as e:
			return py.No(e)
	if response:	
		return N.copy_request_to_flask_response(q,response)
	else:
		return q
	
def eng_dwi(response,dwi,ecdict=py.No('auto load'),sort_kw={},**ka):
	if not ecdict:
		ecdict=U.get_or_dill_load_and_set(r'C:\test\ecdict-770611.dill')
		# F.dill_load()
	
	sort_kw=U.get_duplicated_kargs(ka,'skw','sort','s',default=sort_kw)
	
	
	K_deci='deci-%s'%py.id(ecdict)
	deci=U.get(K_deci)
	if not deci:
		deci=U.get_or_set(K_deci,{i.word:n for n,i in enumerate(ecdict)},)
		
		
	def get3(w,count=0):
		row=ecdict[deci[w]]
		zh=row.translation.replace('\\n','\n')
		return count or dwi[w],w,zh
	r=[]
	re=[]
	rw=[]
	for w,count in dwi.items():
		if w in deci:
			rw.append(w)
			r.append(get3(w),)
		else:
			re.append(w)
	ree=[]		
	for w in re:
		wl=w.lower()
		if wl in deci and wl not in rw:
			r.append(get3(wl,count=dwi[w]),)
		else:
			ree.append(w)
			
	U.set('eng_dwi.ree',ree)		
	U.set('eng_dwi.dree',{w:dwi[w] for w in ree})		
	if sort_kw:
		r=U.sort(r,**sort_kw)
	return eng_list(response,r)		
def eng_list(response,a):
	'''

<meta name="viewport" content="width=device-width, initial-scale=0.5, minimum-scale=0.5, maximum-scale=1.0,user-scalable=1" cmt=禁止缩放/> 



<button style="height:33; width: 77%; " id=btn onclick="document.getElementById('btn').innerText=(window.outerWidth - 8) / window.innerWidth"></button>

'''    	
	if not a:
		response.set_data('eng_list not a %r'%a)
		return a
	main=''
	la0=len(a[0])
	is_namedtuple=py.getattr(a[0],'_fields',None)
	n=-1
	for row in a:
		# n,en,zh=-1,'',''
		if la0!=3:n+=1
		if la0==2:  en,zh=row
		if la0==3:n,en,zh=row
		if is_namedtuple:# len==13
			en=row.word
			zh=row.translation.replace('\\n','\n')
		main+=r'''
<tr>
	<th class="num" onclick="play('{en}')">{n}</th>
	<th class=en onclick="play('{en}')"> <a>{en}</a>		</th>
	<th class=zh onclick="play('{en}')">{zh}</th>
</tr> 	
'''.format(n=n,en=en,zh=zh)

	r=T.html_template(globals=py.globals(),locals=py.locals(),s=r'''


	
<style type="text/css">

table,th,td,textarea{
	padding:0px;
	margin:0px;
	border:1px solid #00000022;/*修复调整 textarea大小导致下分割线消失的问题*/
	border-spacing: 0px;
	font-size: 3.5vh;
}
.num{
	width:5%;  
}
.en{
	width:45%;  
}
.zh{
	width:45%;  
}

</style>	


<table id="mytable" style=" width: 100%; ">
<thead>
	<tr>
		<th class="num">NO.</th>
		<th class=en>English		</th>
		<th class=zh>Zh</th>
	</tr> 	
	  
</thead>
    <tbody>

$main$
	
	</tbody>
  </table>	
	
	
<div style=" position:fixed; left:0px; bottom:0px; width:100%; height:5vh; background-color:#00aa00BB; z-index:9999;">
<input id="find" type="text" style=" display: inline-block;width:80%; height:100%;font-size: 4vh; color:red; background-color:#00aa0011;" onchange="find()">
</input>

<button style="    float:right;  width:20%; height:100%; color:blue;" onclick="window.location.reload(true);font-size:33vh;"> Z </button>

<button style="    float:right;  width:20%; height:100%; color:blue;" onclick="window.location.reload(true);font-size:33vw;"> S </button>

</div>

<script>
function play(word){
	console.log(word)
	var audio = new Audio();
	audio.src ="$U.get_or_set('rpc.server.base','/')$a=N.geta();N.HTML.eng_audio(response,a)%23-" + encodeURI(word);
	audio.play();
}

var dtx = new Map() //{} //Uncaught TypeError: dtx.get is not a function
var dtn = new Map() 

function find(){
	var t=document.getElementById('find').value
	var sx="//th[@class='en' and contains( .,'"+t+"')]"
	// if(var x=) Uncaught SyntaxError: Unexpected token var
	if(x=dtx.get(t)){ 
		
	}else{
		var x=document.evaluate("//th[@class='en' and contains( .,'"+t+"')]", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null)
		dtx.set(t,x)
	}
	
	if(x.snapshotLength){
	
	}else{
		
	
	}
	
	
	
	e=xpath(sx)
	
	e.scrollIntoView()
	e.setAttribute('style','color:yellow')
	e.click()
	scrollBy(0,-99)
	setTimeout(function(){
		e.setAttribute('style','color:black')
	
	},666)
	
	// document.getElementById('find').innerText=new Date()
}

function xpath(sp,ele){
    //var sp = "//a[text()='SearchingText']";
	if(ele){
		if(!sp.startsWith('.')){
			sp='.'+sp
		}
	}else{
		ele=document//直接重新赋值参数不用加 var
	}
    return document.evaluate(sp, ele, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}//end xpath


function disable_scale(){
	var metaTag=document.createElement('meta');
	metaTag.name = "viewport"
	metaTag.content = "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0"
	document.getElementsByTagName('head')[0].appendChild(metaTag);


}

//setTimeout(,3333)


</script>
	
	''')
	response.headers['Content-Type']='text/html;charset=utf-8';
	response.set_data(r)
	return a
def flask_ls(response,request=None):
	if not request:from flask import request
	r=T.html_template(globals=py.globals(),locals=py.locals(),s='''
<a href=></a>
	
	''',)
	
def flask_get_all_upload_files(upload_dir=py.No('U.gst/upload_dir',no_raise=1),save_size=py.No('8 MB',no_raise=1),request=None,):
	'''save_size <=0 : save_all
	'''
	from shutil import copyfileobj
	# U,T
	if not request:from flask import request
	if not upload_dir:
		upload_dir=U.get_or_set('rpc.server.upload_dir',U.gst+'upload_dir/')
	else:
		upload_dir=U.set('rpc.server.upload_dir',upload_dir)
	F.mkdir(upload_dir)
	if not save_size:
		save_size= U.get('rpc.server.upload.save_size',1024*1024*8)
	save_size=F.IntSize(py.int(save_size))	
	U.set('rpc.server.upload.save_size',save_size)	
	
	d={}
	for k,f in request.files.items(multi=True):# 默认multi=False，始终只能获取一个，坑！
		b=f.stream.read(save_size)
		if py.len(b)<save_size:
			if py.len(b)>99:
				sr="<{0} >'{1}...{2}'".format(F.readable_size(b),repr(b[:50])[2:-1],repr(b[-50:])[2:-1])  
				d[f]=U.object_custom_repr(b,repr=sr)
			else:
				d[f]=b
		else:
			fn=upload_dir+f.filename
			with py.open(fn,'wb') as fp:
				fp.write(b)
				copyfileobj(f.stream, fp)
			d[f]=fn
			
	return d
		# f.save(f.name)
files=save_file=save_files=flask_files=flask_save_all_upload_files=flask_get_all_upload_files	
	
ghtml_txt='''
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<style type="text/css">
	input[type="submit"]{
		width:100%;
	}
	input.url{
		width:49%; /*50% break line*/
	}	
	button.edit_btn{
		height: 33;
		width: 44;
		padding: 0 0 0 0;		
		margin: 0 0 0 0;		
	}
</style> 
</head>
	
<form method="post" enctype="multipart/form-data" action="$U.get_or_set('rpc.server.base','/')$r=U.set_multi($name$_form=request.form,$name$_files=N.HTML.flask_get_all_upload_files(),$name$_data=q.get_data(),);F.dp(request.form,'$name$_form');">
	<input type="submit" />
	<hr>
	<input type="file" multiple name="f">
	<hr>
	<div>
		<small style="
			padding: 22;
		">$name$:</small>
<!-- indent outdent 无效 -->
<button type="button" class="edit_btn" onclick="edit(this.innerText)">indent</button>
<button type="button" class="edit_btn" onclick="edit(this.innerText)">outdent</button>

<button type="button" class="edit_btn" onclick="edit(this.innerText)">forwardDelete</button>
<button type="button" class="edit_btn" onclick="edit(this.innerText)">delete</button>
<button type="button" class="edit_btn" onclick="edit('selectAll');edit('delete')">del all</button>
<!-- \n 不行，语法错误，被onclick转义了一次 -->
<button type="button" class="edit_btn" onclick="edit('insertText','\\n')">Enter</button>

<button type="button" class="edit_btn" onclick="edit(this.innerText)">selectAll</button>
<button type="button" class="edit_btn" onclick="edit(this.innerText)">paste</button>
<button type="button" class="edit_btn" onclick="edit(this.innerText)">copy</button>
<button type="button" class="edit_btn" onclick="edit(this.innerText)">cut</button>

<button type="button" class="edit_btn" onclick="edit(this.innerText)">undo</button>
<button type="button" class="edit_btn" onclick="edit(this.innerText)">redo</button>



	</div>
	
	
	<div style="height:60%;" > 
		<textarea id="textarea" name="t" style="width:100%; height: 100%;" >$(F.dl('t_form') or U.get('t_form') or {}).get('t','')$</textarea>
	</div>
	
	<hr>
	<input type="submit" />
	<input id=url_start class=url type="text" name="url_start" 
commt="/-                         U.set('rpc.server.upload.save_size',...code... "
value="$U.get('rpc.server.base')#$U.set('rpc.server.upload.save_size',$U.int_exp(U.get('rpc.server.upload.save_size',8*1024*1024),1024)#$);">
	<input id=url_end   class=url type="text" name="url_end" value="%23-">
</form> 
<script> 
function edit(command,text){
	document.querySelector('textarea#textarea').focus()
	return document.execCommand(command, true,text);
}

var form  = document.querySelector('form');
var original_action=form.getAttribute('action');
original_action=original_action.substr($len(U.get('rpc.server.base'))#$) 
// if(original_action.startsWith('/')){
//}
document.querySelector('input#url_start').addEventListener('input', function(e){
	if(!e.srcElement.value.endsWith(';')){
		e.srcElement.value+=';'
	}
	
	form.setAttribute('action',e.srcElement.value+original_action)
	console.log(form.getAttribute('action'))
});
document.querySelector('input#url_end').addEventListener('input', function(e){
	form.setAttribute('action',original_action+e.srcElement.value)
	console.log(form.getAttribute('action'))
});

</script>
'''	
def textarea(response,name='t',upload_dir=py.No('U.gst/upload_dir',no_raise=1),):
	"""
	 <input type="text" name="t">
	
	"""
	U.r(N.HTML)
	if not U.all_in(name,T.aZ+'_'):
		raise py.ArgumentError(name,'must be alphabet_')
	r=T.html_template(globals=globals(),locals=locals(),s=ghtml_txt,)
	# r=format(r,name=name)
	response.headers['Content-Type']='text/html;charset=utf-8';
	return response.set_data(r)
txt=text=textarea
	
def html_script(response,*urls,rpc_base=None,max_show_len=999):
	if not rpc_base:rpc_base=U.get_or_set('rpc_base','/')
	html=''
	for url in urls:
		if ('://' not in url) and (not F.exist(url) ):
			html+="""
<hr>
{url}
<hr>
<script> {url} </script>
			
			""".format(url=url)
			continue
		html+="""
<hr>
{url}
<hr>
{js}
<script src="{rpc_base}r=N.get('''{url}''')">
</script>

	""".format(url=url,rpc_base=rpc_base,js=N.get(url)[:max_show_len] ) 
	return N.flask_html_response(response=response,remove_tag=[],html=html )
N.html_script=N.htmlScript=N.script=html_script

G_SELECT_ID=U.get_or_set(__name__+'.G_SELECT_ID','__qgb_id__') # 注意千万不能和待选择的key相同
G_SELECT_URL=U.get_or_set(__name__+'.G_SELECT_URL','__qgb_url__')
gid_select=U.get_or_set(__name__+'.gid_select',{})
def select_result(q,response,**ka):
	if N.is_flask_request(q):
		q=q.values
	if G_SELECT_ID not in q:
		raise py.ArgumentError('要post {id:,k...} 后的 request.values, 直接用get不带参数 是不行的。',q,response,ka)
	# if 'id' not in r:
	# 	raise py.ArgumentError('r not have id !',r)

	# if id not in gid_select:
	# 	raise py.ArgumentError('not found id in gid_select:',r)

		# if k not in r:
		# 	raise py.ArgumentError('unexpected submit key (must in r or disabled) :',k,v,q)
	qs=py.set()
	for k,v in q.items():
		if k==G_SELECT_URL:
			ka['url']=v
			continue
		if k==G_SELECT_ID:
			# id=v
			# id=py.int(id)
			r=gid_select[ py.int(v) ]
			disabled=r.disabled # 检查是否是 select对象
			continue
		if v!='on':
			raise py.ArgumentError('unexpected submit value (must be "on") :',k,v,q)
		k=int(k)		
		qs.add(k)
	# q=dict(q) # 如果不进行转换 就 id=q.pop('id')  TypeError("'CombinedMultiDict' objects are immutable")
	
	r.update_status(qs)
	# for k in py.list(r):
	# 	if id(k) not in qs:
	# 		r.move_to_disabled(k)
	# 		# ##disabled[k]=r.pop(k)
	# 		continue
	
	# for k in py.list(disabled):
	# 	if id(k) in qs:
	# 		r.move_back(k)
			# r[k]=disabled.pop(k)
			# continue

	return select(r,response=response,**ka)

def select(iterable,**ka):
	'''
#<!-- 
				# 不能用  editable="false" readyonly  
				#   <h6>包裹input无效 </h6>   
				# background="green" 无效 , lavender淡紫色, 熏衣草花 ,#e6e6fa 太淡啦
				#  -->	
	 '''
	response=U.get_duplicated_kargs(ka,'p','resp','response','rp')
	request=U.get_duplicated_kargs(ka,'q','req','request','requests','rq')
	url=U.get_duplicated_kargs(ka,'url','mark_url', 'request_url')
	 
	if N.is_flask_request(request) and not url:
		url=request.url	
	if N.is_flask_request(url):
		url=request.url
	if url:
		url=T.url_decode(url)
	else:
		url=''
	
	ha='''
<head>
	<style type="text/css">
		textarea {
			background: lightgoldenrodyellow;
			width:80%;
			
			# rows:1; # 无效

		}

	</style>
</head>	
<form action="/r=N.HTML.select_result(request,response)%23"  method="post">
	{rows}
	<input type="submit" > 
</form>

'''
		####################
	hd='''
<span > {i} </span>
<input type="checkbox" name="{name}" {checked} > {k} </input>
<textarea> {v} </textarea>
<hr>'''
	########################
	def do_resp(r,kv,disabled):
		if response:
			rows='''
<input  type="text"  readonly="readonly"  name="{G_SELECT_ID}" value={id}  style="
    # background: aqua;
    background: cyan;
" >
<input  type="text"  readonly="readonly"  name="{G_SELECT_URL}" value={url} style="
    background: lightgray;
	width:80%
"> 
<br>
			'''.format(url=url,id=id,   G_SELECT_ID=G_SELECT_ID,G_SELECT_URL=G_SELECT_URL   )
			i=0
			# fk=lambda k: T.html_encode(repr(k))  #为啥会出现 0 ☑ q." checked > '
			fk=lambda _k:T.html_encode(repr(_k))  
			fv=lambda _v:T.html_encode(repr(_v)[:155-1] )# 全中文 80% 正好两行
			# U.msgbox(py.list(kv)[:9])
			for k,v in kv:
				# k,v=fk(k),fv(v)
				# U.msgbox(k,v)
				rows+=hd.format(i=i,name=r.id(k,v), k=fk(k),v=fv(v) ,checked='checked')
				i+=1
			for k,v in disabled:
				# k,v=fk(k),fv(v)
				rows+=hd.format(i=i,name=r.id(k,v), k=fk(k),v=fv(v) ,checked='')
				i+=1
			# py.importU().log(rows)	
			response.headers['Content-Type']='text/html;charset=utf-8';
			response.set_data(    T.format( ha, rows=rows  )     )	
		return r

	id=getattr(iterable,'id',0)
	if not id:
		id=py.id(iterable)
	if py.isdict(iterable):
		if isinstance(iterable,DictSelect):
			rd=iterable
		elif id not in gid_select:
			rd = gid_select[id]=DictSelect(iterable)
			rd.id=id
		else:
			rd = gid_select[id]
		return do_resp(rd,rd.items(),rd.disabled.items())

	if py.islist(iterable):
		if isinstance(iterable,ListSelect):
			rd=iterable
		elif id not in gid_select:
			rd = gid_select[id]=ListSelect(iterable)
			rd.id=id
		else:
			rd = gid_select[id]
		return do_resp(  rd,enumerate(rd),enumerate(rd.disabled) 	)

################################################

class ListSelect(py.list):
	'''
	'''
	def __init__(self,*args, **ka):
		'''Initialize an ordered dictionary.  The signature is the same as
		regular dictionaries.  Keyword argument order is preserved.
		'''
		if not args:
			raise TypeError("descriptor '__init__' of select object "
							"needs an argument")
		# self, *args = args
		if len(args) > 1:
			raise TypeError('expected at most 1 arguments, got %d' % len(args))
		super().__init__(*args)
		# args=args[0]

		try:
			self.disabled=args.disabled # 没有类型检查，self 与 disabled 类型不同就完蛋
		except AttributeError:
			try:
				self.disabled
			except AttributeError:
				self.disabled=[]

	def id(self,k,v):
		return py.id(v)
	
	def update_status(self,ids):
		si=py.set()
		
		# for i,v in enumerate(self.disabled):

		for i,v in enumerate(self):
			if id(v) not in ids:
				si.add(i)
		n=0
		for i in si:
			v=self.pop(i+n)
			self.disabled.append(v)
			n=n-1
				# self.disabled.append(v)


class DictSelect(py.dict):
	'''
	'''
	def __init__(*args, **ka):
		'''Initialize an ordered dictionary.  The signature is the same as
		regular dictionaries.  Keyword argument order is preserved.
		'''
		if not args:
			raise TypeError("descriptor '__init__' of 'DictSelect' object "
							"needs an argument")
		self, *args = args
		if len(args) > 1:
			raise TypeError('expected at most 1 arguments, got %d' % len(args))
		args=args[0]

		try:
			self.disabled=args.disabled # 没有类型检查，self 与 disabled 类型不同就完蛋
		except AttributeError:
			try:
				self.disabled
			except AttributeError:
				self.disabled={}

		self.update(args, **ka)

	# def disable(self,key):
