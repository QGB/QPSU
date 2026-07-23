import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))

from dependency_analyzer import analyze_python_dependencies


def test_analyze_python_dependencies_detects_external_dependencies():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / "local_mod.py").write_text("VALUE = 1\n", encoding="utf-8")
        pkg_dir = root / "pkg"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("", encoding="utf-8")
        (pkg_dir / "helper.py").write_text("from pkg import helper\n", encoding="utf-8")
        (root / "main.py").write_text(
            "import os\nimport requests\nfrom local_mod import VALUE\nfrom pkg import helper\n",
            encoding="utf-8",
        )

        results = analyze_python_dependencies(root)
        by_path = {item["path"]: item["dependencies"] for item in results}

        assert by_path["main.py"] == ["requests"]
        assert by_path["pkg/helper.py"] == []


def test_analyze_python_dependencies_handles_function_scope_and_builtins():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / "main.py").write_text(
            "import _ast\n\n"
            "def foo():\n"
            "    import requests\n"
            "    return requests.get('https://example.com')\n",
            encoding="utf-8",
        )

        results = analyze_python_dependencies(root)
        by_path = {item["path"]: item["dependencies"] for item in results}

        assert by_path["main.py"] == ["requests"]
