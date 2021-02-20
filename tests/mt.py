gdpin={}

import M

M.f=open('data.txt','w')

import machine
for index in range(44):
	if index in [6,7,8,9,10,11,12]:
		M.f.write('=='+str(index)+'\n')
		M.f.flush()
		continue
	M.f.write(str(index)+'\n')
	M.f.flush()
	print(index)
	if (index,0) in gdpin:
		print('skip0-',index)
		continue
	try:
		gdpin[(index,0)]=machine.Pin(index, machine.Pin.IN, machine.Pin.PULL_UP)
	except Exception as e:
		print(index,e)
for k,p in gdpin.items():
	print(p.value(),k[0])
	
# machine.Pin( , machine.Pin.IN, machine.Pin.PULL_UP)	