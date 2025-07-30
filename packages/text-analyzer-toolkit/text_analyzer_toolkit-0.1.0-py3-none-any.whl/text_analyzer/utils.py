import re

def clean_text(text):
    """Utility function to clean text."""
    if not text:
        return ""
    # Remove extra whitespace and normalize
    cleaned = re.sub(r'\s+', ' ', text.strip())
    return cleaned

def count_words(text):
    """Simple word counting utility."""
    if not text:
        return 0
    return len(text.split())

def extract_emails(text):
    """Extract email addresses from text."""
    if not text:
        return []
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)

def extract_urls(text):
    """Extract URLs from text."""
    if not text:
        return []
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_pattern, text)