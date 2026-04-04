def parse_jk_log(content):
    '''
    终极版：解析无换行符的JK BMS日志（bytes/str通用）
    核心：按时间戳正则拆分单行日志为多行
    '''
    import pandas as pd
    import re
    # 1. 统一转为字符串 + 清理空白字符
    if isinstance(content, bytes):
        content = content.decode('utf-8').strip()
    else:
        content = content.strip()
    
    # 2. 关键：用正则拆分单行日志为多行（匹配时间戳开头的行）
    # 正则匹配：YYYY-MM-DD HH:MM:SS 格式的时间戳
    time_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
    # 拆分后重组每行（保留时间戳+后续内容）
    parts = re.split(time_pattern, content)
    # 过滤空值 + 重组为 ["时间戳 内容", "时间戳 内容"...]
    log_lines = []
    for i in range(1, len(parts), 2):
        if i+1 < len(parts):
            line = parts[i] + parts[i+1]
            if line.strip():
                log_lines.append(line.strip())
    
    if not log_lines:
        return pd.DataFrame()  # 无有效日志
    
    # 3. 提取表头（第一行的列名部分）
    # 表头行是日志第一行的列名（你日志里的表头是固定的）
    header_str = 'RTC时间戳,系统日志,充电管状态,放电管状态,均衡状态,加热状态,最高单体编号,最低单体编号,最高单体电压,最低单体电压,电池电压,电池电流,剩余容量,实际容量,最高温度,最低温度,功率温度,加热电流'
    headers = [h.strip() for h in header_str.split(',')]
    
    # 4. 解析所有数据行（按逗号+空格拆分）
    data_lines = []
    sep_pattern = r'\s*[,，]\s*'  # 匹配逗号/中文逗号+任意空格
    for line in log_lines:
        # 拆分每行数据（保证列数和表头一致）
        row = re.split(sep_pattern, line)
        row = row[:len(headers)] + ['']*(len(headers)-len(row))
        data_lines.append(row)
    
    # 5. 构建DataFrame
    df = pd.DataFrame(data_lines, columns=headers)
    if df.empty:
        return df
    
    # 6. 智能转换数值列（只转换存在的列）
    numeric_cols = []
    for col in df.columns:
        try:
            pd.to_numeric(df[col], errors='raise')
            numeric_cols.append(col)
        except (ValueError, TypeError):
            continue
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 7. 解析时间戳
    if 'RTC时间戳' in df.columns:
        df['RTC时间戳'] = pd.to_datetime(df['RTC时间戳'], errors='coerce')
        df = df.sort_values('RTC时间戳').reset_index(drop=True)
    
    return df
parse=log=parse_log=parse_jk_log