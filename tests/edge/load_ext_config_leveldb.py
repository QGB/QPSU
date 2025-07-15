import os,struct,binascii,re,json

def parse_log_file(file_path): # 解析 LevelDB 的 .log 文件
    results = {}
    with open(file_path, 'rb') as f:
        block_offset = 0
        while True:
            header = f.read(7) # 读取记录头 (7字节)
            if not header or len(header) < 7: break
            crc = struct.unpack('<I', header[:4])[0] # 解析记录头 (CRC32 + 长度 + 类型)
            length = struct.unpack('<H', header[4:6])[0]
            record_type = header[6]
            payload = f.read(length) # 读取有效载荷
            if len(payload) < length: break
            type_map = {1: "FULL", 2: "FIRST", 3: "MIDDLE", 4: "LAST"} # 解析记录类型
            try: # 解码字符串数据（尝试UTF-8解码，失败则忽略错误）
                decoded = payload.decode('utf-8', errors='ignore')
            except:
                decoded = binascii.hexlify(payload).decode('ascii')
            results.setdefault(type_map.get(record_type, "UNKNOWN"), []).append({ # 保存记录
                "crc32": f"0x{crc:08X}",
                "length": length,
                "payload": decoded
            })
            block_offset += 7 + length
    return results

def parse_manifest(file_path): # 解析 MANIFEST 文件
    with open(file_path, 'rb') as f:
        data = f.read()
        if b'leveldb.BytewiseComparator' in data: # 识别常见模式
            return {"comparator": "leveldb.BytewiseComparator"}
        return {"raw_data": binascii.hexlify(data[:100]).decode('ascii') + "..."}

def parse_ldb_file(file_path): # 解析 LevelDB 的 .ldb 文件（简化版，提取可打印字符串）
    results = {"strings": []}
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            # 查找至少10个字符长的可打印字符串序列
            printable_strings = re.findall(b"[ -~]{10,}", content)
            for s in printable_strings:
                results["strings"].append(s.decode('utf-8', errors='ignore'))
    except Exception as e:
        results["error"] = str(e)
    return results

def analyze_leveldb(db_dir): # 分析整个 LevelDB 数据库目录，解析所有数据并返回
    db_data = {"files": {}, "summary": {"total_files": 0, "total_size": 0, "last_modified": None}}
    for filename in os.listdir(db_dir):
        file_path = os.path.join(db_dir, filename)
        if not os.path.isfile(file_path): continue
        file_stats = os.stat(file_path)
        file_info = {"size": file_stats.st_size, "last_modified": file_stats.st_mtime, "content": {}}
        db_data["summary"]["total_files"] += 1
        db_data["summary"]["total_size"] += file_stats.st_size
        if filename.endswith('.log'): # 根据文件类型调用不同解析器
            file_info["type"] = "LOG"
            file_info["content"] = parse_log_file(file_path)
        elif filename.endswith('.ldb'):
            file_info["type"] = "LDB"
            file_info["content"] = parse_ldb_file(file_path)
        elif 'MANIFEST' in filename:
            file_info["type"] = "MANIFEST"
            file_info["content"] = parse_manifest(file_path)
        elif filename == 'CURRENT':
            file_info["type"] = "CURRENT"
            with open(file_path, 'rb') as f:
                file_info["content"] = f.read().decode('utf-8', errors='ignore').strip()
        elif filename == 'LOCK':
            file_info["type"] = "LOCK"
            file_info["content"] = "Empty lock file"
        else:
            file_info["type"] = "UNKNOWN"
        db_data["files"][filename] = file_info
        if not db_data["summary"]["last_modified"] or file_stats.st_mtime > db_data["summary"]["last_modified"]: # 更新最后修改时间
            db_data["summary"]["last_modified"] = file_stats.st_mtime
    return db_data

