#coding=utf-8
import json
import re
import urllib.request
from typing import List, Dict

# 优先使用 packaging 库解析语义化版本，没有则使用正则安全降级
try:
    from packaging.version import parse as parse_version
except ImportError:
    def parse_version(v_str: str):
        # 提取版本号中的数字进行元组比较，如 "0.11.1" -> (0, 11, 1)
        nums = re.findall(r'\d+', v_str)
        return tuple(int(x) for x in nums) if nums else (0,)

def get_json(url: str) -> dict:
    req = urllib.request.Request(
        url, 
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[错误] 请求 {url} 失败: {e}")
        return {}

def get_latest_5_versions(pkg: str) -> List[str]:
    """动态获取 PyPI 上某个包最新的 5 个有效版本号"""
    data = get_json(f"https://pypi.org/pypi/{pkg}/json")
    if not data or "releases" not in data:
        return []

    # 过滤出含有发布文件且非空的版本
    valid_versions = [ver for ver, files in data["releases"].items() if files]

    # 按语义化版本号从大到小排序
    sorted_versions = sorted(valid_versions, key=parse_version, reverse=True)
    return sorted_versions[:5]

def query_version_deps(pkg: str, version: str) -> dict:
    """获取指定包+版本的实际依赖配置"""
    data = get_json(f"https://pypi.org/pypi/{pkg}/{version}/json")
    if not data:
        return {"version": version, "ocp_deps": [], "all_deps": []}

    info = data.get("info", {})
    reqs = info.get("requires_dist") or []

    # 筛选包含 "ocp" 的依赖项（忽略大小写）
    ocp_deps = [r for r in reqs if "ocp" in r.lower()]

    return {
        "version": version,
        "ocp_deps": ocp_deps,
        "all_deps": reqs
    }

def main():
    packages = ["cadquery", "build123d", "cadquery-ocp-novtk"]
    results = {}

    print("🚀 开始向 PyPI 发起 HTTP 请求，动态检索最新版本...\n")

    for pkg in packages:
        print(f"==================== {pkg} ====================")
        top5 = get_latest_5_versions(pkg)
        print(f"检索到最新 5 个版本: {top5}")

        pkg_results = []
        for ver in top5:
            dep_info = query_version_deps(pkg, ver)
            pkg_results.append(dep_info)
            ocp_str = "; ".join(dep_info["ocp_deps"]) if dep_info["ocp_deps"] else "无直接 OCP 依赖"
            print(f"  ├─ [{pkg} {ver}]: {ocp_str}")

        results[pkg] = pkg_results
        print()

    # 汇总打印表格
    print("=" * 85)
    print("========== 动态检索 OCP 依赖对照表 ==========")
    fmt = "| {:<20} | {:<12} | {}"
    print(fmt.format("Package", "Version", "OCP 依赖约束"))
    print("-" * 85)

    for pkg, ver_list in results.items():
        for item in ver_list:
            dep_text = "; ".join(item["ocp_deps"]) if item["ocp_deps"] else "无直接 OCP 依赖"
            print(fmt.format(pkg, item["version"], dep_text))

if __name__ == "__main__":
    main()                                                              # 39 
