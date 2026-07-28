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

##### pip install
```
pip install qpsu
```

可选安装依赖

```
mamba install -c conda-forge -y cchardet plyvel

pip install requests urllib3 lxml beautifulsoup4 numpy pillow cryptography pandas matplotlib openpyxl pyyaml pyparsing psutil tqdm pytz python-dateutil chardet six scapy paramiko tornado aiohttp flask werkzeug websockets watchdog pyqrcode pyzbar pyaxmlparser pyDes rsa passlib demjson3 xlrd xlwt xmltodict PyPDF2 jieba nest-asyncio sortedcontainers sympy colormath lemminflect markdown html2text cssselect progressbar ping3 dill pympler python-miio msmart fake-headers tld tftpy zhconv

```


