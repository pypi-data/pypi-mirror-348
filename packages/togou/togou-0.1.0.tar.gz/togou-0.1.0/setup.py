# setup.py

from setuptools import setup, find_packages
import os

# 读取 README.md 作为 long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取 requirements.txt 中的依赖
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="togou",  # 包名（pip install togou）
    version="0.1.0",  # 版本号
    author="今天掉头发了嘛",  # 作者名
    author_email="qwqssr@qq.com",  # 作者邮箱
    description="A distributed-safe file writer with sync/async/thread/process support",  # 简短描述
    long_description=long_description,  # 长描述（从 README.md 读取）
    long_description_content_type="text/markdown",  # README 类型
    url="https://github.com/yourname/togou ",  # 项目主页（GitHub 地址）
    packages=find_packages(),  # 自动发现包目录
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
    ],
    install_requires=read_requirements(),  # 安装依赖项
    python_requires='>=3.7',  # 支持的 Python 版本
    include_package_data=True,  # 是否包含非 .py 文件（如 LICENSE、README）
    keywords="file-writer redis distributed-lock async safe-io",  # 搜索关键词
)