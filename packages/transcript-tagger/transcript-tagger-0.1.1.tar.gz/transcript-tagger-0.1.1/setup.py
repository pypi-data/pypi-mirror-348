#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="transcript-tagger",
    version="0.1.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A toolkit for tagging and analyzing transcript content using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/transcript-tagger",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "tenacity>=8.0.0",
        "textstat>=0.7.3",
        "wordfreq>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "transcript-tagger=transcript_tagger_sdk.cli:main",
        ],
    },
    package_data={
        "transcript_tagger_sdk": ["py.typed"],
    },
) 