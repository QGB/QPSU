if __name__.startswith('qgb.N'):from qgb import py
else:
	from pathlib import Path
	gsqp=Path(__file__).absolute().parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
U,T,N,F=py.importUTNF()
ids=U.get('ids')
did=U.get('did',{})
did_err=U.get('did_err',{})
did2=U.get('did2',{})
if not ids:raise EnvironmentError('need ids set')
ids=py.set(ids)
cache_path=F.mkdir(f'{U.gst}ids-{len(ids)}')
gid=None
def next_id(template='{}'):
	'''
set().pop() #KeyError: 'pop from an empty set'  ,pop no args

'''
	global gid
	for id in ids.difference(did):
		gid=id
		return template.format(id)
	return ''
	
def receive(request):
	data=T.json_loads(request.get_data())
	if not py.istr(data):
		F.dill_dump(file=cache_path+'dill/'+gid,obj=data)
		return U.set_dict_value_list(did_err,gid,data)
	if gid in did:
		return U.set_dict_value_list(did2,gid,data)
	did[gid]=F.write(cache_path+gid+'.html',data)
	return gid

	
def got_err():
	return py.str(U.get('taobao_sf'))

def gc():
	for id in U.progressbar(list(B.did)):
		if F.exist(r'C:\test\ids-3208\{}.html'.format(id)):
			B.did[id]=''
	



'''


await post("https://okfw.net/sc=T.json_loads(request.get_data())",main_post_code)





'''

