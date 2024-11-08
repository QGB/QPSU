#coding=utf-8
import sys,pathlib               # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

def getClientOrderListUnion(print_result=True):
	'''
	'JLCGROUP_SESSIONID' 不提供返回 #{"success":false,"code":401,"message":"用户未登录或会话失效","data":null}
'''	
	import requests
	d = N.get_cookies_dict_from_browser('jlc.com','JLC_CUSTOMER_CODE','JLCGROUP_SESSIONID','XSRF-TOKEN')#XSRF-TOKEN 有时获取不到?
	assert len(d)==3

	headers = {
		'x-xsrf-token': d['XSRF-TOKEN'],
	}

	json_data = {
		'orderBeginTime': '2024-08-10',
		'orderEndTime': '',
		'orderStatus': '',
		'orderStatusForlist': '',
		'orderType': '',
		'pcbFileName': '',
		'produceOrderCode': '',
		'waitAffirm': False,
		'produceOrderAccessId': '',
		'searchSource': 6,
		'customerCode': d['JLC_CUSTOMER_CODE'],
		'orderStatusList': [],
		'pageNum': 1,
		'pageSize': 20,
		'whetherFollow': None,
	}

	response = requests.post(
		'https://www.jlc.com/api/newOrder/NewOrderList/v1/getClientOrderListUnion',
		cookies=d,
		headers=headers,
		json=json_data,
	)
	if print_result:print(response,response.text[:99])
	return response.json()