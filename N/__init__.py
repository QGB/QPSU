#coding=utf-8
import sys
if __name__.endswith('qgb.N'):from qgb import py
else:
	from pathlib import Path
	gsqp=Path(__file__).parent.parent.parent.absolute().__str__()
	if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
	from qgb import py
	# import py  #'py': <module 'py' from '..\\py.py'>,

# __all__=['N','HTTPServer']

gError=[]
def setErr(ae):
	U=py.importU()
	global gError
	if U.gbLogErr:# U.
		if type(gError) is list:gError.append(ae)
		elif gError:gError=[gError,ae]
		else:gError=[ae]
	else:
		gError=ae
	if U.gbPrintErr:U.pln('#Error ',ae) # U.

try:
	if __name__.endswith('qgb.N'):
		from . import HTTP
		from . import HTTPServer
	else:
		import HTTP
		import HTTPServer
except Exception as ei:
	py.traceback(ei)

	
if py.is3():
	from http.server import SimpleHTTPRequestHandler,HTTPServer as _HTTPServer
else:
	from SimpleHTTPServer import SimpleHTTPRequestHandler
	from BaseHTTPServer import HTTPServer as _HTTPServer
	
def uploadServer(port=1122,host='0.0.0.0',dir='./',url='/up'):
	'''curl  http://127.0.0.1:1122/up -F file=@./U.py
	'''
	U=py.importU()	
	
	from flask import Flask,request,make_response, send_from_directory
	app= Flask('uploadServer'+U.stime_() )
	@app.route(url,methods=['POST','GET'])
	def upload_file():
		file = request.files['file']
		if file:
			filename = U.path.join(dir, file.filename)
			file.save(filename)			
			r= make_response(filename)
			r.headers['Content-Type'] = 'text/plain;charset=utf-8'
			return r
	app.run(host=host,port=port,debug=0,threaded=True)	
		
def rpcServer(port=23571,thread=True,ip='0.0.0.0',ssl_context=(),currentThread=False,app=None,key=None,pformat_kw={'width':144},
execLocals=None,locals=None,globals=None,qpsu='py,U,T,N,F',importMods='sys,os',request=True):
	'''
	locals : execLocals
	if app : port useless
	key char must in T.alphanumeric
	ssl_context default use https port=443 
	'''
	from threading import Thread
	U=py.importU()
	T=py.importT()
	
	if execLocals:
		warnning='### deprecated args execLocals {ip}:{port}'.format(ip=ip,port=port)
		U.log(warnning)
		globals=execLocals
		locals={'warnning':warnning} #同时模仿以前可以保存变量的效果
		
	if not globals:globals={}
	
	for modName in importMods.split(','):
		globals[modName]=U.getMod(modName)
	if qpsu:
		for modName in qpsu.split(','):
			globals[modName]=U.getMod('qgb.'+modName)	
		globals['pformat_kw']=pformat_kw
		
	from flask import Flask,make_response
	from flask import request as _request
	
	app=app or Flask('rpcServer'+U.stime_()   )
	
	def _flaskEval():
		nonlocal globals,locals,pformat_kw
		code=T.urlDecode(_request.url)
		code=T.sub(code,':{}/'.format(port) )
		U.log( (('\n'+code) if '\n' in code else code)[:99]	)
		# U.ipyEmbed()()
		_response=make_response()
		_response.headers['X-XSS-Protection']=0
		_response.headers['Access-Control-Allow-Origin'] = '*'
		_response.headers['Content-Type'] = 'text/plain;charset=utf-8'
		
		if request:#rpcServer config
			globals['request']=_request
			globals['response']=_response
			globals['q']=_request
			globals['p']=_response
		if not globals:globals=None # 如果globals 为空dict，防止闭包保存变量，保持globals在每个请求重新为空这一特性
		r=U.execResult(code,globals=globals,locals=locals,pformat_kw=pformat_kw) #因为在这里一般指定了 不为None的 globals，所以在每个请求中可以共享 
		if not _response.get_data():
			_response.set_data(r)
		return _response
	
	if py.istr(key):
		if py.len(key)<1:return py.No('key length < 1',key)
		for i in key:
			if i not in T.alphanumeric:
				return py.No('key char must in T.alphanumeric',key)
		@app.route('/#'+key+'\n<path:text>',
			methods=['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE', 'HEAD', 'PATCH'])
		def flaskEval(*a,**ka):return _flaskEval()
	else:
		@app.errorhandler(404)
		def flaskEval(*a,**ka):return _flaskEval()
		
	if not app.name.startswith('rpcServer'):
		return (py.No('caller provide app,so no thread start'),app)
	
	flaskArgs=py.dict(host=ip,port=port,debug=0,threaded=False)
	
	if ssl_context:
		flaskArgs['ssl_context']=ssl_context
		if port==23571:
			port=443
			flaskArgs['port']=port
			
	if currentThread or not thread:
		return app.run(**flaskArgs)
	else:
		t= Thread(target=app.run,name='qgb thread '+app.name,kwargs=flaskArgs)
		t.start()
		return (t,app)
