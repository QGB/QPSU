#coding=utf-8
import sys,pathlib               # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()
from qgb.tests import taobao_trade as tb

gd=F.dill_load('C:/test/vivo_login.dill')
import asyncio

async def login():

	# ph=await tb.get_page(url='https://yun.vivo.com.cn/#/home')
	# if ph:await ph.reload()
	
	# pyw=await tb.get_page(url='https://yun.vivo.com.cn/#/welcome')
	# if pyw:await pyw.click("#background > div > div > div.text-content > div.button > button")

	# print(U.stime(),'wait login page 2. ph,pyw',[ph,pyw])
	# await asyncio.sleep(1)
	
	page=await tb.get_or_new_page(url='https://passport.vivo.com.cn/#/login')
	# print('page',page)
	try:
		t=await page.evaluate('() => document.title')
		if t=='身份验证':await page.reload()
		
		# await page.click('div.login > div > div.layout > div.inner-box > div.toggle-module > span:nth-child(2)')
		# await tb.press_keys(page,gd['p'],selector='div.inner-box > div:nth-child(3) > div:nth-child(2) > div:nth-child(1) > div.phone-box > input')

		# await tb.press_keys(page,gd['pw'],selector='div.pwd-box > input[type=password]')
		# await page.click("div.login > div > div.layout > div.inner-box > div.os-pc-btn")
		es=await page.xpath('//span[contains(text(), "密码登录")]')
		assert len(es)==1
		await es[0].click()
		# print('t',U.stime(),t,gd)
		await tb.press_keys(page, gd['p'], selector='input[placeholder="请输入手机号/邮箱/vivo号"]')
		await tb.press_keys(page, gd['pw'], selector='input[placeholder*="密码"]')		
		btn=await page.xpath('//div[contains(text(), "登录") and contains(@class, "btn")]')
		btn=btn[0]
		await btn.click()
		
		print(U.stime(),'wait after click login 2',page)
		await asyncio.sleep(2)
	except Exception as e:
		print(U.stime(),e)
		return page

	
	dr=await get_cookies()
	return send(dr,1)

	
async def get_cookies():
	'''
属性	Cookie 1 (国际版)	Cookie 2 (中国版)	差异说明
name	vivo_account_cookie_iqoo_checksum	vivo_account_cookie_iqoo_checksum	名称相同
value	c41e260cbc009c45a2b6aab12fce060d.1745127814090	388a0d60eed3e82129d6cf7bd3b18331.1745663888355	校验值和时间戳不同，可能对应不同账号/会话
domain	.vivo.com	.vivo.com.cn	国际版 vs 中国版域名，反映区域部署差异	
	'''
	cy=['JSESSIONID','vivo_account_cookie_iqoo_deviceid','account','vivo_account_cookie_iqoo_checksum','vivo_account_cookie_iqoo_openid','vivo_account_cookie_iqoo_authtoken','vivo_account_cookie_iqoo_vivotoken','vivo_account_cookie_iqoo_regioncode','pwd','clientId','log_r_flow_no','log_r_reuslt','vivo_account_cookie_cloud_checksum','vivo_account_cookie_cloud_openid','vivo_yun_csrftoken']
	# ph=await tb.get_or_new_page(url='https://yun.vivo.com.cn/#/home')
	# ph=await tb.get_or_new_page(url='https://pc.vivo.com.cn/suite?origin=cloudWeb#/cloudService')
	# ph=await tb.get_or_new_page(url='https://find.vivo.com.cn/')
	ph=await tb.get_or_new_page(url='https://find.vivo.com.cn/findphone/bound')
	cs=await tb.get_all_cookies(ph)
	vcs=[d for d in cs if 'vivo.com.cn' in d['domain']]
	dr={}
	# for k,v in dc.items():
	for k in cy:
		i=[d for d in vcs if d['name']==k]
		if len(i)<1:
			ia=[d for d in cs if d['name']==k]
			print(k,i,ia)
			break
		dr[k]=i[0]['value']
	print(U.len(cy,dr))
	if len(cy)!=len(dr):
		return py.No(len(cy),len(dr),dr)
	return dr
	
def send(cookies,cmdType=2):
	''' cmdType: 1,return location,  2 sound  , 4和 8 都是锁定，必须要云账号密码解锁
	
vivo.send(dr,8)
'{"code":0,"msg":"操作成功","data":{"cmdId":1451147966,"serverTime":1717471878200}}'
	
vivo.send(dr,3)           ###<py.No|'{"code":403,"data":{"needSliderVerification":false,"supportIdentityVerificationType":0,"sequenceNo":"CLOUD20240604230212130","needIdentityVerification":true},"msg":"未进行身份校验"}'  2024-06-04__23.02.11__>
	

vivo.send(dr,0) ###<py.No|'{"code":400,"msg":"请求参数错误","data":{}}'  2024-06-04__23.05.52__>

vivo.send(dr,-1)###<py.No|'{"code":500,"msg":"操作失败","data":{}}'  2024-06-04__23.05.57__>

dv=U.dict_get_multi_keys_return_dict(dr,'vivo_account_cookie_cloud_checksum','vivo_account_cookie_cloud_openid',);vivo.send(dv,1)#loc
	'''
	gd['data']['cmdType']=str(cmdType)
	
	headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ru;q=0.5,ja;q=0.4,zh-TW;q=0.3,it;q=0.2,de;q=0.1',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',

    'Origin': 'https://find.vivo.com.cn',
    'Referer': 'https://find.vivo.com.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-yun-csrftoken': '94b7c5cb-9c1f-486d-81ad-ceffb7a46690.1716452535233',
}
	t=N.HTTP.post('https://webcloud.vivo.com.cn/findphone/operate', cookies=cookies, headers=headers, data=gd['data'],proxy='',return_text=1)
	if "操作成功" in t:
		return t
	return py.No(t)	
	