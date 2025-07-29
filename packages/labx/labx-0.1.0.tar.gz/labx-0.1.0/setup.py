from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="labx",  # Make sure this name is unique on PyPI
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "windows-curses; platform_system=='Windows'",
    ],
    entry_points={
        "console_scripts": [
            "labx=labx.cli:main",
        ],
    },
    author="ChatGPT",
    author_email="gpt@chat.com",
    description="A CLI to browse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="cli, pastebin, downloader, curses",
    url="https://github.com/hahaha/labx",  # Optional, GitHub link
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
