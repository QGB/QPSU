import sys
from pathlib import Path
gsqp=Path(__file__).parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works

if len(sys.argv )>1:
	if sys.argv[1].lower() in ['eval','rpc','oncall']:
		from qgb import N
		N.rpcServer()

if len(sys.argv )==1:
	from qgb import U
	U.main() 


# from __future__ import absolute_import
# try:
	# from qgb import U
# except:
	# from . import U