def print_results(results, verbose=False): # 格式化打印结果，verbose控制输出详细程度
    print(f"LevelDB 数据库分析报告")
    print(f"文件总数: {results['summary']['total_files']}")
    print(f"总大小: {results['summary']['total_size'] / 1024:.2f} KB")
    print(f"最后修改时间: {results['summary']['last_modified']}")
    print("-" * 80)
    for filename, info in results["files"].items():
        print(f"\n文件: {filename} ({info['type']})")
        print(f"大小: {info['size']} 字节 | 修改时间: {info['last_modified']}")
        if info["type"] == "LOG":
            # 打印原始分组信息
            for rec_type, records in info["content"].items():
                if rec_type in ["FIRST", "MIDDLE", "LAST", "FULL", "UNKNOWN"]:
                    print(f"  原始 {rec_type} 记录 ({len(records)} found)")
            # 打印新解析的信息
            if "parsed_records" in info["content"]:
                # 统计成功解析为dict的数量
                parsed_count = sum(1 for r in info["content"]["parsed_records"] if isinstance(r.get("parsed_payload"), dict))
                print(f"  => 成功拼接并解析的完整记录: {len(info['content']['parsed_records'])} (其中 {parsed_count} 条为JSON)")
        elif info["type"] == "LDB":
            if "error" in info["content"]:
                print(f"  解析LDB文件时出错: {info['content']['error']}")
            elif "strings" in info["content"] and info["content"]["strings"]:
                print(f"  提取的可打印字符串 ({len(info['content']['strings'])} found)")
        elif info["type"] == "MANIFEST":
            for k, v in info["content"].items():
                print(f"  {k}: {v}")
        elif info["type"] == "CURRENT":
            print(f"  当前清单: {info['content']}")

# ==============================================================================
# 新增的完美解析代码
# ==============================================================================

def try_parse_json_payload(payload):
    """
    健壮的JSON解析函数：尝试从一个可能包含前后缀的字符串中提取并解析JSON。
    """
    if not isinstance(payload, str):
        return payload

    # 寻找最外层的 '{' 和 '}' 来捕获最完整的JSON对象
    start_brace = payload.find('{')
    end_brace = payload.rfind('}')

    if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
        json_str = payload[start_brace : end_brace + 1]
        try:
            # 尝试将提取出的字符串解析为JSON
            return json.loads(json_str)
        except json.JSONDecodeError:
            # 如果解析失败，说明它不是一个有效的JSON，返回原始payload
            return payload
    
    return payload

def add_reassembled_parsing(results, db_dir):
    """
    通过重新读取log文件来正确地拼接分块记录(FIRST, MIDDLE, LAST)，
    然后对拼接后的完整payload进行JSON解析。
    这个函数会直接修改传入的results字典，在log文件的content中新增一个'parsed_records'列表。
    """
    if "files" not in results:
        return results

    for filename, info in results["files"].items():
        if info.get("type") != "LOG":
            continue

        file_path = os.path.join(db_dir, filename)
        if not os.path.isfile(file_path):
            continue

        parsed_records = []
        reassembly_buffer = [] 
        
        try:
            with open(file_path, 'rb') as f:
                while True:
                    header = f.read(7)
                    if len(header) < 7: break
                    
                    _, length, record_type = struct.unpack('<IHb', header)
                    payload = f.read(length)
                    if len(payload) < length: break

                    # 记录类型: 1=FULL, 2=FIRST, 3=MIDDLE, 4=LAST
                    if record_type == 1: # FULL
                        reassembly_buffer = []
                        decoded_payload = payload.decode('utf-8', errors='ignore')
                        parsed_content = try_parse_json_payload(decoded_payload)
                        parsed_records.append({"type": "FULL", "parsed_payload": parsed_content})

                    elif record_type == 2: # FIRST
                        reassembly_buffer = [payload]

                    elif record_type == 3: # MIDDLE
                        if reassembly_buffer:
                            reassembly_buffer.append(payload)

                    elif record_type == 4: # LAST
                        if reassembly_buffer:
                            reassembly_buffer.append(payload)
                            full_payload_bytes = b''.join(reassembly_buffer)
                            decoded_payload = full_payload_bytes.decode('utf-8', errors='ignore')
                            parsed_content = try_parse_json_payload(decoded_payload)
                            parsed_records.append({"type": "REASSEMBLED", "parsed_payload": parsed_content})
                            reassembly_buffer = []
        except Exception as e:
            info["content"]["parsing_error"] = str(e)

        # 将新解析的、完整的记录列表添加到结果中
        info["content"]["parsed_records"] = parsed_records
            
    return results


def main():
    db_path = r"C:\Users\qgb\AppData\Local\Microsoft\Edge\User Data\Default\Local Extension Settings\fdbloeknjpnloaggplaobopplkdhnikc"
    results = analyze_leveldb(db_path)
    # 调用新的完美解析函数，它需要知道db_path才能重新读取文件
    jw = add_reassembled_parsing(results, db_path) 
    # 使用更新后的print_results函数打印摘要
    print_results(jw)
    rs=jw['files']['000085.log']['content']['parsed_records']
    for i in range(len(rs)):
        d=rs[i]
        name=d['parsed_payload']['defaultProfileName']
        print(i,name)
if __name__ == "__main__":main()        