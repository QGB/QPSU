#coding=utf-8
import sys,pathlib			   # .py/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()
from qgb import Win

import websocket, json, time, requests
from logging import info as log_info
from urllib.parse import quote, urlsplit, urlunsplit
gport_default=9222
def remove_fragment(url):  # 删除URL中的片段标识
    parsed = urlsplit(url); return urlunsplit(parsed._replace(fragment=""))

def filter_target_cookies(cookies, target_names=['U_JWT_TOKEN', 'U_CSRF_TOKEN']):
    d={c['name']: c['value'] for c in cookies if c['name'] in target_names}  # 过滤目标cookies
    if len(d)!=len(target_names):
        log_info(f'filter_target_cookies 不匹配 {target_names} {d}')
        return False
    return d

def find_login_page(port):
    try:  # 查找登录页面
        response = requests.get(f"http://127.0.0.1:{port}/json/list", timeout=5)
        pages = response.json()
        for page in pages:
            if "passport.ucloud.cn/login" in page.get('url', ''): 
                return page['webSocketDebuggerUrl']  # 返回登录页面的WebSocket URL
        return None
    except Exception: return None

def refresh_page(ws_url):
    try:  # 刷新页面
        ws = websocket.create_connection(ws_url, timeout=10, suppress_origin=True)
        refresh_cmd = {"id": 3, "method": "Page.reload", "params": {"ignoreCache": True}}
        ws.send(json.dumps(refresh_cmd)); time.sleep(0.5); ws.close()
        return True
    except: return False

def click_login_button(ws_url):  # 尝试点击登录按钮
    try:
        ws = websocket.create_connection(ws_url, timeout=10, suppress_origin=True)
        click_cmd = {
            "id": 2, "method": "Runtime.evaluate", "params": {
                "expression": """
                    var btn = document.querySelector('button#login.uc-fe-button');
                    if(btn) { btn.click(); '点击成功'; } else '找不到按钮';
                """, "userGesture": True, "awaitPromise": True
            }
        }
        ws.send(json.dumps(click_cmd)); result = json.loads(ws.recv())
        click_ok = '点击成功' in result.get('result', {}).get('result', {}).get('value', '')
        ws.close(); return click_ok
    except: return False

def open_url_in_browser(port, url):  # 打开URL
    try:
        response = requests.put(f"http://127.0.0.1:{port}/json/new?{quote(url, safe=':/?&=#')}", timeout=5)
        return response.status_code == 200
    except: return False

def get_page_cookies(ws_url='',port=gport_default):  # 获取页面cookies
    try:
        if not ws_url:
            page=requests.get(f"http://127.0.0.1:{port}/json/list", timeout=5).json()[0]
            ws_url=page.get('webSocketDebuggerUrl', '')
        ws = websocket.create_connection(ws_url, timeout=10, suppress_origin=True)
        ws.send(json.dumps({"id":1,"method":"Network.getAllCookies","params":{}}))
        result = json.loads(ws.recv()); ws.close()
        return result.get('result', {}).get('cookies', [])
    except Exception as e:
        U.print_traceback_in_except(ws_url,e)
        # log_info(e)
        return []

def get_console_ucloud_page(port, target_url):  # 获取控制台页面
    try:
        pages = requests.get(f"http://127.0.0.1:{port}/json/list", timeout=5).json()
        for page in pages:
            if "console.ucloud.cn" in page.get('url', ''): 
                return page['webSocketDebuggerUrl']  # 返回控制台页面的WebSocket URL
        return None
    except: return None

def delete_cookies(*names,domain='.ucloud.cn', ws_url='', port=gport_default):
    """批量删除指定名称的 Cookies（单次WebSocket连接）"""
    try:
        if not ws_url:
            page = requests.get(f"http://127.0.0.1:{port}/json/list", timeout=5).json()[0]
            ws_url = page.get('webSocketDebuggerUrl', '')
        ws = websocket.create_connection(ws_url, timeout=10, suppress_origin=True)
        try:  # 注释：确保连接关闭
            results = []
            for i, name in enumerate(names, 1):
                params = {"name": name, "domain": domain}
                ws.send(json.dumps({"id":i,"method":"Network.deleteCookies","params":params}))
                response = json.loads(ws.recv())
                success = response.get('result', {}).get('success', False)
                results.append(success)
                log_info(f"delete_cookies name={name} {params} {response}")
            return all(results)
        finally:
            ws.close()  # 注释：无论如何都关闭连接
    except Exception as e:
        U.print_traceback_in_except(ws_url, e)
        return False  # 注释：任何异常都返回False
#### 	cookies end ####





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
    # if result['payload']['exp']<U.itime_sec():1/0
    return result  # 返回解析结果
