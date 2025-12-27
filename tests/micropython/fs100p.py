def send(b,eol=\r\n wait_time=0.2):
 uart.write(b)
 time.sleep(wait_time)
 return uart.read(100) or b''
 
 
 
def send(b, wait_time=0.2):
 if isinstance(b, str):b = b.encode()
 uart.write(b)
 time.sleep(wait_time)
 return uart.read(100) or b''
 
import machine,time
uart=machine.UART(1, baudrate=115200, tx=8, rx=5, timeout=1000)  
def send(b, eol='\r\n', wait_time=0.2,p=0,rsize=1024):
 if isinstance(b, str):b=b.encode() + eol.encode()
 uart.write(b)
 time.sleep(wait_time)
 rb=uart.read(rsize)
 if p:print(rb)
 return rb
 
 send('+++', eol='', wait_time=1.1)
 send('a', eol='')
 
 
def http(host='192.168.1.199',port=1144,method='GET', path='/', headers=None, body=None,wait_sec=1):
 # send(f'AT+SOCK=TCPC,"{host}",{port}',)
 send('AT+SOCK=TCPC,192.168.1.199,1144,1144',p=1)
 send('AT+ENTM',p=1)
 time.sleep(wait_sec)
 request = f'{method} {path} HTTP/1.1\r\nHost: {host}\r\n'
 if headers:request += f"{headers}\r\n"
 if body: request += f"Content-Length: {len(body)}\r\n\r\n{body}"
 else: request += "\r\n"
 uart.write(request.encode())
 time.sleep(wait_sec)
 return uart.read(1000)
 
 
def get_public_ip():
 send('AT+SOCK=TCPC,"myip.ipip.net",80')
 send('AT+ENTM')
 time.sleep()
 uart.write(b'GET / HTTP/1.1\r\nHost: myip.ipip.net\r\nConnection: close\r\n\r\n')
 time.sleep(2)
 return uart.read(500)
 
 
send('AT+SOCK=TCPC,192.168.1.199,1144,1144', p=1)
send('AT+ENTM', p=1)
time.sleep(1)
request='GET / HTTP/1.1\r\nHost: 192.168.1.199\r\n\r\n'
uart.write(request)
time.sleep(1)
uart.read(1000)