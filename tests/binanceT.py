#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

from logging import info as log_info
import json,pandas,numpy
class MyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, pandas.Timestamp):
			return obj.value
			# 将 Timestamp 对象转化为毫秒
			# print(obj.value)
			# return int(obj.value // 10**6)
		return super().default(obj)
json_dumps_ka=dict(cls=MyEncoder,) #indent=0

gdq={'BTC': [290, 172],
 'ETH': [65, 161],
 'USDT': [384, 118],
 'BNB': [61, 235],
 'TUSD': [27, 40],
 'USDC': [66, 25],
 'XRP': [1, 1],
 'TRX': [1, 1],
 'TRY': [199, 7],
 'EUR': [32, 23],
 'ZAR': [3, 2],
 'IDRT': [1, 3],
 'UAH': [4, 3],
 'DAI': [4, 1],
 'BRL': [20, 21],
 'DOGE': [1, 0],
 'PLN': [3, 1],
 'RON': [3, 1],
 'ARS': [2, 0],
 'FDUSD': [92, 0],
 'AEUR': [3, 0],
 'JPY': [7, 0],
 'MXN': [1, 0],
 'CZK': [1, 0]}

gdims={'1s': 1000,
 '1m':  1000*60,
 '3m':  1000*60*3,
 '5m':  1000*60*5,
 '15m': 1000*60*15,
 '30m': 1000*60*30,
 '1h':  1000*60*60,
 '2h':  1000*60*60*2,
 '4h':  1000*60*60*4,
 '6h':  1000*60*60*6,
 '8h':  1000*60*60*8,
 '12h': 1000*60*60*12,
 '1d':  1000*60*60*24,
 '3d':  1000*60*60*24*3, # *3
 '1w':  1000*60*60*24*7, # *7
 '1M':  1000*60*60*24*31, #
 }
gdi_okx={'1s': '1s',
 '1m': '1m',
 '3m': '3m',
 '5m': '5m',
 '15m': '15m',
 '30m': '30m',
 '1h': '1H',
 '2h': '2H',
 '4h': '4H',
 '6h': '6H',
 '8h': '8H',
 '12h': '12H',
 '1d': '1D',
 '3d': '3D',
 '1w': '1W',
 '1M': '1M'}
rpcka=U.get('rpcka')
def get_rpcka():
	global rpcka
	if not rpcka:rpcka=U.get('rpcka')
	if not rpcka:raise py.EnvironmentError('no rpcka ')
	return rpcka
def get_srpcka(ka):
	srpcka=''
	for k,a in ka.items():
		if k.startswith('convert'):
			srpcka+=f'{k}={a!r},'
		if k.startswith('p'):
			srpcka+=f'{k}={a!r},'
			
	if 'convert_func' not in srpcka:srpcka+='convert_func=float,'
	return srpcka

