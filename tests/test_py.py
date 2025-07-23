#coding=utf-8
import unittest

import sys;'qgb.U' in sys.modules or sys.path.append('G:/QGB/babun/cygwin/lib/python2.7/');from qgb import *
py=U.py

class T(unittest.TestCase):
    def test_istr(self):
        self.assertEquals(py.istr(b'123'),False )
        self.assertEquals(py.istr(unicode()) ,True   )
		
if __name__ == '__main__':
    unittest.main()

#python3 test_py.py
#pass ,2 fail