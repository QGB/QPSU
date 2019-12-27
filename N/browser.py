if __name__.endswith('qgb.N'):from qgb import py
else:
	print(__name__)
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
U,T,N,F=py.importUTNF()
ids=U.get('ids')
did=U.get('did',{})
did_err=U.get('did_err',{})
did2=U.get('did2',{})
if not ids:raise EnvironmentError('need ids set')
ids=py.set(ids)

gid=None
def next_id():
	'''
set().pop() #KeyError: 'pop from an empty set'  ,pop no args

'''
	global gid
	for id in ids.difference(did):
		gid=id
		return id
	return 
	
def receive(request):
	data=T.json_loads(request.get_data())
	if gid in did:
		U.set_dict_value_list(did2,gid,data)
		return '#err {} {}'.format(gid,'did2')
	did[gid]=data
	return gid

	
	