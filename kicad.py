#coding=utf-8
import sys,pathlib				 # .py/qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import pcbnew
################################################
import locale
locale.setlocale(locale.LC_ALL, '')


################################################
def text(t="Hello",x=90000000,y=90000000,pcb=None):
	# pcb = pcbnew.BOARD()
	if not pcb:pcb = pcbnew.GetBoard()
	# txt = pcbnew.TEXTE_PCB(pcb) #AttributeError: module 'pcbnew' has no attribute 'TEXTE_PCB'
	txt = pcbnew.PCB_TEXT(pcb) # 6.0
	txt.SetText(t)
	txt.SetPosition(pcbnew.wxPoint(x,y))
	txt.SetHorizJustify(pcbnew.GR_TEXT_HJUSTIFY_CENTER)
	txt.SetTextSize(pcbnew.wxSize(10000000, 10000000))
	# txt.SetThickness(1000000) #AttributeError: 'PCB_TEXT' object has no attribute 'SetThickness'
	txt.SetTextThickness(1000000) 
	pcb.Add(txt)

	# pcb.Save('C:/Users/qgb/Documents/kicad-pdf/T/a.Save.kicad_pcb')
	
	return text
txt=text	

def get_pcb():
	return pcbnew.GetBoard()
pcb=get_pcb	
	
def drawLine(x1, y1, x2, y2, width=1,pcb=None):
	if not pcb:pcb = pcbnew.GetBoard()

	# line = pcbnew.DRAWSEGMENT()
	line = pcbnew.PCB_SHAPE()
	line.SetStart(pcbnew.wxPoint(x1, y1))
	line.SetEnd(pcbnew.wxPoint(x2, y2))
	line.SetLayer(pcbnew.Edge_Cuts)
	line.SetWidth(pcbnew.FromMM(width))
	pcb.Add(line)
	
	return line
	
def get_draw(e,pcb=None):
	if not pcb:pcb = pcbnew.GetBoard()
		
	if py.isint(e):
		if e<999:
			return GetDrawings()[e][1]
		else:
			e=py.hex(e)[2:].upper()
	if py.istr(e):
		# return [i[1] for i in GetDrawings() if e in i[-1]]
		return [py.repr(i) for i in pcb.GetDrawings()]
		e=[i for i in pcb.GetDrawings() if e in py.repr(i)][0]
	return e	
get=get_draw	
	
def get_length_of_two_point(start,end):
	return ((end.x-start.x)**2+(end.y-start.y)**2)**0.5
	
def GetDrawings(enumerate=False,pcb=None):
	if not pcb:pcb = pcbnew.GetBoard()
	r=[]
	for n,e in py.enumerate(pcb.GetDrawings()):
		t=''
		c=e.GetClass()
		try:
			if c=='PTEXT':
				t=e.GetText()
			if c=='PCB_SHAPE':
				t=[e.ShowShape(),e.GetWidth(),get_length_of_two_point(e.GetStart(),e.GetEnd()),e.GetStart(),e.GetEnd(),]
				
		except Exception as err:
			t=py.repr(err)
		r.append([n,e,c,t])	
	return r

def get_all_footprints(pcb=None):
	if not pcb:pcb = pcbnew.GetBoard()
	r=[]
	lfps=py.list(pcb.Footprints())
	ga=[U.StrRepr(i) for i in py.dir(lfps[0]) if i.startswith('Get')]
	r.append(['No.']+ga)
	for n,a in py.enumerate(lfps):
		row=[n]
		for s in ga:
			try:
				row.append(py.getattr(a,s)())
			except Exception as e:
				row.append(e)
			
		r.append(row)
		# path=a.GetPath().AsString()
		# r.append([n,a,a.GetPosition(),a.GetPadCount(),path,a.GetFPIDAsString(),])
	return r
fps=Footprints=get_all_footprints	
	
def set(e,t,x,y,pcb=None):
	if not pcb:pcb = pcbnew.GetBoard()
	e=get_draw(e,pcb=pcb)
	M=10**6
	if x<M:x=x*M
	if y<M:y=y*M

	e.SetPosition(pcbnew.wxPoint(x,y))
	e.SetText(t)
	return e,t,x,y
	
def set_footprint(f,x=0,y=0,pcb=None):
	if not pcb:pcb = pcbnew.GetBoard()
	f=F.auto_path(f)
	name=T.sub_last(f,'/','.kicad_mod')
	sp  =T.sub_last(f,'','/'+name)
	plugin = pcbnew.IO_MGR.PluginFind(1)
	m=plugin.FootprintLoad(sp,name)
	if not m:
		return py.No(f,name)
	m.SetPosition(pcbnew.wxPoint(x,y))#x横向右  y 纵向下
	pcb.Add(m)
	return m
	
