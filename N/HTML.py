#coding=utf-8
import sys #endswith 是为了适配qgb处于另外一个包内的情况
if __name__.endswith('qgb.N.HTML'):from .. import py
else:
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
U,T,N,F=py.importUTNF()

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
			disabled=r.disabled
			continue
		if v!='on':
			raise py.ArgumentError('unexpected submit value (must be "on") :',k,v,q)
		k=int(k)		
		qs.add(k)
	# q=dict(q) # 如果不进行转换 就 id=q.pop('id')  TypeError("'CombinedMultiDict' objects are immutable")
	
	for k in py.list(r):
		if id(k) not in qs:
			disabled[k]=r.pop(k)
			continue
	
	for k in py.list(disabled):
		if id(k) in qs:
			r[k]=disabled.pop(k)
			continue

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
			for k,v in kv:
				# k,v=fk(k),fv(v)
				rows+=hd.format(i=i,name=py.id(k), k=fk(k),v=fv(v) ,checked='checked')
				i+=1
			for k,v in disabled:
				# k,v=fk(k),fv(v)
				rows+=hd.format(i=i,name=py.id(k), k=fk(k),v=fv(v) ,checked='')
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
		return do_resp(rd,rd.items(),rd.disabled.items())

################################################

class ListSelect(py.list):
	'''
	'''
	def __init__(*args, **kwds):
		'''Initialize an ordered dictionary.  The signature is the same as
		regular dictionaries.  Keyword argument order is preserved.
		'''
		if not args:
			raise TypeError("descriptor '__init__' of select object "
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
				self.disabled=[]


class DictSelect(py.dict):
	'''
	'''
	def __init__(*args, **kwds):
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

		self.update(args, **kwds)

	# def disable(self,key):
