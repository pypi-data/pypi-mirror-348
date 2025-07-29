from setuptools import setup, find_packages

setup(
    name="ByteDarkLock-BDL",
    version="1.0.1",
    author="FakeFountain548",
    author_email="gaelsolanoespinosa@gmail.com",
    description="Symmetric encryption and descryption (ByteDarkLock).",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FakeFountain548/ByteDarkLock-BDL",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "cryptography>=3.4.7",
        "Pillow>=8.1.0",
    ],
)