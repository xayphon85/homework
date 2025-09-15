# calculator-server/app/schemas.py
from typing import Any
from pydantic import BaseModel
from datetime import datetime

class BaseExpression(BaseModel):
    expr: str

# ExpressionIn = what the client sends
class ExpressionIn(BaseExpression):
    pass

# ExpressionOut = what the server returns about an expression
class ExpressionOut(BaseExpression):
    result: Any | None = None
    timestamp: str | None = None

# CalculatorLog is a specific kind of ExpressionOut stored in history
class CalculatorLog(ExpressionOut):
    result: Any
    timestamp: str = datetime.now().isoformat() + "Z"
