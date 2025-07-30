from setuptools import setup, find_packages

setup(
    name="kevins_torch",
    version="0.2.2",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "numpy>=1.21.0",
        "Pillow>=8.0.0",
    ],
    author="Kevin",
    author_email="qazsskevin@gmail.com",
    description="A collection of PyTorch utilities for image AI training",
    long_description=open("README.md", encoding="utf-8").read(), # Specify UTF-8 encoding
    long_description_content_type="text/markdown",
    url="https://github.com/qazsskevin/kevins_torch",  # 使用一個範例 URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)