def set_fp(f=r'C:\Program Files\KiCad\6.0\share\kicad\footprints\Connector_HDMI.pretty',pcb=None):
	if not pcb:pcb = pcbnew.GetBoard()
	# p=r'C:\Program Files\KiCad\6.0\share\kicad\footprints'
	f=F.auto_path(f)
	# 
	name=T.sub_last(f,'/','.pretty')
	
	src_type=pcbnew.IO_MGR.GuessPluginTypeFromLibPath(f)# int 1
	plugin = pcbnew.IO_MGR.PluginFind(src_type)
	
	M=13*10**6
	sp='C:/Program Files/KiCad/6.0/share/kicad/footprints/Connector_Molex.pretty/'
	fs=[i for i in F.ls(sp) if i.endswith('.kicad_mod')]
	dxi={0: 0, 2: 1, 3: 2, 18: 3, 19: 4, 20: 5, 21: 6, 22: 7, 26: 8}
	for x,y in U.range2d(27,27):
		if not (17<x<21 or x in [0,2,3,21,22,26]):continue
		n=x*27+y
		f=fs[n]
		_x=x
		x=dxi[x]
		# if y not in [0,1,8,9]:continue
		if y==0:
			text(f'{_x}',x*M*4,-2*M,pcb=pcb)
		name=T.sub_last(f,'/','.kicad_mod')
		m=plugin.FootprintLoad(sp,name)
		if not m:
			return f,name
		m.SetPosition(pcbnew.wxPoint(x*M*4,y*M))#x横向右  y 纵向下
		pcb.Add(m)
		# if n==99:break
	return src_type,plugin
	
	# m = pcbnew.FootprintLoad(f,name)
	
	# return f,m
	# return m
	
def add_pad( x=0,y=0,size=2, name='', pad_type='standard', shape='circle',
			drill=1.0, layers=None,pcb=0):
	"""Create a pad on the module
	Args:
		position: pad position in mm
		size: pad size in mm, value if shape == 'circle', tuple otherwise
		name: pad name/number
		pad_type: One of 'standard', 'smd', 'conn', 'hole_not_plated'
		shape: One of 'circle', 'rect', 'oval', 'trapezoid'
		drill: drill size in mm, single value for round hole, or tuple for oblong hole.
		layers: None for default, or a list of layer definitions (for example: ['F.Cu', 'F.Mask'])
	"""
	if not pcb:pcb = pcbnew.GetBoard()
		
	pad = pcbnew.PAD(pcb)
	return pad
	pad.type = pad_type
	pad.shape = shape
	pad.size = size
	pad.name = name
	pad.position = position
	pad.layers = layers

	self._module.Add(pad._pad)
	return pad

	
from KicadModTree import *
import KicadModTree
def km_text(kicad_mod,t,at=[6,6],size=[1,1]):
	kicad_mod.append(KicadModTree.Text(type='reference', text=t, at=at,size=size,layer='F.SilkS'))
	# kicad_mod.append(KicadModTree.Text(type='reference', text=t, at=at,size=size,layer='B.SilkS'))#lceda 不能有两个 reference  导入错误
	# kicad_mod.append(KicadModTree.Text(type='value', text='vf '+t, at=at,size=size,layer='F.SilkS'))
	# kicad_mod.append(KicadModTree.Text(type='value', text='vb '+t, at=at,size=size,layer='B.SilkS'))
	# at[1]+=5
	# kicad_mod.append(KicadModTree.Text(type='value', text=t, at=at,size=size,layer='F.Cu')) 
	kicad_mod.append(KicadModTree.Text(type='value', text=t, at=at,size=size,layer='B.Cu'))
	
def new_footprint_holes(start=0.25,end=5.9,step=0.01,delta=0.3):
	import numpy
	name=fr'{start}-{end},{step} holes  '
	kicad_mod = Footprint(name)
	kicad_mod.setDescription(name)
	km_text(kicad_mod,name,at=[-1,4]) 
	m=1
	for x in numpy.arange(start,end,step):
		x=py.float(x)
		print(m,type(x),x)
		# s=min(x+0.1,delta)
		s=x+0.1
		kicad_mod.append(Pad(number=x,type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
			at=[m,0], size=[s,s], drill=x, layers=Pad.LAYERS_THT))
		m=m+x+s	
	file_handler = KicadFileHandler(kicad_mod)
	fname=f'{T.file_legalized(name)}.kicad_mod'
	file_handler.writeFile(fname)
	
	return kicad_mod,fname
	
