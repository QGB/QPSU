import win32file
import win32con

def exclusive_open_read_no_share(file_path):
    # Windows API 参数
    access = win32con.GENERIC_READ  # 只读权限
    share_mode = 0                  # 禁止其他进程读写（完全独占）
    creation = win32con.OPEN_EXISTING  # 打开已存在的文件
    flags = win32con.FILE_ATTRIBUTE_NORMAL

    # 调用 Windows API 打开文件
    handle = win32file.CreateFile(
        file_path,
        access,
        share_mode,  # 关键：share_mode=0 表示完全独占
        None,
        creation,
        flags,
        None
    )
    return handle

# 示例用法（读取文件）
try:
    file_path = r'C:\test\win10\run2.bat'
    handle = exclusive_open_read_no_share(file_path)
    
    # 读取文件内容
    data = win32file.ReadFile(handle,4096)  # 读取前4096字节
    print(f"读取内容: {data[1].decode('utf-8')}")  # data[1] 是字节数据
    
    # 关闭句柄
    win32file.CloseHandle(handle)
except Exception as e:
    print(f"操作失败: {e}")