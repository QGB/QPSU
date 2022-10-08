#coding=utf-8
import sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import frida  #导入frida模块

jscode = """
    Java.perform(function(){  
        // 获取当前安卓设备的安卓版本
        var v = Java.androidVersion;
        send("version:"+v);
        
        // 获取该应用加载的所有类
        var classnames = Java.enumerateLoadedClassesSync();
        for (var i=0;i<classnames.length;i++){
            send("class name:"+classnames[i])
        }
    });
"""

def on_message(message,data): #js中执行send函数后要回调的函数
    if message["type"] == "send":
        print("[*] {0}".format(message["payload"]))
    else:
        print(message)
    
# device=frida.get_usb_device()
def get_device(device=''):
	if not device:
		host='192.168.1.14'
	elif py.istr(device):
		host=device
	else:
		return device
	return frida.get_device_manager().add_remote_device(host)
	
def get_apps_ps(device=''):
	device=get_device(device)

	scope='minimal'  # full
	apps=device.enumerate_applications() 
	U.pprint(U.stime(),apps)

	ps = device.enumerate_processes(scope=scope)
	U.pprint(U.stime(),ps)
	return apps,ps
# N.rpc_set_local(apps=apps,ps=ps)#TypeError: can't pickle _frida.Application objects

device=get_device()
process = device.attach('Termux') #进程 name ,不是 'com.termux' 包名
script = process.create_script(jscode) #创建js脚本
script.on('message',on_message) #加载回调函数，也就是js中执行send函数规定要执行的python函数
script.load() #加载脚本
# sys.stdin.read()
