#coding=utf-8
import sys,pathlib               # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

def get_copyq_clipboard_items(end=9,start=0,filter='',strip=True,**ka):
	"""获取 CopyQ 剪贴板中的项目
range(stop) 
range(start, stop[, step]) 	

filter : end 999 大约0.6 秒，end 2000 大约1.3秒，end 5000 大约4.2 秒，    ， end 9999 大约7 秒， 

	"""
	import subprocess
	end=U.get_duplicated_kargs(ka,'end','n','stop','limit',default=end)
	filter=U.get_duplicated_kargs(ka,'filter','s','search','find',default=filter)
	
	if py.istr(end):
		assert not filter
		filter=end
		if start>0:
			end=start
			start=0
		else:
			end=2000	
	if start and start>end:start,end=end,start
	
	split=U.random_choice(T.azAZ09,9)
	
	try:
		# 调用 CopyQ 命令行接口获取多个剪贴板项目
		result = subprocess.run([r'C:\QGB\copyq-6.2.0\copyq.exe', 'eval', rf"items = []; for (i = {start}; i <= {end}; ++i)"+r" { items.push(''+read(i)); }; print(items.join('"+split+r"'));"], capture_output=True, text=True,encoding='utf-8')
		if result.returncode == 0:
			# 解析输出，每行一个项目
			items = result.stdout.strip().split(split)
			if filter:
				items=[i for i in items if filter in i]

			if strip:
				for n in py.range(py.len(items)):
					items[n]=items[n].strip()
			return items
		else:
			print(f"Error: {result.stderr}")
			return []
	except Exception as e:
		# print(f"Error: {e}")
		return py.No(e)

if __name__ == "__main__":
	items = get_copyq_clipboard_items()
	print("CopyQ 剪贴板项目:", items)