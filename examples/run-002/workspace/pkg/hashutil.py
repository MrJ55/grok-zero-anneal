import hashlib

def merkle_join(parts: list[str]) -> str:
    """Return sha256 hex digest of parts joined with NUL bytes."""
    return hashlib.sha256(chr(0).join(parts).encode()).hexdigest()
