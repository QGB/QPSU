#coding=utf-8
import sys #endswith 是为了适配qgb处于另外一个包内的情况
if __name__.endswith('qgb.N.HTML'):from .. import py
else:
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
U,T,N,F=py.importUTNF()

def get_char_img_bytes(char, size=32, background='white', foreground='black', font_name="Arial"):
	from PIL import Image, ImageFont, ImageDraw, ImageColor
	import matplotlib.font_manager as fm
	if not py.istr(char): char = T.string(char)
	assert len(char) == 1

	font = ImageFont.truetype(fm.findfont(fm.FontProperties(family=font_name)), int(size * 0.8))
	img = Image.new('RGBA' if background == 'transparent' else 'RGB', (size, size), 
					(0, 0, 0, 0) if background == 'transparent' else ImageColor.getrgb(background))
	
	draw = ImageDraw.Draw(img)
	w, h = draw.textbbox((0, 0), char, font=font)[2:]
	draw.text(((size - w) // 2, (size - h) // 2 - size // 18), #  18 让上下居中
			  char, fill=ImageColor.getrgb(foreground), font=font)
	
	from qgb import pil;return pil.pil_image_to_bytes(img,'png') if background=='transparent' else pil.pil_image_to_bytes(img,'bmp')
	return [[0 if pixel else 1 for pixel in row] for row in img.getdata()]# 转换为点阵数据
bmp_char=get_bmp_char=get_char_img_bytes

def get_bmp_bytes(rgb=None,size=(16,16)):
	if not rgb:
		rgb = U.get_or_set('get_bmp.rgb', (255,0,0))
		size = U.get_or_set('get_bmp.size', 16)
	if py.isint(size):size=[size,size]
	width,height = size

	import struct
	r, g, b = (max(0, min(255, c)) for c in rgb)# 确保输入的RGB颜色值在0-255范围内
	bgr_color = bytes([b, g, r])# 将RGB转换为BGR字节顺序
	bytes_per_pixel = 3
	# 计算关键参数
	bytes_per_row = (width * bytes_per_pixel + 3) // 4 * 4  # 每行字节数（含填充）
	pixel_data_size = bytes_per_row * height                 # 像素数据总大小
	file_size = 14 + 40 + pixel_data_size                    # 文件总大小

	bmp_header = struct.pack(# BMP文件头（14字节）
		'<2sIII',
		b'BM',               # 文件标识
		file_size,           # 文件总大小（小端序）
		0,                   # 保留字段
		54                   # 像素数据偏移（14+40）
	)

	bmp_info = struct.pack(# BMP信息头（40字节）
		'<IIIHHIIIIII',
		40,                  # 信息头大小
		width,               # 图片宽度（小端序）
		height,              # 图片高度（正数表示倒序存储）
		1,                   # 颜色平面数（固定为1）
		24,                  # 每像素位数（24位BGR）
		0,                   # 压缩方式（BI_RGB）
		pixel_data_size,     # 像素数据大小（包含填充）
		3780,                # 水平分辨率（像素/米）
		3780,                # 垂直分辨率
		0,                   # 调色板颜色数（无调色板）
		0                    # 重要颜色数（全重要）
	)
	pixels = b''
	for _ in range(height):# 生成像素数据（含行填充）
		row = bgr_color * width                # 单行像素数据
		padding = b'\x00' * (bytes_per_row - len(row))  # 填充字节
		pixels += row + padding
	return bmp_header + bmp_info + pixels
generate_solid_ico=get_ico=get_bmp=get_bmp_bytes

def format(s,**ka):
	ka={'{%s}'%k:v for k,v in ka.items()}
	return T.replacey(s,ka)

def dict_list_number_edit(response,adict,get=False,set=None):
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
	response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
	# response.headers['Access-Control-Max-Age'] = '3600'
	if get:
		# response.headers['Content-Type']='text/html;charset=utf-8'	
		return T.json_dumps(adict)

	from flask import request
	if set:
		d=request.get_json()
		adict.update(d)
		return T.json_dumps({'time':U.stime()})
		return U.stime(),d,adict
	dict_name='okx_private.gdsr4'
	u=request.url
	s1=T.sub_last(u,'%2C','%2C')
	s2=T.sub_last(u,'%2C','%29')
	if s1:dict_name=s1
	elif s2:dict_name=s2
	
	# return u,s1,s2
	html=F.read_qpsu_file('dict_list_number_edit.html')
	html=N.HTML.format(html,dict_name=dict_name,func_name='N.HTML.dict_list_number_edit')
	response.headers['Content-Type']='text/html;charset=utf-8'
	response.set_data(html)


AC_DEFAULT=py.No('auto use last,not change')	
# AC_DEFAULT=U.get_or_set('N.HTML.AC_DEFAULT',lazy_default=lambda:py.No('auto use last,not change')	)
# print(repr(AC_DEFAULT))
def hualin(t=30,fan_speed=100,mode='cool',toggle_display=True,power=AC_DEFAULT,fan_only=False,**ka):
	''' 
[<fan_speed_enum.Auto: 102>,
 <fan_speed_enum.Full: 100>,
 <fan_speed_enum.High: 80>,
 <fan_speed_enum.Medium: 60>,
 <fan_speed_enum.Low: 40>,
 <fan_speed_enum.Silent: 20>]
''' 
	try:
		from msmart.device import air_conditioning
		import msmart.device.AC.appliance
		operational_mode_enum=msmart.device.AC.appliance.air_conditioning.operational_mode_enum
		dio={1: operational_mode_enum.auto,
	2: operational_mode_enum.cool,
	3: operational_mode_enum.dry,
	4: operational_mode_enum.heat,
	5: operational_mode_enum.fan_only}
		dso={'auto': operational_mode_enum.auto,
	'cool': operational_mode_enum.cool,
	'dry': operational_mode_enum.dry,
	'heat': operational_mode_enum.heat,
	'fan_only': operational_mode_enum.fan_only}
		dfka=U.get_or_dill_load('hualin-2')
	except:
		import msmart.device
		air_conditioning=msmart.device.AirConditioner
		operational_mode_enum=msmart.device.AirConditioner.OperationalMode
		dio = {
			1: operational_mode_enum.AUTO,
			2: operational_mode_enum.COOL,
			3: operational_mode_enum.DRY,
			4: operational_mode_enum.HEAT,
			5: operational_mode_enum.FAN_ONLY,
			# 6: operational_mode_enum.SMART_DRY  # 根据需求添加
		}
		dso = {
			'auto': operational_mode_enum.AUTO,
			'cool': operational_mode_enum.COOL,
			'dry': operational_mode_enum.DRY,
			'heat': operational_mode_enum.HEAT,
			'fan_only': operational_mode_enum.FAN_ONLY,
			# 'smart_dry': operational_mode_enum.SMART_DRY
		}
		dfka=U.get_or_dill_load('hualin-2')
		dfka={'air_conditioning':{'ip': '192.168.1.176', 'port': 6444, 'device_id': 208907213152422},
		'authenticate':dfka['authenticate']
		}
	
	mode=U.get_duplicated_kargs(ka,'mode','mod','m','moshi','mo',default=mode)
	fan_only=U.get_duplicated_kargs(ka,'fan_only','fan','wind','only_wind','sf',default=fan_only)
	def get_mode():
		nonlocal mode
		if py.isint(mode):return dio[mode]
		if py.istr(mode):
			mode=mode.lower()
			if mode in dso:return dso[mode]
			elif mode.startswith('c'):return dso['cool']
			elif mode.startswith('warm'):return dso['heat']
			elif mode.startswith('wind'):return dso['fan_only']
		raise py.NotImplementedError(mode)
	
	power=U.get_duplicated_kargs(ka,'power','on','open','p','po',default=power)
	
	
	a=U.get_or_set('msmart.device.air_conditioning:hualin',
		lazy_default=lambda:air_conditioning(**dfka['air_conditioning']),
		)
	
	if not power is AC_DEFAULT:		
		if power:
			a.power_state=True
		else:
			a.power_state=False
			a.apply()
			return a
	
	
	fan_speed=U.get_duplicated_kargs(ka,'wind_speed','fan_speed','speed','fs','S',default=fan_speed)# 100 max , 102 auto
	if py.isint(fan_speed):
		if fan_speed==5 or 80<fan_speed    :fan_speed=100
		if fan_speed==4 or 60<fan_speed<=80:fan_speed=80
		if fan_speed==3 or 40<fan_speed<=60:fan_speed=60
		if fan_speed==2 or 20<fan_speed<=40:fan_speed=40
		if fan_speed==2 or 9 <fan_speed<=20:fan_speed=20
			
	
	
	a.authenticate(**dfka['authenticate'])
	if power is AC_DEFAULT:a.power_state=True
	a.eco_mode=False
	a.operational_mode=get_mode() #a.operational_mode_enum.cool
	a.fan_speed=fan_speed
	a.target_temperature=t
	a.apply()
	if toggle_display and not a.display_on:a.toggle_display()
	return a,t,fan_speed,toggle_display,a.operational_mode
ac2=hualin


def oshwhub_tb():
	code=r"""
ps=await tb.get_or_new_page('https://oshwhub.com/sign_in',select_tab=0)	
"""
	# is_req=N.is_flask_request()
	# code=code.replace('is_req',py.repr(is_req))
	import asyncio
	asyncio.set_event_loop(U.get('asyncio.get_event_loop()')) 
	r= U.get_ipython(raise_exception=1).run_cell(code,store_history=True)
	if r.result:
		return r.result
	# and py.islist(r.result):
		# return ','.join(r.result)
	return r

def vivo(a=2):
	code=rf"""
from qgb.tests import vivo
U.r(vivo)
ck=await vivo.get_cookies()
if not vivo.send(ck,{a}):
	await vivo.login()
	ck=await vivo.get_cookies()
	vivo.send(ck,{a})
"""
	import asyncio
	asyncio.set_event_loop(U.get('asyncio.get_event_loop()')) 
	r= U.get_ipython(raise_exception=1).run_cell(code,store_history=True)
	if r.result:
		return r.result
	return r

def oshwhub():
	code=r"""
gods=U.get('oshwhub'+U.stime()[:10],[])
if gods and U.get_current_datetime().day==int(gods[-1]):
	1/0
from qgb.tests import taobao_trade as tb
is_600=U.get_current_day_passed_seconds()<600
try:
	ps=await tb.get_or_new_page('https://oshwhub.com/sign_in',select_tab=is_600)
except Exception as e:
	U.print_traceback_in_except(e)
	U.kill('chrome.exe',ask=0)
	U.sleep(1)
	!start "" C:\Users\qgb\AppData\Local\CentBrowser\Application\chrome.exe --remote-debugging-port=9222
	1/0
	
if is_600:await ps.reload()
sd=str(U.get_current_datetime().day)

ods=await ps.evaluate('''
y=document.querySelectorAll('div[class*=calendar_signIn-mark] > span[class*=calendar_day]')
ds=[]
for(e of y){
	ds.push(e.textContent)
}
ds
''')

async def oshwhub_qd(recursive=True):	
	Win.foreground('嘉立创EDA开源硬件平台')
	es=await ps.xpath( '//span[contains(text(), "立即签到")]')
	if es:
		await es[0].click()
		print(U.stime(),'oshwhub sucess click:',es)
	else:
		print(U.stime(),'oshwhub not found',es)
		await ps.reload()
		if recursive:
			await tb.A.sleep(3)
			await oshwhub_qd(recursive=False)
	return es		
if len(ods)>int(sd): #每月一号
	await ps.reload()
	print(U.stime(),'incorrect ods=',ods,'force_reload')
	ods=[]	
if (sd not in ods) or (U.stime()[8:10] not in ods):
	# print(U.stime(),'oshwhub_qd',sd,ods)
	await oshwhub_qd()
if U.get_current_datetime().weekday()==6:# 0-6	
	es=await ps.xpath( '//span[contains(text(), "7天好礼")]')           
	if es:await es[0].click()
if (U.get_current_datetime()+U.time_delta(days=1)).day==1:#月度最后一天	
	es=await ps.xpath( '//span[contains(text(), "月度好礼")]')           
	if es:await es[0].click()	
U.set('oshwhub'+U.stime()[:10],ods)	
','.join(ods)
"""
	# is_req=N.is_flask_request()
	# code=code.replace('is_req',py.repr(is_req))
	import asyncio
	asyncio.set_event_loop(U.get('asyncio.get_event_loop()')) 
	r= U.get_ipython(raise_exception=1).run_cell(code,store_history=True)
	if r.result:
		return r.result
	# and py.islist(r.result):
		# return ','.join(r.result)
	return r

def iptv(v=512):
	import asyncio
	asyncio.set_event_loop(U.get('asyncio.get_event_loop()')) 
	return U.get_ipython(raise_exception=1).run_cell(f'''
from qgb.tests import GS3105	
ps=await GS3105.plogin()
await GS3105.setv(ps,{v})	
''')	

JS_async_post='''
async function post(url,data){
	if(typeof a!='string')data=JSON.stringify(data)

	return new Promise(function (resolve, reject) {
		var xhr = new XMLHttpRequest();
		xhr.open('post', url, true);
		xhr.onload = function () {
			resolve(xhr.response);
		};
		xhr.send(data)
	});
}
'''

def sendkey_list(response):
	ki=U.get_or_dill_load_and_set('ki')
	
	la=[]
	for k,i in ki:
		la.append(f'<a href="#{i}" n={i} > {i} {k} </a>')
	sla='<br>'.join(la)
	
	html='''
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">

%(sla)s

<script>
%(JS_async_post)s



for(e of document.querySelectorAll("a")){

	e.onclick=async (event)=>{
		et=event.target
		await post(
"http://192.168.1.12:8888/cmd/sendkey?KeyCode="+et.getAttribute('n')
		)
		
	};

}

		

function a_onclick(event){
	e=event.target
	

	
}
 
</script>
	
'''%py.locals()
	
	response.headers['Content-Type']='text/html;charset=utf-8'
	response.set_data(html)
k8888=sendkey_list
	
def get_or_input_html(response,*name):
	# v= U.get(name[0],)
	v=U.get_or_set_sys_level(name[0])
	# if not v:
		# raise v
	# print(v)	
	return v	
	
def xiaomi_air_conditioner_control(response=None,token=py.No('auto get'),t=0,angle=None,sleep=AC_DEFAULT,swing=False,lcd=None,volume=AC_DEFAULT,mode=AC_DEFAULT,wind_speed=AC_DEFAULT,before=None,after=None,power=AC_DEFAULT,ip=AC_DEFAULT,**ka):
	''' 风扇水平 0 时，环境感知温度会立马降低 
	
'''	
	# U.r(py,U,T,N,F,N.HTTP,N.HTML) # 用了会造成 global AC_DEFAULT 与 default arg 中 默认参数 不一致
	angle=U.get_duplicated_kargs(ka,'angle','angel','jd','ang','a','j',default=angle)
	power=U.get_duplicated_kargs(ka,'power','on','open','p','po',default=power)
	sleep=U.get_duplicated_kargs(ka,'sleep','set_silent','silent','s',default=sleep)
	volume=U.get_duplicated_kargs(ka,'volume','voice','sound','sy','v',default=volume)
	mode=U.get_duplicated_kargs(ka,'mode','cooling','c','cool','m',default=mode)
	wind_speed=U.get_duplicated_kargs(ka,'wind_speed','fan_speed','speed','fs','S',default=wind_speed)# 4 max , 5 auto
	swing=U.get_duplicated_kargs(ka,'swing','bd','bf','w',default=swing)# 
	
	if not token:token=get_or_input_html(response,'miio.token')
	if not token:return token
	
	import miio
	
	if not ip:
		ip=U.get_or_dill_load_or_dill_dump_and_set('miio.ip','192.168.1.88')
	else:	
		ip=N.auto_ip(ip)
		U.set_and_dill_dump('miio.ip',ip)
	
	if py.getattr(miio,'Device',0):
		d=U.get_or_set(ip+':'+token,
				lazy_default=lambda:miio.Device(ip=ip,token=token),
			)	
	else:
		d=U.get_or_set(ip+':'+token,
				lazy_default=lambda:miio.device.Device(ip=ip,token=token),
			)	
	
		
		
	if not volume is AC_DEFAULT:	
		if volume:
			d.send('set_volume_sw',['on'])
		else:
			d.send('set_volume_sw',['off'])
	
	if py.callable(before):
		before(d)
		
	if not power is AC_DEFAULT:		
		if power:
			d.send('set_power',['on'])
		else:
			d.send('set_power',['off'])
			U.set('miio.ip',ip)
			return d
		# if not power:
	ip=U.set('miio.ip',ip)
	
	# if t==88:
		# d.send('set_power',['off'])
		# return
		
	if not sleep is AC_DEFAULT:
		if sleep:
			ia=0
			ib=0# ia.ib（wind模式时间，先废弃）
			if py.isstr(sleep):
				assert py.len(sleep)%4==0
				ia=py.int(sleep)
			if py.isint(sleep):
				if sleep>999:
					ia=sleep
					ib=100
				elif sleep>60:
					d.send("set_silent", ['on']) #sleep
					d.send("set_idle_timer", [sleep])
				
			if py.isfloat(sleep) :#and sleep>60:
				ia,ib=U.tuple_operator(py.str(sleep).split('.'),py.int)
				
			if ia:
				if power is AC_DEFAULT:d.send('set_power',['on'])
				if not mode:
					m=U.time().month
					if m<4 or m>10:
						d.send("set_mode", ['heat'])
					if 5<m<11 or (m==5 and U.time().day>20):
						d.send("set_mode", ['cooling'])
				
				
				if ia>99999:  #9999秒 一个多小时，少了
					sa=py.str(ia)
					assert py.len(sa)%4==0
					ia=0
					spower=''
					swind=''
					for ina in py.range(py.len(sa)//4):
						isa=sa[4*ina:4*ina+4]
						ta=py.int(isa[:2]) # Temperature
						
						if ta==88:spower=',power=0'
						if ta==77:swind=",mode='wind'"
						
						
						ia=ia+py.int(isa[2:])*60 # ta 经历 ia 秒
						
						if ina==0:
							if ta==77:
								N.HTML.ac(mode='wind')
							elif ta==88:
								N.HTML.ac(power=False)
							else:	
								N.HTML.ac(t=ta)
							continue
						
						
						se=f'lambda:print({ina},{ta},N.HTML.ac(t={ta}{spower}{swind}),U.stime())'
						ft=eval(se)
						print(ina,ta,ia,U.Timer(ft,ia,name=f'Timer.ac.{ina}'),se)
						
						if ta==88:spower=',power=1'# 为循环的其他温度开机 
						if ta==77:swind=",mode='cooling'"
				else:
					for ina in range(9):
						ina=U.get(f'Timer.ac.{ina}')
						if ina:ina.cancel()
							
				d.send("set_silent", ['off'])
				
				# t2=U.Timer(lambda:N.HTML.ac(mode='wind',power=AC_DEFAULT),ia,name='Timer.ac.wind')
				# print(t2)
				# ishutdown=ia+ib
				# print('ac.sleep ',ia,'wind',ib,'shutdown:',ia+ib,'#',U.time()+U.time_delta(seconds=ia+ib))
				
				d.send("set_idle_timer", [ia+ib])
				
				

		else:
			d.send("set_silent", ['off'])
		
	if not t:
		t=N.geta()
		t=U.float(t)
	if t:
		if t<16:t=16
		if 32<t<160:t=32
		if t<=32:t=t*10
			
		if t<160:t=160
		if t>320:t=320
		
		d.send("set_temperature", [t] )	
	
	def set_angle():
		d.send("set_vertical", ['off'])#swing on/off
		d.send("set_ver_pos", [70])
		U.sleep(21)
		d.send("set_ver_pos", [0])
		U.sleep(21)
		d.send("set_ver_pos", [angle])
	
	if swing:
		d.send("set_vertical", ['on'])#swing on/off
	
	if py.isint(lcd):
		d.send('set_lcd',[lcd])
		
	if py.isint(angle):
		d.send('set_ver_range',[0,70])
		t=U.thread(target=set_angle)
		U.set(angle,t)
		t.start()
		# if angle<35
		
	if mode:
		if py.istr(mode):
			m=mode[0].lower()
			if m=='w':
				d.send("set_mode", ['wind'])
			elif m=='c':
				d.send("set_mode", ['cooling'])
			elif m=='h':
				d.send("set_mode", ['heat'])
			else:
				raise py.ArgumentError(mode)
		else:
			d.send("set_mode", ['cooling'])
		
	if wind_speed:
		if py.isint(wind_speed):
			wind_speed=py.min(wind_speed,5)
			d.send("set_spd_level",[wind_speed])
		else:	
			d.send("set_spd_level",[4])
		
	if py.callable(after):
		after(d)
		
	# return d,py.id(d)
	
	return d
ac=xiaomi_air_conditioner_control	

# print(repr(AC_DEFAULT))

# def list_2d_txt_href(response,a,file_column=None,**ka):
def google_search_result_zhihu(response,word='',hs='',proxy='127.0.0.1:21080',u_size=36+4,force_reload=False,timeout=99*1000,**ka):
	if not word:
		if response:
			word=N.geta()
		else:
			word=U.cbg(edit_prompt='keyword:')
			
	url=('https://www.google.com/search?q=site:zhihu.com+'
		+T.url_encode(word)	)
	if force_reload:
		print('force_reload',py.len(U.del_set(url)))
		
	if not hs and not U.get(url):	
		U.set('gzurl',url)	
		print(U.stime(),'set gzurl')
		import asyncio
		asyncio.set_event_loop(U.get('asyncio.get_event_loop()')) 
#如果不【set_event_loop】  RuntimeError: There is no current event loop in thread 'Thread-26685'. 
#如果此时 MainThread 想要运行 await ，RuntimeError: This event loop is already running，必须要等其他线程运行完成		
		rx=U.get_ipython(raise_exception=1).run_cell(f'''
	from qgb.tests import taobao_trade;
	print(U.stime(),'start google_zhihu, getting page...')
	pa_google_zhihu=await taobao_trade.new_page(U.get('gzurl'),timeout={timeout});#fix错误结果，再说没必要两次缓存
	print(U.stime(),pa_google_zhihu)
	h_google_zhihu=await pa_google_zhihu.evaluate("document.documentElement.outerHTML");
	print(U.stime(),'get html',py.len(h_google_zhihu))
	U.set_no_return(U.get('gzurl'),h_google_zhihu)

	''')
	if not hs:hs=U.get(url)
		
	# hs=N.HTTP.get(u,proxy=proxy,print_req=1)
	# l2=[[T.sub(a,'href="','"'),T.html2txt(a)] for a in hs]     
	bs=T.BeautifulSoup(hs)
	es=bs.select('a')
	l2=[]
	for e in es:
		u=e.get('href')
		if not u:continue
		u=u.replace('site:zhihu.com',' site_zhihu_com ')
		if 'zhihu.com' not in u[:33]:continue
	#    if not u.startswith('http'):continue
		iz=u.index
		l2.append([u,e.text])
		
	# return U.StrRepr(hs,repr=f'{py.len(hs)} {hs[:44]}'),l2
	
	zhihu_mark='.zhihu.com/'
	dr={}
	lr=[]
	for n,(u,t) in py.enumerate(l2):
		if zhihu_mark not in u:continue
		u=T.sub(u,zhihu_mark)
		
		t=T.replacey(t,['https://www.zhihu.com ›','https://www2.zhihu.com ›','http://www.zhihu.com ›','http://www2.zhihu.com ›','http://www-quic.zhihu.com ›','https://zhuanlan.zhihu.com › ...','...  更多','question','answer'
			],'').strip()
		
		iq=u.find('?')
		if iq!=-1:
			if not U.one_in(['?page='],u):
				u=u[:iq]
		t=T.replace_all_spaces(t,' ')
		
		if u in dr:
			if '查看所有帖子'==t:continue
			
		U.set_dict_value_list(dr,u,t)
		
		
		lr.append([U.IntRepr(n,size=4),U.StrRepr(u,size=u_size),t])
		
	# lr=U.sort(lr,c=1)	
	lr.sort(key=lambda x:x[1])
	U.set('dr',dr)
	if not response:
		return lr
	
	def html_callback(html,*a,**ka):
		bs=T.BeautifulSoup(html)
		es=bs.select(f'body > table > tbody > tr > td:nth-of-type({1+1})')
		
		t=''
		for ne,e in py.enumerate(es):
			u=e.text
			ea=bs.new_tag('a')
			ea.attrs["target"]='_blank'
			t=T.eol.join(dr[u])
			ea.append(t)
			if '/answer/' in u:
				u='answer/'+T.sub(u,'/answer/')
			u=u.replace('column/p/','articles/')	
			u=u.replace('p/','articles/')	
				
			ea.attrs['href'  ]=f"zhihu://{u}"
			e.clear()
			e.append(ea)		
			# py.list(e.parent.children)[2]=u
			
		html=py.str(bs)
		return html
		
		
	return list_2d(response,U.col(lr,0,1,1),html_callback=html_callback,**ka)
	
	# return lr	
zhihu=google_zhihu=google_search_result_zhihu		

def fullscreen_img(response,img):
	if py.istr(img) and '://' in img:
		u=img
	else:
		k='img-%s'%py.id(img)
		U.set(k,img)
		u=U.get('rpc.server.base')+f"N.img(p,U.get({repr(k)}))"

	html='''
<!doctype html>
<html lang="en"><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>HTML5 Fullscreen API
</title>

<style type="text/css">
body {
	background-color: #f3f3f3;
	margin: 0; /* 修复 左上 白边  【user agent stylesheet 8px】无效 */
}

.html5-fullscreen-api {
	position: relative;
}
.html5-fullscreen-api img {
	max-width: 100%;
	border: 0px solid #fff;
	box-shadow: 0px 0px 50px #ccc;
}
.html5-fullscreen-api .fs-button {
	z-index: 100;
	display: inline-block;
	position: absolute;
	top: 0px;
	right: 0px;
	cursor: pointer;
}
.html5-fullscreen-api .fs-button:after {
	display: inline-block;
	width: 100%;
	height: 100%;
	font-size: 32px;
	font-family: 'ModernPictogramsNormal';
	color: rgba(255,255,255,.5);
	cursor: pointer;
	content: "v";
}
.html5-fullscreen-api .fs-button:hover:after {
	color: rgb(255,255,255);
}
#fullscreen:-webkit-full-screen .fs-button:after {
	content: "X";
}
#fullscreen:-webkit-full-screen {
	width: 100%;
}
#fullscreen:-webkit-full-screen img {
	display: block;
	height: 100%;
	margin-left: auto;
	margin-right: auto
}

#fullscreen:-moz-full-screen .fs-button:after {
	content: "X";
}
#fullscreen:-moz-full-screen {
	width: 100%;
}
#fullscreen:-moz-full-screen img {
	display: block;
	height: 100%;
	margin-left: auto;
	margin-right: auto;
}

img{
		width:100%;
		padding: 0 0 0 0;		
		margin: 0 0 0 0;
		
}

</style> 

<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

<script>
$(document).ready(function(){
	$('.fs-button').on('click', function(){
		var elem = document.getElementById('fullscreen');

		if (
			document.fullscreenEnabled ||
			document.webkitFullscreenEnabled ||
			document.mozFullScreenEnabled ||
			document.msFullscreenEnabled
		) {
			if (
				document.fullscreenElement ||
				document.webkitFullscreenElement ||
				document.mozFullScreenElement ||
				document.msFullscreenElement
			) {
				if (document.exitFullscreen) {
					document.exitFullscreen();
				} else if (document.webkitExitFullscreen) {
					document.webkitExitFullscreen();
				} else if (document.mozCancelFullScreen) {
					document.mozCancelFullScreen();
				} else if (document.msExitFullscreen) {
					document.msExitFullscreen();
				}
			} else {
				if (elem.requestFullscreen) {
					elem.requestFullscreen();
				} else if (elem.webkitRequestFullscreen) {
					elem.webkitRequestFullscreen();
				} else if (elem.mozRequestFullScreen) {
					elem.mozRequestFullScreen();
				} else if (elem.msRequestFullscreen) {
					elem.msRequestFullscreen();
				}
			}
		} else {
			alert('Fullscreen is not supported on your browser.');
		}
	});
});

setTimeout(function(){
	// $('.fs-button').click()
},666)
</script>
</head>

<body>

<div id="fullscreen" class="html5-fullscreen-api">
	<img src="img_url">
	<span class="fs-button"></span>
</div>


</body>
</html>

'''.replace('img_url',u) # %py.locals()
	response.headers['Content-Type']='text/html;charset=utf-8';
	response.set_data(html)
	return 	html
fsimg=imgfs=fullscreen_img

def a_href(response,u=''):
	if not u:
		u=U.cbg()
	u=N.auto_url(u)
	html='<br>'*5+f"""
<a href="{u}">{u}</a>	
	"""
	response.headers['Content-Type']='text/html;charset=utf-8';
	response.set_data(html)
	return  u
HREF=URL=href=a_href	

def list_github_search(response,a,txt_column=-1,**ka):
	if txt_column<0:
		txt_column=py.len(a[0])+txt_column
	
	def github_txt_column_callback(html,head):
		bs=T.BeautifulSoup(html)
		style=bs.find('head').find('style')
		# py.pdb()()
		style.string=style.text.replace(list_2d_CSS_MARK,'''

/* Html { */
	/* font-size: 2vh; */
/* } 	 

body > table > tbody > tr > 
textarea{
	white-space: pre;
	overflow-wrap: normal;
	
}


	// display: inline-block;
	// transform: rotateY(180deg);
		

	,table 
	
*/
#box{
	/* display: flex; */
	flex-wrap: wrap;	
	flex-direction: column;
	width:90vh;
}


td:nth-of-type(5){
	text-align: right;
}


td:nth-of-type(5) > textarea{
	width:90vh;
	/* text-align: right; */
	 /* display: flex; */
	 /* color: blue; */
}

td:nth-of-type(6){
	color: red;
}

td:nth-of-type(7) > textarea{
	width:110vh;
	/* height:5em; */
	/* min-width:70vw; */
	/* font-size:1.1vw; 
	overflow-x: scroll;
	
	*/
}

.wrapper {
  /* background: #EFEFEF; */
  box-shadow: 1px 1px 10px #999;
  margin: 0;
  text-align: right;
  position: relative;

  width: 110vh;
  padding-top: 5px;
}
.scrolls {
  overflow-x: hidden;
  overflow-y: scroll;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  white-space: nowrap
  text-align: left;
}
		
.scrolls>p {		
	color:gray;
}
''')	
		dclu=U.get('dclu',{})
		es=bs.select(f'body > table > tbody > tr > td:nth-of-type({1+txt_column-2})')
		for ne,e in py.enumerate(es):
			s=a[ne][txt_column]
			lu=dclu.get(s,None)
			if lu:
				# m=U.max_len(lu)+18
				# lu=[T.justfy('https://github.com'+i,method=T.wc_rjust,size=m) for i in lu]
				# ea=bs.new_tag('textarea')
				# ea.attrs['rows']=f"""{s.count(T.eol)-1};"""
				# ea.attrs['readonly'] = 'readonly'
				# ea.attrs['wrap'] = 'off'
				# ea.append(T.eol.join(lu))
				
				sn='#L'+T.regex_match_one(s,r'\d+')
				slu=T.eol.join(f'<a target="_blank" href="https://github.com{i}{sn}">{i[1:]}</a>' for i in lu)
#				ea=T.bs_tag(f'''
#<div id="box" style="height:{s.count(T.eol)*2.36+4}vh;">
#{slu}
#
#</div>''')
				ea=T.bs_tag(f'''
<div class="wrapper" >
  <div class="scrolls" style="height:{s.count(T.eol)*1.9}vh;">
  {slu}
  </div>
</div> 
  
  ''')
				
				
				e.clear()
				e.append(ea)
			
		es=bs.select(f'body > table > tbody > tr > td:nth-of-type({1+txt_column})')
		for ne,e in py.enumerate(es):
			ea=bs.new_tag('textarea')
			s=a[ne][txt_column].strip()
			ea.attrs['rows']=f"""{s.count(T.eol)+1};"""
			#ea.attrs['style']=f"""height:{s.count(T.eol)*2.36+4}vh;"""
			#ea.attrs['style']=f"""height:{s.count(T.eol)*1.1+2.4}em;"""
			ea.attrs['readonly'] = 'readonly'
			ea.append(s)
			e.clear()
			e.append(ea)
		return	py.str(bs)+'''
<script>
// r=[]
for(e of document.querySelectorAll("td:nth-of-type(5) > textarea")){
	//console.log(e)
	// e.scrollLeft=e.scrollWidth
	e.scrollLeft=e.scrollWidth*1.03-575
	// 少 1 都有个别没有到位 
	
	// r.push([e.scrollLeft,e.scrollWidth])
}



</script>
'''		
	return list_2d(response,a,html_callback=github_txt_column_callback,**ka)	
gs=github_search=list_github_search


def list_2d_txt_href(response,a,url_index_dict=None,txt_column=None,attrs_cols=137,index=False,**ka):
	''' url_index_dict [1,2] : 1.href == 2(url)
url_index_dict == int 默认 url最后一列 url_index_dict={index:-1}	
	
url尽量放在列表靠后的列，简化影响	

TODO:  list pop multiple indexes  您需要以相反的顺序删除它们，以免丢弃后续索引。
'''
	url_index_dict=U.get_duplicated_kargs(ka,'url_index_dict','u','uc','ui','url','u_col','ucol','ucolumn',default=url_index_dict)
	txt_column=U.get_duplicated_kargs(ka,'txt_column','txt','t','text','txt_col','t_col','tcol','tcolumn',default=txt_column)
	if not py.isdict(url_index_dict):
		if py.isint(url_index_dict):
			url_index_dict={url_index_dict:-1}
		elif not url_index_dict:
			url_index_dict={}
		else:
			url_index_dict={url_index_dict[0]:url_index_dict[1]}
	a=[py.list(row).copy() for row in a]
	diu={}
	for ia,iu in url_index_dict.items():
		diu[iu]=[row.pop(iu) for row in a]
		
	def href_column_callback(html,head):
		nonlocal a,url_index_dict,txt_column

		bs=T.BeautifulSoup(html)
		for ia,iu in url_index_dict.items():
			es=bs.select(f'body > table > tbody > tr > td:nth-of-type({1+ia})')
			for ne,e in py.enumerate(es):
				f=a[ne][ia]
				ea=bs.new_tag('a')
				ea.attrs['href'  ]=diu[iu][ne]
				ea.attrs["target"]='_blank'
				ea.append(f)
				e.clear()
				e.append(ea)
		
		if txt_column:
			es=bs.select(f'body > table > tbody > tr > td:nth-of-type({1+txt_column})')
			# print(es,txt_column)
			for ne,e in py.enumerate(es):
				ea=bs.new_tag('textarea')
				# print(ne,a[ne])
				s=a[ne][txt_column]
				if not s:continue
				s=s.strip()
				ea.attrs['rows']=f"""{s.count(T.eol)+1};"""
				ea.attrs['cols']=f"""{attrs_cols}"""
				ea.attrs['readonly'] = 'readonly'
				ea.append(s)
				e.clear()
				e.append(ea)
				
		return py.str(bs)		
	return list_2d(response,a,html_callback=href_column_callback,index=index,**ka)
list_txt=list_2d_txt=listu=list_url=list_2d_url=list_2d_href=list_2d_txt_href	

def list_2d_href_file_column(response,a,file_column=None,**ka):
	file_column=U.get_duplicated_kargs(ka,'file_column','cf','fc','f_col','fcol','fcolumn',default=file_column)
	def file_column_callback(html,head):
		nonlocal file_column,a
		if not py.isint(file_column):return html
		
		if file_column <0:file_column=py.len(a[0])+file_column
		from bs4 import BeautifulSoup
		
		from flask import request
		rpc_base=request.url_root[:-1]+U.get_or_set('rpc.server.base','/')
		url_read='a=N.geta();r=F.read(a)%23-'
		url_read='a=N.geta();N.flask_text_response(p,F.read(a))%23-'#fix 有些txt文件会变下载框
		# url_read='a=N.geta();N.html(p,F.read(a))%23-'
		
		bs=T.BeautifulSoup(html)
		# if debug:
			# U.set('html',html)
			# U.set('bs',bs)
		es=bs.select(f'body > table > tbody > tr > td:nth-of-type({1+file_column})')
		for ne,e in py.enumerate(es):
			f=a[ne][file_column]
			# if e.text!=f:
				# print('#error a[',ne,file_column,'!= e.text')
				# continue
				
			# e.string.replace_with(f'<a href="http://{request.remote_addr}/{f}">{f}</a>' )	
			# U.get_or_set('es.list',[]).append(e)
			# ea=BeautifulSoup(f'<a href=>{f}</a>'			
			ea=bs.new_tag('a')
			# ea.attrs['href']=f"http://{request.remote_addr}/{f}"
			# ea.attrs['href'  ]=f"{rpc_base+url_read}{f}"
			ea.attrs['href'  ]=f"{U.get_or_set('rpc.server.base','/')}{url_read}{f}"
			ea.attrs["target"]='_blank'
			ea.append(f)
			
			e.clear()
			e.append(ea)		
			
			
		html=py.str(bs)
		return html
	
		# def file_column_callback():pass
	return list_2d(response,a,html_callback=file_column_callback,**ka)
		

list_2d_CSS_MARK='/*css*/'
def list_2d(response,a,html_callback=None,index=True,sort_kw=U.SORT_KW_SKIP,column_type_dict=None,sort_ka=py.dict(ascending=True,),bottom_head=False,debug=False,to_html_ka=None,exclude_cols=None,order_cols=None,js='<script> </script>',millisecond_type_col=None,timezone='UTC',**ka):
	''' ,sort_ka=py.dict(ascending=False) #倒序 从大到小
	'''
	index=U.get_duplicated_kargs(ka,'index','n','enu','add_index','enumerate',default=index)
	sort_kw=U.get_duplicated_kargs(ka,'skw','sort','s',default=sort_kw)
	column_type_dict    =U.get_duplicated_kargs(ka,'column_type_dict','type','t',default=column_type_dict if column_type_dict else {},)
	millisecond_type_col=U.get_duplicated_kargs(ka,'millisecond_type_col','ms','millisecond','milliseconds',default=millisecond_type_col)
	if not column_type_dict and millisecond_type_col!=None:  # column_type_dict==None 不行
		if ',' in millisecond_type_col:
			column_type_dict={}
			for cname in millisecond_type_col.split(','):
				column_type_dict[cname]='ms'
		else:		
			column_type_dict={millisecond_type_col:'ms'}
	
	sort_ka=U.get_duplicated_kargs(ka,'ska','sort_ka','sa',default=sort_ka)
	bottom_head=U.get_duplicated_kargs(ka,'bottom_head','title_bottom','bottom','bhead','tb','bh','hb',default=bottom_head)
	exclude_cols=U.get_duplicated_kargs(ka,'exclude_cols','exclude','exclude_col','del_cols','del_col',default=exclude_cols)
	order_cols=U.get_duplicated_kargs(ka,'order_cols','order','order_col','cols_order','column_order','keys','ks','title',default=order_cols)
	js=U.get_duplicated_kargs(ka,'js','javascript','code','script','jscode',default=js)
	if js and '</' not in js:js=f'<script>{js}</script>'
	if not py.isdict(sort_ka):
		if sort_ka:
			sort_ka=py.dict(ascending=True,)
		else:
			sort_ka=py.dict(ascending=False,)
	# if py.isint(sort_kw): # U.sort 中已经处理
	if not to_html_ka:to_html_ka={}
	
	if 'float_format' not in to_html_ka:
		to_html_ka['float_format']='{}'.format
		
	if py.isint(timezone):
		import pytz
		timezone = pytz.FixedOffset(timezone * -60 )# 8 hours * 60 minutes,如不-60变成UTC-8
	# 
	# return a

	# request,ucode,urla=N.geta(return_other_url={'url_decode':1,
	# '%23-':1
	# },return_request=True)
	
	import pandas
	df = pandas.DataFrame(data=a)
	if exclude_cols:
		if not U.iterable_but_str(exclude_cols):exclude_cols=[exclude_cols]
		df = df.drop(columns=exclude_cols)
	
	if order_cols:
		order_cols=py.list(order_cols)
		df=df[order_cols]
	
	if py.isdict(sort_kw) and not column_type_dict:
		for k,v in sort_kw.items():
			if py.isint(v) and k in ['c','col','column']:
				sort_kw=v
				break
			# if not py.isint(k):continue
			column_type_dict=sort_kw
			sort_kw=k
			break
	
	for cname,type in column_type_dict.items():
		if type=='ms':
			df[cname]=pandas.to_numeric(df[cname])  # 转换为数值类型 避免警告  FutureWarning: The behavior of 'to_datetime' with 'unit' when parsing strings is deprecated
			valid_mask = df[cname] > 0 # 对有效值进行时间戳转换，无效值保留原始值
			df[cname] = (
				pandas.to_datetime(df[cname][valid_mask], unit='ms', utc=True)
				.dt.tz_convert(timezone).dt.tz_localize(None)  # 时区处理
				.reindex(df.index)  # 保持与原数据索引一致
				.fillna(df[cname])  # 无效值填充为原始数值
			)

			# df[cname]=pandas.to_datetime(df[cname],unit='ms',)
			if timezone!='UTC':df[cname]=df[cname].dt.tz_localize(timezone).dt.tz_convert('UTC').dt.tz_localize(None) #.dt.tz_convert('UTC')不能省略 。否则显示UTC时间
			continue
		if type in ['t','time','s',]:
			df[cname]=pandas.to_numeric(df[cname])
			df[cname] = pandas.to_datetime(df[cname],unit='s',)
			if timezone!='UTC':df[cname]=df[cname].dt.tz_localize(timezone).dt.tz_convert('UTC').dt.tz_localize(None)
			continue
		df[cname] = df[cname].astype(type)

	try:
		if py.isint(sort_kw):
			df2=df.sort_values(df.columns[sort_kw],**sort_ka)
			if py.type(df2)==pandas.core.frame.DataFrame:df=df2 # fix inplace=True
		if py.istr(sort_kw):	
			df2=df.sort_values(sort_kw,**sort_ka)
			if py.type(df2)==pandas.core.frame.DataFrame:df=df2
	except TypeError as e:
		print(e,'       fallback: U.sort',U.stime())
		a=U.sort(a,sort_kw=sort_kw)
		return list_2d(response=response,a=a,html_callback=html_callback,index=index,
		# sort_kw=sort_kw,
		column_type_dict=column_type_dict,sort_ka=sort_ka,debug=debug,to_html_ka=to_html_ka,**ka,)
		
	if index:
		# df.reset_index(drop=True)
		# df.reset_index(drop=False)
		sindex_col='-1#t'#'-1n'
		if sindex_col in df:
			pass
		else:
			df.insert(0, sindex_col, py.range(py.len(df)) )
		index=False
		
	html=df.to_html(index=index,**to_html_ka) 
	
	if bottom_head and py.len(df)>(bottom_head if py.isint(bottom_head) else 34):
		thead=T.sub(html,'<thead>','</thead>')
		html=T.replace_last_one(html,'</tbody>',thead+'</tbody>')
	
# <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
	head='''
<head>
<style type="text/css">
table,th,td,textarea{
	padding:0px;
	margin:0px;
	border:1px solid green;/*没有solid 导致分割线消失*/
	border-spacing: 0px;
}
table>thead>tr {
	position: sticky;
	top: 0;
	background: white;
	z-index: 1;
}
'''+list_2d_CSS_MARK+'''
</style> 
</head>
'''	
	html=head+html+js
	if py.callable(html_callback):
		html=html_callback(html=html,head=head)

	if debug:return html
	
	response.headers['Content-Type']='text/html;charset=utf-8';
	response.set_data(html)
	return df
list=table=l2d=_2d_list=list2d=list_2d

def everything_search_image(response,add_offset=32,**ka):
	U.r(py,U,T,N,F,N.HTTP,N.HTML,)
	add_offset=U.get_duplicated_kargs(ka,'add_offset','offset','oa','ao','add',default=add_offset)
	# py.pdb()()
	# ucode=T.url_decode(ucode)
	# if not ucode.endswith('%23-'):
		# ucode+='%23-'
	request,ucode,a=N.geta(return_other_url={'url_decode':1,'%23-':1},return_request=True)
	
	U.set('rf',request.form )
	if request.form.get('a',''):	
		a=request.form.get('a','')

	
	if a:a=U.set('esimg.a',a)
	else:a=U.get('esimg.a')
	
	dua=T.parse_url_arg(a)     
	offset=py.int(dua.get('offset',0))
	search=dua.get('search','')
	
	def offset_url(previous=False):
		if add_offset:
			if previous:
				return T.replace_url_arg(a,'offset',offset-add_offset)
			else:	
				return T.replace_url_arg(a,'offset',offset+add_offset)
		else:	
			return a
		# U.print_repr(add_offset,request.form,ucode,a,newa)	
		
		
	es_base='http://'+T.get_url_netloc(a)
	h=N.HTTP.get(a,proxy=0)
	bs=T.BeautifulSoup(h)
	efs=bs.select('td[class=file]  a')
	if not efs:#NMM管理器 8888
		efs=bs.select('body > ul > section.files > li > a')
		
		
	# U.set('efs',[h,bs,fs])
	r=r"""
<meta name="viewport" content="width=device-width, initial-scale=0.3, minimum-scale=0.3, maximum-scale=1.0,user-scalable=0" cmt=禁止缩放/> 
	
<style type="text/css">
html,body{margin:0;pading:0;}/*不然两侧有空白*/	
img{
		width:100%;
		padding: 0 0 0 0;		
		margin: 0 0 0 0;
	}
/*

height: 25px;
*/	

	input,div{
border:1px solid #000000;
width: 99%;/*不然桌面会有下侧滚动条*/
overflow-x: auto;
white-space: nowrap;
overflow-y: hidden;
}
textarea.img_path{
	font-size:1.5vh; /*相对 屏幕高度*/
	direction: rtl; /*
		text-align: right;
		
		从右向左超出*/
	width:96%;
	padding:0px;
	margin:0px;
	border:1px solid #00000022; /*修复调整 textarea大小导致下分割线消失的问题*/
	border-spacing: 0px;
	resize: none; /*禁用 调整大小*/
	white-space: pre;/*以下3行，禁用 自动换行 */
	overflow-wrap: normal;
	overflow-x: scroll;
	
	height:2.3vh; /*隐藏滚动条 后，下方很多空白*/
}



textarea.img_path::-webkit-scrollbar,div::-webkit-scrollbar {
	display: none;    /* 隐藏滚动条 */
} 

div.scroll{
	height:15%;
	font-size:3vh;
	background:grey;
}

br {
   display: block;
   margin: 10px 0;
}

.submit{
	font-size:3vh;
	height:31%;
	width:99%;/*不然桌面会有下侧滚动条*/
	background:green;	
	text-align: left;
}

div.submit{
	height:15%;
}
input[type="text"]{
	font-size:1.8vh;
	
}

/*
	# height:555;
	# background:grey;

*/

</style> 

<script src="http://libs.baidu.com/jquery/2.1.4/jquery.min.js"></script>
<script>

 
</script>
	
"""+f"""
<form method="post" enctype="multipart/form-data" action="{ucode+offset_url(previous=True)}">
	<input type="text" name="a" value="{T.url_decode(offset_url(previous=True))}"/>
	<button type="submit" class="submit" id="previous" value="">
		↑ input[type="text"] added (previous=True)<br>
		current offset {offset} see browser url bar!<br>
		previous offset - {add_offset}
	</button>
</form>	

<div class="scroll" onclick="window.scrollTo(0, document.body.scrollHeight);">scroll to bottom</div>		

<div class="submit" onclick="document.getElementById('next').click()">next offset + {add_offset}</div>		

<!-- 

-->	
"""	

	for n,e in py.enumerate(efs):
		u=es_base+e.get('href')
		se=f''' <img src={u}>	
<i>{n}</i>		
<textarea class="img_path">{T.url_decode(u)}</textarea>		
		'''
		#RTL 文字从右至左  注意使用 f-string 执行顺序问题
#很奇怪 加空格显示 n总是在u的后面		
#>=={'77{} {} 99'.format(n,u)}++ 显示 ++http://192.168.1.3/C%3A/test/xsnvshen_a/24936/33978-8.jpg 99 772
#复制出来不是
		r+=se
	r=r+f'''	
<div class="scroll" onclick="window.scrollTo(0,0);">scroll to head</div>		
	
<div class="submit" onclick="document.getElementById('previous').click()"> previous offset - {add_offset}</div>			
	
<form method="post" enctype="multipart/form-data" action="{ucode+offset_url(previous=False)}">
	<input type="text" name="a" value="{T.url_decode(offset_url(previous=False))}"/>
	<button type="submit" class="submit" id="next" value="">
		↑ input[type="text"] added (previous=False)<br>
		current offset {offset} see browser url bar!<br>
		next offset + {add_offset}
	</button>
</form>		
'''	
	# response.set_data( h)
	response.headers['Content-Type']='text/html;charset=utf-8';
	response.set_data(r)
	return efs
esimg=everything_search_image

def eng_audio(response,word,audio_path='C:/test/google_translate_tts/',proxies="socks5h://192.168.1.20:41080",curl=False,**ka):
	if 'google_translate_tts' not in audio_path:
		audio_path+='google_translate_tts/'

	F.mkdir(audio_path)
	f=audio_path+'%s.dill'%word
	t0=U.timestamp()
	q=F.dill_load(f)
	# if not q:
		# q=F.dill_load(f )
	if not q:
	
		proxies=N.HTTP.auto_proxy(proxies,ka)#only return proxies, del proxy keys in ka
		
		# if N.check_port(21080):
			# proxy='socks5://127.0.0.1:21080'
		# else:	
			# proxy=None
	
		try:
			u='https://translate.googleapis.com/translate_tts?client=gtx&ie=UTF-8&tl=en&tk=775040.775040&q='+T.url_encode(word)
			if curl:
				import requests
				q=requests.Response()	
				q.status_code=200 # 不加这句 dill_load 时：requests\models.py  if 400 <= self.status_code < 500: ## TypeError: '<=' not supported between instances of 'int' and 'NoneType'
				q._content=N.curl(proxies=proxies,max_show_bytes_size=False,url=u)
			else:
				q=N.HTTP.request(u,proxies=proxies,timeout=6,**ka)
				b=q.content
				
			F.dill_dump(file=f,obj=q)
		except Exception as e:
			return py.No(e)
	if response:	
		# if py.isbyte(q)
		return N.copy_request_to_flask_response(q,response)
	else:
		return q
	
gskip_eng_list=T.del_space('''start,align,position,the,of,to,a,that,this,is,it,and,in,for,on,we,be,I,tank,you,will,as,from,are,with,there,engines,would,at,but,can,flight,
captions,
''').split(',')
def eng_dwi(response,dwi,ecdict=py.No('auto load'),sort_kw={},**ka):
	if not ecdict:
		ecdict=U.get_or_dill_load_and_set(r'C:\test\ecdict-770611.dill')
	dw3_freq=U.get_or_dill_load_and_set('C:/test/dw3-54150.dill')
		
		
		# F.dill_load()
	K_deci='deci-%s'%py.id(ecdict)
	deci=U.get(K_deci)
	if not deci:
		deci=U.get_or_set(K_deci,{i.word:n for n,i in enumerate(ecdict)},)
		
	
	sort_kw=U.get_duplicated_kargs(ka,'skw','sort','s',default=sort_kw)
	
	
		
	def get3(w,count=0):
		row=ecdict[deci[w]]
		zh=row.translation.replace('\\n','\n')
		if w in dw3_freq:
			f=dw3_freq[w][0]# TOTAL, RANK ,PoS
		else:
			f=0
		return count or dwi[w],f,w,zh
	r=[]
	re=[]
	rw=[]
	for w,count in dwi.items():
		if w in gskip_eng_list:continue
		if w in deci:
			rw.append(w)
			r.append(get3(w),)
		else:
			re.append(w)
	ree=[]		
	for w in re:
		wl=w.lower()
		if wl in deci and wl not in rw:
			r.append(get3(wl,count=dwi[w]),)
		else:
			ree.append(w)
			
	U.set('eng_dwi.ree',ree)		
	U.set('eng_dwi.dree',{w:dwi[w] for w in ree})		
	if sort_kw:
		r=U.sort(r,**sort_kw)
	return eng_list(response,r)		
	
def eng_list(response,a):
	'''

<meta name="viewport" content="width=device-width, initial-scale=0.5, minimum-scale=0.5, maximum-scale=1.0,user-scalable=1" cmt=禁止缩放/> 



<button style="height:33; width: 77%; " id=btn onclick="document.getElementById('btn').innerText=(window.outerWidth - 8) / window.innerWidth"></button>

'''    	
	if not a:
		response.set_data('eng_list not a %r'%a)
		return a
	main=''
	la0=len(a[0])
	is_namedtuple=py.getattr(a[0],'_fields',None)
	n=-1
	for row in a:
		# n,en,zh=-1,'',''
		if la0==2:
			n+=1
			en,zh=row
		elif la0==3:n,en,zh=row
		elif la0==4:
			n,nf,en,zh=row
			n=n,nf
		# if la0!=3:
		if is_namedtuple:# len==13
			en=row.word
			zh=row.translation.replace('\\n','\n')
		main+=r'''
<tr>
	<th class="num" onclick="play('{en}')">{n}</th>
	<th class=en onclick="play('{en}')"> <a>{en}</a>		</th>
	<th class=zh onclick="play('{en}')">{zh}</th>
</tr> 	
'''.format(n=n,en=en,zh=zh)

	r=T.html_template(globals=py.globals(),locals=py.locals(),s=r'''


	
<style type="text/css">

table,th,td,textarea{
	padding:0px;
	margin:0px;
	border:1px solid #00000022;/*修复调整 textarea大小导致下分割线消失的问题*/
	border-spacing: 0px;
	font-size: 3.5vh;
}
.num{
	width:5%;  
}
.en{
	width:45%;  
}
.zh{
	width:45%;  
}

</style>	


<table id="mytable" style=" width: 100%; ">
<thead>
	<tr>
		<th class="num">NO.</th>
		<th class=en>English		</th>
		<th class=zh>Zh</th>
	</tr> 	
	  
</thead>
	<tbody>

$main$
	
	</tbody>
  </table>	
	
	
<div style=" position:fixed; left:0px; bottom:0px; width:100%; height:5vh; background-color:#00aa00BB; z-index:9999;">
<input id="find" type="text" style=" display: inline-block;width:80%; height:100%;font-size: 4vh; color:red; background-color:#00aa0011;" onchange="find()">
</input>

<button style="    float:right;  width:20%; height:100%; color:blue;" onclick="window.location.reload(true);font-size:33vh;"> Z </button>

<button style="    float:right;  width:20%; height:100%; color:blue;" onclick="window.location.reload(true);font-size:33vw;"> S </button>

</div>

<script>
function play(word){
	console.log(word)
	var audio = new Audio();
	audio.src ="$U.get_or_set('rpc.server.base','/')$a=N.geta();N.HTML.eng_audio(response,a)%23-" + encodeURI(word);
	audio.play();
}

var dtx = new Map() //{} //Uncaught TypeError: dtx.get is not a function
var dtn = new Map() 

function find(){
	var t=document.getElementById('find').value
	var sx="//th[@class='en' and contains( .,'"+t+"')]"
	// if(var x=) Uncaught SyntaxError: Unexpected token var
	if(x=dtx.get(t)){ 
		
	}else{
		var x=document.evaluate("//th[@class='en' and contains( .,'"+t+"')]", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null)
		dtx.set(t,x)
	}
	
	if(x.snapshotLength){
	
	}else{
		
	
	}
	
	
	
	e=xpath(sx)
	
	e.scrollIntoView()
	e.setAttribute('style','color:yellow')
	e.click()
	scrollBy(0,-99)
	setTimeout(function(){
		e.setAttribute('style','color:black')
	
	},666)
	
	// document.getElementById('find').innerText=new Date()
}

function xpath(sp,ele){
	//var sp = "//a[text()='SearchingText']";
	if(ele){
		if(!sp.startsWith('.')){
			sp='.'+sp
		}
	}else{
		ele=document//直接重新赋值参数不用加 var
	}
	return document.evaluate(sp, ele, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}//end xpath


function disable_scale(){
	var metaTag=document.createElement('meta');
	metaTag.name = "viewport"
	metaTag.content = "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0"
	document.getElementsByTagName('head')[0].appendChild(metaTag);


}

//setTimeout(,3333)


</script>
	
	''')
	response.headers['Content-Type']='text/html;charset=utf-8';
	response.set_data(r)
	return a
def flask_ls(response,request=None):
	if not request:from flask import request
	r=T.html_template(globals=py.globals(),locals=py.locals(),s='''
<a href=></a>
	
	''',)
	
def flask_get_all_upload_files(upload_dir=py.No('U.gst/upload_dir',no_raise=1),save_size=py.No('8 MB',no_raise=1),request=None,):
	'''save_size <=0 : save_all
	'''
	from shutil import copyfileobj
	# U,T
	if not request:from flask import request
	if not upload_dir:
		upload_dir=U.get_or_set('rpc.server.upload_dir',U.gst+'upload_dir/')
	else:
		upload_dir=U.set('rpc.server.upload_dir',upload_dir)
	F.mkdir(upload_dir)
	if py.isno(save_size):
		save_size= U.get('rpc.server.upload.save_size',1024*1024*8)
	save_size=F.IntSize(py.int(save_size))	
	U.set('rpc.server.upload.save_size',save_size)	
	
	d={}
	for k,f in request.files.items(multi=True):# 默认multi=False，始终只能获取一个，坑！
		b=f.stream.read(save_size)
		if py.len(b)<save_size:
			if py.len(b)>99:
				sr="<{0} >'{1}...{2}'".format(F.readable_size(b),repr(b[:50])[2:-1],repr(b[-50:])[2:-1])  
				d[f]=U.object_custom_repr(b,repr=sr)
			else:
				d[f]=b
		else:
			fn=upload_dir+f.filename
			with py.open(fn,'wb') as fp:
				fp.write(b)
				copyfileobj(f.stream, fp)
			d[f]=fn
			
	return d
		# f.save(f.name)
files=save_file=save_files=flask_files=flask_save_all_upload_files=flask_get_all_upload_files	
	
ghtml_txt=r'''
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<style type="text/css">
	input[type="submit"]{
		width:100%;
	}
	input.url{
		width:49%; /*50% break line*/
	}	
	button.edit_btn{
		height: 33;
		width: 44;
		padding: 0 0 0 0;		
		margin: 0 0 0 0;		
	}
</style> 
</head>
	
<form method="post" enctype="multipart/form-data" action="$U.get_or_set('rpc.server.base','/')$r=U.set_multi($name$_form=request.form,$name$_files=N.HTML.flask_get_all_upload_files(),$name$_data=q.get_data(),);F.dp(request.form,'$name$_form');">
	<input type="submit" />
	<hr>
	<input type="file" multiple name="f">
	<hr>
	<div>
		<small style="
			padding: 22;
		">$name$:</small>
<!-- indent outdent 无效 -->
<button type="button" class="edit_btn" onclick="edit(this.innerText)">indent</button>
<button type="button" class="edit_btn" onclick="edit(this.innerText)">outdent</button>

<button type="button" class="edit_btn" onclick="edit(this.innerText)">forwardDelete</button>
<button type="button" class="edit_btn" onclick="edit(this.innerText)">delete</button>
<button type="button" class="edit_btn" onclick="edit('selectAll');edit('delete')">del all</button>
<!-- \n 不行，语法错误，被onclick转义了一次 -->
<button type="button" class="edit_btn" onclick="edit('insertText','\\n')">Enter</button>

<button type="button" class="edit_btn" onclick="edit(this.innerText)">selectAll</button>
<button type="button" class="edit_btn" onclick="edit(this.innerText)">paste</button>
<button type="button" class="edit_btn" onclick="edit(this.innerText)">copy</button>
<button type="button" class="edit_btn" onclick="edit(this.innerText)">cut</button>

<button type="button" class="edit_btn" onclick="edit(this.innerText)">undo</button>
<button type="button" class="edit_btn" onclick="edit(this.innerText)">redo</button>

<button type="button" class="edit_btn" onclick="insert_cbg()">U.cbg()</button>



	</div>
	
	
	<div style="height:60%;" > 
		<textarea id="textarea" name="t" style="width:100%; height: 100%;" >$(F.dl('t_form') or U.get('t_form') or {}).get('t','')$</textarea>
	</div>
	
	<hr>
	<input type="submit" />
	<input id=url_start class=url type="text" name="url_start" 
commt="/-                         U.set('rpc.server.upload.save_size',...code... "
value="$U.get('rpc.server.base')#$U.set('rpc.server.upload.save_size',$U.int_exp(U.get('rpc.server.upload.save_size',8*1024*1024),1024)#$);">
	<input id=url_end   class=url type="text" name="url_end" value="%23-">
</form> 
<script> 

$JS_async_post$

async function insert_cbg() {
	t=await post('$N.get_rpc_base_local()#$r=U.cbg()')
	if(!t.endsWith('\n')){
		t=t+'\n'
	} 
	e=document.querySelector('textarea#textarea')
	if(!e.value.startsWith(t)){
		e.value = t+e.value
	}
		
}

function edit(command,text){
	document.querySelector('textarea#textarea').focus()
	return document.execCommand(command, true,text);
}

var form  = document.querySelector('form');
var original_action=form.getAttribute('action');
original_action=original_action.substr($len(U.get('rpc.server.base'))#$) 
// if(original_action.startsWith('/')){
//}
document.querySelector('input#url_start').addEventListener('input', function(e){
	if(!e.srcElement.value.endsWith(';')){
		e.srcElement.value+=';'
	}
	
	form.setAttribute('action',e.srcElement.value+original_action)
	console.log(form.getAttribute('action'))
});
document.querySelector('input#url_end').addEventListener('input', function(e){
	form.setAttribute('action',original_action+e.srcElement.value)
	console.log(form.getAttribute('action'))
});

</script>
'''	
def textarea(response,name='t',upload_dir=py.No('U.gst/upload_dir',no_raise=1),):
	"""
	 <input type="text" name="t">
	
	"""
	U.r(N.HTML)
	if not U.all_in(name,T.aZ+'_'):
		raise py.ArgumentError(name,'must be alphabet_')
	r=T.html_template(globals=globals(),locals=locals(),s=ghtml_txt,)
	# r=format(r,name=name)
	response.headers['Content-Type']='text/html;charset=utf-8';
	return response.set_data(r)
txt=text=textarea
	
def html_script(response,*urls,rpc_base=None,max_show_len=999):
	if not rpc_base:rpc_base=U.get_or_set('rpc_base','/')
	html=''
	for url in urls:
		if ('://' not in url) and (not F.exist(url) ):
			html+="""
<hr>
{url}
<hr>
<script> {url} </script>
			
			""".format(url=url)
			continue
		html+="""
<hr>
{url}
<hr>
{js}
<script src="{rpc_base}r=N.get('''{url}''')">
</script>

	""".format(url=url,rpc_base=rpc_base,js=N.get(url)[:max_show_len] ) 
	return N.flask_html_response(response=response,remove_tag=[],html=html )
N.html_script=N.htmlScript=N.script=html_script

G_SELECT_ID=U.get_or_set(__name__+'.G_SELECT_ID','__qgb_id__') # 注意千万不能和待选择的key相同
G_SELECT_URL=U.get_or_set(__name__+'.G_SELECT_URL','__qgb_url__')
gid_select=U.get_or_set(__name__+'.gid_select',{})
def select_result(q,response,**ka):
	if N.is_flask_request(q):
		q=q.values
	if G_SELECT_ID not in q:
		raise py.ArgumentError('要post {id:,k...} 后的 request.values, 直接用get不带参数 是不行的。',q,response,ka)
	# if 'id' not in r:
	# 	raise py.ArgumentError('r not have id !',r)

	# if id not in gid_select:
	# 	raise py.ArgumentError('not found id in gid_select:',r)

		# if k not in r:
		# 	raise py.ArgumentError('unexpected submit key (must in r or disabled) :',k,v,q)
	qs=py.set()
	for k,v in q.items():
		if k==G_SELECT_URL:
			ka['url']=v
			continue
		if k==G_SELECT_ID:
			# id=v
			# id=py.int(id)
			r=gid_select[ py.int(v) ]
			disabled=r.disabled # 检查是否是 select对象
			continue
		if v!='on':
			raise py.ArgumentError('unexpected submit value (must be "on") :',k,v,q)
		k=int(k)		
		qs.add(k)
	# q=dict(q) # 如果不进行转换 就 id=q.pop('id')  TypeError("'CombinedMultiDict' objects are immutable")
	
	r.update_status(qs)
	# for k in py.list(r):
	# 	if id(k) not in qs:
	# 		r.move_to_disabled(k)
	# 		# ##disabled[k]=r.pop(k)
	# 		continue
	
	# for k in py.list(disabled):
	# 	if id(k) in qs:
	# 		r.move_back(k)
			# r[k]=disabled.pop(k)
			# continue

	return select(iterable=r,response=response,**ka)

def select(response,iterable,**ka):
	'''
#<!-- 
				# 不能用  editable="false" readyonly  
				#   <h6>包裹input无效 </h6>   
				# background="green" 无效 , lavender淡紫色, 熏衣草花 ,#e6e6fa 太淡啦
				#  -->	
	 '''
	# response=U.get_duplicated_kargs(ka,'p','resp','response','rp')
	request=U.get_duplicated_kargs(ka,'q','req','request','requests','rq')
	url=U.get_duplicated_kargs(ka,'url','mark_url', 'request_url')
	 
	if N.is_flask_request(request) and not url:
		url=request.url	
	if N.is_flask_request(url):
		url=request.url
	if url:
		url=T.url_decode(url)
	else:
		url=''
	
	ha='''
<head>
	<style type="text/css">
		textarea {
			background: lightgoldenrodyellow;
			width:80%;
			
			# rows:1; # 无效

		}

	</style>
</head>	
<form action="/r=N.HTML.select_result(request,response)%23"  method="post">
	{rows}
	<input type="submit" > 
</form>

'''
		####################
	hd='''
<span > {i} </span>
<input type="checkbox" name="{name}" {checked} > {k} </input>
<textarea> {v} </textarea>
<hr>'''
	########################
	def do_resp(r,kv,disabled):
		if response:
			rows='''
<input  type="text"  readonly="readonly"  name="{G_SELECT_ID}" value={id}  style="
	# background: aqua;
	background: cyan;
" >
<input  type="text"  readonly="readonly"  name="{G_SELECT_URL}" value={url} style="
	background: lightgray;
	width:80%
"> 
<br>
			'''.format(url=url,id=id,   G_SELECT_ID=G_SELECT_ID,G_SELECT_URL=G_SELECT_URL   )
			i=0
			# fk=lambda k: T.html_encode(repr(k))  #为啥会出现 0 ☑ q." checked > '
			fk=lambda _k:T.html_encode(repr(_k))  
			fv=lambda _v:T.html_encode(repr(_v)[:155-1] )# 全中文 80% 正好两行
			# U.msgbox(py.list(kv)[:9])
			for k,v in kv:
				# k,v=fk(k),fv(v)
				# U.msgbox(k,v)
				print(type(r),r.id)
				rows+=hd.format(i=i,name=r.id(k,v),k=fk(k),v=fv(v),checked='checked')
				i+=1
			for k,v in disabled:
				# k,v=fk(k),fv(v)
				rows+=hd.format(i=i,name=r.id(k,v), k=fk(k),v=fv(v) ,checked='')
				i+=1
			# py.importU().log(rows)	
			response.headers['Content-Type']='text/html;charset=utf-8';
			response.set_data(    T.format( ha, rows=rows  )     )	
		return r

	id=getattr(iterable,'id',0)
	if not id:
		id=py.id(iterable)
	if py.isdict(iterable):
		if isinstance(iterable,DictSelect):
			rd=iterable
		elif id not in gid_select:
			rd = gid_select[id]=DictSelect(iterable)
			# rd.id=id
		else:
			rd = gid_select[id]
		return do_resp(rd,rd.items(),rd.disabled.items())

	if py.islist(iterable):
		if isinstance(iterable,ListSelect):
			rd=iterable
		elif id not in gid_select:
			rd = gid_select[id]=ListSelect(iterable)
			# rd.id=id
		else:
			rd = gid_select[id]
		return do_resp(rd,enumerate(rd),enumerate(rd.disabled) 	)
		
		
def markdown(response,t=''):
	'''
pip install markdown	
	'''
	if not t:
		t=U.cbg()
	# U,T,N	
	import markdown
	html=markdown.markdown(t,extensions=['fenced_code'])
	response.headers['Content-Type']='text/html;charset=utf-8';
	response.set_data(html)
md=markdown	
	
################################################

class ListSelect(py.list):
	'''
	'''
	def __init__(self,*args, **ka):
		'''Initialize an ordered dictionary.  The signature is the same as
		regular dictionaries.  Keyword argument order is preserved.
		'''
		if not args:
			raise TypeError("descriptor '__init__' of select object "
							"needs an argument")
		# self, *args = args
		if len(args) > 1:
			raise TypeError('expected at most 1 arguments, got %d' % len(args))
		super().__init__(*args)
		# args=args[0]

		try:
			self.disabled=args.disabled # 没有类型检查，self 与 disabled 类型不同就完蛋
		except AttributeError:
			try:
				self.disabled
			except AttributeError:
				self.disabled=[]

	def id(self,k,v):
		return py.id(v)
	
	def update_status(self,ids):
		si=py.set()
		
		# for i,v in enumerate(self.disabled):

		for i,v in enumerate(self):
			if id(v) not in ids:
				si.add(i)
		n=0
		for i in si:
			v=self.pop(i+n)
			self.disabled.append(v)
			n=n-1
				# self.disabled.append(v)


class DictSelect(py.dict):
	'''
	'''
	def __init__(*args, **ka):
		'''Initialize an ordered dictionary.  The signature is the same as
		regular dictionaries.  Keyword argument order is preserved.
		'''
		if not args:
			raise TypeError("descriptor '__init__' of 'DictSelect' object "
							"needs an argument")
		self, *args = args
		if len(args) > 1:
			raise TypeError('expected at most 1 arguments, got %d' % len(args))
		args=args[0]

		try:
			self.disabled=args.disabled # 没有类型检查，self 与 disabled 类型不同就完蛋
		except AttributeError:
			try:
				self.disabled
			except AttributeError:
				self.disabled={}

		self.update(args, **ka)

	# def disable(self,key):