def get_kline_without_pandas(symbol='ETH',interval='1s',start=0,end=0,day='',second=0,kline_range=(-500,500),auto_expand_range=False,return_json=True,debug=False,futures=0,**ka):
	'''  U.cbs(U.stime_to_ms_int(U.cbg(p=1))-1000*60*60*8,p=1)
	'''
	symbol=U.get_duplicated_kargs(ka,'symbol','s','S',default=symbol)
	interval=U.get_duplicated_kargs(ka,'interval','i','it',default=interval)
	second=U.get_duplicated_kargs(ka,'second','sec','ms',default=second)
	futures=U.get_duplicated_kargs(ka,'futures','f','fur',default=futures)
	
	symbol=symbol.upper()
	seq=T.endswith(symbol,*gdq)
	assert len(seq)<=1
	b=''
	if symbol in gdq or not seq:
		b=symbol
		symbol=b+'USDT'
	elif seq:
		b=symbol[:-len(seq[0])]
		
	if second and not (start and end):
		if py.istr(second):
			second=U.stime_to_ms(second,timezone=8)
		elif U.slen(second)==10:second*=1000
		
		cms=U.itime_ms()
		if auto_expand_range and second+kline_range[1]*gdims[interval]>cms:
			kline_range=py.list(kline_range)#TypeError: 'tuple' object does not support item assignment
			kline_range[1]=(cms-second)//gdims[interval]+1
			kline_range[0]=-(1000-kline_range[1])
		start=second+kline_range[0]*gdims[interval]
		start=py.max(start,0)
		end=second+kline_range[1]*gdims[interval]
	if debug:
		return U.v.rpc_get(f"B.get_kline_without_pandas({symbol!r},interval={interval!r},start={start!r},end={end!r},{get_srpcka(ka)})",**get_rpcka())

	if '-' in symbol:  # okx
		# 构建URL
		url = f"https://www.okx.com/api/v5/market/history-candles?instId={symbol}&bar={gdi_okx[interval]}&limit=100"
		# 发送请求
		response = requests.get(url,proxies={'https':get_rpcka()['proxy']})
		data_json = response.json()
		# 检查返回码
		if data_json['code'] == '0':
			data = data_json['data']  # 这是一个列表，包含99条K线数据（每条9个字段）
		else:
			# return py.No(response.text)
			# 如果出错，可以打印错误信息，并返回空列表？根据上下文，后面转换函数会处理空列表
			log_info(f"Error from OKX: {response.text}",)
			data = []
	elif futures:
		data=N.rpc_get(f"B.get_futures_kline({symbol!r},interval={interval!r},start={start!r},end={end!r},{get_srpcka(ka)})",**get_rpcka())
	else:
		data=N.rpc_get(f"B.get_kline_without_pandas({symbol!r},interval={interval!r},start={start!r},end={end!r},{get_srpcka(ka)})",**get_rpcka())
	
	if return_json:
		return convert_klines_to_json(data)
	return data
	
get_klines=get_kline=get_kline_without_pandas


def agg_kline(symbol,interval='1d',start=0,end='',symbol_old='BUSD',return_json=True,**ka):
	symbol_old=U.get_duplicated_kargs(ka,'symbol_old','old','prev','old_symbol',default=symbol_old)
	# if len(symbol)<9:
	symbol=symbol.upper()
	seq=T.endswith(symbol,*gdq)
	assert len(seq)<=1
	b=''
	if symbol in gdq or not seq:
		b=symbol
		if symbol_old=='BUSD':symbol_old=b+symbol_old
		symbol=b+'USDT'
	elif seq:
		q=seq[0]
		b=symbol[:-len(q)]
		if symbol_old=='BUSD':symbol_old=b+symbol_old
	
		
		
		
	rpcka=get_rpcka()
	# rpcka.update(ka)
	
	
	old=[]
	if symbol_old:
		# if interval in ['1d','3d','1w','1M']
		f=f'binance/{symbol_old}={interval}.dill'
		old=F.dill_load_file(f)
		if not old:
			old=N.rpc_get(f"B.get_kline_without_pandas({symbol_old!r},interval={interval!r},start={start!r},{get_srpcka(ka)})",**rpcka)
			if old:
				print(U.stime(),'dill_dump',F.dill_dump(obj=old,file=f))
	if old:
		if not start and interval in ['1d','3d',]:
			start=old[-1][0]
			if isinstance(start,pandas.Timestamp):start=start.value
		
	data=N.rpc_get(f"B.get_kline_without_pandas({symbol!r},interval={interval!r},start={start!r},end={end!r},{get_srpcka(ka)})",**rpcka)	
	
	if b=='FTT':
		n2=n3=0			
		if interval=='1M':
			for n,row in enumerate(data):
				if row[0]==1667260800000:n2=n#22-11-01
				if row[0]==1693526400000:#23-09-01
					n3=n
					break
			data=data[:n2]+old[17:]+data[n3+1:]		
			old=[]
		elif interval=='1w':
			for n,row in enumerate(data):
				if row[0]==1668384000000:n2=n#22-11-14					
				if row[0]==1694995200000:#23-09-18
					n3=n
					break
			data=data[:n2]+old[74:118]+data[n3:]
		elif interval=='3d':
			for n,row in enumerate(data):				
				if row[0]==1695859200000:#2023-09-28 08
					n3=n
					break
			# assert old[0][0]==1623974400000 # 2021-06-18 08
			data_2021=N.rpc_get(f"B.get_kline_without_pandas({symbol!r},interval={interval!r},start=0,end=1623974400000,{get_srpcka(ka)})",**rpcka)	
			data=data_2021+old[:277]+data[n3:]  # 3d周期 BUSD 和USDT  有偏差一天
			
		elif interval=='1d':
			for n,row in enumerate(data):				
				if row[0]==1695945600000:#2023-09-29 08
					n3=n
					break
			assert old[0][0]==1623974400000 # 2021-06-18	
			data_2021=N.rpc_get(f"B.get_kline_without_pandas({symbol!r},interval={interval!r},start=0,end=1623974400000,{get_srpcka(ka)})",**rpcka)	
			data=data_2021+old[1:833]+data[n3:]
			
		else:
			return U.enu(old),data,F.delete(f)
	
		old=[]
	
		
	
	if old and not data:data=old
	
	if return_json==None:# 测试代码  用于查看中间状态
		if old:data=old+data
		return data
	
	if old:
		while old and data[0][0]<=old[-1][0]:
			if data[0][0]==old[-1][0] and data[0][1]>old[-1][1]*1.01:
				data[0][1]=old[-1][1]
				if data[0][1]<data[0][3]:data[0][3]=py.min(old[-1][3],data[0][3]) # 防止KLineChart自动修复造成跳空
			old=old[:-1]
			
		data=old+data
		
	
	if return_json:
		return convert_klines_to_json(data)
	return data
	
