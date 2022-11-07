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
# from skidl import *  
# from skidl import generate_pcb

import skidl,kinparse

def my_empty_footprint_handler(part):
    """Function for handling parts with no footprint.

    Args:
        part (Part): Part with no footprint.
    """
    ref_prefix = part.ref_prefix.upper()

    if ref_prefix in ("R", "C", "L") and len(part.pins) == 2:
        # Resistor, capacitors, inductors default to 0805 SMD footprint.
        part.footprint = 'Resistor_SMD:R_0805_2012Metric'

    elif ref_prefix in ('Q',) and len(part.pins) == 3:
        # Transistors default to SOT-23 footprint.
        part.footprint = 'Package_TO_SOT_SMD:SOT-23'

    else:
        # Everything else goes to the default empty footprint handler.
        skidl.default_empty_footprint_handler(part)

# Replace the default empty footprint handler with your own handler.
skidl.empty_footprint_handler = my_empty_footprint_handler

# Create parts with no footprints.
r = skidl.PartTmplt("Device", "R")
r1, r2 = r(), r()
r2.footprint='Resistor_SMD:R_1206_3216Metric'

# Generate a netlist. R1 has no footprint so it will be assigned an 0805.
# R2 already has a footprint so it will not change because it is not passed
# to the empty footprint handler.

snetlist=skidl.generate_netlist()

netlist=kinparse.parse_netlist(snetlist)
for n,part in enumerate(netlist.parts):
    #fp_lib, fp_name = part.footprint.split(":")
    #print(n,fp_lib, fp_name)
    print(n,part.footprint)
# py.pdb()()
# print(generate_pcb())
