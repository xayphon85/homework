from pydantic import BaseModel
from typing import List


class Expression(BaseModel):
    expr: str
    
    def expand_percent(self, expr: str) -> str:
        """Expand the % symbols in the expression"""
        from calculator import expand_percent
        return expand_percent(expr)


class CalculatorLog(BaseModel):
    timestamp: str
    expr: str
    result: float
