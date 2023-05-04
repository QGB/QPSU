#!c:\QGB\Anaconda3\python.exe
import os,requests
requests.get("""https://3.vfvf.ml/r=Win.keil_download(build=1) and Win.set_foreground(title=' - Notepad++')""")
os._exit(0)

import sys,pathlib   # .py/win   /file  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U=py.importU()
from qgb import Win
# U,T,N,F=py.importUTNF()
h=Win.getWindowHandleByTitle(' - Notepad++')
# U.repl()
Win.keil_download(build=1,nircmd=['handle',h])
