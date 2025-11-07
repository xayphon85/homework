from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from database import init_db, get_session
from models import CalculatorLog
from asteval import Interpreter

app = FastAPI()
init_db()

aeval = Interpreter()

@app.post("/calculate")
def calculate(expression: str, session: Session = Depends(get_session)):
    result = aeval(expression)
    log = CalculatorLog(expression=expression, result=result)
    session.add(log)
    session.commit()
    session.refresh(log)
    return {"expression": expression, "result": result}

@app.get("/history")
def get_history(session: Session = Depends(get_session)):
    logs = session.exec(select(CalculatorLog)).all()
    return logs

@app.delete("/history")
def clear_history(session: Session = Depends(get_session)):
    session.exec("DELETE FROM calculatorlog")
    session.commit()
    return {"message": "History cleared"}
