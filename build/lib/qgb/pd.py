from pandas import *

def df_to_namedtuples(df):
	from collections import namedtuple
	cs= df.columns
	
	Row = namedtuple('Row',cs)
	for row in df.itertuples():
		yield Row(*row[1:])
yield_namedtuple=df2namedtuples=df_to_namedtuples		

def read_csv(file,encoding=None,delimiter=',',keep_default_na=False,):
	''' keep_default_na : use float nan ,not empty string ''
the  na_filter=False can change your columns type to object
	
	'''
	file=autoPath(file)
	if not encoding:encoding=detectEncoding(file)
	import pandas as pd
	df = pd.read_csv(file, delimiter=delimiter,encoding=encoding,keep_default_na=keep_default_na)
	r=[]
	is1=False
	if py.len(df.columns)==1:is1=True
	for i in df.values:
		if is1:
			r.append(i[0])
		else:
			r.append(tuple(i))
	return r	
	