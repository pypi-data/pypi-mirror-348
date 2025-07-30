from setuptools import setup, find_packages

setup(
    name="ivrs_client",             # 包名
    version="0.1.1",              # 版本号
    description="Client Building for Intelligent Voice Response System", 
    author="Nana",
    author_email="hukmonjikoladafa@gmail.com",
    packages=find_packages(),     # 自动包含所有子包
    python_requires='>=3.6',      # Python版本要求
)
