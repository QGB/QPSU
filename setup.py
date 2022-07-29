from setuptools import setup, find_packages

print('#'*99,find_packages())

setup(
    name="qgb",
    version="0.01",
    packages=['qgb'],
    package_dir={
        'qgb': '.',
    },
)

