from . import py
U,T,N,F=py.importUTNF()
import serial
ENCODING='utf-8'
g=U.get(__name__+'_g')

def list_all_com_ports():
    from serial.tools import list_ports
    r={}
    for cp in list_ports.comports():    
        d=r[cp.device]=(cp.__dict__)
        d['obj']=cp
    return r
list=list_all=list_com=list_com_ports=list_all_com_ports

def open_device(device, baudrate=115200, timeout=5):
    '''    'COM4',b,timeout=5sec
    def __init__(self,
                 port=None,
                 baudrate=9600,
                 bytesize=EIGHTBITS,
                 parity=PARITY_NONE,
                 stopbits=STOPBITS_ONE,
                 timeout=None,
                 xonxoff=False,
                 rtscts=False,
                 write_timeout=None,
                 dsrdtr=False,
                 inter_byte_timeout=None,
                 exclusive=None,
                 **kwargs):
'''
    global g
    g=serial.Serial(device, baudrate, timeout=timeout) 
    U.set(__name__+'_g',g)
    return g
open=open_port=open_device

def write_one_line(input,dev=None,wait=1,encoding=ENCODING,p=True):
    global g
    if not dev:dev=g=U.get(__name__+'_g')
    else      :g=U.set(__name__+'_g',dev)
    if py.istr(input):
        input=input.encode(encoding)
    if not input.endswith(b'\r\n'):
        input+=b'\r\n'
    g.write(input)
    U.sleep(wait)
    return read_all(dev=g,encoding=encoding,p=p)
w=write=write_line=write_one_line


def read_all(dev=None,encoding=ENCODING,p=True):
    global g
    if not dev:dev=g=U.get(__name__+'_g')
    else      :g=U.set(__name__+'_g',dev)
    b=g.read_all()
    s=b.decode(encoding)
    if(p):
        print(s)
        return None
        return len(b)
    return b
r=read=read_all

