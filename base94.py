#!/usr/bin/python
#base94 decode

tati_string = "replace me"

def decode(input):
	output = 0
	base = T.asciiPrint[1:]
	power = 0
	for c in input:
		output += base.index(c) * len(base)**power
		power += 1
	return T.i2s(output,94,base)
 
 
def encode(input):
	output = ''
	base = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}'
	while input > 0:
		r = input % len(base)
		output += base[r]
		input = int((input-r) / len(base))
	return output

i=decode(tati_string)

print i,type(i),encode(i)