def B_get_klines(symbol,start,end,day='',interval='1s',return_json=True):
	''' ='UNFIUSDT'
	
'''	
	rpcka=get_rpcka()
	
	data=N.rpc_get(f"B.get_klines(symbol={symbol!r},start='{day} {start}',end='{day} {end}',interval={interval!r})",**rpcka)
	
	if return_json:
		return convert_klines_to_json(data)
	else:
		return data

def convert_klines_to_json(klines):
	rds = []
	# if 'pandas.core.frame.DataFrame' in py.str(py.type(klines)):
	if isinstance(klines,pandas.DataFrame):
		if py.len(klines.columns) == 12:
			klines['OpenTime']=klines['OpenTime'].apply(lambda x: x.timestamp()*1000).astype(numpy.int64)
			klines=py.list(klines.values)
		else:
			ds = klines.to_dict(orient='records')
			for d in ds:
				kline_data = {
					'timestamp': int(d['close_datetime'].timestamp() * 1000),
					'open': d['open'],
					'high': d['high'],
					'low': d['low'],
					'close': d['close'],
					'volume':d['volume'],
					'turnover':d['quote_volume'],
				}
				rds.append(kline_data)
	if py.islist(klines):
		if not klines:pass# rds=[]
		elif len(klines[0]) == 9:  #  处理OKX 9字段格式: [ts, o, h, l, c, vol, volCcy, volCcyQuote, confirm]
			for v in klines:
				kline_data = {
					'timestamp': int(v[0]),  # 时间戳(毫秒)
					'open': float(v[1]),     # 开盘价
					'high': float(v[2]),     # 最高价
					'low': float(v[3]),      # 最低价
					'close': float(v[4]),    # 收盘价
					'volume': float(v[5]),   # 基础货币成交量
					'turnover': float(v[7])  # 计价货币成交额(volCcyQuote)
				}
				rds.append(kline_data)
		
		# 处理12字段格式
		elif len(klines[0]) == 12:
			for v in klines:
				kline_data = {
					'timestamp': v[0],
					'open': 	py.float(v[1]),
					'high': 	py.float(v[2]),
					'low':  	py.float(v[3]),
					'close':	py.float(v[4]),
					'volume':	py.float(v[5]),
					'turnover': py.float(v[7]),
				}
				rds.append(kline_data)	
		elif py.len(klines[0])==7 and py.isdict(klines[0]) and 'turnover' in klines[0]:
			rds=klines
	elif py.istr(klines):
		return klines
	
		
	return json.dumps(rds,**json_dumps_ka)
