from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="youtube_talha",
    version="1.0.1",
    packages=find_packages(),  # Corrected line
    install_requires=[
        "pytubefix",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "youtube-talha=youtube_talha.downloader:main",  # Corrected line to point to downloader.py
        ],
    },
)
