#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import re

print("----------") 
print("Found packages:", find_packages()) 
print("----------") 

# 读取版本号
with open(os.path.join('pixiv_tag_downloader', '__init__.py'), encoding='utf-8') as f:
    version = re.search(r"__version__\s*=\s*'([^']+)'", f.read()).group(1)

# 读取README文件
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# 读取依赖列表
with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='pixiv_tag_downloader',
    version=version,
    description='根据标签下载Pixiv用户作品的工具',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Mannix Sun',
    author_email='root@teamcs.org',
    url='https://github.com/TrustAsia/PixivTagDownloader',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'pixiv-tag-downloader=pixiv_tag_downloader.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Utilities',
    ],
    keywords='pixiv, download, tag, artwork, manga, novel',
)