import re

MALICIOUS_PATTERNS = [
    r"(?i)union\s+select",
    r"(?i)<script.*?>",
    r"(?i)onerror\s*=",
    r"(?i)drop\s+table",
    r"(?i)base64_decode\(",
    r"(?i)etc/passwd",
]

def is_safe_input(value):
    if not value:
        return True
    for pattern in MALICIOUS_PATTERNS:
        if re.search(pattern, value):
            return False
    return True
