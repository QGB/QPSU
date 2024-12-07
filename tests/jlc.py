#coding=utf-8
import sys,pathlib               # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()
import requests

def get_d3(d3,**ka):
	if d3:pass
	else:
		d3 = N.get_cookies_dict_from_browser('.jlc.com','JLC_CUSTOMER_CODE','JLCGROUP_SESSIONID','XSRF-TOKEN',**ka)#XSRF-TOKEN 有时获取不到?
	if len(d3)!=3:print(d3)
	assert len(d3)==3
	return d3
	
def getClientOrderListUnion(past_days=90,print_result=True,d3=None,**ka):
	'''
	'JLCGROUP_SESSIONID' 不提供返回 #{"success":false,"code":401,"message":"用户未登录或会话失效","data":null}
'''	
	d3=get_d3(d3,**ka)

	headers = {
		'x-xsrf-token': d3['XSRF-TOKEN'],
	}

	json_data = {
		'orderBeginTime': U.stime(U.get_time_obj()-U.time_delta(days=past_days))[:10],
		'orderEndTime': '',
		'orderStatus': '',
		'orderStatusForlist': '',
		'orderType': '',
		'pcbFileName': '',
		'produceOrderCode': '',
		'waitAffirm': False,
		'produceOrderAccessId': '',
		'searchSource': 6,
		'customerCode': d3['JLC_CUSTOMER_CODE'],
		'orderStatusList': [],
		'pageNum': 1,
		'pageSize': 20,
		'whetherFollow': None,
	}

	response = requests.post(
		'https://www.jlc.com/api/newOrder/NewOrderList/v1/getClientOrderListUnion',
		cookies=d3,
		headers=headers,
		json=json_data,
	)
	if print_result:print(response,response.text[:99])
	return response.json()

def selectExpressSchedule(index=0,jo=None,d3=None,print_result=True,**ka):
	jo=U.get_duplicated_kargs(ka,'jo','getClientOrderListUnion_json','getClientOrderListUnion','order_list','json','j',default=jo)
	d3=get_d3(d3,**ka)
	if not jo:
		jo=getClientOrderListUnion(d3=d3,print_result=print_result)
	
	data = {
		'customerCode': d3['JLC_CUSTOMER_CODE'],
		'customerOrderAccessId': jo['body']['clientOrderList'][index]['customerOrderAccessId'],
		'produceOrderAccessId':jo['body']['clientOrderList'][index]['produceOrderAccessId'],
	}

	response = requests.post(
		'https://www.jlc.com/api/newOrder/NewOrderList/v1/selectExpressSchedule',
		cookies=d3,
		headers={'x-xsrf-token': d3['XSRF-TOKEN'],} ,
		data=data,
	)
	if print_result:print(response,response.text[:99])
	return response.json()
get_express=selectExpressSchedule	
	
def selectWipProcess(index=0,jo=None,d3=None,print_result=True,**ka):
	jo=U.get_duplicated_kargs(ka,'jo','getClientOrderListUnion_json','getClientOrderListUnion','order_list','json','j',default=jo)
	d3=get_d3(d3,**ka)
	if not jo:
		jo=getClientOrderListUnion(d3=d3,print_result=print_result)
	
	data = {
		'customerCode': d3['JLC_CUSTOMER_CODE'],
		'customerOrderAccessId': jo['body']['clientOrderList'][index]['customerOrderAccessId'],
		'produceOrderAccessId':jo['body']['clientOrderList'][index]['produceOrderAccessId'],
"orderType":1, #没有orderType同样返回{"success":false,"code":500,"message":"系统发生未知错误，请稍后重试","data":null}
	}

	response = requests.post(
		'https://www.jlc.com/api/newOrder/NewOrderList/v1/selectWipProcess',
		cookies=d3,
		headers={'x-xsrf-token': d3['XSRF-TOKEN'],} ,
json=data,#如果用data= {"success":false,"code":500,"message":"系统发生未知错误，请稍后重试","data":null}
	)
	
	if print_result:
		print(U.v.requests.post(
		'https://www.jlc.com/api/newOrder/NewOrderList/v1/selectWipProcess',
		cookies=d3,
		headers={'x-xsrf-token': d3['XSRF-TOKEN'],} ,
json=data,
	))
		print(response,response.text[:99])
	return response.json()
get_factor_process=selectWipProcess

	
	