def all_j_diff(*lists):
	ra=[]
	for ilist in lists:
		for i in ilist:
			if not (py.istr(i) or py.isnumeric(i)