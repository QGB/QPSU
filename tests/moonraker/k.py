import json,socket
import sys,os
if 'qgb.U' not in sys.modules:
	_qp='/mnt/c/QGB/babun/cygwin/bin/'
	if os.path.exists(_qp):sys.path.insert(0,_qp)
	else:sys.path.insert(0,'/home/qgb/')
from qgb import *

import libinput.constant,time
print(libinput.constant.Event.KEYBOARD_KEY)
for _k in dir(libinput.define.Key):
	if _k.startswith('KEY_'):
		globals()[_k]=getattr(libinput.define.Key,_k)

client=None
def send_jsonrpc(method="printer.firmware_restart",aid=9876543210):
	'''
{"jsonrpc":"2.0","method":"printer.firmware_restart","params":{},"id":5487}
{"jsonrpc":"2.0","method":"printer.restart","params":{},"id":1061}


{'jsonrpc': '2.0',
 'error': {'code': 400,
  'message': '{\'error\': \'WebRequestError\', \'message\': \'Lost communication with MCU \\\'mcu\\\'\\nOnce the underlying issue is corrected, use the\\n"FIRMWARE_RESTART" command to reset the firmware, reload the\\nconfig, and restart the host software.\\nPrinter is shutdown\\n\'}'},
 'id': 1680613507}  # 未连接
 
 {'error': {'code': 400, 'message': '{\'error\': \'WebRequestError\', \'message\': \'Lost communication with MCU \\\'mcu\\\'\\nOnce the underlying issue is corrected, use the\\n"FIRMWARE_RESTART" command to reset the firmware, reload the\\nconfig, and restart the host software.\\nPrinter is shutdown\\n\'}'},
  'id': 1680614108,
  'jsonrpc': '2.0'} #已连接 未重置
 
'''	
	# printer.restart
	msg = {"jsonrpc": "2.0","method": method,"params": {}}
	msg["id"] = aid
	data = json.dumps(msg).encode() + b"\x03"
	client.send(data)
	
def send_gcode(client,gcode,aid=9876543210):
	'''S300, 8000:100圈 ，28秒
100/28=3.5714285714285716
60*_ =214.2857142857143 每分钟

400 硬木板上无震动
405 硬木板上启动时轻微震动
410 硬木板上启动时轻微震动
415 硬木板上断续震动
420 硬木板上轻微震动
490 缓冲不震动 按住丢步
560 缓冲不震动 偶尔有丢步  100圈 ，14秒
'''	
	# if gcode.startswith('G1 '):
		# gcode='G91\n'+gcode
	msg = {"jsonrpc": "2.0","method": "printer.gcode.script","params": {"script": gcode}}
	# msg["id"] = id(msg)
	msg["id"] = aid
	data = json.dumps(msg).encode() + b"\x03"
	client.send(data)

	s=f""":{U.stime()[-8:].replace('__','')}   {gcode}"""  #{client.recv(99999)}

	# print()
	N.get(f"""http://127.0.0.1:7125/-wsm.notify_clients('gcode_response',[{repr(s)}])""")
	# wsm.notify_clients('gcode_response',[])
	# return client,wsm,gcode
def get_speed_factor():
	'''
{'result': {'eventtime': 49489.199346832,
  'status': {'gcode_move': {'speed_factor': 1.65,
    'speed': 6000.0,
    'extrude_factor': 1.0,
    'absolute_coordinates': False,
    'absolute_extrude': True,
    'homing_origin': [0.0, 0.0, 0.0, 0.0],
    'position': [0.0, 0.0, 0.0, 0.0],
    'gcode_position': [0.0, 0.0, 0.0, 0.0]}}}}	
	
'''	
	js=N.HTTP.get_json('http://127.0.0.1:7125/printer/objects/query?gcode_move',)
	speed_factor=js['result']['status']['gcode_move']['speed_factor']
	return py.int(speed_factor*100)
	
def init():
	b=b''
	for i in range(99):
		if b and py.len(b)<2000:#1397 1398
			break
		b=client.recv(99999)
			
	aid=U.itime()
	send_gcode(client,gcode_init+'\nG28',aid)
	b=client.recv(99999)
	
	lr=[]
	for i in b.split(T.byte256_list[3])[::-1]:
		js=T.json_loads(i)
		lr.append(js)
		if js and 'error' in js:
			if 'WebRequestError' in js['error']['message']:
				send_jsonrpc(method="printer.firmware_restart",aid=aid)
				print(U.stime(),js['error']['message'])
			# if js['id']==aid:
				# break
	return lr
