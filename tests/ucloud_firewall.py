#coding=utf-8
import sys,pathlib			   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

from logging import info as log_info
import websocket, json, time, requests
def get_ucloud_websocket_url(port=9222):
	"""获取UCloud页面的WebSocket调试URL"""
	try:
		url = f"http://127.0.0.1:{port}/json/list"
		response = requests.get(url, timeout=5)
		for page in response.json():
			if "ucloud.cn" in page['url'][:30]: # 不要改
				log_info(f"找到UCloud页面: {page['url']}")
				return page['webSocketDebuggerUrl']
		log_info("未找到UCloud页面"); return None
	except Exception as e:
		log_info(f"获取页面信息失败: {e}"); import traceback; traceback.print_exc(); return None

def get_all_cookies(ws_url):
	"""通过WebSocket获取所有cookies"""
	ws = None
	try:
		log_info(f"连接到WebSocket端点: {ws_url}")
		ws = websocket.create_connection(ws_url, timeout=10, suppress_origin=True)
		log_info("连接成功建立"); command = {"id":1,"method":"Network.getAllCookies","params":{}}
		print("发送命令:", json.dumps(command)); ws.send(json.dumps(command))
		log_info("等待响应..."); time.sleep(2); result = ws.recv()
		log_info("收到响应:"); log_info(result[:500])  # 只打印前500个字符
		result_data = json.loads(result); return result_data.get('result', {}).get('cookies', [])
	except json.JSONDecodeError: log_info("响应不是有效的JSON"); return []
	except Exception as e: log_info(f"WebSocket操作失败: {e}"); import traceback; traceback.print_exc(); return []
	finally: 
		if ws and ws.connected: ws.close()

def filter_target_cookies(cookies, target_names=['U_JWT_TOKEN', 'U_CSRF_TOKEN']):
	"""过滤目标cookies"""
	return {c['name']: c['value'] for c in cookies if c['name'] in target_names}

	







import json, requests, base64
from urllib.parse import quote
from datetime import datetime, timezone
def decode_jwt(jwt_token):  # 解析JWT令牌信息
	parts = jwt_token.split('.')  # 分割令牌为三部分
	if len(parts) != 3: return {"error": "❌ 无效的 JWT 格式，应包含三部分"}  # 格式检查
	header_encoded, payload_encoded, signature = parts  # 解构各部分
	result = {}
	try:  # 解析头部
		header_encoded += '=' * (4 - len(header_encoded) % 4)  # Base64填充
		header_decoded = base64.urlsafe_b64decode(header_encoded).decode('utf-8')  # 解码头部
		result["header"] = json.loads(header_decoded)  # 加载JSON头部
	except Exception as e: result["header_error"] = f"❌ 头部解码失败: {e}"  # 错误处理
	try:  # 解析有效载荷
		payload_encoded += '=' * (4 - len(payload_encoded) % 4)  # Base64填充
		payload_decoded = base64.urlsafe_b64decode(payload_encoded).decode('utf-8')  # 解码有效载荷
		result["payload"] = json.loads(payload_decoded)  # 加载JSON有效载荷
		if "iat" in result["payload"]:  # 处理签发时间
			result["payload"]["iat_formatted"] = datetime.fromtimestamp(
				result["payload"]["iat"], tz=timezone.utc
			).strftime('%Y-%m-%d %H:%M:%S UTC')  # 格式化时间
		if "exp" in result["payload"]:  # 处理过期时间
			result["payload"]["exp_formatted"] = datetime.fromtimestamp(
				result["payload"]["exp"], tz=timezone.utc
			).strftime('%Y-%m-%d %H:%M:%S UTC')  # 格式化时间
			if "iat" in result["payload"]:  # 计算有效期
				remaining = result["payload"]["exp"] - result["payload"]["iat"]  # 剩余秒数
				days = remaining // (24 * 3600)  # 计算天数
				hours = (remaining % (24 * 3600)) // 3600  # 计算小时
				minutes = (remaining % 3600) // 60  # 计算分钟
				result["payload"]["validity"] = f"{days}天 {hours}小时 {minutes}分钟"  # 有效期字符串
	except Exception as e: result["payload_error"] = f"❌ 有效载荷解码失败: {e}"  # 错误处理
	result["signature"] = {"length": len(signature), "digest": f"{signature[:20]}..."}  # 签名信息
	return result  # 返回解析结果
