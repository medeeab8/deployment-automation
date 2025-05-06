#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deployment-automation",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A flexible application deployment framework that supports packaging and deploying different types of applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/deployment-automation",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Software Distribution",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyyaml>=5.1",
    ],
    extras_require={
        "wheel": ["wheel"],
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "deployment-tool=src.deployer:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)