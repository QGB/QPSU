#coding=utf-8
import sys,pathlib
gsqp=pathlib.Path(__file__).absolute(
		).parent.parent.__str__()
	#*.py /qgb   /[gsqp]  
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import asyncio
try:
	import aiohttp
except Exception as ge:
	print(ge)

def get_asyncio_task_by_coro_name(s,loop=None):
	''' asyncio.all_tasks(loop=gloop))[1];r=k._coro.__name__ '''
	for t in asyncio.all_tasks(loop=loop):
		if t._coro.__name__==s:return t
	return py.No(f'can not found asyncio_task t._coro.__name__=={s!r}')
get_task=get_asyncio_task_by_coro_name

def sync_call_async(af,timeout=60,gloop=None):
	if not gloop:
		gloop = U.get_or_set('gloop', lazy_default=lambda:asyncio.get_event_loop())
	future = asyncio.run_coroutine_threadsafe(af, gloop)
	try:
		# 等待任务完成（timeout 自动终止任务）
		rnone=future.result(timeout=timeout)
	except TimeoutError:
		logging.error(f"任务执行超时{timeout}s")
	except Exception as e:
		logging.error(f"任务执行失败:{str(e)}")
	finally:
		future.cancel()
	return af,future,rnone
call=acall=sync_call=sync_call_async

async def send_post_request(url, data):
	async with aiohttp.ClientSession() as session:
		session.post(url, data=data,return_response=False)
	'''		
        async with 
		as response:
            # 获取响应状态码
            status_code = response.status

            # 读取响应内容
            response_text = await response.text()

            # 打印响应状态码和内容
            # print(f"Status code: {status_code}")
            # print(f"Response: {response_text}")

'''


def patch_nest_asyncio():
	import nest_asyncio
	return nest_asyncio.apply()
nest=nest_asyncio=patch_nest_asyncio
	
async def sleep(sec):
	return await asyncio.sleep(sec)
	
	
async def websocket_client_send(url,astr,subprotocols=None,verify=True):
	import websockets
	if verify:sslopt={}
	else:
		import ssl
		sslopt={"cert_reqs": ssl.CERT_NONE}
	
	url=N.auto_url(url,default_protocol='ws')
	# py.pdb()()
	if py.istr(subprotocols):subprotocols=[subprotocols]
	#TypeError: BaseEventLoop.create_connection() got an unexpected keyword argument 'sslopt'    

	async with websockets.connect(url, subprotocols=subprotocols,sslopt=sslopt) as ws:
		await ws.send(astr)
		r = await ws.recv()
		return r
ws_send=websocket_client_send		

async def chrome_devtools_protocol_send(url,astr,params={},id=0):
	astr=astr.strip()
	if not id:id=U.ct()
	if py.istr(astr) and not (astr.startswith('{') and astr.endswith('}')):
		astr=py.dict(id=id,method=astr,params=params,)
	if py.isdict(astr):
		astr=T.json_dumps(astr)
	return astr,await websocket_client_send(url,astr)
csend=cws_send=c_ws_send=chrome_devtools_protocol_send

def async_to_sync(callable):
	''' (Pdb) A.a2s(connection.send)
*** TypeError: Called with unsupported argument: <bound method Connection.send of <pyppeteer.connection.Connection objec
t at 0x0000026A719AD108>>
'''
	import syncer
	return syncer.sync_fu(callable)
a2s=async_to_sync
# async def t(a):
	
async def multi_get(urls,timeout=10,connect_limit=100,fetch_print=True,return_time=False,check='No Sec-WebSocket-Key header',**ka):
	import aiohttp
	if py.isnum(timeout):	
		timeout = aiohttp.ClientTimeout(total=timeout)	
	connector = aiohttp.TCPConnector(limit=connect_limit)	
	
	gr={}
	async def fetch_url(session,url,n=0):
		text=''
		t=U.ftime()
		try:
			async with session.get(url,ssl=False,**ka) as response:
				text=await response.text()
				if check and py.istr(check):
					if py.istr(text) and check in text:
						gr[url]=text
					else:
						if fetch_print:print(n,url,U.ftime()-t,repr(text)[:99],sep='\t')
						return
				else:gr[url]=text	
		except Exception as e:
			# gr[url]=e
			if fetch_print:print(n,url,U.ftime()-t,e,sep='\t')
			return
		t=U.ftime()-t	
		if return_time:gr[url]=url,t,gr[url]
		return n,url,t,U.len(text)
	start_time = U.ftime()
	async with aiohttp.ClientSession(timeout=timeout,connector=connector) as session:
		tasks = []
		for n,url in enumerate(urls):
			tasks.append(  asyncio.ensure_future(fetch_url(session,url,n=n))  )
		responses = await asyncio.gather(*tasks)
	total_time = U.ftime() - start_time
	
	if fetch_print:
		for i, response in enumerate(responses):
			if response:
				print(i,response,sep='\t')

	print(f'{U.stime()} Total time: {total_time} seconds',)
	gr={k:v for k,v in gr.items() if v}
	return gr

	
def sync_multi_get(urls,**ka):
	loop = asyncio.get_event_loop()
	result = loop.run_until_complete(multi_get(urls,**ka))
	return result
	
	
	
	