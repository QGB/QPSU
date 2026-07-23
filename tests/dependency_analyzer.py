import argparse
import ast
import fnmatch
import importlib.util
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


STANDARD_LIBRARY_MODULES = {
    "abc",
    "argparse",
    "array",
    "ast",
    "asyncio",
    "base64",
    "binascii",
    "bisect",
    "builtins",
    "bz2",
    "calendar",
    "cmath",
    "collections",
    "contextlib",
    "copy",
    "csv",
    "ctypes",
    "dataclasses",
    "datetime",
    "decimal",
    "difflib",
    "enum",
    "errno",
    "fnmatch",
    "functools",
    "gc",
    "getopt",
    "glob",
    "gzip",
    "hashlib",
    "heapq",
    "hmac",
    "html",
    "http",
    "idlelib",
    "inspect",
    "io",
    "itertools",
    "json",
    "logging",
    "math",
    "mimetypes",
    "multiprocessing",
    "operator",
    "os",
    "pathlib",
    "pdb",
    "pickle",
    "platform",
    "pprint",
    "queue",
    "random",
    "re",
    "shlex",
    "signal",
    "site",
    "socket",
    "sqlite3",
    "stat",
    "statistics",
    "string",
    "struct",
    "subprocess",
    "sys",
    "tempfile",
    "textwrap",
    "threading",
    "time",
    "tkinter",
    "traceback",
    "types",
    "typing",
    "unittest",
    "urllib",
    "uuid",
    "venv",
    "warnings",
    "wave",
    "weakref",
    "webbrowser",
    "xml",
    "zipfile",
    "zlib",
}


def _normalize_module_name(name: str) -> str:
    if not name:
        return ""
    return name.split(".")[0]


def _iter_python_files(root: Path, patterns: List[str] | None = None, exclude_tests: bool = True) -> List[Path]:
    files = [p for p in root.rglob("*.py") if p.is_file()]
    if exclude_tests:
        files = [p for p in files if "tests" not in p.relative_to(root).parts]

    if patterns:
        matched: Set[Path] = set()
        for pattern in patterns:
            normalized = pattern.replace("\\", "/")
            for path in files:
                rel = path.relative_to(root).as_posix()
                if fnmatch.fnmatch(rel, normalized) or fnmatch.fnmatch(str(path), normalized):
                    matched.add(path)
        return sorted(matched)

    return sorted(files)


def _collect_imports(file_path: Path) -> List[Tuple[str, str]]:
    try:
        tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
    except (SyntaxError, UnicodeDecodeError):
        return []

    imports: List[Tuple[str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((alias.name, "import"))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append((node.module, "from"))
    return imports


def _is_stdlib_module(name: str) -> bool:
    if not name:
        return True
    normalized = _normalize_module_name(name)
    if normalized in STANDARD_LIBRARY_MODULES:
        return True
    if normalized.startswith("_"):
        return True
    if importlib.util.find_spec(normalized) is None:
        return False
    return normalized in sys.stdlib_module_names if hasattr(sys, "stdlib_module_names") else False


def _resolve_local_modules(root: Path, files: List[Path]) -> Set[str]:
    module_names: Set[str] = set()
    for file_path in files:
        rel = file_path.relative_to(root)
        parts = list(rel.with_suffix("").parts)
        if parts and parts[-1] == "__init__":
            parts = parts[:-1]
        if not parts:
            continue

        module_names.add(".".join(parts))
        for index in range(1, len(parts)):
            module_names.add(".".join(parts[:index]))
    return module_names


def analyze_python_dependencies(root: Path, patterns: List[str] | None = None, exclude_tests: bool = True) -> List[Dict[str, object]]:
    root = root.resolve()
    py_files = _iter_python_files(root, patterns, exclude_tests=exclude_tests)
    local_modules = _resolve_local_modules(root, py_files)

    results: List[Dict[str, object]] = []
    for file_path in py_files:
        rel_path = file_path.relative_to(root).as_posix()
        dependencies: Set[str] = set()
        for module_name, _kind in _collect_imports(file_path):
            normalized = _normalize_module_name(module_name)
            if normalized in {"", "__future__"}:
                continue
            if normalized in local_modules:
                continue
            if normalized.startswith("qgb"):
                continue
            if module_name.startswith("."):
                continue
            if _is_stdlib_module(normalized):
                continue
            dependencies.add(normalized)

        results.append({"path": rel_path, "dependencies": sorted(dependencies)})

    return results


def _write_requirements(path: Path, dependencies: List[Dict[str, object]]) -> None:
    packages: Set[str] = set()
    for item in dependencies:
        packages.update(item.get("dependencies", []))

    requirements = sorted(packages)
    path.write_text("\n".join(requirements) + ("\n" if requirements else ""), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Python dependencies in a folder")
    parser.add_argument("target", nargs="?", default=".", help="Folder to scan")
    parser.add_argument("--patterns", nargs="*", default=None, help="Optional file patterns to include, e.g. *.py")
    parser.add_argument("--include-tests", action="store_true", help="Include files under the tests directory")
    parser.add_argument("--output", default="requirements.txt", help="Path to write generated requirements.txt")
    parser.add_argument("--json", action="store_true", help="Print JSON summary instead of plain text")
    args = parser.parse_args()

    root = Path(args.target).resolve()
    results = analyze_python_dependencies(root, args.patterns, exclude_tests=not args.include_tests)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for item in results:
            deps = ", ".join(item["dependencies"]) or "(none)"
            print(f"{item['path']}: {deps}")

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = (Path.cwd() / output_path).resolve()
    _write_requirements(output_path, results)
    print(f"\nWrote requirements to {output_path}")


if __name__ == "__main__":
    main()
