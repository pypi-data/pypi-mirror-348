# setup.py - 用于打包和分发 MySQLHelper 项目
import setuptools


# 读取项目 README.md 作为长描述，将显示在 PyPI 项目页面上
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# 使用 setuptools.setup 配置项目打包信息
setuptools.setup(
    # 项目名称 - 将作为 PyPI 上的包名 (pip install DecoKit")
    name="DecoKit",
    
    # 版本号 - 遵循语义化版本规范 (MAJOR.MINOR.PATCH)
    version="0.1.0",
    
    # 作者信息
    author="cxfjh",
    author_email="2449579731@qq.com",
    
    # 项目简短描述 - 显示在 PyPI 包列表中
    description="装饰器工具集",
    
    # 项目详细描述 - 从 README.md 读取
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # 项目源码地址 (通常是 GitHub 仓库)
    url="https://github.com/cxfjh/DecoTools",
    
    # 自动发现并包含所有项目包 (需包含 __init__.py 文件)
    packages=setuptools.find_packages(),
    
    # 项目分类器 - 帮助用户在 PyPI 上筛选和发现项目
    classifiers=[
        "Programming Language :: Python :: 3",             # 支持的 Python 版本
        "License :: OSI Approved :: MIT License",         # 开源许可证类型
        "Operating System :: OS Independent",             # 跨平台支持
        "Topic :: Database",                              # 数据库相关主题
        "Topic :: Software Development :: Libraries",     # 开发库类别
    ],
    
    # 最低 Python 版本要求
    python_requires=">=3.6",
    
    # 项目关键词 - 提高在 PyPI 上的搜索可见性
    keywords="deco tools decorator, 装饰器, 工具集",
)