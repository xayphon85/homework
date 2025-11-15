import math
from datetime import datetime
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from asteval import Interpreter

from app.dependencies import expand_percent, get_or_create_session
from app.schemas import Expression
from app.core.db import get_db
from app.models import CalculatorLog, Session as SessionModel

# Create router
router = APIRouter()

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@router.post("/calculate")
def calculate(
    expression: Expression,
    response: Response,
    db: Session = Depends(get_db),
    session: SessionModel = Depends(get_or_create_session)
):
    try:
        code = expand_percent(expression.expr)
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expression.expr, "result": "", "error": msg}
        
        # Save to database with session
        log_entry = CalculatorLog(
            expr=expression.expr,
            result=float(result),
            timestamp=datetime.utcnow(),
            session_id=session.id
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        
        return {"ok": True, "expr": expression.expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expression.expr, "error": str(e)}
