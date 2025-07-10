import regex

# You do not need to change anything in this function, it is already quite good
def remove_headers_footers(text, header_patterns=None, footer_patterns=None):
    """Remove header/footer lines based on regex patterns."""
    if header_patterns is None:
        # More practical pattern: remove lines containing "Page X", "Ref No: Y"
        header_patterns = [r'^(Page)\s+\d+', r'^(Ref No):.*$']
    if footer_patterns is None:
        footer_patterns = [r'^.*Footer.*$'] # Keep the old footer pattern

    for pattern in header_patterns + footer_patterns:
        text = regex.sub(pattern, '', text, flags=regex.MULTILINE | regex.IGNORECASE)

    return text.strip()


def remove_special_characters_vietnamese_safe(text):
    """
    Remove unwanted special characters but keep all letters and numbers of all languages (including Vietnamese).
    \p{L} -> Any Unicode letter (a, b, c, d...)
    \p{N} -> Any Unicode number (1, 2, 3...)
    \s -> Whitespace
    Explicitly listed punctuation: .,;:'"?!-
    """
    # This regex keeps letters, numbers, whitespace, and necessary punctuation
    pattern = r'[^\p{L}\p{N}\s.,;:\'"?!-]'
    
    # Replace unwanted characters (e.g., emoji, block characters, etc.) with a space
    text = regex.sub(pattern, ' ', text)
    return text.strip()

def normalize_repeated_punctuation(text):
    """
    Normalize repeated punctuation marks (e.g., ... to ., ?? to ?, !! to !)
    ([.?!]) -> Capture one of ., ?, ! into group 1.
    \1+ -> Find one or more occurrences of the captured character in group 1.
    r'\1' -> Replace the entire found sequence with just one character from group 1.
    """
    text = regex.sub(r'([.?!])\1+', r'\1', text)
    return text.strip()

def normalize_whitespace(text):
    """Normalize excessive whitespace and newlines."""
    # Replace multiple consecutive newlines with a single newline (to keep paragraph structure)
    text = regex.sub(r'\n{3,}', '\n\n', text)
    # Replace multiple spaces/tabs with a single space
    text = regex.sub(r'[ \t]+', ' ', text)
    
    return text.strip()

def preprocess_text(text: str) -> str:
    """
    Complete pipeline for text preprocessing, safe for Vietnamese.
    """
    if not isinstance(text, str):
        return ""

    # 1. Remove large unnecessary blocks like header/footer
    text = remove_headers_footers(text)
    
    # 2. Safely remove unwanted special characters
    text = remove_special_characters_vietnamese_safe(text)

    # 3. Normalize repeated punctuation
    text = normalize_repeated_punctuation(text)

    # 4. Normalize whitespace (usually done last for cleanup)
    text = normalize_whitespace(text)

    return text.strip()
