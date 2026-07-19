def all_j_diff(*lists):
	ra=[]
	for ilist in lists:
		for i in ilist:
			if not (py.istr(i) or py.isnumeric(i)):
				pass  # 处理非字符串或数字的情况
	return ra