def ucloud_update_firewall(rules, jwt_token,csrf_token,fw_id="firewall-ai30lbps",project_id="org-lezenq", region="hk"):  # 更新防火墙函数
	jwt_info = decode_jwt(jwt_token)  # 解析JWT令牌
	print("JWT 令牌解析结果:", jwt_info)  # 打印解析结果
	print(f"  签发时间: {jwt_info.get('payload', {}).get('iat_formatted', '未知')}")
	print(f"  过期时间: {jwt_info.get('payload', {}).get('exp_formatted', '未知')}")
	print(f"  有效期: {jwt_info.get('payload', {}).get('validity', '未知')}")
	print(f"  sub: {jwt_info.get('payload', {}).get('sub', '未知')}")
	url = "https://api.ucloud.cn/?Action=UpdateFirewall"  # API地址
	cookies = {"U_JWT_TOKEN": jwt_token}  # 设置Cookie
	headers = {  # 请求头配置
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",  # 内容类型
		"U-CSRF-Token": csrf_token,  # CSRF令牌
	}
	rule_data = []  # 存储规则数据
	for i, rule in enumerate(rules):  # 处理每条规则
		protocol_port = rule["协议及端口"]  # 获取协议端口
		if ":" in protocol_port: protocol, port = protocol_port.split(":")  # 分割协议端口
		else: protocol, port = protocol_port, ""  # ICMP协议处理
		action = "ACCEPT" if rule["策略"] == "接受" else "DROP"  # 策略转换
		priority = "HIGH" if rule["优先级"] == "高" else "MEDIUM" if rule["优先级"] == "中" else "LOW"  # 优先级转换
		ip, comment = rule["源地址"], rule["备注"]  # 获取IP和备注
		rule_str = f"{protocol}|{port}|{ip}|{action}|{priority}|{comment}"  # 构建规则字符串
		rule_data.append(f"Rule.{i}={quote(rule_str, safe='')}")  # URL编码并添加
	timestamp = int(datetime.now().timestamp() * 1000)  # 当前时间戳（毫秒）
	base_params = [  # 基础参数
		f"ProjectId={project_id}",  # 项目ID
		f"Region={region}",  # 区域参数  {"Message":"Missing params [az_group]","RetCode":220}
		f"FWId={fw_id}",  # 防火墙ID {"Message":"Missing params [FWId|GrouppId]","RetCode":220}
		"Action=UpdateFirewall",  # 操作名称 
		f"_timestamp={timestamp}",  # 时间戳
	]
	payload = "&".join(base_params + rule_data)  # 合并所有参数
	print("\n正在发送防火墙更新请求...")
	try:  # 发送请求
		response = requests.post(url, headers=headers, cookies=cookies, data=payload, timeout=30)  # POST请求
		print(f"状态码: {response.status_code}\n响应内容: {response.text}")  # 打印响应
		if response.status_code == 200:  # 处理成功响应
			try:
				json_response = response.json()  # 解析JSON响应
				if json_response.get("RetCode") == 0: print("✅ 防火墙规则更新成功！"); return True  # 成功处理
				else: print(f"❌ 更新失败: {json_response.get('Message', '未知错误')}")  # 失败处理
			except: print("⚠️ 接收到非JSON格式响应，请检查请求参数")  # 解析异常
		else: print(f"❌ 请求失败，状态码: {response.status_code}")  # HTTP错误
	except Exception as e: print(f"❌ 请求过程中发生错误: {e}")  # 请求异常
	return False  # 返回失败
	
def main():	
	# 主程序  # [ {'策略': '接受', '协议及端口': 'TCP:443', '源地址': '0.0.0.0/0', '优先级': '高', '备注': '-'} ,]
	file_json = r"D:\Documents\Downloads\ucloud  175 Firewall-Rule-Template-json.json"
	log_info(f"\n>>>> 步骤0: 读取 {file_json}...")
	with open(file_json, 'r', encoding='utf-8') as f:
		json_data = json.load(f)  # 读取整个JSON数据
		data = json_data['data']  # 获取规则数据部分
	ip = N.get_pub_ip_str()
	assert ip
	ip_in_data=[d for d in data if d['源地址'] == ip]
	assert not ip_in_data ,f'{ip_in_data} \t ip {ip} 已经存在 '
	data.insert(0, {'策略': '接受', '协议及端口': 'ICMP', '源地址': ip, '优先级': '高', '备注': U.stime()})
	data.insert(0, {'策略': '接受', '协议及端口': 'TCP:22', '源地址': ip, '优先级': '高', '备注': U.stime()})

	
	log_info("\n>>>> 步骤1: 查找UCloud页面WebSocket端点...")
	ws_url = get_ucloud_websocket_url(9222) or 1/0
	log_info(f"页面的WebSocket调试URL: {ws_url}")

	log_info("\n>>>> 步骤2: 通过WebSocket获取cookies...")
	if not (all_cookies := get_all_cookies(ws_url)): log_info("未获取到任何cookies"); 1/0
	log_info(f"获取到 {len(all_cookies)} 个cookies")

	log_info("\n>>>> 步骤3: 过滤目标cookies...")
	if target_cookies := filter_target_cookies(all_cookies):
		log_info("\n成功获取目标cookies:")
		for name, value in target_cookies.items():print(f"{name}: {value}")
	else:
		log_info("\n未获取到目标cookies")
		print("所有cookies名称:", [c['name'] for c in all_cookies])

	
	ru=ucloud_update_firewall(rules=data,jwt_token=target_cookies['U_JWT_TOKEN'],csrf_token=target_cookies['U_CSRF_TOKEN'])  # 执行防火墙更新
	if ru:
		json_str = json.dumps({'data': data}, ensure_ascii=False, separators=(',', ':'))
		json_str = json_str.replace('{"策略":', '\n{"策略":')  # 在每条规则前添加换行
		json_str = json_str.replace('{"data":[', '{"data": [\n').replace('}]}', '\n]}')
		with open(file_json, 'w', encoding='utf-8') as f:	# 将修改后的数据写回文件
			f.write(json_str)