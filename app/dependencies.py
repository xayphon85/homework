# dependencies.py
from collections import deque
from app.calculator import expand_percent as _expand_percent

HISTORY_MAX = 1000
history = deque(maxlen=HISTORY_MAX)

def expand_percent(expr: str) -> str:
    """
    Expand % symbols in an arithmetic expression.

    Thin wrapper that defers to calculator.expand_percent for the logic,
    but keeps your FastAPI dependency-style import surface here.
    """
    return _expand_percent(expr)

def get_history():
    """
    Dependency that returns the in-memory history deque.
    """
    return history