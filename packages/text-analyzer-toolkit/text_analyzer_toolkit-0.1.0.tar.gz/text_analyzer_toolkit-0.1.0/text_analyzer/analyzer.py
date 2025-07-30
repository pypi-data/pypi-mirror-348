import re
from collections import Counter
import string

class TextAnalyzer:
    """A class for analyzing text data."""
    
    def __init__(self, text=""):
        self.text = text
        self.cleaned_text = self._clean_text()
    
    def _clean_text(self):
        """Clean the text by removing punctuation and converting to lowercase."""
        if not self.text:
            return ""
        # Remove punctuation and convert to lowercase
        cleaned = re.sub(r'[^\w\s]', '', self.text.lower())
        return cleaned
    
    def word_count(self):
        """Count total number of words."""
        if not self.cleaned_text:
            return 0
        return len(self.cleaned_text.split())
    
    def character_count(self, include_spaces=True):
        """Count characters in the text."""
        if include_spaces:
            return len(self.text)
        return len(self.text.replace(' ', ''))
    
    def most_common_words(self, n=5):
        """Return the n most common words."""
        if not self.cleaned_text:
            return []
        words = self.cleaned_text.split()
        return Counter(words).most_common(n)
    
    def average_word_length(self):
        """Calculate average word length."""
        if not self.cleaned_text:
            return 0
        words = self.cleaned_text.split()
        if not words:
            return 0
        return sum(len(word) for word in words) / len(words)
    
    def sentence_count(self):
        """Count number of sentences."""
        if not self.text:
            return 0
        sentences = re.split(r'[.!?]+', self.text)
        # Filter out empty strings
        sentences = [s.strip() for s in sentences if s.strip()]
        return len(sentences)
    
    def reading_time(self, wpm=200):
        """Estimate reading time in minutes based on words per minute."""
        word_count = self.word_count()
        return round(word_count / wpm, 2)
    
    def get_summary(self):
        """Get a summary of all text statistics."""
        return {
            "word_count": self.word_count(),
            "character_count": self.character_count(),
            "character_count_no_spaces": self.character_count(False),
            "sentence_count": self.sentence_count(),
            "average_word_length": round(self.average_word_length(), 2),
            "reading_time_minutes": self.reading_time(),
            "most_common_words": self.most_common_words()
        }