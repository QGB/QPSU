#coding=utf-8
import sys,pathlib
#                     *.py /N     /qgb    /[gsqp]  # 如果要修改路径，框选两行，一起删除
gsqp=pathlib.Path(__file__).parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U=py.importU()

import asyncio

gde_count={}

dip_open_ports={}
dip_close_ports={}

async def check_port(target_ip, port, semaphore,timeout=1,loopm=None):
	try:
		async with semaphore:
			con = await asyncio.open_connection(target_ip, port)

			try:
				await asyncio.wait_for(con,timeout,loop=loopm)
				U.set_dict_value_list(dip_open_ports,target_ip,port)
			except Exception as e:
				# If this is reach -> port closed
				U.set_dict_value_list(dip_close_ports,target_ip,port)
				pass
	except Exception as e:
		U.set_dict_plus_1(gde_count,e)

def scan_ip(target_ip,ports=range(1,65536)):
	if U.isLinux():
		import uvloop
		asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
		MAX_SEMAPHORE_NUM = 9999 #2048
	if U.isWin():
		MAX_SEMAPHORE_NUM = 999 #2048

	semaphore = asyncio.Semaphore(MAX_SEMAPHORE_NUM)
	asyncio.set_event_loop(asyncio.new_event_loop())
	loop = asyncio.get_event_loop()
	
	tasks = []
	for p in ports:
		tasks.append(asyncio.ensure_future(
			check_port(target_ip, p, semaphore, timeout=5, loopm=loop)))
	try:
		loop.run_until_complete(wait_with_progress(tasks))
	except KeyboardInterrupt as e:
		print('[-] Cancel task...')
		for task in asyncio.Task.all_tasks():
			task.cancel()
		loop.stop()
		loop.run_forever()
	finally:
		loop.close()


from tqdm import tqdm

async def wait_with_progress(coroutines):
    for f in coroutines:#tqdm(asyncio.as_completed(coroutines),total=len(coroutines)):
        await f
