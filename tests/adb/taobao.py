def taobao_open_link(h5Url, action="ali.open.nav", module="tmm", source="outside", adb_path="adb"):
    import subprocess
    from urllib.parse import quote
    encoded_h5Url = quote(h5Url, safe="")  # 保持变量名与参数名一致
    
    # 严格保持参数顺序和拼接方式
    tbopen_uri = (
        "tbopen://m.taobao.com/tbopen/index.html?"
        f"action={action}&"  # 使用传入的action参数
        f"module={module}&"
        f"source={source}&"
        f"h5Url={encoded_h5Url}"  # 修正变量名拼写错误
    )
    
    # 严格保留原始命令结构，仅替换adb_path变量
    cmd = (
        f'"{adb_path}" shell "am start -a android.intent.action.VIEW '  # 使用传入的adb_path
        f"-d '{tbopen_uri}' "
        '-p com.taobao.taobao"'
    )
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        # 保持原始返回逻辑
        return (True, "Success") if result.returncode == 0 else (False, result.stderr)
    except Exception as e:
        return (False, str(e))
open=open_link=taobao_open=taobao_open_link