# schemas.py
from pydantic import BaseModel

# ---- Base ----
class BaseExpression(BaseModel):
    expr: str

# ---- In (request) ----
class ExpressionIn(BaseExpression):
    """Payload coming in from client."""
    pass

# Keep the original name for compatibility if other modules import Expression
Expression = ExpressionIn

# ---- Out (response / log) ----
class CalculatorLog(ExpressionIn):
    """Log/response that extends the input with computed fields."""
    timestamp: str
    result: float

# Alias per the practice guideline
ExpressionOut = CalculatorLog