to_json=convert_klines_to_json	
	
def binance_history_get_kline(symbol="BTCUSDT",timeframe="1m",start="2022-12-14",end="2022-12-24",return_json=False):
	'''
pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com binance-history
'''	
	tas=(symbol,timeframe,start,end)
	print(tas)
	klines = U.get(tas)
	if py.isno(klines):
		import binance_history
		klines = binance_history.fetch_klines(
			symbol=symbol,
			timeframe=timeframe,
			start=start,
			end=end,
		)
		U.set(tas,klines)	
	if return_json:
		return convert_klines_to_json(klines)
	else:
		return klines

def get_kline_1s(symbol,date='',return_json=False):
	'''
	# from datetime import date
	# start=date.fromisoformat("2022-02-14")#01 02 month
'''
	if symbol.startswith('?') and '=' in symbol:
		date=T.sub(symbol,'=','')
		symbol=T.sub(symbol,'?','=')
	start=U.parse_time(date).date()
	return get_kline(symbol=symbol,timeframe="1s",start=start.isoformat(),end=(start+U.time_delta(days=1)).isoformat(),return_json=return_json)

try:
	from binance.client import Client
except:
	Client=py.No
class QClient(Client):
	def __init__(self,*a,**ka):
		'''self, api_key: Optional[str] = None, 
		api_secret: Optional[str] = None,
		requests_params: Dict[str, str] = None,
		tld: str = 'com',
		testnet: bool = False
	):
	'''
		print(a,ka)
		super().__init__(*a,**ka)
		# return self #TypeError: __init__() should return None, not 'QClient'

	# def _init_session(self) -> requests.Session:

	# 	session=super()._init_session()
		
	# 	print(U.stime(),U.set('session',session))

	# 	return session

	def _request(self, method, uri: str, signed: bool, force_params: bool = False, **kwargs):
		'''
_request('get','https://api.binance.com/api/v3/ping',False,False,)
'''
		headers={'Accept': 'application/json, text/plain, */*',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'zh-CN',
 'Connection': 'keep-alive',
 'Cookie': 'cid=a3i3LEkf; '
		   'SERVERID=b6179fbc6d4f08aade16b460b14584fc|1672541045|1672540216',
 'Host': 'www.mokexapp.cz',
#  'Host': 'api.binance.com',
 'Sec-Fetch-Dest': 'empty',
 'Sec-Fetch-Mode': 'cors',
 'Sec-Fetch-Site': 'cross-site',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
			   '(KHTML, like Gecko) Binance/1.40.0 Chrome/89.0.4389.128 '
			   'Electron/12.0.7 Safari/537.36 (electron 1.40.0)',
 'bnc-currency': 'USD',
 'bnc-time-zone': 'Asia/Shanghai',
 'bnc-uuid': '03fe5662-a6b9-4334-a9c2-16acd14b0588',
 'clienttype': 'electron',
 'device-info': 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6Ijc2OCwxMzY2IiwiYXZhaWxhYmxlX3NjcmVlbl9yZXNvbHV0aW9uIjoiNzY4LDEzMDQiLCJzeXN0ZW1fdmVyc2lvbiI6IldpbmRvd3MgMTAiLCJicmFuZF9tb2RlbCI6InVua25vd24iLCJzeXN0ZW1fbGFuZyI6InpoLUNOIiwidGltZXpvbmUiOiJHTVQrOCIsInRpbWV6b25lT2Zmc2V0IjotNDgwLCJ1c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQmluYW5jZS8xLjI3LjAgQ2hyb21lLzg5LjAuNDM4OS4xMjggRWxlY3Ryb24vMTIuMC43IFNhZmFyaS81MzcuMzYgKGVsZWN0cm9uIDEuMjcuMCkiLCJsaXN0X3BsdWdpbiI6IkNocm9taXVtIFBERiBWaWV3ZXIsQ2hyb21pdW0gUERGIFZpZXdlciIsImNhbnZhc19jb2RlIjoiZWQ0OTFiZjEiLCJ3ZWJnbF92ZW5kb3IiOiJHb29nbGUgSW5jLiIsIndlYmdsX3JlbmRlcmVyIjoiQU5HTEUgKEludGVsKFIpIEhEIEdyYXBoaWNzIDU1MDAgRGlyZWN0M0QxMSB2c181XzAgcHNfNV8wKSIsImF1ZGlvIjoiMTI0LjA0MzQ3NTI3NTE2MDc0IiwicGxhdGZvcm0iOiJXaW4zMiIsIndlYl90aW1lem9uZSI6IkFzaWEvU2hhbmdoYWkiLCJkZXZpY2VfbmFtZSI6IkNocm9tZSBWODkuMC40Mzg5LjEyOCAoV2luZG93cykiLCJmaW5nZXJwcmludCI6IjkzYmUxZTVhZWFiYWY2MjY5NjdkZjNmNGE0OGE5ZGQ1IiwiZGV2aWNlX2lkIjoiIiwicmVsYXRlZF9kZXZpY2VfaWRzIjoiIiwibG9naW5faXAiOiIxOTIuMTY4LjguOCIsIm1hY19hZGRyZXNzIjoiMmM6YjI6MWE6ODI6ODE6ZGUiLCJhcHBfaW5zdGFsbF9kYXRlIjoxNjM3NjA4NDkxfQ==',
 'fvideo-id': '427d2f15cef9abeeb46629a93d2daa3213fa402c',
 'lang': 'zh-CN',
 'mclient-x-tag': 'pch5D9lsORjgObhyjdSK',
 'versionname': '1.40.0'}
		if uri.endswith('api/v3/ping'):
			headers['Host']='www.mokexapp.cz'


		print(U.v._request(method, uri, signed, force_params, **kwargs))
		uri=uri.replace('api.binance.com','www.mokexapp.cz')
		return super()._request(method, uri, signed, force_params,headers=headers, **kwargs)


