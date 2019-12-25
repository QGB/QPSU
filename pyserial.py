from . import py
U,T,N,F=py.importUTNF()
import serial
ENCODING=U.get(__name__+'_encoding','utf-8')
devs=U.get(__name__+'_devs',{})
g=U.get(__name__+'_g')
if g:
    devs[g.port.upper()]=g

def list_all_com_ports():
    from serial.tools import list_ports
    r={}
    for cp in list_ports.comports():    
        d=r[cp.device]=(cp.__dict__)
        d['obj']=cp
    return r
list=list_all=list_com=list_com_ports=list_all_com_ports

def set(var):
    a=U.getArgsDict()
    if py.len(a)!=1:raise py.EnvironmentError(var,a)
    k,v=a.popitem()
    if var!=v:raise py.EnvironmentError('var,v not match',var,v)
    if not var:
        return U.get(__name__+'_'+k)
    if k=='g':
        devs[dev.port.upper()]=dev
        U.set(__name__+'_devs',devs)
    return U.set(__name__+'_'+k,var)

def set_g(dev):
    global g
    # if not dev:return py.No()
    devs[dev.port.upper()]=dev
    U.set(__name__+'_devs',devs)
    g=U.set(__name__+'_g',dev)
    return g
def open_device(dev, baudrate=115200, timeout=5,dtr=False):
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
    if isinstance(dev,serial.Serial):
        dev=dev.port
        # return set_g(dev)
    if py.isint(dev):
        dev='COM{}'.format(dev)
    dev=dev.upper()
    for k in py.list(devs):
        if k.upper()==dev:
            v=devs[k]
            try:
                v.flush()
                return set_g(v)
            except serial.SerialException:
                devs.pop(k)
    com = serial.Serial()
    com.port = dev
    com.baudrate = baudrate
    com.timeout = timeout
    com.setDTR(dtr)
    com.open()
    return set_g(com)
    
open=open_port=open_dev=open_device

def write_one_line(input,dev=None,wait=1,encoding=ENCODING,eol=b'\r\n',p=True):
    global g
    if not dev:dev=g=U.get(__name__+'_g')
    else      :g=U.set(__name__+'_g',dev)
    if not py.isbytes(input):
        input=str(input)
    if py.istr(input):
        input=input.encode(encoding)
    if not input.endswith(eol):
        input+=eol
    try:
        g.write(input)
    except serial.SerialException:
        g=open_device(dev=g.port,baudrate=g.baudrate,timeout=g.timeout,
            dtr=g._dtr_state, )
        g.write(input)
    U.sleep(wait)
    return read_all(dev=g,encoding=encoding,p=p)
w=write=write_line=write_one_line


def read_all(dev=None,encoding=ENCODING,p=True):
    global g
    if not dev:dev=g=U.get(__name__+'_g')
    else      :g=U.set(__name__+'_g',dev)
    b=g.read_all()
    if p:
        try:
            s=b.decode(encoding)
        except Exception as e:
            return b,e
        if s:print(s)
        return None
    return b
r=read=read_all
def read_all_wait(dev,wait):
    wait=py.max(0.1,wait)
    r=b''
    while 1:
        U.sleep(wait)
        c=dev.read(dev.in_waiting)
        if c:
            r+=c
        else:
            return r
if U.iswin():
    isWin=True
    from serial import win32 

def dtr_click(dev=None,wait=0.2):
    '''s.setDTR(False) '''
    if not dev:dev=g
    if dev.dtr:
        dev.dtr=0
        U.sleep(wait)
        dev.dtr=1
    else:
        dev.dtr=1
        U.sleep(wait)
        dev.dtr=0
        
def dtr_high(dev=None):
    '''s.setDTR(False) '''
    if not dev:dev=g
    if isWin:r=win32.EscapeCommFunction(dev._port_handle, win32.CLRDTR)
high=dtr_high
def dtr_low(dev=None):
    if not dev:dev=g
    if isWin:r=win32.EscapeCommFunction(dev._port_handle, win32.SETDTR) #r=1
l=o=low=dtr_low

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

AT_TIMEOUT=U.get(__name__+'_'+"AT_TIMEOUT",6)
AT_P=U.get(__name__+'_AT_'+"P",True)
AT_EOL=U.get(__name__+'_AT_'+"EOL",b'\r\n')
def AT(cmd='',dev=None,timeout=AT_TIMEOUT,p=AT_P,encoding=ENCODING,eol=AT_EOL):
    if not dev:dev=g
    cmd=set(cmd)
    if cmd[:3] not in {'AT+',b'AT+'}:
        cmd=cmd.upper() # bytes ok
    if not cmd:
        cmd=b'AT'
    if not py.isbytes(cmd):cmd=cmd.encode(encoding)
    if not cmd.startswith(b'AT'):cmd=b'AT+'+cmd
    b=read_all(dev=dev,encoding=encoding,p=0)
    if b:
        print(b.decode(encoding))
        print('='*11,len(b),'='*11)
    t=timeout*0.001
    start = U.timestamp()
    dev.write(cmd+eol)
    U.sleep(max(0.5,t))
    b=dev.read(dev.in_waiting)
    blines=b.splitlines()
    if blines[0].strip()!=cmd.strip():
        return py.No('{}!={}'.format(b,cmd))
    while len(blines)<4: # err=4,gmr=7  
        c = dev.read(1)
        if c:
            b=b+c+read_all_wait(dev=dev,wait=t)
            # b=b+c+dev.read_all()
            break
        if (U.timestamp()-start)>timeout:
            return py.No('timeout',timeout,b)    
        U.sleep(t)
    time=U.timestamp()-start
    if p:
        try:
            s=b.decode(encoding)
        except:
            s=b
        print(s.strip())
        print('takes {:.3f} sec'.format(time,) , '%s blines'%len(blines), )
        return None
    return b,time
at=AT   

def AT_CSYSHEAP(dev=None,encoding=ENCODING):
    if not dev:dev=g
    for cmd in ['AT+CSYSHEAP',]:#'AT+CSYSFLASH',
        b,time= AT(cmd=cmd  ,  dev=dev,p=0)
        s=b.decode(encoding)
        U.p(s)
        i=T.filter_int(s,3)
        if i:
            i=py.int(i[0])
            U.p(F.readableSize(i),'\ntakes %.3f sec'%time , )
        
    
df=disk_usage=AT_CSYSHEAP

def AT_CWLAP(dev=None):
    if not dev:dev=g
    r=AT(cmd='AT+CWLAP'  ,  dev=dev,p=False)
lap=at_cwlap=AT_CWLAP

def AT_CWJAP(name,password,dev=None,timeout=AT_TIMEOUT,p=AT_P):
    if not dev:dev=g
    return AT(cmd='AT+CWJAP="{}","{}"'.format(name,password),
            dev=dev,timeout=timeout,p=p)
jap=at_jap=at_cwjap=AT_CWJAP

def AT_PING(ping_host=None,dev=None,timeout=AT_TIMEOUT,p=AT_P):
    if not dev:dev=g
    ping_host=set(ping_host)
    return AT(cmd='AT+PING="{}"'.format(ping_host),
            dev=dev,timeout=timeout,p=p)

ping=at_ping=AT_PING