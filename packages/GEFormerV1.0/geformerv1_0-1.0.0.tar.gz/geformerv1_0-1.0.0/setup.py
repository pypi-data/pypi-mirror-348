import pathlib
from setuptools import setup

here = pathlib.Path(__file__).parent

# 读取 requirements.txt
with open(here / "requirements.txt", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="GEFormerV1.0",
    version="1.0.0",
    description="Meta-package that installs all dependencies for YourModel",
    long_description=(here / "README.md").read_text(encoding="utf-8"),
    include_package_data=True,
    long_description_content_type="text/markdown",
    author="yz",
    author_email="wgs2038@163.com",
    url="https://github.com/Deep-Breeding/GEFormer",  # 如有代码仓库
    packages=["GEFormer"],    # 即使目录空也写上
    install_requires=requirements,  # 核心依赖列表
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