########### flaskEval end ###########	
	if py.is3():from http.server import BaseHTTPRequestHandler as h
	class H(SimpleHTTPRequestHandler):
		def do_GET(s):
			code=s.path[1:]
			try:
				r=execResult(code)
				s.send_response(200)
			except Exception as e:
				s.send_response(500)
				
			s.send_header("Content-type", "text/plain")
			s.end_headers()		
			
			if not py.istr(r):
				r=repr(r)
			if py.is3():
				r=r.encode('utf8')
			s.wfile.write(r)
	

		
	# with _HTTPServer((ip,port), H) as httpd:
		# sa = httpd.socket.getsockname()
		# serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
		# print(serve_message.format(host=sa[0], port=sa[1]))
		# try:
			# if currentThread or not thread:httpd.serve_forever()
			# else:
				# t= Thread(target=httpd.serve_forever,name='qgb.rpcServer '+U.stime() )
				# t.start()
				# return t
				
		# except KeyboardInterrupt:
			# print("\nKeyboard interrupt received, exiting.")
	
# class rpcServer(HTTPHandler):
	# def __init__
		# super()
		
	
def rpcClient(url_or_port='http://127.0.0.1:23571',code=''):
	if py.isint(url_or_port):
		url='http://127.0.0.1:'+py.str(url_or_port)
	else:
		url=py.str(url_or_port)
	if not url.endswith('/'):url+='/'
	T=py.importT()
	code=T.urlEncode(code)
	return get(url+code)
	# if py.is3():
		# from xmlrpc.client import ServerProxy,MultiCall
	# server = ServerProxy(url)
	# return server
	
	
def get(url,protocol='http',file=''):
	U=py.importU()
	T=U.T
	if '://' in url:
		p=T.sub(url,'',':')
		if p:protocol=p
		else:raise U.ArgsErr(url)
	else:url=protocol+'://'+url
	if url.startswith('http'):
		# import HTTP
		return HTTP.get(url,file=file)	
	raise U.NotImplementedError
	return U.getAllMods()

def http(url,method='get',*args):
	return HTTP.method(url,method,*args)

def ipLocation(ip,reverse_ip=False,
junk=['本机地址  CZ88.NET','IANA 保留地址','局域网 IP','局域网 对方和您在同一内部网'] ):
	location=' '.join(ip_location_qqwry(ip))
	location=location.replace('CZ88.NET','').strip() #去除包含的
	
	if location in junk:
		return ip
		location=py.No(location)	
	if reverse_ip:
		return '%-15s [%s] '%(ip,location)
		# return '{0} [{1}] '.format(ip,location)
	else:
		return location		
sip_location=sipLocation=ip_location=ipLocation

