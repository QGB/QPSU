import sys;'qgb.U' in sys.modules or sys.path.append('C:/QGB/babun/cygwin/bin/');from qgb import *

from bokeh.plotting import figure
from bokeh.io import output_notebook, push_notebook, show

# output_notebook()
from bokeh.resources import INLINE
output_notebook(INLINE) # 需要在jupyter内运行？
U.pln(U.pid,INLINE)
U.pause()

plot = figure()
plot.circle([1,2,3], [4,6,5])

handle = show(plot, notebook_handle=True)

# Update the plot title in the earlier cell
plot.title.text = "New Title"
push_notebook(handle=handle)


