import re


# Unicode to ASCII operator mapping
_UNICODE_OPERATORS = {
    '×': '*',  # multiplication
    '÷': '/',  # division
    '−': '-',  # minus sign
    '＋': '+',  # fullwidth plus
    '＊': '*',  # fullwidth asterisk
    '／': '/',  # fullwidth slash
    '－': '-',  # fullwidth minus
}

_percent_pair = re.compile(r"""
    (?P<a>\d+(?:\.\d+)?)
    \s*(?P<op>[+\-*/])\s*
    (?P<b>\d+(?:\.\d+)?)%
""", re.VERBOSE)
_number_percent = re.compile(r"(?P<n>\d+(?:\.\d+)?)%")

def expand_percent(expr: str) -> str:
    """Handle A op B% and standalone N% patterns."""
    # Normalize Unicode operators to ASCII
    s = expr
    for unicode_op, ascii_op in _UNICODE_OPERATORS.items():
        s = s.replace(unicode_op, ascii_op)
    
    while True:
        # Replace A op B%
        m = _percent_pair.search(s)
        if not m:
            break
        a, op, b = m.group("a", "op", "b")
        if op in "+-":
            repl = f"{a} {op} (({b}/100)*{a})"
        elif op == "*":
            repl = f"{a} * ({b}/100)"
        else:
            repl = f"{a} / ({b}/100)"
        s = s[:m.start()] + repl + s[m.end():]

    # Replace B%
    s = _number_percent.sub(lambda m: f"({m.group('n')}/100)", s)
    return s