######################  qqwry   ###########################
gw_qqwry=['CoreLink骨干网', '不丹', '东帝汶', '中非', '丹麦', '乌克兰', '乌兹别克斯坦', '乌干达', '乌拉圭', '乍得', '也门', '亚太地区', '亚洲', '亚美尼亚', '以色列', '伊拉克', '伊朗', '伯利兹', '佛得角', '俄罗斯', '保加利亚', '克罗地亚', '关岛', '冈比亚', '冰岛', '几内亚', '几内亚比绍', '列支敦士登', '刚果共和国', '刚果民主共和国', '利比亚', '利比里亚', '加勒比海地区', '加拿大', '加纳', '加蓬', '匈牙利', '北美地区', '北马其顿', '北马里亚纳群岛', '南极洲', '南苏丹', '南非', '博茨瓦纳', '卡塔尔', '卢旺达', '卢森堡', '印尼', '印度', '印度尼西亚', '危地马拉', '厄瓜多尔', '厄立特里亚', '叙利亚', '古巴', 
'台湾省', '台湾省云林县', '台湾省南投县', '台湾省南投县南投市', '台湾省台东县', '台湾省台中市', '台湾省台北市', '台湾省台南市', '台湾省嘉义县', '台湾省嘉义市', '台湾省基隆市', '台湾省宜兰县', '台湾省屏东县', '台湾省彰化县', '台湾省新北市', '台湾省新竹县', '台湾省新竹市', '台湾省桃园市', '台湾省澎湖县', '台湾省花莲县', '台湾省苗栗县', '台湾省金门县', '台湾省高雄市', 
'吉尔吉斯斯坦', '吉布提', '哈萨克斯坦', '哥伦比亚', '哥斯达黎加', '喀麦隆', '图瓦卢', '土库曼斯坦', '土耳其', '圣卢西亚', '圣基茨和尼维斯', '圣多美和普林西比', '圣巴泰勒米', '圣文森特和格林纳丁斯', '圣皮埃尔和密克隆群岛', '圣诞岛', '圣马力诺', '圭亚那', '坦桑尼亚', '埃及', '埃塞俄比亚', '基里巴斯', '塔吉克斯坦', '塞内加尔', '塞尔维亚', '塞拉利昂', '塞浦路斯', '塞舌尔', '墨西哥', '多哥', '多米尼克', '多米尼加', '奥兰群岛', '奥地利', '委内瑞拉', '孟加拉', '孟加拉国', '安哥拉', '安圭拉', '安提瓜和巴布达', '安道尔', '密克罗尼西亚联邦', '尼加拉瓜', '尼日利亚', '尼日尔', '尼泊尔', '巴勒斯坦', '巴哈马', '巴基斯坦', '巴巴多斯', '巴布亚新几内亚', '巴拉圭', '巴拿马', '巴林', '巴西', '布基纳法索', '布隆迪', '希腊', '帕劳', '库克群岛', '库拉索', '开曼群岛', '德国', '意大利', '所罗门群岛', '托克劳', '拉美地区', '拉脱维亚', '挪威', '捷克', '摩尔多瓦', '摩洛哥', '摩纳哥', '文莱', '斐济', '斯威士兰', '斯洛伐克', '斯洛文尼亚', '斯里兰卡', '新加坡', '新喀里多尼亚', '新西兰', '日本', '智利', '朝鲜', '柬埔寨', '根西岛', '格林纳达', '格陵兰', '格鲁吉亚', '梵蒂冈', '欧洲', '欧洲地区', '欧盟', '欧美地区', '比利时', '毛里塔尼亚', '毛里求斯', '汤加', '沙特阿拉伯', '法国', '法属圣马丁', '法属圭亚那', '法属波利尼西亚', '法罗群岛', '波兰', '波多黎各', '波斯尼亚和黑塞哥维那', '泰国', '泽西岛', '津巴布韦', '洪都拉斯', '海地', '澳大利亚', '澳洲', '澳门', '爱尔兰', '爱沙尼亚', '牙买加', '特克斯和凯科斯群岛', '特立尼达和多巴哥', '玻利维亚', '瑙鲁', '瑞典', '瑞士', '瓜德罗普', '瓦利斯和富图纳群岛', '瓦努阿图', '留尼汪岛', '白俄罗斯', '百慕大', '直布罗陀', '福克兰群岛', '科威特', '科摩罗', '科特迪瓦', '科索沃', '秘鲁', '突尼斯', '立陶宛', '索马里', '约旦', '纳米比亚', '纽埃', '缅甸', '罗马尼亚', '美国', '美属维尔京群岛', '美属萨摩亚', '美洲地区', '老挝', '肯尼亚', '芬兰', '苏丹', '苏里南', '英国', '英属印度洋领地', '英属维尔京群岛', '荷兰', '荷兰加勒比', '荷兰省', '荷属圣马丁', '莫桑比克', '莱索托', '菲律宾', '萨尔瓦多', '萨摩亚', '葡萄牙', '蒙古', '蒙特塞拉特岛', '西班牙', '诺福克岛', '贝宁', '赞比亚', '赤道几内亚', '越南', '阿塞拜疆', '阿富汗', '阿尔及利亚', '阿尔巴尼亚', '阿曼', '阿根廷', '阿联酋', '阿鲁巴', '非洲地区', '韩国', '韩国首尔', '香港', '马尔代夫', '马恩岛', '马拉维', '马提尼克', '马来西亚', '马约特', '马绍尔群岛', '马耳他', '马达加斯加', '马里', '黎巴嫩', '黑山'] 
#278

