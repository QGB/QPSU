#coding=utf-8
import requests,os,sys,pathlib   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()


from binance.client import Client

class QClient(Client):
	def __init__(self,*a,**ka):
		'''self, api_key: Optional[str] = None, 
		api_secret: Optional[str] = None,
        requests_params: Dict[str, str] = None,
		tld: str = 'com',
        testnet: bool = False
    ):
	'''
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
		
		print(U.v._request(method, uri, signed, force_params, **kwargs))
		uri=uri.replace('api.binance.com','www.mokexapp.cz')
		return super()._request(method, uri, signed, force_params,headers=headers, **kwargs)
