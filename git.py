if __name__.endswith('qgb.F'):from . import py
else:import py
U,T,N,F=py.importUTNF()

import dulwich
from dulwich import client,index,repo,porcelain

import os
import shutil

# from six.moves import urllib
# opener = urllib.request.build_opener()
# headers={'Authorization':F.read('Authorization')}
# opener.addheaders = py.list(headers.items())
# urllib.request.install_opener(opener)
grepo=U.get('git.repo')

def clone(url,path=None):
	client, target = dulwich.client.get_transport_and_path(url) #c , 'user/repo'
	if not path:
		if target.endswith('.git'):
			target=target[:-4]
		path=target
	path=F.mkdir(path)
	ls=F.ls(path)
	if len(ls)>1: #skip .git
		return py.No('Not empty dir:'+path,ls)
	if len(ls)==1:
		r = dulwich.repo.Repo(path)
	else:	
		r = dulwich.repo.Repo.init(path)
	print(U.stime(),'fetching url...')
	remote_refs = client.fetch(url, r)
	r[b"HEAD"] = remote_refs[b"HEAD"]

	print(U.stime(),'build_index_from_tree ...')
	index.build_index_from_tree(r.path, r.index_path(), r.object_store, r[b'HEAD'].tree)
	
	r.close()
	return path,r

def up(url,path=None,commit_msg=None,username=None,password=None,branch='master',**ka):
	'''
porcelain.push(repo.path,"https://wrong_name@e.coding.net/...",'master',username='correct_name',password=_) ## 也会GitProtocolError: unexpected http resp 401 for

porcelain.push(repo.path,"https://http://e.coding.net/...",'master',username='correct_name',password=_)  #  OK!	
	'''
	global grepo
	if ':' not in url:
		url='https://'+url
	domain=T.netloc(url)
	if not username:
		username=U.get_or_input(domain+'_git.username')
	ka['username']=username
	if not password:
		password=U.get_or_input(domain+'_git.password')
	ka['password']=password
	if not 'refspecs' in ka:
		ka['refspecs']=branch
	if not path and '/qpsu' in url.lower():
		path=U.get_qpsu_dir()
	if not path:	
		_client, target = dulwich.client.get_transport_and_path(url) 
		if target.endswith('.git'):
			target=target[:-4]
		path=target
		
	path=F.auto_path(path)
	ls=[i[len(path):] for i in F.ls(path,d=0,f=1,r=1)]
	if len(ls) < 1:
		return py.No('Not contains .git dir:'+path,ls)

	repo=dulwich.repo.Repo(path)
	U.pln(path,'add ...',U.stime())
	repo.stage(['git.py'],)
	dulwich.porcelain.add(repo.path)
	# repo.stage(['a']) 
	# cid=repo.do_commit(message=b"dulwic")	
	# author = "{0} <{1}>".format(name, email)
	# author=author.encode('utf-8')
	U.pln('commit ...',U.stime())
	# bhash=repo.do_commit(message=commit_msg
				  # , author=author
				  # , committer=author 
				  # , merge_heads=None
					  # )
	bhash,commit_msg=commit(repo,commit_msg)					
	r= bhash,commit_msg, ka
	repo.close()
	U.pln('push ...',U.stime())
	try:
		dulwich.porcelain.push(repo.path, url , **ka )
	except Exception as e:
		U.print_tb()
		U.v.dulwich.porcelain.push(repo.path, url , **ka )
		r=py.No(e,r)
	return r
	# porcelain.push(repo.repo.path, result.url, branch_name, errstream=outstream)					
	
def commit(repo,commit_msg):
	if not commit_msg:
		commit_msg='dulwich_'+U.stime()
	if not py.isbytes(commit_msg):
		commit_msg=commit_msg.encode('utf-8')
			
	index = repo.open_index()
	new_tree = index.commit(repo.object_store)
	if new_tree != repo[repo.head()].tree:
		bhash=repo.do_commit(commit_msg, tree=new_tree)
		return bhash,commit_msg
	else:
		return b'',py.No("Empty commit!")

def log(max_entries=11,repo=None):
	
	return dulwich.porcelain.log(max_entries=max_entries) 