g_reserved_qqwry=[ 'IANA机构', 'IANA保留地址', '运营商级NAT','本机地址', '本地', 'IANA', '局域网']
# 7
	
gn_qqwry=['上海', '云南', '内蒙古', '北京', '南京', '吉林', '四川', '天津', '宁夏', '安徽', '山东', '山西', '广东', '广西', '新疆', '江苏', '江西', '河北', '河南', '浙江', '海南', '湖北', '湖南', '甘肃', '福建', '西藏', '贵州', '辽宁', '重庆', '陕西', '青海', '黑龙江', '东北三省', '广州市清', '长春工业', '西安石油', '北方工业', '首都经贸', '首都师范', '宁波大学', '华中农业', '中国人民', '华东师范', '中南大学', '长江大学', '东北农业', '对外经济', '东华大学', '华南理工', '华中科技', '武汉大学', '大连理工', '南开大学', '中国', '中国青岛嘉华网络BGP', '中国农业科学院', '雅虎中国', '雅虎中国公司', '中国CEI(中国经济信息网)骨干网', '中国国际电子商务中心', '中国电信', '南昌理工学院', '电信'] 
#63
# 203.14.187.0-255 ('电信', ' CZ88.NET')

	
def ip_location_qqwry(ip,dat_path=py.importU().gst+'qqwry.dat'):
	'''return ('地区' , '运营商')
if want update qqwry.dat , reloa N module,and call this with dat_path !!!
warnning: NOT thread safe !!!

pip install qqwry-py3

pip install qqwry  # Not have cz88update
	'''	
	if ('q' not in ip_location_qqwry.__dict__):
		U=py.importU()
		F=py.importF()
		import qqwry
		
		if not dat_path:
			if U.isWin():
				qqwry_path=r'C:\Program Files (x86)\cz88.net\ip\qqwry.dat'
				if F.exist(qqwry_path):
					dat_path=qqwry_path
			if not dat_path:
				dat_path=U.gst+'qqwry.dat'
				
		if not F.exist(dat_path):
			U.log(['updateQQwry length:', qqwry.updateQQwry(dat_path)] )
			
		ip_location_qqwry.q = qqwry.QQwry()
		ip_location_qqwry.q.load_file(dat_path,loadindex=True)
	
	return ip_location_qqwry.q.lookup(ip)  #('北京市', '联通')

