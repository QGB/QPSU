from skidl import Pin, Part, Alias, SchLib, SKIDL, TEMPLATE

SKIDL_lib_version = '0.0.1'

skidl_test_lib = SchLib(tool=SKIDL).add_parts(*[
        Part(**{ 'name':'GND', 'dest':TEMPLATE, 'tool':SKIDL, 'description':'Power symbol creates a global label with name "GND" , ground', 'tool_version':'kicad', 'datasheet':'', '_match_pin_regex':False, 'keywords':'power-flag', 'value_str':'GND', 'ref_prefix':'#PWR', 'num_units':1, 'fplist':[], 'do_erc':True, 'aliases':Alias(), 'pin':None, 'footprint':None, 'pins':[
            Pin(num='1',name='GND',func=Pin.types.PWRIN,do_erc=True)] }),
        Part(**{ 'name':'VCC', 'dest':TEMPLATE, 'tool':SKIDL, 'description':'Power symbol creates a global label with name "VCC"', 'tool_version':'kicad', 'datasheet':'', '_match_pin_regex':False, 'keywords':'power-flag', 'value_str':'VCC', 'ref_prefix':'#PWR', 'num_units':1, 'fplist':[], 'do_erc':True, 'aliases':Alias(), 'pin':None, 'footprint':None, 'pins':[
            Pin(num='1',name='VCC',func=Pin.types.PWRIN,do_erc=True)] }),
        Part(**{ 'name':'Q_PNP_CBE', 'dest':TEMPLATE, 'tool':SKIDL, 'description':'PNP transistor, collector/base/emitter', 'tool_version':'kicad', 'datasheet':'~', '_match_pin_regex':False, 'keywords':'transistor PNP', 'value_str':'Q_PNP_CBE', 'ref_prefix':'Q', 'num_units':1, 'fplist':[], 'do_erc':True, 'aliases':Alias(), 'pin':None, 'footprint':None, 'pins':[
            Pin(num='1',name='C',func=Pin.types.PASSIVE,do_erc=True),
            Pin(num='2',name='B',func=Pin.types.INPUT,do_erc=True),
            Pin(num='3',name='E',func=Pin.types.PASSIVE,do_erc=True)] }),
        Part(**{ 'name':'R', 'dest':TEMPLATE, 'tool':SKIDL, 'description':'Resistor', 'tool_version':'kicad', 'datasheet':'~', '_match_pin_regex':False, 'keywords':'R res resistor', 'value_str':'10K', 'ref_prefix':'R', 'num_units':1, 'fplist':['R_*'], 'do_erc':True, 'aliases':Alias(), 'pin':None, 'footprint':None, 'pins':[
            Pin(num='1',name='~',func=Pin.types.PASSIVE,do_erc=True),
            Pin(num='2',name='~',func=Pin.types.PASSIVE,do_erc=True)] })])