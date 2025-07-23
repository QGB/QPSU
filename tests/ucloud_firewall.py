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
# 主程序  # [ {'策略': '接受', '协议及端口': 'TCP:443', '源地址': '0.0.0.0/0', '优先级': '高', '备注': '-'} ,]
with open(r"D:\Documents\Downloads\ucloud  175 Firewall-Rule-Template-json.json", encoding='utf-8') as f: 
    data = json.load(f)['data']  # 读取规则数据
jwt_token = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTMyMzMzNDEsImp0aSI6IkRKYWR3WVdRR1dXRWgzd1hJVkpXdDEiLCJpYXQiOjE3NTMxOTAxNDEsInN1YiI6InVjczppYW06OjY2NTY4NjIyOnVzZXIvMTUxMzI1NTY3Iiwicm9vdCI6dHJ1ZSwic2QiOnt9fQ.cUuQZVvqL63xOj42ueLDRvHbqggN9XcgKDuQPF_Cw7JQajHWu8TLxKdJMJ5ScknvFd7v97DXKn0-sj1aceKu-w"  # JWT令牌
ucloud_update_firewall(rules=data,jwt_token=jwt_token,csrf_token="64be75b61eccf3c0f171eef241c61f2b")  # 执行防火墙更新
