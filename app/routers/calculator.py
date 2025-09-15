# app/routers/calculator.py
from datetime import datetime
from fastapi import APIRouter, Depends
from app.schemas import CalculatorLog, ExpressionIn
from app.dependencies import aeval, expand_percent_dep, get_history

router = APIRouter()

@router.post("/calculate")
def calculate(
    expr_and_code: tuple[ExpressionIn, str] = Depends(expand_percent_dep),
    history = Depends(get_history),
):
    expr_in, code = expr_and_code
    try:
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr_in, "result": "", "error": msg}

        log = CalculatorLog(
            expr=expr_in.expr,
            result=result,
            timestamp=datetime.now().isoformat() + "Z",
        )
        history.appendleft(log)
        return {"ok": True, "expr": expr_in, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr_in, "error": str(e)}

    return {"ok": True, "expr": {"expr": expr_in.expr}, "result": result, "error": ""}
