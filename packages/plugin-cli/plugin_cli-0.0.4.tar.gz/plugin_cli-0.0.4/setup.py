#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 zhaosonggo@gmail.com, All rights reserved.
# Licensed under the Apache License Version 2.0 that can be found in the
# LICENSE file in the root directory of this source tree

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

version = "0.0.4"

setuptools.setup(
    name="plugin-cli",
    version=version,
    author="Song Zhao",
    author_email="zhaosonggo@163.com",
    description="Rapidly Build a Plugin-Based CLI Tool Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/zhaosong-lmm_admin/cli-framework",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