def get_ws_key(key):
	headers={'Accept': 'application/json, text/plain, */*',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'zh-CN',
 'Connection': 'keep-alive',
 'Cookie': 'cid=a3i3LEkf; '
		   'SERVERID=b6179fbc6d4f08aade16b460b14584fc|1672541045|1672540216',
 'Host': 'www.mokexapp.cz',
 'Sec-Fetch-Dest': 'empty',
 'Sec-Fetch-Mode': 'cors',
 'Sec-Fetch-Site': 'cross-site',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
			   '(KHTML, like Gecko) Binance/1.40.0 Chrome/89.0.4389.128 '
			   'Electron/12.0.7 Safari/537.36 (electron 1.40.0)',
 'bnc-currency': 'USD',
 'bnc-time-zone': 'Asia/Shanghai',
 'bnc-uuid': '03fe5662-a6b9-4334-a9c2-16acd14b0588',
 'clienttype': 'electron',
 'device-info': 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6Ijc2OCwxMzY2IiwiYXZhaWxhYmxlX3NjcmVlbl9yZXNvbHV0aW9uIjoiNzY4LDEzMDQiLCJzeXN0ZW1fdmVyc2lvbiI6IldpbmRvd3MgMTAiLCJicmFuZF9tb2RlbCI6InVua25vd24iLCJzeXN0ZW1fbGFuZyI6InpoLUNOIiwidGltZXpvbmUiOiJHTVQrOCIsInRpbWV6b25lT2Zmc2V0IjotNDgwLCJ1c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQmluYW5jZS8xLjI3LjAgQ2hyb21lLzg5LjAuNDM4OS4xMjggRWxlY3Ryb24vMTIuMC43IFNhZmFyaS81MzcuMzYgKGVsZWN0cm9uIDEuMjcuMCkiLCJsaXN0X3BsdWdpbiI6IkNocm9taXVtIFBERiBWaWV3ZXIsQ2hyb21pdW0gUERGIFZpZXdlciIsImNhbnZhc19jb2RlIjoiZWQ0OTFiZjEiLCJ3ZWJnbF92ZW5kb3IiOiJHb29nbGUgSW5jLiIsIndlYmdsX3JlbmRlcmVyIjoiQU5HTEUgKEludGVsKFIpIEhEIEdyYXBoaWNzIDU1MDAgRGlyZWN0M0QxMSB2c181XzAgcHNfNV8wKSIsImF1ZGlvIjoiMTI0LjA0MzQ3NTI3NTE2MDc0IiwicGxhdGZvcm0iOiJXaW4zMiIsIndlYl90aW1lem9uZSI6IkFzaWEvU2hhbmdoYWkiLCJkZXZpY2VfbmFtZSI6IkNocm9tZSBWODkuMC40Mzg5LjEyOCAoV2luZG93cykiLCJmaW5nZXJwcmludCI6IjkzYmUxZTVhZWFiYWY2MjY5NjdkZjNmNGE0OGE5ZGQ1IiwiZGV2aWNlX2lkIjoiIiwicmVsYXRlZF9kZXZpY2VfaWRzIjoiIiwibG9naW5faXAiOiIxOTIuMTY4LjguOCIsIm1hY19hZGRyZXNzIjoiMmM6YjI6MWE6ODI6ODE6ZGUiLCJhcHBfaW5zdGFsbF9kYXRlIjoxNjM3NjA4NDkxfQ==',
 'fvideo-id': '427d2f15cef9abeeb46629a93d2daa3213fa402c',
 'lang': 'zh-CN',
 'mclient-x-tag': 'pch5D9lsORjgObhyjdSK',
 'versionname': '1.40.0',
 'X-MBX-APIKEY':key,
 }
	rp=requests.post('https://www.mokexapp.cz/api/v1/userDataStream', headers=headers)
	print(rp.text)
	return rp
	