###################  qqwry end ###########################
def address_coordinate(address,raw_response=True):
	import requests
	cookies = {
		'BAIDUID': '7240C1BD73BF5509083867D8372AA3C8:FG=1',
		'PSTM': '1547906786',
		'BDUSS': 'dnamEzZk5OT3N6R3J2QnJVckMtdjdIMm54ZjY3VWNsTGQ5SmtodjVOS2JaOE5jQVFBQUFBJCQAAAAAAAAAAAEAAACYT6sRUUdCQ1MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJvam1yb2ptcaV',
		'MCITY': '-%3A',
		'H_WISE_SIDS': '131410_126124_128701_129321_114744_128142_120764_120189_131601_118886_118868_131402_118843_118833_118797_130762_131650_131577_131535_131534_131529_130222_131390_129565_107320_131394_130123_131518_131240_131195_117327_130347_117436_130075_129647_124635_130690_131435_131687_131036_131047_129981_130989_129901_129479_129646_124802_131467_131424_110085_127969_131506_123290_131094_131297_128200_131550_131264_131262_128600',
		'BIDUPSID': '2DD44AA3F0CF69531B5E310CF80AEBD8',
		'pgv_pvi': '6249972736',
		'pgv_si': 's660814848',
		'ZD_ENTRY': 'google',
		'H_PS_PSSID': '1453_21112_18560_29523_29521_29720_29568_29220_22159',
	}
	headers = {
		'Pragma': 'no-cache',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 YaBrowser/19.3.1.779 Yowser/2.5 Safari/537.36',
		'Accept': '*/*',
		'Referer': 'https://maplocation.sjfkai.com/',
		'Connection': 'keep-alive',
		'Cache-Control': 'no-cache',
	}
	# '湖南省长沙市长沙县长沙经济技术开发区开元东路华润置地广场一期12幢'
	params=(('address', address),
	('output', 'json'),
	('ak', 'gQsCAgCrWsuN99ggSIjGn5nO'),
	('callback', 'showLocation0'))

	response = requests.get('https://api.map.baidu.com/geocoder/v2/', headers=headers, params=params, cookies=cookies)
	s=response.content.decode('utf-8')
	s=s.replace('showLocation0&&showLocation0(','')
	s=s.replace('}})','}}')
	T=py.importT()
	try:
		json=T.json_loads(s)
	except Exception as e:
		json={'err_s':s,
			  'err':e}
	response.close()
	if raw_response:
		json['raw_response']=response
	return json
	
map_location=address_coordinate	
	
	
	
def whois(domain,raw_response=False):
	'''
In [59]: [i for i in dw if 'admin_name' not in dw[i] ] #58643
['csfangyi.com', 'xn--xuw24ggz9aile.cn', '06jd.com', 'yzy88.com', 'cshelong.com']

''' 
	T=py.importT()
	import requests
	cookies = {	'st': '95f5609d7aaadb13806df43e2ca1961c',	}
	headers = {
		'Pragma': 'no-cache',
		'Origin': 'http://whois.4.cn',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
	'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 YaBrowser/19.3.1.779 Yowser/2.5 Safari/537.36',

		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Cache-Control': 'no-cache',
		'X-Requested-With': 'XMLHttpRequest',
		'Connection': 'keep-alive',
		'Referer': 'http://whois.4.cn/batch',
	}

	data = {'domain': domain,  'isRefresh': '1'}
	response=requests.post('http://whois.4.cn/api/main',headers=headers,cookies=cookies,data=data)
	json=T.json_loads(response.content.decode('utf-8'))
	response.close()
	if raw_response:
		json['raw_response']=response
	return json
	
	
def bulk_whois(domain_list,args):
	import requests,json,logging
	bulkwhois_base_url = 'https://www.whoisxmlapi.com/BulkWhoisLookup/bulkServices/'
	session = requests.session()
	data = {
		"domains": domain_list,
		"password": args.password,
		"username": args.username,
		"outputFormat": 'json'
	}
	header = {'Content-Type': 'application/json'}
	# Posting task to API
	response = session.post(bulkwhois_base_url + 'bulkWhois',
							 data=json.dumps(data),
							 headers=header,
							 timeout=5)
	if response.status_code != 200:
		logging.error("wrong response code: %i" % response.status_code)
		return response
	response_data = json.loads(response.text)
	if response_data['messageCode'] == 200:
		logging.debug('Response: ' + response.text)
		del data['domains']
		data.update({
			'requestId': response_data['requestId'],
			'searchType': 'all',
			'maxRecords': 1,
			'startIndex': 1
		})
	else:
		logging.error('Response: ' + response.text)
		return response

	# waiting for job complete
	logging.debug("data:" + str(data))
	recordsLeft = len(domain_list)
	while recordsLeft > 0:
		time.sleep(args.interval)
		response = session.post(bulkwhois_base_url + 'getRecords',
								headers=header,
								data=json.dumps(data))
		if response.status_code != 200:
			logging.error("wrong response code: %i" % response.status_code)
			exit(1)
		recordsLeft = json.loads(response.text)['recordsLeft']
		logging.debug('Response: ' + response.text)

	data.update({'maxRecords': len(args.domains)})
	# dump json data
	time.sleep(args.interval)
	response = session.post(bulkwhois_base_url + 'getRecords',
							headers=header,
							data=json.dumps(data))
	with open(args.output + '.json','w') as json_file:
		json.dump(json.loads(response.text),json_file)

	# download csv data
	time.sleep(args.interval)
	with open(args.output + '.csv', 'wt') as csv_file:
		response = session.post(bulkwhois_base_url + 'download',
								headers=header,
								data=json.dumps(data))
		for line in response.text.split('\n'):
			clear_line = line.strip()
			# remove blank lines
			if clear_line != '':
				csv_file.write(clear_line + '\n')
