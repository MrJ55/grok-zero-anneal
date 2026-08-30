import re

_KV_RE = re.compile(r'''([^\s=]+)=(?:"([^"]*)"|'([^']*)'|([^\s]*))''')

def parse_kv(line: str) -> dict[str, str]:
    """Parse space-separated k=v tokens into a dict. Empty line -> {}."""
    if not line or not line.strip():
        return {}
    result: dict[str, str] = {}
    for m in _KV_RE.finditer(line):
        key = m.group(1)
        if m.group(2) is not None:
            val = m.group(2)
        elif m.group(3) is not None:
            val = m.group(3)
        else:
            val = m.group(4) if m.group(4) is not None else ""
        result[key] = val
    return result
