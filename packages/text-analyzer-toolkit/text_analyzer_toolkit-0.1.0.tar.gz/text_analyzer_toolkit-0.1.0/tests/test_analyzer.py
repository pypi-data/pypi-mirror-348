import pytest
from text_analyzer import TextAnalyzer

def test_word_count():
    analyzer = TextAnalyzer("Hello world! This is a test.")
    assert analyzer.word_count() == 6

def test_empty_text():
    analyzer = TextAnalyzer("")
    assert analyzer.word_count() == 0
    assert analyzer.character_count() == 0
    assert analyzer.sentence_count() == 0

def test_character_count():
    analyzer = TextAnalyzer("Hello")
    assert analyzer.character_count() == 5
    
def test_sentence_count():
    analyzer = TextAnalyzer("Hello. How are you? I'm fine!")
    assert analyzer.sentence_count() == 3

def test_get_summary():
    analyzer = TextAnalyzer("Hello world! This is a test.")
    summary = analyzer.get_summary()
    assert "word_count" in summary
    assert "character_count" in summary