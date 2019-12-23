from . import py
U,T,N,F=py.importUTNF()
import serial
ENCODING=U.get(__name__+'_encoding','utf-8')
g=U.get(__name__+'_g')

def list_all_com_ports():
    from serial.tools import list_ports
    r={}
    for cp in list_ports.comports():    
        d=r[cp.device]=(cp.__dict__)
        d['obj']=cp
    return r
list=list_all=list_com=list_com_ports=list_all_com_ports

def open_device(device, baudrate=115200, timeout=5,dtr=False):
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
    if py.isint(device):
        device='COM{}'.format(device)
    com = serial.Serial()
    com.port = device
    com.baudrate = baudrate
    com.timeout = timeout
    com.setDTR(dtr)
    com.open()
    g=com
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

if U.iswin():
    isWin=True
    from serial import win32 
def dtr_high(dev=None):
    '''s.setDTR(False) '''
    if not dev:dev=g
    if isWin:win32.EscapeCommFunction(dev._port_handle, win32.CLRDTR)

def dtr_low(dev=None):
    if not dev:dev=g
    if isWin:win32.EscapeCommFunction(dev._port_handle, win32.SETDTR)

def swi(a,b,time,dev=None):
    if not dev:dev=g
    count=[0]
    try:
        _sw(dev,count,time,a,b)
    except:
        pass
    finally:
        dtr_high(dev) # shutdown
    return count[0]

def sw(a,b,time=U.IMAX,dev=None):
    if not dev:dev=g
    a=0.000001*a
    b=0.000001*b
    count=[0]
    try:
        _sw(dev,count,time,a,b)
    except:
        pass
    finally:
        dtr_high(dev) # shutdown
    return count[0]
gb_sw=True
def _sw(dev,count,time,a,b):
    ''' micro second '''
    global gb_sw
    gb_sw=True
    start=U.timestamp()
    while gb_sw:
        count[0]+=1
        if (U.timestamp()-start)>time:
            return
        if count[0]%2==0:
            dtr_low(dev)
            U.sleep(a)
        else:
            dtr_high(dev)
            U.sleep(b)
