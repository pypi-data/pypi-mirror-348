#!/usr/bin/env python3
from setuptools import setup, find_packages
import os

# Read the long description from README.md
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name="brainlift",
    version="0.2.0",
    description="BrainLift Manager (BLM) - A command-line interface for the BrainLift knowledge management system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Trilogy Group",
    author_email="info@trilogy.com",
    url="https://github.com/trilogy-group/-brainlift-cli",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.15.0",
    ],
    entry_points={
        "console_scripts": [
            "blm=blm.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="brainlift, knowledge management, cli, ai, vector search",
    python_requires=">=3.7",
)
