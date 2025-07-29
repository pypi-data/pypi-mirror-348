from setuptools import setup

setup(
    name="feishu_bitable_query",
    version="0.1",
    py_modules=["main"],  # 假设你的代码文件名为main.py
    install_requires=[
        "lark-oapi>=1.0.0",  # 飞书开放平台SDK
        "requests>=2.25.0"   # lark-oapi的底层依赖（通常会自动安装）
    ],
    python_requires=">=3.7",  # 要求Python 3.7+
)