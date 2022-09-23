#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()
N.rpcServer(globals=globals(),locals=locals(),port=1122,currentThread=0,no_banner=1)

import pdb
# import ipdb.__main__

def foo(x):
  return x+1

class RunningTrace():
  def set_running_trace(self):
    frame = sys._getframe().f_back
    self.botframe = None
    self.setup(frame, None)
    while frame:
      frame.f_trace = self.trace_dispatch
      self.botframe = frame
      frame = frame.f_back
    self.set_continue()
    self.quitting = False
    sys.settrace(self.trace_dispatch)

class ProgrammaticPdb(pdb.Pdb, RunningTrace):
  pass

# class ProgrammaticIpdb(ipdb.__main__.debugger_cls, RunningTrace):
  # pass

pp = ProgrammaticPdb()
#pp = ProgrammaticIpdb(ipdb.__main__.def_colors)

#pp.onecmd('b bar.py:38') # Works before set_running_trace
pp.set_running_trace()
pp.onecmd('b foo')       # only works after calling set_running_trace
# pp.onecmd('exit')       # only works after calling set_running_trace
# pp.onecmd('l')

x=-1
x=2
x=0
x=foo(x)

print('foo ',x)

# N.rpcServer(globals=globals(),locals=locals(),port=U.pid,currentThread=1,no_banner=1)