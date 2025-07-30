from setuptools import setup, find_packages
import os

# 读取README文件作为长描述，确保使用UTF-8编码
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
try:
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "视觉AI网关MCP服务 - 详细描述请参见项目主页。"

setup(
    name="mcp-vision-gateway",  # PyPI上的包名
    version="0.1.4",           # 更新版本号
    packages=find_packages(),  # 自动查找包目录
    author="MCP Vision Gateway Authors",
    author_email="your.email@example.com",  # 请替换为您的邮箱
    description="连接MCP与视觉AI模型的网关服务，支持图像处理和纯文本对话",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mcp-vision-gateway",  # 请替换为您的项目URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mcp>=1.6.0",  # 依赖MCP SDK
        "requests>=2.25.0",  # 用于HTTP请求
    ],
    entry_points={
        "console_scripts": [
            "mcp-vision-gateway=mcp_vision_gateway.__main__:main",
        ],
    },
) 