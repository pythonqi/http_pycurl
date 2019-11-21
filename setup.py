# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="http_pycurl",
    version="1.0.0",
    author="pythonqi",
    author_email="pythonqi@outlook.com",
    description="http_pycurl rewraps pycurl.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pythonqi/http_pycurl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.4',
)