################### whois end #####################





def netplan_add_routes(ip,gateway=py.No('auto use first'),
	adapter=py.No('auto use first who has routes'),
	yamlFile=r'/etc/netplan/50-cloud-init.yaml' ):
	''' '''
	U=py.importU()
	F=U.F
	n=F.readYaml(yamlFile)
	for adapterName,v in n['network']['ethernets'].items():
		if ( (not gateway) or (not adapter) ) and 'routes' in v:
			for dipg in v['routes']:
				gateway=dipg['via'] if not gateway else gateway
				adapter=adapterName if not adapter else adapter
				break
	if ('.' not in ip ) or (not gateway) or (not adapter):
		raise py.ArgumentError('please specify ip gateway adapter',ip,gateway,adapter)
	adapterV=n['network']['ethernets'][adapter]
	if 'routes' not in adapterV:
		adapterV['routes']=[]
	routes= adapterV['routes']
			
	for i in routes:
		if ip==i['to']:
			i['via']=gateway
			break
	else:
		routes.insert(0,{'to':ip,'via':gateway } )
		
	# import os;os.system('sudo netplan apply')
	
	return (ip,gateway,adapter,F.writeYaml(yamlFile,n) )
	

def get_ip_from_mac(mac):
	'''mac=='' return all ip
	'''
	U=py.importU()
	T=U.T
	r=U.cmd('arp','-a').splitlines() 
	r=[T.sub(i,'  ', '   ') for i in r if mac in i]
	r=[i for i in r if i]
	if py.len(r)==0:
		return py.No('no ip match mac:{} in arp table!'.format(mac))
	if py.len(r)>1:
		return py.No('more then 1 ip matched mac:{} in arp table!'.format(mac),r)
	if py.len(r)==1:
		return r[0]

def getLAN_IP_HOSTS(ip='192.168.1.{}',count=256):
	import socket
	for i in range(count):
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			s.connect((ip.format(i), 9))
			my_ip = s.getsockname()[0]
			print(my_ip, flush=True)	
	r=getAllAdapter()
	return r

def getAllAdapter():
	U=py.importU()
	if U.iswin():
		from qgb import Win
		return Win.getAllNetworkInterfaces()

