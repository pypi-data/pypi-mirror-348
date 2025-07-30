from text_analyzer.utils import clean_text, count_words

def test_clean_text():
    assert clean_text("  Hello   world  ") == "Hello world"
    assert clean_text("") == ""

def test_count_words():
    assert count_words("hello world") == 2
    assert count_words("") == 0