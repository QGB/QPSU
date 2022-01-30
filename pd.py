from pandas import *

def df_to_namedtuples(df):
	from collections import namedtuple
	cs= df.columns
	
	Row = namedtuple('Row',cs)
	for row in df.itertuples():
		yield Row(*row[1:])
yield_namedtuple=df2namedtuples=df_to_namedtuples		

