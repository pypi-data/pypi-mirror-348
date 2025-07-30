#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages            #这个包没有的可以pip一下
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.EN.md").read_text()

setup(
    name = "lunax",      #这里是pip项目发布的名称
    version = "0.0.6",  #版本号，数值大的会优先被pip
    keywords = ["pip", "tabular data"],			# 关键字
    description = "A machine learning framework.",	# 描述
    long_description=long_description,
    long_description_content_type='text/markdown',
    license = "MIT Licence",		# 许可证

    url = "https://github.com/yangfa-zhang/lunax",     #项目相关文件地址，一般是github项目地址即可
    author = "yangfa-zhang",			# 作者
    author_email = "yangfa1027@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy", "pandas","xgboost","tabulate","python-abc","typing","scikit-learn","optuna","lightgbm","catboost","matplotlib","seaborn"]          #这个项目依赖的第三方库
)
