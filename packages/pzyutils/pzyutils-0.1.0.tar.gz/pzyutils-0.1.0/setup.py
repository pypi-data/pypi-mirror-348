from setuptools import setup, find_packages

setup(
    name="pzyutils",  # 包名
    version="0.1.0",    # 版本号
    author="pengying", # 作者名
    author_email="15970840304@163.com",  # 作者邮箱
    description="useful tool set",  # 简短描述
    long_description=open("README.md").read(),  # 长描述（通常是 README 文件）
    long_description_content_type="text/markdown",  # 描述格式
    url="https://github.com/pnightowl/pzyutils",  # 项目主页（如 GitHub）
    packages=find_packages(),  # 自动发现包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Python 版本要求
    install_requires=[  # 依赖项
        "openpyxl>=3.1.5",
        
    ],
)