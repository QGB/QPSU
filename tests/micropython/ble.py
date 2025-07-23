from machine import Pin, Timer, SoftI2C
from time import sleep_ms
import ubluetooth
# from esp32 import raw_temperature
# from hdc1080 import HDC1080
import gc
	
class BLE():
	def __init__(self, name):   
		self.name = name
		self.ble = ubluetooth.BLE()
		self.ble.active(True)

		self.led = Pin(12, Pin.OUT)
		self.timer1 = Timer(0)
		# self.timer2 = Timer(1)
		
		self.disconnected()
		self.ble.irq(self.ble_irq)
		self.register()
		self.advertiser()

	def connected(self):		
		self.timer1.deinit()
		# self.timer2.deinit()
	
	def blink(self,a):
		'''a= Timer(3fca88b0; alarm_en=1, auto_reload=1, counter_en=1) '''
		# print(a)
		self.led(1)
		sleep_ms(200)
		self.led(0)
	def disconnected(self):		
		self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=self.blink )
		
		# self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0))   

	def ble_irq(self, event,data):
		print(event,data)
		if event == 1:
			'''Central disconnected'''
			self.connected()
			self.led(1)
		
		elif event == 2:
			'''Central disconnected'''
			self.advertiser()
			self.disconnected()
		
		elif event == 3:
			'''New message received'''			
			buffer = self.ble.gatts_read(self.rx)
			message = buffer.decode('UTF-8').strip()
			print(message)			
			if message == 'red_led':
				red_led.value(not red_led.value())
				print('red_led', red_led.value())
				self.send('re	d_led' + str(red_led.value()))
			elif message=='ip':
				rs=repr(sta_if.ifconfig())
				self.send(rs)
			elif message.startswith('!'):
				ssid,pw=message[1:].split(',')
				# sta_if.active(True)
				if not sta_if.isconnected():
					sta_if.disconnect()
					sta_if.connect(ssid,pw);
				with open('webrepl_cfg.py' ,'w') as f:
					f.write("""
PASS='1234'
dsp={'%s':'%s'}
					""".strip()%(ssid,pw))
				self.send('OK')
			elif message == '1':
				self.send('str(sensor.read_temperature(True))')
				# print(sensor.read_temperature(True))
			else:
				gc.collect()#M.gc()
				try:
					exec(message,globals(),locals())
					if 'r' in locals():
						r=locals()['r']
						if not isinstance(r,str):
							r=repr(r)
					else:
						r='can not found r in locals()'
				except Exception as e:
					r=repr(e)
					del e
				self.send(r)		   
		   
		   
	def register(self):		
		# Nordic UART Service (NUS)
		NUS_UUID ='6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
		RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
		TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
			
		BLE_NUS = ubluetooth.UUID(NUS_UUID)
		BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
		BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
			
		BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
		SERVICES = (BLE_UART, )
		((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

	def send(self, data):
		self.ble.gatts_notify(1, self.tx, data + '\n')#OSError: -128

	def advertiser(self):
		name = bytes(self.name, 'UTF-8')
		self.ble.gap_advertise(100, bytearray(b'\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)
		
# test
# i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
# sensor = HDC1080(i2c)
red_led = Pin(2, Pin.OUT)
# if __name__=='__main__':
def main():
	try:
		ble = BLE("ESP32")
		print(ble)
	except Exception as ble:
		ble=ble