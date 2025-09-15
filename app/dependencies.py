# app/dependencies.py
from __future__ import annotations

import math, re
from collections import deque
from typing import Any, Deque, Tuple
from fastapi import HTTPException
from asteval import Interpreter
from app.schemas import ExpressionIn

_percent_pair = re.compile(r"""
    (?P<a>\d+(?:\.\d+)?)
    \s*(?P<op>[+\-*/])\s*
    (?P<b>\d+(?:\.\d+)?)%
""", re.VERBOSE)
_number_percent = re.compile(r"(?P<n>\d+(?:\.\d+)?)%")

def expand_percent(expr: str) -> str:
    s = expr
    while True:
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
    s = _number_percent.sub(lambda m: f"({m.group('n')}/100)", s)
    return s

def expand_percent_dep(payload: ExpressionIn) -> Tuple[ExpressionIn, str]:
    """Read the request body once, expand it, and return (original, code)."""
    try:
        code = expand_percent(payload.expr)
        code = code.replace("÷", "/").replace("×", "*")
        return payload, code
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid expression: {e}")

HISTORY_MAX = 1000
history: Deque[Any] = deque(maxlen=HISTORY_MAX)

aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})

def get_history():
    return history
