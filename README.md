# QGB's Python Simplified Utils
## Usability important than performance

In this project, 'qgb' is the top module name.<br>
QPSU also called 'UTNF' because qgb module mainly directly contains :
```
    qgb.U (Utils main) ,
    qgb.T (Text utils) ,
    qgb.N (Network utils) ,
    qgb.F (File utils)
```

`qgb.py` module is a independent lightweight wrapper of python core api.

Full document see: https://deepwiki.com/QGB/QPSU/2.4-n-module-(network-core)

### Install
##### directly clone 
```
$ git clone https://github.com/QGB/QPSU qgb
$ python -m qgb # it will print like below

import sys;'qgb.U' in sys.modules or sys.path.append('/home/qgb/');from qgb import *

# now, you can paste this line to your IPython or python project.

from qgb import * # equals: from qgb import U,T,N,F,py 
# if in Windows system, Win module automatically added.
# if in IPython, ipy module automatically added.
```

##### pip install   # TODO

