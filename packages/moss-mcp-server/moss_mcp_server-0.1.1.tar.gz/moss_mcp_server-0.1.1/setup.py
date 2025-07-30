from setuptools import setup, find_packages

setup(
    name="moss_mcp_server",  # 包名，pip install 时用这个
    version="0.1.1",
    description="Moss 收银台mcp工具",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="fenda",
    author_email="alashanprivate@163.com",
    url="https://github.com/alashanprivate/moss_mcp_server",  # 可选：放 GitHub 仓库地址
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)