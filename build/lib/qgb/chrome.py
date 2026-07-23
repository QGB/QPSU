#coding=utf-8
import sys,os
if __name__.endswith('qgb.chrome'):from . import py
else:import py
U,T,N,F=py.importUTNF()

# import pychrome  
import pyppeteer  
import asyncio

def connect(ws):
	''' qgb
print(connection, browserContextIds, ignoreHTTPSErrors, defaultViewport)	
<pyppeteer.connection.Connection object at 0x0000016D1F3B2D88> [] False {'width': 800, 'height': 600}	
	'''
	


loop=asyncio.get_event_loop()
def windows_asyncio_KeyboardInterrupt_patch():
	loop.call_later(0.1, windows_asyncio_KeyboardInterrupt_patch)

if '__main__' in __name__:
	try:
		loop.call_later(0.1, wakeup)
		print(U.stime(),'call_later')
		loop.run_forever()
		print(U.stime(),'run_forever')
	except BaseException:
		# U.msgbox(U.stime())
		U.exit(msg='KeyboardInterrupt')



def parse_cookies(raw_text):
	"""将开发者工具 devtools 》应用 》复制的 Cookie 表格文本解析为字典"""
	cookies = {}
	for line in raw_text.strip().split('\n'):
		# 拆分制表符分隔的字段
		parts = line.strip().split('\t')
		# 确保至少包含名称和值两个字段（过滤空行和无效行）
		if len(parts) >= 2 and parts[0] and parts[1]:
			key = parts[0].strip()
			value = parts[1].strip()
			# 过滤空值条目（如 pcbOperationCode 的空值情况）
			if value:
				cookies[key] = value
	return cookies


