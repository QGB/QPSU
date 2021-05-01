import numpy as np
#True False array。 
a = (a < 255).astype(np.int_) # <255 变 1， 255及以上 变0
a[:,6] # 获取 第 6 列