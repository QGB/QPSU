import numpy as np
#True False array。 
def test():
	a = (a < 255).astype(np.int_) # <255 变 1， 255及以上 变0
	a[:,6] # 获取 第 6 列
	
	
def counts(a):
	
	unique, counts = np.unique(a, return_counts=True)	
	return np.asarray((unique, counts)).T.tolist()