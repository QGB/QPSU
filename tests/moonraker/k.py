import sys;'qgb.U' in sys.modules or sys.path.insert(0,'/mnt/c/QGB/babun/cygwin/bin/');from qgb import *
import libinput.constant,time
print(libinput.constant.Event.KEYBOARD_KEY)
import json,socket

def send_gcode(client,gcode):
    if gcode.startswith('G1 '):
        gcode='G91\n'+gcode
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
gmove_unit=10
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
    send_gcode(client,f'M220 S300')
    # for i in range(999):
    #     if wsm:            
    #         try:
    #             break
    #         except Exception as e:
    #             gerr.append([e,sf])
    #             continue
    #     if server:
    #         try:
    #             wsm=server.lookup_component("websockets")
    #             break
    #         except:continue
    #     if not server and 'server' in g:
    #         server=g['server']
    #     time.sleep(0.1)    
        # send_gcode(0,wsm,e)

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
                if kcode == libinput.define.Key.KEY_LEFT:
                    send_gcode(client,f'G1 X-{gmove_unit} F6000')
                if kcode == libinput.define.Key.KEY_RIGHT:
                    send_gcode(client,f'G1 X+{gmove_unit} F6000')
                if kcode == libinput.define.Key.KEY_HOME:
                    send_gcode(client,'G28')
            elif kstate == libinput.constant.KeyState.RELEASED:
                print(f"{td:.3f} {kcode} released")
                
        t0=t
# key_thread=U.thread(target=read_key_events)
# key_thread.start()
# client=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
if __name__ == "__main__":
    N.rpcServer(globals=globals(),locals=locals(),port=7126)
    read_key_events()