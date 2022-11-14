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
def text(t="Hello",pcb=None):
	# pcb = pcbnew.BOARD()
	if not pcb:pcb = pcbnew.GetBoard()
	# txt = pcbnew.TEXTE_PCB(pcb) #AttributeError: module 'pcbnew' has no attribute 'TEXTE_PCB'
	txt = pcbnew.PCB_TEXT(pcb) # 6.0
	txt.SetText(t)
	txt.SetPosition(pcbnew.wxPoint(90000000,90000000))
	txt.SetHorizJustify(pcbnew.GR_TEXT_HJUSTIFY_CENTER)
	txt.SetTextSize(pcbnew.wxSize(10000000, 10000000))
	# txt.SetThickness(1000000) #AttributeError: 'PCB_TEXT' object has no attribute 'SetThickness'
	txt.SetTextThickness(1000000) 
	pcb.Add(txt)

	pcb.Save('C:/Users/qgb/Documents/kicad-pdf/T/a.Save.kicad_pcb')
	
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
	
def set_fp(f=r'C:\Program Files\KiCad\6.0\share\kicad\footprints\Package_BGA.pretty\Xilinx_FFG1761.kicad_mod',pcb=None):
	if not pcb:pcb = pcbnew.GetBoard()
	f=F.auto_path(f)
	name=T.sub_last(f,'/','.kicad_mod')
	m = pcbnew.FootprintLoad(f,name)
	
	return f,m
	pcb.Add(m)
	return m
	
from KicadModTree import *
def new_footprint ():

	footprint_name = "example_footprint"

	# init kicad footprint
	kicad_mod = Footprint(footprint_name)
	kicad_mod.setDescription("A example footprint")
	kicad_mod.setTags("example")

	# set general values
	kicad_mod.append(Text(type='reference', text='REF**', at=[0, -3], layer='F.SilkS'))
	kicad_mod.append(Text(type='value', text=footprint_name, at=[1.5, 3], layer='F.Fab'))

	# create silkscreen
	kicad_mod.append(RectLine(start=[-2, -2], end=[5, 2], layer='F.SilkS'))

	# create courtyard
	kicad_mod.append(RectLine(start=[-2.25, -2.25], end=[5.25, 2.25], layer='F.CrtYd'))

	# create pads
	kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
						 at=[0, 0], size=[2, 2], drill=1.2, layers=Pad.LAYERS_THT))
	kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
						 at=[3, 0], size=[2, 2], drill=1.2, layers=Pad.LAYERS_THT))

	# add model
	kicad_mod.append(Model(filename="example.3dshapes/example_footprint.wrl",
						   at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

	# output kicad model
	file_handler = KicadFileHandler(kicad_mod)
	file_handler.writeFile('example_footprint.kicad_mod')
	
	return kicad_mod
	
	