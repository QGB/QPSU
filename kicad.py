import pcbnew

def text(t="Hello",pcb=None):
	# pcb = pcbnew.BOARD()
	if not pcb:
		pcb = pcbnew.GetBoard()
	# txt = pcbnew.TEXTE_PCB(pcb) #AttributeError: module 'pcbnew' has no attribute 'TEXTE_PCB'
	txt = pcbnew.PCB_TEXT(pcb) # 6.0
	txt.SetText(t)
	txt.SetPosition(pcbnew.wxPoint(90000000, 90000000))
	txt.SetHorizJustify(pcbnew.GR_TEXT_HJUSTIFY_CENTER)
	txt.SetTextSize(pcbnew.wxSize(10000000, 10000000))
	# txt.SetThickness(1000000) #AttributeError: 'PCB_TEXT' object has no attribute 'SetThickness'
	txt.SetTextThickness(1000000) 
	pcb.Add(txt)

	pcb.Save('C:/Users/qgb/Documents/kicad-pdf/T/a.Save.kicad_pcb')
	
	return text
txt=text	

def pcb():
	return pcbnew.GetBoard()