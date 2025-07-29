#!/usr/bin/env python3

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


__version__ = "0.1.0"

setup(
    name="leonbonetti.fast-mcp",
    version=__version__,
    description="Small selection of utilities for python ai processes",
    long_description_content_type="text/markdown",
    long_description=read("README.md"),
    author="Leonardo Bonetti",
    author_email="leonardobonetti.w@gmail.com",
    url="https://github.com/LeonBonetti/FastMCP",
    packages=[
        "fast_mcp",
    ],
    license="proprietary",
    install_requires=[
        "langchain==0.3.21",
        "langchain-core==0.3.47",
        "langchain-openai==0.3.9",
        "langchain-text-splitters==0.3.7",
        "langsmith==0.3.18",
        "tiktoken==0.9.0"
    ],
    classifiers=[
        "Topic :: Utilities",
        "License :: Other/Proprietary License",
    ],
)
