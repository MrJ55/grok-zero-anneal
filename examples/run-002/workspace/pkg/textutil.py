import re

def slugify(text: str) -> str:
    """Lowercase, non-alnum to hyphen, collapse hyphens, strip edges."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')
