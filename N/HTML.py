#coding=utf-8
import sys #endswith 是为了适配qgb处于另外一个包内的情况
if __name__.endswith('qgb.N.HTML'):from .. import py
else:
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
U,T,N,F=py.importUTNF()

def format(s,**ka):
	ka={'{%s}'%k:v for k,v in ka.items()}
	return T.replacey(s,ka)

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
flask_save_all_upload_files=flask_get_all_upload_files	
	
def textarea(response,name='t',upload_dir=py.No('U.gst/upload_dir',no_raise=1),):
	"""
	 <input type="text" name="t">
	
	"""
	
	r=T.html_template(globals=globals(),locals=locals(),s='''
<head>
<style type="text/css">
	input[type="submit"]{
		width:100%;
	}
	input.url{
		width:49%; /*50% break line*/
	}	
</style> 
</head>
	
<form method="post" enctype="multipart/form-data" action="$U.get_or_set('rpc.server.base','/')$r=U.set_multi($name$_form=request.form,$name$_files=N.HTML.flask_get_all_upload_files(),$name$_data=q.get_data(),);">
	<input type="submit" />
	<hr>
	<input type="file" multiple name="f">
	<hr>
	<div><small>$name$:</small></div >
	<div style="height:60%;" > 
		<textarea name="t" style="width:100%; height: 100%;" ></textarea>
	</div>
	
	<hr>
	<input type="submit" />
	<input id=url_start class=url type="text" name="url_start" 
commt="/-                         U.set('rpc.server.upload.save_size',$code$ "
value="$U.get('rpc.server.base')#$U.set('rpc.server.upload.save_size',$U.int_exp(U.get('rpc.server.upload.save_size',8*1024*1024),1024)#$);">
	<input id=url_end   class=url type="text" name="url_end" value="%23-">
</form> 
<script> 
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
''',)
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
			# U.msgbox(list(kv)[:9])
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
