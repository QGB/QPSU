from android.bluetooth import BluetoothDevice

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
	scan_receiver = BroadcastReceiver(on_scan_results, actions=[BluetoothDevice.ACTION_SCAN_RESULTS_AVAILABLE])  
	discovery_receiver = BroadcastReceiver(on_discovery_finished, actions=[BluetoothAdapter.ACTION_DISCOVERY_FINISHED])

