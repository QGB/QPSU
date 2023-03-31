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
def send_gcode(client,gcode):
	'''S300, 8000:100圈 ，28秒
100/28=3.5714285714285716
60*_ =214.2857142857143 每分钟

S490 不震动 按住丢步
S560 不震动 偶尔有丢步  100圈 ，14秒
'''	
	# if gcode.startswith('G1 '):
		# gcode='G91\n'+gcode
	msg = {"jsonrpc": "2.0","method": "printer.gcode.script","params": {"script": gcode}}
	# msg["id"] = id(msg)
	msg["id"] = 9876543210
	data = json.dumps(msg).encode() + b"\x03"
	client.send(data)

	s=f""":{U.stime()[-8:].replace('__','')}   {gcode}"""  #{client.recv(99999)}

	# print()
	N.get(f"""http://192.168.1.20:7125/-wsm.notify_clients('gcode_response',[{repr(s)}])""")
	# wsm.notify_clients('gcode_response',[])
	# return client,wsm,gcode

gerr=[]
gmove_unit=80*10
gcode_move='''
G91
G1 {0} F6000'''.strip()
gmax_speed=490

gcode_init=''
gdk={}
def update(move_unit=0,max_speed=0):
	global gdk,gcode_init,gmax_speed,gmove_unit
	
	if not move_unit:move_unit=gmove_unit
	gmove_unit=move_unit
	
	gdk={
KEY_RIGHT:gcode_move.format(f'X+{gmove_unit}'),
KEY_LEFT :gcode_move.format(f'X-{gmove_unit}'),
KEY_UP   :gcode_move.format(f'Y+{gmove_unit}'),
KEY_DOWN :gcode_move.format(f'Y-{gmove_unit}'),
KEY_HOME :gcode_init+'\nG28',
KEY_BACK :'M84',
KEY_MUTE   :lambda:update(max_speed=gmax_speed+10),
KEY_COMPOSE:lambda:update(max_speed=gmax_speed-10),

	}

	if not max_speed:max_speed=gmax_speed
	gmax_speed=max_speed
	gcode_init=f'''
SET_VELOCITY_LIMIT VELOCITY={max_speed}
M220 S{max_speed}
'''.strip()

	if client:send_gcode(client,gcode_init)
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
	client.connect(sf)

	print(N.get('http://192.168.1.20:7125/-wsm=p.server.lookup_component(%22websockets%22);r=wsm'))
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
				if py.istr(gcode):send_gcode(client,gcode)
				if py.callable(gcode):gcode()
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
				
		t0=t
# key_thread=U.thread(target=read_key_events)
# key_thread.start()
# client=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
if __name__ == "__main__":
	N.rpcServer(globals=globals(),locals=locals(),port=7126)
	read_key_events()