#coding=utf-8
import requests,os,sys,pathlib   # .py/qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import requests
cookies = U.get_or_dill_load_and_set('dcookies_jlc')

headers = {
    'authority': 'lceda.cn',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ru;q=0.5,ja;q=0.4,zh-TW;q=0.3,it;q=0.2,de;q=0.1',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # Requests sorts cookies= alphabetically
    'origin': 'https://lceda.cn',
    'referer': 'https://lceda.cn/editor',
    'sec-ch-ua': U.stime(),
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': U.stime(),
    'x-requested-with': 'XMLHttpRequest',
}

def get_all_components():
	return requests.get('https://lceda.cn/api/components?version=6.5.23&docType=4&uid=f87c808f549443acbac8e59cc590cbc3&type=3&tag%5B%5D=All').json()

def delete_component(uuid):
	data = {
		'uuid': uuid,#'f90fe65a90d94ea4a573b0fb60a43ca5',
		'version': '6.5.23',
	}
	rp=response = requests.post(f'https://lceda.cn/api/components/{uuid}/delete', cookies=cookies, headers=headers, data=data)
	return rp,rp.json()