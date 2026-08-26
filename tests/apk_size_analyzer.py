import zipfile
import gzip
import io
import tarfile
import sys

# ====== 修改这里为你的 APK 路径 ======
APK_PATH = "/workspaces/kivy/bin/hualing-0.1-arm64-v8a-debug.apk"
# ======================================

# ---------- 第一步：列出 APK 内最大的 20 个文件 ----------
print("=" * 60)
print("📦 APK 文件大小分析")
print("=" * 60)

with zipfile.ZipFile(APK_PATH, 'r') as z:
    entries = []
    for info in z.infolist():
        if info.is_dir():
            continue
        entries.append((info.filename, info.file_size, info.compress_size))

entries.sort(key=lambda x: x[1], reverse=True)

total_orig = sum(e[1] for e in entries)
total_comp = sum(e[2] for e in entries)

print(f"文件总数: {len(entries)}")
print(f"未压缩总大小: {total_orig / (1024**2):.2f} MB")
print(f"压缩后总大小: {total_comp / (1024**2):.2f} MB\n")
print("最大的 20 个文件：")
for i, (name, orig, comp) in enumerate(entries[:20], 1):
    print(f"{i:3}. {name}")
    print(f"     原始: {orig/(1024**2):.2f} MB, 压缩: {comp/(1024**2):.2f} MB")

# 找出最大的那个文件
if not entries:
    sys.exit(0)
biggest_name, biggest_orig, biggest_comp = entries[0]

# ---------- 第二步：尝试深入分析最大文件（如果是 tar/gzip 包） ----------
print("\n" + "=" * 60)
print(f"🔬 尝试深入分析最大文件: {biggest_name}")
print("=" * 60)

with zipfile.ZipFile(APK_PATH, 'r') as z:
    raw = z.read(biggest_name)

# 尝试打开为 tar 包（可能是普通 tar 或 gzip 压缩的 tar）
try:
    # 先检测 gzip 魔术字节
    if raw[:2] == b'\x1f\x8b':
        print("检测到 gzip 压缩格式，正在解压...")
        tar_bytes = gzip.decompress(raw)
        print(f"解压后数据大小: {len(tar_bytes)/1024**2:.2f} MB")
        tar_stream = io.BytesIO(tar_bytes)
    else:
        print("文件未被 gzip 压缩，尝试直接作为 tar 包解析...")
        tar_stream = io.BytesIO(raw)

    with tarfile.open(fileobj=tar_stream) as tar:
        members = tar.getmembers()
        files = [(m.name, m.size) for m in members if m.isfile()]
        files.sort(key=lambda x: x[1], reverse=True)
        total_tar = sum(s for _, s in files)

        print(f"\n内部文件总数: {len(files)}")
        print(f"内部文件总大小: {total_tar/1024**2:.2f} MB\n")

        TOP_N = 30
        print(f"最大的 {min(TOP_N, len(files))} 个内部文件：")
        for i, (name, size) in enumerate(files[:TOP_N], 1):
            print(f"{i:3d}. {name}  ({size/1024**2:.2f} MB)")

except (tarfile.TarError, gzip.BadGzipFile, EOFError) as e:
    print(f"\n无法解析该文件为 tar 包: {e}")
    print("可能不是 tar 归档文件，或使用了不支持的压缩格式。")

print("\n✅ 分析完毕（所有操作均在内存中进行，未生成磁盘文件）")