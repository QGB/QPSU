import zipfile, gzip, io, tarfile, sys

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

# ---------- 第二步：如果最大文件是 .so，进一步深入分析 ----------
if not biggest_name.endswith('.so'):
    print("\n最大文件不是 .so 文件，无需进一步分析。")
    sys.exit(0)

print("\n" + "=" * 60)
print(f"🔬 深入分析最大 .so 文件: {biggest_name}")
print("=" * 60)

with zipfile.ZipFile(APK_PATH, 'r') as z:
    raw = z.read(biggest_name)

# 检测是不是 gzip 压缩（libpybundle.so 是 gzip 压缩的 tar 包）
if raw[:2] != b'\x1f\x8b':
    print("该 .so 文件不是 gzip 压缩格式，无法自动分析内部结构。")
    print("建议使用 readelf、nm 或 bloaty 工具手动分析。")
    sys.exit(0)

print("检测到 gzip 压缩格式，正在解压...")
tar_bytes = gzip.decompress(raw)
print(f"解压后 tar 大小: {len(tar_bytes)/1024**2:.2f} MB")

# 解析 tar 并列出内部文件
with tarfile.open(fileobj=io.BytesIO(tar_bytes)) as tar:
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

print("\n✅ 分析完毕（所有操作均在内存中进行，未生成磁盘文件）")