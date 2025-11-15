from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List

from app.schemas import CalculatorLog, SessionInfo, SessionNameUpdate
from app.core.db import get_db
from app.dependencies import get_or_create_session
from app.models import CalculatorLog as CalculatorLogModel, Session as SessionModel

# Create router
router = APIRouter()


@router.get("/session")
def get_session_info(
    response: Response = None,
    session: SessionModel = Depends(get_or_create_session)
) -> SessionInfo:
    """Get current session information."""
    return SessionInfo(
        id=session.id,
        name=session.name,
        started_at=session.started_at.isoformat() + "Z",
        ended_at=session.ended_at.isoformat() + "Z" if session.ended_at else None
    )


@router.put("/session/name")
def update_session_name(
    name_update: SessionNameUpdate,
    response: Response = None,
    db: Session = Depends(get_db),
    session: SessionModel = Depends(get_or_create_session)
) -> SessionInfo:
    """Update the name of the current session."""
    session.name = name_update.name.strip() if name_update.name.strip() else None
    db.commit()
    db.refresh(session)
    
    return SessionInfo(
        id=session.id,
        name=session.name,
        started_at=session.started_at.isoformat() + "Z",
        ended_at=session.ended_at.isoformat() + "Z" if session.ended_at else None
    )


@router.get("/history")
def get_history_endpoint(
    limit: int = 50,
    response: Response = None,
    db: Session = Depends(get_db),
    session: SessionModel = Depends(get_or_create_session)
) -> List[CalculatorLog]:
    # Query logs from database filtered by session, ordered by timestamp descending (most recent first)
    logs = (
        db.query(CalculatorLogModel)
        .filter(CalculatorLogModel.session_id == session.id)
        .order_by(desc(CalculatorLogModel.timestamp))
        .limit(max(0, min(limit, 1000)))
        .all()
    )
    
    # Convert to Pydantic models
    return [
        CalculatorLog(
            expr=log.expr,
            result=log.result,
            timestamp=log.timestamp.isoformat() + "Z"
        )
        for log in logs
    ]


@router.delete("/history")
def clear_history(
    response: Response = None,
    db: Session = Depends(get_db),
    session: SessionModel = Depends(get_or_create_session)
):
    # Delete calculator logs for current session only
    db.query(CalculatorLogModel).filter(CalculatorLogModel.session_id == session.id).delete()
    db.commit()
    return {"ok": True, "cleared": True}
