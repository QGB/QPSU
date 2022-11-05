#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()
##### fix #####
U.logging.root.handlers[0].stream=sys.stderr
U.set_env(KICAD_SYMBOL_DIR=r'C:\Program Files\KiCad\share\kicad\library')


#################
#C:\Program Files\KiCad\6.0\bin>
# python -m pip install -i http://pypi.doubanio.com/simple --trusted-host pypi.doubanio.com   dill ipython
#pip install skidl
from skidl import *  
from skidl import generate_pcb

# Create part templates.
q = Part("Device", "Q_PNP_CBE", dest=TEMPLATE)
r = Part("Device", "R", dest=TEMPLATE)

# Create nets.
gnd, vcc = Net("GND"), Net("VCC")
a, b, a_and_b = Net("A"), Net("B"), Net("A_AND_B")

# Instantiate parts.
gndt = Part("power", "GND")             # Ground terminal.
vcct = Part("power", "VCC")             # Power terminal.
q1, q2 = q(2)                           # Two transistors.
r1, r2, r3, r4, r5 = r(5, value="10K")  # Five 10K resistors.

# Make connections between parts.
a & r1 & q1["B C"] & r4 & q2["B C"] & a_and_b & r5 & gnd
b & r2 & q1["B"]
q1["C"] & r3 & gnd
vcc += q1["E"], q2["E"], vcct
gnd += gndt

netlist=generate_netlist()


# py.pdb()()
print(generate_pcb())
