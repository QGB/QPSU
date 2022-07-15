#coding=utf-8
import sys,pathlib				# *.py  /qgb   /[gsqp]
gsqp=pathlib.Path(__file__).absolute().parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()


import numpy  # as np
#True False array。 
def test():
	a = (a < 255).astype(numpy.int_) # <255 变 1， 255及以上 变0
	a[:,6] # 获取 第 6 列
	
	
def counts(a,return_dict=True,one_value=False):
	
	unique, counts = numpy.unique(a, return_counts=True)	
	r= numpy.asarray((unique, counts)).T.tolist()
	if one_value and py.len(r)==1:
		return r[0][0]
	if return_dict:
		return py.dict(r)
	return r
	
def reverse_enumerate(a):
	m=a.shape[0]-1
	#(0,),v
	for n,v in py.enumerate(numpy.flip(a)):
		yield m-n,v
		
def enumerate(a,reverse=False):
	'''
0,v0 ... 9,v9
reverse:
9,v9 ... 0,v0
'''	
	if reverse:
		return reverse_enumerate(a)
	else:
		return py.enumerate(a)


#select columns by condition from 3d array
def select_columns(a,condition):
	''' condition: list of bool
	'''
	return a[:,condition]

def expand_2d_array(a,top=0,bottom=0,left=0,right=0,mode='constant',constant_values=0):
	''' only support 2d array
bottom	= 0

	'''
	return numpy.pad(a,[(top,bottom),(left,right)],mode,constant_values=constant_values)
pad=pad2d=expand_array	

def pad_array(a,pad_width,mode='constant',constant_values=0):
	''' pad_width: [(d1_head,d1_tail),(d2_head,d2_tail), ...]
	'''
	return numpy.pad(a,pad_width,mode,constant_values=constant_values)