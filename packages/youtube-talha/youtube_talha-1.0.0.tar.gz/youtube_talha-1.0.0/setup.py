from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="youtube_talha",
    version="1.0.0",
    packages=find_packages(where="."),
    package_dir={"": "."},
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
            "youtube-talha=youtube_talha.cli:main",
        ],
    },
)