def clamp(x: float, lo: float, hi: float) -> float:
    """Return x limited to [lo, hi]. Assume lo <= hi."""
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x
