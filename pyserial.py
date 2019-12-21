import serial

def list_com_ports():
    from serial.tools import list_ports
    r={}
    for cp in list_ports.comports():    
        d=r[cp.device]=(cp.__dict__)
        d['obj']=cp
    return r



