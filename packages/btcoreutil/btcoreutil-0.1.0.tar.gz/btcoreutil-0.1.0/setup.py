# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

from setuptools import setup

with open("README.md") as f:
    doc = f.read()

setup(
    name="btcoreutil",
    description="Utility library for Bitcoin Core",
    long_description=doc,
    long_description_content_type="text/markdown",
    author="Joel Torres",
    author_email="jt@joeltorres.org",
    url="https://github.com/joetor5/btcoreutil",
    license="MIT",
    platforms="any",
    python_requires=">=3.4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
