#coding=utf-8  
import sys,pathlib					 # *.py  /qgb   /[gsqp]
gsqp=pathlib.Path(__file__).absolute().parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import jieba.posseg as pseg

def participle(s):
	d={}
	max_len=0
	for pair in pseg.cut(s):
		w=pair.word
		len=T.wcswidth(w)
		if len>max_len:
			max_len=len
		if w in d:
			if d[w][0]!=pair.flag:
				U.set(__surfix='jb.participle.',s=s,pair=pair,d=d)
				raise Exception('Unexpected ')
			d[w][-1]+=1
		else:
			d[w]=[pair.flag,1]
	return [(U.StrRepr(w,size=max_len),U.StrRepr(v[0],size=3),v[1]) for w,v in d.items()]
词性标注=分词=fc=fenci=participle