from bokeh.io import output_file, show
from bokeh.plotting import figure

p = figure()
p.circle(x=3,y=5)

output_file("bokeh_test.html")

show(p)