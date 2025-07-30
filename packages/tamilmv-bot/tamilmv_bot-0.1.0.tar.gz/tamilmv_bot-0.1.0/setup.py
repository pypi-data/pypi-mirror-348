from setuptools import setup, find_packages
from pathlib import Path

# README ফাইল পড়ার জন্য
readme_path = Path(__file__).parent / "README.md"
try:
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Telegram bot for downloading from Tamilmv"

# requirements.txt ফাইল পড়ার জন্য
req_path = Path(__file__).parent / "requirements.txt"
try:
    with open(req_path, "r", encoding="utf-8") as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    requirements = []
    print("Warning: requirements.txt file not found!")

setup(
    name="tamilmv-bot",
    version="0.1.0",
    description="Telegram bot for downloading from Tamilmv",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MY-HERO-OP",
    author_email="heron3477@gmail.com",
    url="https://github.com/MY-HERO-OP/1tamilmv_v2_Bot",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
