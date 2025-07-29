from setuptools import setup
from pathlib import Path

current_dir = Path(__file__).parent

setup(
    name="stv_utils",
    version="0.0.5",
    py_modules=["stv_utils"],
    description="一些常用函数与方法",
    long_description=open("README.md", 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="\033[96m星灿长风v(github.com/StarWindv)\033[0m",
    author_email="starwindv.stv@gmail.com",
    url="", 
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)
