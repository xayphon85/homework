import math
from datetime import datetime
from fastapi import APIRouter, Depends
from asteval import Interpreter
from typing import List

from app.dependencies import expand_percent, get_history
from app.schemas import Expression

# Create router
router = APIRouter()

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@router.post("/calculate")
def calculate(expression: Expression, history = Depends(get_history)):
    try:
        code = expand_percent(expression.expr)
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expression.expr, "result": "", "error": msg}
        history.appendleft({
            "timestamp": datetime.now().isoformat() + "Z",
            "expr": expression.expr,
            "result": result,
        })
        return {"ok": True, "expr": expression.expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expression.expr, "error": str(e)}
