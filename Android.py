def bluetooth_getBondedDevices():
	from jnius import autoclass,cast
	BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
	adapter = BluetoothAdapter.getDefaultAdapter() 
	r=[]
	for n,d in enumerate(adapter.getBondedDevices().toArray()):
		r.append([n,d.name,d])
	return r
getBondedDevices=bluetooth_getBondedDevices


scan_receiver = None  
def on_scan_results(context, intent):
    global scan_receiver,scan_results
    scan_results = adapter.getScanResults()  # 获取扫描结果设备列表
    # 处理扫描结果...
	
    if adapter.getScanMode() != BluetoothAdapter.SCAN_MODE_CONNECTABLE_DISCOVERABLE:
        adapter.cancelDiscovery()   # 取消扫描          
        scan_receiver.unregister()  # 取消广播接收器

def on_discovery_finished(context, intent): 
    scan_receiver.unregister()   # 取消广播接收器
    adapter.startDiscovery()     # 如果需要再启动新扫描

def main():
	from android.bluetooth import BluetoothDevice
	scan_receiver = BroadcastReceiver(on_scan_results, actions=[BluetoothDevice.ACTION_SCAN_RESULTS_AVAILABLE])  
	discovery_receiver = BroadcastReceiver(on_discovery_finished, actions=[BluetoothAdapter.ACTION_DISCOVERY_FINISHED])


def scan():
	from android.permissions import request_permissions, Permission 
	request_permissions([
Permission.BLUETOOTH_CONNECT,Permission.BLUETOOTH_SCAN,
Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE,
])

	from android.broadcast import BroadcastReceiver
	from android.runnable import run_on_ui_thread
	# from android import intent

	from jnius import autoclass,cast
	import jnius,time
	
	BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
	BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice') 
	Intent = autoclass('android.content.Intent')
	IntentFilter = autoclass('android.content.IntentFilter')
	
	# Context = autoclass('android.content.Context')
	# context = Context()           # 创建Context对象
	# app_context = context.getApplicationContext()   # 调用方法	
	PythonActivity = autoclass('org.kivy.android.PythonActivity')
	currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
	context = currentActivity.getApplicationContext()
	
	adapter = BluetoothAdapter.getDefaultAdapter() 
	# adapter.startDiscovery()
	
	filter = IntentFilter(BluetoothDevice.ACTION_FOUND)
	
	UUID = autoclass('java.util.UUID')
	for device in adapter.getBondedDevices().toArray():
		if device.getName() != 'btgrblesp':continue
		socket = device.createRfcommSocketToServiceRecord(
			UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
		recv_stream = socket.getInputStream()
		send_stream = socket.getOutputStream()
		socket.connect()
		break
		
	InputStreamReader = autoclass('java.io.InputStreamReader') 
	BufferedReader = autoclass('java.io.BufferedReader')	
	input_stream = jnius.cast('java.io.InputStream', recv_stream)
	reader = BufferedReader(InputStreamReader(input_stream)) 	
		
		
	# buffer=[]	
	# for i in range(9):
		# byte = recv_stream.read()
		# if byte == b'\n':  # 如果收到换行符
			# break
		# buffer.append(byte)	
		
	return adapter,device,recv_stream,send_stream,reader,reader.readLine()
	
	
	
	return adapter,currentActivity,context
	time.sleep(1) 
	return adapter.getScanResults()
	
	devices = []
	for i in range(2):   # 扫描10秒
		time.sleep(1)
		paired_devices = adapter.getBondedDevices()
		discovered_devices = adapter.getDiscoveredDevices()
		for device in discovered_devices:
			if device not in paired_devices and device not in devices:
				devices.append(device)
				print(device.getName(), device.getAddress())
				
	adapter.cancelDiscovery()
	return devices
	# print('Found {} bluetooth devices!'.format(len(devices)))

def termux_android():
	'''
pkg install python python-dev bluetooth  android-headers 	
	pip install androidhelper '''
	import androidhelper 
	droid = androidhelper.Android()

def kivy():
	from kivy.uix.toast import toast
	from kivy.event import EventDispatcher
	