from pathlib import Path
from setuptools import find_packages, setup

ROOT = Path(__file__).resolve().parent
README = (ROOT / "README.md").read_text(encoding="utf-8")

setup(
    name="qpsu",
    version="0.1.0",
    description="Utility package for qgb/python scripts",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "tests.*", "build", "build.*"]),
    include_package_data=True,
    package_dir={"": "."},
    python_requires=">=3.8",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

