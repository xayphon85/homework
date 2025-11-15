# dependencies.py
from collections import deque
from fastapi import Cookie, Response, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.calculator import expand_percent as _expand_percent
from app.core.db import get_db as _get_db
from app.models import Session as SessionModel

HISTORY_MAX = 1000
history = deque(maxlen=HISTORY_MAX)

def expand_percent(expr: str) -> str:
    """
    Expand % symbols in an arithmetic expression.

    Thin wrapper that defers to calculator.expand_percent for the logic,
    but keeps your FastAPI dependency-style import surface here.
    """
    return _expand_percent(expr)

def get_history():
    """
    Dependency that returns the in-memory history deque.
    """
    return history


def get_or_create_session(
    response: Response,
    session_id: str | None = Cookie(None),
    x_session_name: Optional[str] = Header(None, alias="X-Session-Name"),
    db: Session = Depends(_get_db)
) -> SessionModel:
    """
    Dependency that gets or creates a session based on cookie.
    If no session_id cookie exists, creates a new session and sets the cookie.
    Frontend can send X-Session-Name header to set/update the session name.
    """
    if session_id:
        try:
            session_id_int = int(session_id)
            # Try to get existing session
            session = db.query(SessionModel).filter(SessionModel.id == session_id_int).first()
            if session and session.ended_at is None:
                # Valid active session - update name if provided
                if x_session_name and x_session_name.strip():
                    session.name = x_session_name.strip()
                    db.commit()
                    db.refresh(session)
                
                # Ensure cookie is set
                response.set_cookie(
                    key="session_id",
                    value=str(session.id),
                    max_age=86400 * 30,  # 30 days
                    httponly=True,
                    samesite="lax"
                )
                return session
        except (ValueError, TypeError):
            # Invalid session_id, create new one
            pass
    
    # Create new session with name from header if provided
    new_session = SessionModel(
        name=x_session_name.strip() if x_session_name and x_session_name.strip() else None,
        started_at=datetime.utcnow(),
        ended_at=None
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    # Set cookie
    response.set_cookie(
        key="session_id",
        value=str(new_session.id),
        max_age=86400 * 30,  # 30 days
        httponly=True,
        samesite="lax"
    )
    
    return new_session