"""YouTube video downloader package by Talha"""
from .downloader import download_highest_quality
from .cli import main

__version__ = "1.0.0"
__all__ = ['download_highest_quality', 'main']