#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='pyinstxtractorcn',
    version='1.0.5',  # 更新版本号以便发布新版本
    description='解包 PyInstaller 生成的 .exe 程序（中文版）',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='JZM',
    author_email='pyinstxtractorcn@outlook.com',
    url='https://github.com/jzm3/pyinstxtractorCN',
    install_requires=[],  # 如有依赖库在此声明
    license='GPLv3',
    
    # 关键配置：定义包和命令行工具
    packages=find_packages(include=['pyinstxtractorcn', 'pyinstxtractorcn.*']),
    entry_points={
        'console_scripts': [
            'pyinstxtractorcn = pyinstxtractorcn.cli:main'
        ]
    },
    include_package_data=True,  # 包含非代码文件（需配合 MANIFEST.in）
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Disassemblers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.6',
    project_urls={
        '文档': 'https://github.com/jzm3/pyinstxtractorCN/wiki',
        '源码': 'https://github.com/jzm3/pyinstxtractorCN',
        '更新日志': 'https://github.com/jzm3/pyinstxtractorCN/releases',
        '问题追踪': 'https://github.com/jzm3/pyinstxtractorCN/issues',
    },
)