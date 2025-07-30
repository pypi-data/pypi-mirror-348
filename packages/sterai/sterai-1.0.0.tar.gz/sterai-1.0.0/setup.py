from setuptools import setup, find_packages
import os

# Read the README.md file for long description
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "An AI-powered MCQ Analysis Tool using Together AI API"

setup(
    name="sterai",
    version="1.0.0",
    author="KnownMe100",
    author_email="knownme100@protonmail.com",
    description="An AI-powered MCQ Analysis Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/knownme100/sterai",
    project_urls={
        "Bug Tracker": "https://github.com/knownme100/sterai/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education :: Testing",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "sterai=sterai.main:main",
        ],
    },
)