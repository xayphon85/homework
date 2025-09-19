from fastapi import APIRouter, Depends
from typing import List

from app.dependencies import get_history
from app.schemas import CalculatorLog

# Create router
router = APIRouter()


@router.get("/history")
def get_history_endpoint(limit: int = 50, history = Depends(get_history)) -> List[CalculatorLog]:
    return [CalculatorLog(**item) for item in list(history)[: max(0, min(limit, 1000))]]


@router.delete("/history")
def clear_history(history = Depends(get_history)):
    history.clear()
    return {"ok": True, "cleared": True}