def new_footprint (w=17.5,yd=17.6,drill_1=0.96,drill_08=0.79,xt=0.1):
	if not xt:xt=w/2
	x0,y0=0,0
	
	tf=rf'"{w},{yd}\n{drill_1},{drill_08} {U.stime()[-8:]}"'
	tf=rf'"{w},{yd}\n{drill_1},{drill_08}  "'

	name=f"{tf[1:-1].replace(T.backslash+'n','='*12)}"
	kicad_mod = Footprint(name)
	kicad_mod.setDescription(name)
	# kicad_mod.setTags('q')

	# add model
	# kicad_mod.append(Model(filename="example.3dshapes/example_footprint.wrl",
						   # at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

	
	# km_text(kicad_mod,) # .split(' ')[0]
	km_text(kicad_mod,name,at=[-9,4+y0],size=[0.5,0.5]) #没有这句 lceda 导入错误
	# kicad_mod.append(KicadModTree.Text(type='value',text=tf,at=[xt,10],size=[1,1],mirror=True,layer='B.SilkS'))
	# kicad_mod.append(KicadModTree.Text(type='value',text='w,yd',at=[8,2],size=[1,1],layer='B.SilkS'))
	# kicad_mod.append(KicadModTree.Text(type='value',text=tf,at=[8,6],size=[1,1],mirror=Fa,layer='B.SilkS'))
		# create courtyard
	# kicad_mod.append(RectLine(start=[-3, -3], end=[17, 17], layer='F.CrtYd'))

	kicad_mod.append(RectLine(start=[0+x0, 0], end=[w+x0, yd], layer='F.SilkS'))
	kicad_mod.append(RectLine(start=[0+x0, 0], end=[w+x0, yd], layer='B.SilkS'))

	for n in range(12):	
		kicad_mod.append(Pad(number=n,type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
			at=[x0+ n*1.27+1.7, 0+yd], size=[drill_08-0.2, 1.6], drill=drill_08, layers=Pad.LAYERS_THT))
			
		n1y=[2.2,4.4][(n+1)%2]	
		kicad_mod.append(Pad(number=n, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
			at=[x0+ n*1.27+1.7, 0+yd+n1y], size=[0.25, n1y*1.7	], drill=drill_1, layers=Pad.LAYERS_THT))				 
	for n in range(14):					 
		sx=4
		n1x=[2.2,4.4][(n+1)%2]
		if n==13:
			sx=1.6
			kicad_mod.append(Pad(number=n, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,at=[x0-sx,n*1.27], size=[sx,0.55], drill=0, layers=Pad.LAYERS_THT))	
			kicad_mod.append(Pad(number=n, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,at=[x0+ w+sx,n*1.27], size=[sx,0.55], drill=0, layers=Pad.LAYERS_THT))	
			
		kicad_mod.append(Pad(number=n, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,at=[x0-n1x,n*1.27], size=[n1x*1.35, 0.25], drill=drill_1, layers=Pad.LAYERS_THT))				 
		kicad_mod.append(Pad(number=n, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,at=[x0+ w+n1x,n*1.27], size=[n1x*1.35, 0.25], drill=drill_1, layers=Pad.LAYERS_THT))				 
						 
		kicad_mod.append(Pad(number=n, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
						 at=[x0,n*1.27], size=[sx, drill_08-0.2], drill=drill_08, layers=Pad.LAYERS_THT)) #左 14
						
						 
		kicad_mod.append(Pad(number=n, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
						 at=[x0+ w,n*1.27], size=[sx, drill_08-0.2], drill=drill_08, layers=Pad.LAYERS_THT))

	# output kicad model	
	file_handler = KicadFileHandler(kicad_mod)
	fname=f'{T.file_legalized(name)}.kicad_mod'
	file_handler.writeFile(fname)
	
	return kicad_mod,fname
	
def generate_all():
	l4_9_1116=[
 (17.8, 18.0, 0.94, 0.76),
 (18.0, 18.2, 0.95, 0.77),
 (18.2, 18.4, 0.96, 0.78),
 (18.4, 18.6, 0.96, 0.79),
 (18.5, 18.7, 0.96, 0.79),
 (18.6, 18.8, 0.96, 0.79),
 (18.7, 18.9, 0.96, 0.80),
 (18.8, 19.0, 0.96, 0.81),
 (19.1, 19.3, 0.96, 0.82)]
 
	l4_9_1123=[
 (18.30, 18.10, 0.90, 0.70),
 (18.35, 18.15, 0.90, 0.70),
 (18.40, 18.18, 0.90, 0.70),
 (18.45, 18.20, 0.90, 0.70),
 (18.42, 18.22, 0.90, 0.70),
 (18.44, 18.24, 0.90, 0.70),
 (18.50, 18.26, 0.90, 0.70),
 (18.54, 18.28, 0.95, 0.75),
 (18.58, 18.30, 0.95, 0.75)]
 
 

	for n,l4 in enumerate(l4_9_1123):
		r=new_footprint(*l4)
		print(n,r)
	# fs=F.ls(U.pwd(),include='.kicad_mod')
	
	# for x,y in U.range2d(4,4):
		# x
gall=generate_all		