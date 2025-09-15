from fastapi import APIRouter, Depends
from app.dependencies import get_history, HISTORY_MAX
from app.schemas import CalculatorLog

router = APIRouter()

@router.get("/history")
def get_history_items(limit: int = 50, history = Depends(get_history)) -> list[CalculatorLog]:
    return list(history)[: max(0, min(limit, HISTORY_MAX))]

@router.delete("/history")
def clear_history_items(history = Depends(get_history)):
    history.clear()
    return {"ok": True, "cleared": True}