#setip 192.168  ,  2.2	
def setIP(ip='',adapter='',gateway='',source='dhcp',mask='',ip2=192.168,dns=py.No('gateway') ):
	'''配置的 DNS 服务器不正确或不存在。   # 其实已经设置好了，可以正常使用'''
	U=py.importU()
	if U.islinux():
		import socket,struct,fcntl
		if not py.isbytes(adapter):adapter=adapter.encode('ascii')
		if not py.isbytes(gateway):gateway=gateway.encode('ascii')
		if not py.isbytes(mask)   :mask=mask.encode('ascii')
			
		SIOCSIFADDR = 0x8916
		SIOCSIFNETMASK = 0x891C
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if mask:
			ifreq = struct.pack('16sH2s4s8s', adapter, socket.AF_INET, b'\x00' * 2, 
			socket.inet_aton(mask), b'\x00' * 8)
			fcntl.ioctl(sock, SIOCSIFNETMASK, ifreq)
			
		bin_ip = socket.inet_aton(ip)
		ifreq = struct.pack('16sH2s4s8s', adapter, socket.AF_INET, b'\x00' * 2, bin_ip, b'\x00' * 8)
		return fcntl.ioctl(sock, SIOCSIFADDR, ifreq)
	
	if not adapter:
		#adapter=u'"\u672c\u5730\u8fde\u63a5"'.encode('gb2312')#本地连接
		try:
			adapter=getAllAdapter()[0][0]	#   ( [11,'192.168.1.111',..] , [..] , ..]
		except:	
			if py.is2():adapter="\xb1\xbe\xb5\xd8\xc1\xac\xbd\xd3"
			else:		adapter="本地连接"
		# from qgb import Win
		# if Win.isxp():
			
	if ip:
		source='static'
		if type(ip) is py.int:
			ip='{0}.2.{1}'.format(ip2,ip)
		if type(ip) is py.float:
			ip='{0}.{1}'.format(ip2,ip)		
		
		if not mask:mask='255.255.255.0'
		if not mask.startswith('mask'):mask='mask='+mask
		
		if not gateway:
			T=py.importT()
			gateway=T.subLast(ip,'','.')+'.1'
		if not gateway.startswith('gateway'):
			if not dns:
				dns=gateway
			dns='address={}  register=primary'.format(dns)
			gateway='gateway='+gateway
			
		if not ip.startswith('addr'):ip='address='+ip
	else:
		ip=''
	r=[ 'netsh interface ip set address name={0} source={1} {2} {3} {4} '.format(adapter,source,ip,mask,gateway),
		'netsh interface ip set dnsservers name={0} source={1} {2}'.format(adapter,source,dns)
		]
	import os
	for i in r:
		os.system(i)
	return r
setip=setIP
def getComputerName():
	import socket
	return socket.gethostname()
gethostname=getHostName=getComputerName

def getArpTable():
	U=py.importU()
	return U.cmd('arp -a')
		
def scanPorts(host,threadsMax=33,from_port=1,to_port=65535,callback=None,ip2=192.168):
	'''return [opens,closes,errors]
	callback(*scanReturns)
	if callback and ports> threadsMax: 剩下结果将异步执行完成
	'''
	U=py.importU()
	from threading import Thread
	import socket
	# host = raw_input('host > ')
	# from_port = input('start scan from port > ')
	# to_port = input('finish scan to port > ')   
	counting_open = []
	counting_close = []
	errors=[]
	threads = []
	if isinstance(host,py.float):host='{0}.{1}'.format(ip2,host)
	
	def scan(port):
		# U.count(1)
		try:
			s = socket.socket()
			result = s.connect_ex((host,port))
			# U.pln('working on port > '+(str(port)))      
			if result == 0:
				counting_open.append(port)
				#U.pln((str(port))+' -> open') 
				s.close()
			else:
				counting_close.append(port)
				#U.pln((str(port))+' -> close') 
				s.close()
		except Exception as e:
			errors.append({port:e})
	def newThread(port):
		t = Thread(target=scan, args=(i,))		
		threads.append(t)
		try:
			t.start()
		except:
			"can't start new thread"
	im=py.float(to_port-from_port+1)
	percent=0.0
	for i in range(from_port, to_port+1):
		if (i/im>percent):
			U.pln( 'Scanning  %.0f%%' % (percent*100), len(threads)     )
			percent+=0.01
			
		if len(threads)<=threadsMax:
			newThread(i)
		else:
			for x in threads:
				if x.isAlive():
					x.join()
					newThread(i)
				else:
					threads.remove(x)
				break
	# if callback:
		# return callback
	[x.join() for x in threads]
	return [counting_open,counting_close,errors]
	

if __name__=='__main__':
	
	
	rpcServer()
	exit()
	U.pln( getLAN_IP())
	exit()
	gsurlip=['http://ip.chinaz.com/getip.aspx'][0]
	
	
	s=http(gsurlip)#.encode('utf8').decode('mbcs')
		 
		 
	U.pln( s.decode('utf8').encode('mbcs'))
	# import chardet
	# U.pln( chardet.detect(s)
	
