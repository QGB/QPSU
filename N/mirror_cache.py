#coding=utf-8
import sys
if __name__.endswith('qgb.N'):from qgb import py
else:
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
U,T,N,F=py.importUTNF()
from requests import request as send_request
from flask import Flask,request,make_response

app=Flask(__name__)
N.rpcServer(locals=globals(),app=app,key='rpc')

def target_to_response(target):
    b=target.raw._fp._safe_read()
    response=make_response()
    response.status_code=target.status_code
    response.headers._list=list(target.headers.items())
    response.set_data(target.content)
    return response

use_cache=True    
@app.errorhandler(404)
def mirror_cache(*a,**ka):
    # us=request.path.split('/')
    path=request.path[1:]
    method=request.method
    fn=cache_path+method+T.url2fn(request.environ.get('HTTP_COOKIE','')+path)
    if use_cache:
        target=F.dill_load(fn)
        if target:return target_to_response(target)
        
    send_headers={}
    for k,v in request.headers.items():
        v=v.replace(request.host,target_host)
        send_headers[k]=v

    target=send_request(method=method, 
        url=target_base_url+path, 
        params=request.args, headers=send_headers, )
    response= target_to_response(target)
    F.dill_dump(protocol=4,obj=target,file=fn)
    return response
def run(target,port=1122,currentThread=True):
    global app,thread,cache_path,target_base_url,target_host
    from six.moves.urllib.parse import urlsplit
    up=urlsplit(url=target)
    target_host=up.netloc
    target_base_url='{}://{}/'.format(up.scheme,target_host)

    cache_path=F.mkdir(target_host) # in gst
    U.log(cache_path)

    flaskArgs=py.dict(port=port,host='0.0.0.0',debug=True,threaded=True)
    if currentThread:
        thread=None
        return app.run(**flaskArgs)
    else:
        thread=U.Thread(target=app.run,name='qgb thread '+app.name,kwargs=flaskArgs)
        thread.start()
        return (thread,app)

if __name__=='__main__':
    a=U.parseArgs(str=r'https://www.dulwich.io',int=1122)
    run(target=a.str,port=a.int)