def ucloud_update_firewall(rules, jwt_token,csrf_token,fw_id="firewall-len=8",project_id="org-len=6", region="hk",**ka):  # 更新防火墙函数
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
    print(f"\n正在发送防火墙更新请求... {rules[:2]}")
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
    
def main(port=gport_default,file_json=r"D:\Documents\Downloads\ucloud  175 Firewall-Rule-Template-json.json",ip_url=''):	
    # 主程序  # [ {'策略': '接受', '协议及端口': 'TCP:443', '源地址': '0.0.0.0/0', '优先级': '高', '备注': '-'} ,]
    # ip = N.get_pub_ip_str()
    
    with open(file_json, 'r', encoding='utf-8') as f:
        json_data = json.load(f)  # 读取整个JSON数据
        data = json_data['data']  # 获取规则数据部分
    ka=T.unrepr(json_data['ka'])
    if not ip_url:ip_url=ka.pop('ip_url')
    # if not ip:
    ip=N.get_pub_ip_str(methods=[ip_url,])
    assert ip
    log_info(f"\n>>>> 步骤0: 读取 {file_json}...  当前IP：{ip}")
    ip_s3_24=T.sub_last(ip,'','.')+'.0/24'
    ip_in_data=[d for d in data if d['源地址'] in (ip,ip_s3_24)]
    assert not ip_in_data ,f'{ip_in_data} \t ip {ip} 已经存在 '  
    comment=Win.get_wifi_name()+ '  ' +U.stime()
    data.insert(0, {'策略': '接受', '协议及端口': 'ICMP', '源地址': ip, '优先级': '高', '备注':comment})
    data.insert(0, {'策略': '接受', '协议及端口': 'TCP:22', '源地址': ip, '优先级': '高', '备注':comment})
  
    #cookies start
    target_url='https://console.ucloud.cn/unet/ufirewall/'+ka['fw_id']
    login_url = f"https://passport.ucloud.cn/login?service={quote(target_url)}#login"
    log_info(f"\n>>>> 步骤1: 开始获取UCloud Cookies... {target_url}  当前IP：{repr(ip)} ")
    console_ws = get_console_ucloud_page(port,target_url)
    for iretry in range(3):
        target_cookies = filter_target_cookies(get_page_cookies(console_ws)) if console_ws else {}
        if not target_cookies:  # 未获取到cookies时执行登录流程
            log_info("未获取到目标Cookies，尝试登录流程")
            login_ws = find_login_page(port)
            if login_ws:  # 如果已有登录页面则刷新
                log_info("刷新已有登录页面"); refresh_page(login_ws); time.sleep(3)
            else:  # 没有则打开新页面
                open_url_in_browser(port, remove_fragment(login_url))
                time.sleep(3); login_ws = find_login_page(port)
            
            if login_ws:
                time.sleep(2)  # 等待页面加载
                if not click_login_button(login_ws):  # 尝试点击登录按钮
                    log_info("点击登录按钮失败，等待用户操作..."); time.sleep(10)
                time.sleep(5); console_ws = get_console_ucloud_page(port,target_url) # 登录后再次尝试获取cookies
                target_cookies = filter_target_cookies(get_page_cookies(console_ws)) if console_ws else {}
            break	
        if target_cookies:  # 输出结果
            log_info(f"成功获取目标Cookies: {', '.join(target_cookies.keys())}")
            jwt_info = decode_jwt(target_cookies['U_JWT_TOKEN'])
            if jwt_info['payload']['exp']<U.itime_sec():
                delete_cookies('U_JWT_TOKEN','U_CSRF_TOKEN',ws_url=console_ws)
                continue
            for name, value in target_cookies.items(): log_info(f"- {name}: {value[:30]}...")
            break
    else:
        log_info("最终未能获取目标Cookies")
        1/0
    #cookies end
    
    ru=ucloud_update_firewall(rules=data,jwt_token=target_cookies['U_JWT_TOKEN'],csrf_token=target_cookies['U_CSRF_TOKEN'],**ka)  # 执行防火墙更新
    if ru:
        json_data['data']=data
        json_str = json.dumps(json_data, ensure_ascii=False, separators=(',', ':'))
        json_str = json_str.replace('{"策略":', '\n{"策略":')  # 在每条规则前添加换行
        json_str = json_str.replace('"data":[', '\n"data":[\n').replace('}]}', '\n]}')
        # U.set('j',json_str)
        end_str='''"TCP:443","源地址":"0.0.0.0/0","优先级":"高","备注":"-"\n'''
        assert end_str in json_str
        json_str = json_str.replace(end_str,					 
                                    end_str[:-1]+'}\n') # fix
        with open(file_json, 'w', encoding='utf-8') as f:	# 将修改后的数据写回文件
            f.write(json_str)
            log_info(f'{f} 已经写回文件')