gerr=[]
gmove_unit=80*10
gcode_move='''
G91
G1 {0} F6000'''.strip()
gmax_speed=490

gcode_init=''
gdk={}
def update(move_unit=0,max_speed=0,p=True):
	'''
SET_VELOCITY_LIMIT ACCEL_TO_DECEL=2200
SET_VELOCITY_LIMIT ACCEL=5100
'''	
	global gdk,gcode_init,gmax_speed,gmove_unit
	
	if not move_unit:move_unit=gmove_unit
	gmove_unit=move_unit
	
	gdk={
KEY_RIGHT:gcode_move.format(f'X+{gmove_unit}'),
KEY_LEFT :gcode_move.format(f'X-{gmove_unit}'),
KEY_UP   :gcode_move.format(f'Y+{gmove_unit}'),
KEY_DOWN :gcode_move.format(f'Y-{gmove_unit}'),
KEY_VOLUMEUP :gcode_move.format(f'Z+{gmove_unit}'),
KEY_VOLUMEDOWN :gcode_move.format(f'Z-{gmove_unit}'),
KEY_HOME :init,
KEY_BACK :'M84',
KEY_MUTE   :lambda:update(max_speed=get_speed_factor()+10),
KEY_COMPOSE:lambda:update(max_speed=get_speed_factor()-10),


	}

	if not max_speed:max_speed=gmax_speed
	gmax_speed=max_speed
	gcode_init=f'''
SET_VELOCITY_LIMIT VELOCITY={max_speed}
M220 S{max_speed}
;move_unit={move_unit}
'''.strip()

	if client:send_gcode(client,gcode_init)
	if p:print(U.stime(),'move_unit:',move_unit,'max_speed:',max_speed)
	
	return move_unit,max_speed
update_gdk=update
	


def read_key_events():
	global client
	li = libinput.LibInput(udev=True)
	li.udev_assign_seat('seat0')
	# g=globals()
	server=wsm=0

	sf=f"{F.get_home()}printer_data/comms/moonraker.sock"
	sf=f"/home/ubuntu/printer_data/comms/moonraker.sock"
	client=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	while True:
		try:
			client.connect(sf)
			break
		except Exception as e:
			print(U.stime(),e)
			U.sleep(10)

	print(N.get('http://127.0.0.1:7125/-wsm=p.server.lookup_component(%22websockets%22);r=wsm'))
	# send_gcode(client,gcode_init)
	update()

	t0=time.monotonic()# sec
	for event in li.get_event():
		t=time.monotonic()
		td=t-t0
		if event.type == libinput.constant.Event.KEYBOARD_KEY:
			kbev = event.get_keyboard_event()
			kcode = kbev.get_key() # constants in  libinput.define.Key.KEY_xxx
			kstate = kbev.get_key_state() # constants   libinput.constant.KeyState.PRESSED or .RELEASED 
			if kstate == libinput.constant.KeyState.PRESSED:
				print(f"{td:.3f} {kcode} pressed") 
				gcode=gdk.get(kcode,'')
				if not gcode:continue
				try:
					if py.istr(gcode):send_gcode(client,gcode)
					if py.callable(gcode):gcode()
				except Exception as e:
					print(U.stime(),e)
				# if  == KEY_BACK:
					# send_gcode(client,,)
				# elif kcode == KEY_RIGHT:
					# send_gcode(client,,)
				# elif kcode == KEY_HOME:
					# send_gcode(client,)
				# elif kcode == KEY_BACK:
					# send_gcode(client,)
					
			elif kstate == libinput.constant.KeyState.RELEASED:
				print(f"{td:.3f} {kcode} released")
				if kcode.name[-1] in T._09:
					if kcode.name=='KEY_0':
						update(move_unit=80*20)
						continue
					update(move_unit=80*py.int(kcode.name[-1])),
		t0=t
# key_thread=U.thread(target=read_key_events)
# key_thread.start()
# client=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
if __name__ == "__main__":
	N.rpcServer(globals=globals(),locals=locals(),port=7126)
	read_key_events()