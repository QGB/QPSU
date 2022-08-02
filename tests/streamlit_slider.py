#coding=utf-8
import sys,pathlib				 # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()


# from __future__ import absolute_import #没用 
# import ast 
# print(ast)
# from matplotlib import rcsetup       

import streamlit.bootstrap

import streamlit as st

x = st.slider('angle',0,70)
st.write(x, 'squared is', x * x)


def ft(*a,**ka):
	global t
	print(U.stime(),t,a,ka)
t = st.slider('temperature',16.0,32.0,step=0.1,on_change=ft,key='t')
st.write(t, 'squared is', t * t)
st.write(st.session_state)


# streamlit.bootstrap.run(__file__,command_line='',args=[], flag_options={})