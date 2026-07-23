#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APK 差异分析工具
- 字节级 diff
- ZIP 条目 diff
- 自动深入 private.tar 内部 diff
"""

import os
import zipfile
import tarfile
import hashlib
import tempfile

# 要分析的两个 APK 文件路径（请根据实际情况修改）
APK1 = "/workspaces/hualing-0.1-arm64-v8a-debug-20260720_132638.apk"
APK2 = "/workspaces/hualing-0.1-arm64-v8a-debug-20260720_132820.apk"

def byte_diff(file1, file2, max_print=100):
    """逐字节对比两个文件，返回差异总数"""
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)
    print(f"\n[字节级 diff]")
    print(f"文件1: {os.path.basename(file1)} ({size1} 字节)")
    print(f"文件2: {os.path.basename(file2)} ({size2} 字节)")

    diff_count = 0
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        offset = 0
        while True:
            b1 = f1.read(1)
            b2 = f2.read(1)
            if not b1 and not b2:
                break
            if b1 != b2:
                diff_count += 1
                if diff_count <= max_print:
                    val1 = b1[0] if b1 else None
                    val2 = b2[0] if b2 else None
                    print(f"  偏移 {offset:>10d}: {val1:3d} -> {val2:3d}")
            offset += 1
    print(f"总差异字节数: {diff_count}")
    if size1 != size2:
        print("注意：文件大小不同，较长文件的多出部分已计入差异")
    return diff_count

def zip_entries_sha256(apk_path):
    """获取 APK 内所有文件的 SHA-256"""
    with zipfile.ZipFile(apk_path, 'r') as z:
        return {name: hashlib.sha256(z.read(name)).hexdigest()
                for name in z.namelist()}

def compare_apk_entries(apk1, apk2):
    """对比两个 APK 的 ZIP 条目差异，返回差异文件名集合"""
    print(f"\n[ZIP 条目 diff]")
    entries1 = zip_entries_sha256(apk1)
    entries2 = zip_entries_sha256(apk2)
    all_names = set(entries1.keys()) | set(entries2.keys())
    diff_files = set()
    for name in sorted(all_names):
        h1 = entries1.get(name, 'MISSING')
        h2 = entries2.get(name, 'MISSING')
        if h1 != h2:
            diff_files.add(name)
            print(f"  差异: {name}")
    if not diff_files:
        print("  所有文件完全相同")
    else:
        print(f"  共 {len(diff_files)} 个文件不同")
    return diff_files

def tar_entries_sha256(tar_path):
    """获取 tar 内所有文件的 SHA-256"""
    with tarfile.open(tar_path, 'r') as tar:
        result = {}
        for member in tar.getmembers():
            if member.isfile():
                f = tar.extractfile(member)
                if f:
                    result[member.name] = hashlib.sha256(f.read()).hexdigest()
        return result

def analyze_private_tar(apk1, apk2):
    """如果 private.tar 有差异，则深入分析"""
    # 提取两个 private.tar 到临时文件
    with tempfile.TemporaryDirectory() as tmpdir:
        tar1_path = os.path.join(tmpdir, "private1.tar")
        tar2_path = os.path.join(tmpdir, "private2.tar")

        try:
            with zipfile.ZipFile(apk1, 'r') as z:
                z.extract('assets/private.tar', path=tmpdir)
                os.rename(os.path.join(tmpdir, 'assets', 'private.tar'), tar1_path)
        except KeyError:
            print("\n[private.tar 分析] 文件1中不存在 assets/private.tar")
            return
        try:
            with zipfile.ZipFile(apk2, 'r') as z:
                z.extract('assets/private.tar', path=tmpdir)
                os.rename(os.path.join(tmpdir, 'assets', 'private.tar'), tar2_path)
        except KeyError:
            print("\n[private.tar 分析] 文件2中不存在 assets/private.tar")
            return

        print(f"\n[private.tar 内部文件 diff]")
        entries1 = tar_entries_sha256(tar1_path)
        entries2 = tar_entries_sha256(tar2_path)
        all_names = set(entries1.keys()) | set(entries2.keys())
        diff_files = []
        for name in sorted(all_names):
            h1 = entries1.get(name, 'MISSING')
            h2 = entries2.get(name, 'MISSING')
            if h1 != h2:
                diff_files.append(name)
                print(f"  差异: {name}")

        print(f"private.tar 内文件总数: {len(all_names)}")
        print(f"差异文件数: {len(diff_files)}")
        if diff_files:
            print("差异文件列表:")
            for name in diff_files:
                print(f"  {name}")

def main():
    for apk in (APK1, APK2):
        if not os.path.exists(apk):
            print(f"错误: 文件不存在 - {apk}")
            return

    # 1. 字节级 diff
    bytes_count=byte_diff(APK1, APK2)

    if bytes_count:
        diff_entries = compare_apk_entries(APK1, APK2)

        # 3. 如果 private.tar 有差异，深入分析
        if 'assets/private.tar' in diff_entries:
            analyze_private_tar(APK1, APK2)
        else:
            print("\nassets/private.tar 无差异，无需进一步分析")

if __name__ == "__main__":
    main()