def bybit_klines(symbol: str='MNTUSDT', interval: str='1', start: int =1738512000000, end: int = 1738598400000, limit: int = 1440,return_json=True,**ka):

	data=N.rpc_get(
	f"bybit.get_kline(symbol={symbol!r},interval={interval!r},start={start!r},end={end!r},limit={limit!r})",
	base='http://10.40.47.90:1133/', 
	proxy='socks5://192.168.1.20:41080',
	template='{base}import bybit;response.set_data(F.serialize({varname}))'
	)
	
	if return_json:
		return convert_klines_to_json(data)
	return data	
bybit_kline=bybit_klines	
	

def dogecoin_2013_2023(return_json=True):
	'''  https://datawrapper.dwcdn.net/S2SIY/33/dataset.csv  '''
	if U.isWin():
		csv_data=F.read_csv(r'C:\Users\qgb\Downloads\dataset.csv')
	if U.isLinux():
		csv_data=F.read_csv(r'/mnt/c/Users/qgb/Downloads/dataset.csv')


	from datetime import datetime
	import pytz  # 需要安装pytz库：pip install pytz
	formatted = []

	for entry in csv_data:
		# 拆分日期和价格
		date_str, price_str = entry.split('\t')
		price = float(price_str)
		
		# 解析日期（格式：dd/mm/yy）
		dt = datetime.strptime(date_str, '%d/%m/%y')
		dt = dt.replace(tzinfo=pytz.UTC)  # 设置为UTC时区
		
		# 生成时间戳（当天起始时间）
		open_time = int(dt.timestamp() * 1000)
		# 当天结束时间（23:59:59.999）
		close_time = open_time + 86399999  # 24*60*60*1000 -1
		
		# 构建数据条目
		formatted.append([
			open_time,          # 开盘时间戳
			price,              # open
			price,              # high
			price,              # low
			price,              # close
			0.0,                # volume
			close_time,         # 收盘时间戳
			0.0,                # quote_asset_volume
			0,                  # count
			0.0,                # taker_buy_volume
			0.0,                # taker_buy_quote_asset_volume
			'0'                 # ignore
		])

	if return_json:return convert_klines_to_json(formatted)
	return formatted

