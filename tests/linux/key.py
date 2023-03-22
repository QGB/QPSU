'''
!apt-get install libinput10
!python3 -m pip install python-libinput

'''
import libinput.constant
print(libinput.constant.Event.KEYBOARD_KEY)
import time
def read_key_events():
	li = libinput.LibInput(udev=True)
	li.udev_assign_seat('seat0')
	t0=time.monotonic()# sec
	for event in li.get_event():
		t=time.monotonic()
		td=t-t0

		# test the event.type to filter out only keyboard events 
		if event.type == libinput.constant.Event.KEYBOARD_KEY:
		
			# get the details of the keyboard event
			kbev = event.get_keyboard_event()
			kcode = kbev.get_key() # constants in  libinput.define.Key.KEY_xxx
			kstate = kbev.get_key_state() # constants   libinput.constant.KeyState.PRESSED or .RELEASED 
			
			# your key handling will look something like this...
			if kstate == libinput.constant.KeyState.PRESSED:
				print(f"{td:.3f} Key {kcode} pressed") 
				
			elif kstate == libinput.constant.KeyState.RELEASED:
				
				# if kbev.get_key() == libinput.define.Key.KEY_ENTER:
				#     print("Enter key released")
					
				# elif kcode == libinput.define.Key.KEY_SPACE:
				#     print("Space bar released")
				# else:
				print(f"{td:.3f} Key {kcode} released")
		t0=t

import json,socket

def send(client,ka):
	'''
{"jsonrpc": "2.0", "method": "notify_gcode_response", "params": ["// Unknown command:\"M118\""]}
'''	
	msg = {"jsonrpc": "2.0",**ka}

	# msg["id"] = id(msg)
	msg["id"] = 9876543210
	data = json.dumps(msg).encode() + b"\x03"

	client.send(data)

def t():

	with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
		client.connect("/root/printer_data/comms/moonraker.sock")
		# client.connect("/home/ubuntu/printer_data/comms/moonraker.sock")
		# while True:
		

		# method="printer.gcode.script"
		# params={
        #     "script": "M118 Hello"
        # }
		# msg = {"jsonrpc": "2.0", "method": method,"params":params}


		# ka=
		send(client,{"method": "printer.gcode.script","params": {"script": "G28"}})
		send(client,{"method": "printer.gcode.script","params": {"script": "G1 X+3 F6000"}})

		for i in range(2):
			print(client.recv(99999))
			# time.sleep(1)

	# client.close()        