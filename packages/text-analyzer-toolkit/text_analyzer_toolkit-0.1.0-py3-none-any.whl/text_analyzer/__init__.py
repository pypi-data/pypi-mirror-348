"""
A simple text analysis package for basic text processing tasks.
"""

__version__ = "0.1.0"
__author__ = "Zoe Duan"

from .analyzer import TextAnalyzer
from .utils import clean_text, count_words

__all__ = ["TextAnalyzer", "clean_text", "count_words"]