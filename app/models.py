from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    # Relationship to calculator_logs
    calculator_logs = relationship("CalculatorLog", back_populates="session")


class CalculatorLog(Base):
    __tablename__ = "calculator_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    expr = Column(Text, nullable=False)
    result = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    session_id = Column(Integer, ForeignKey("session.id"), nullable=True)

    # Relationship to session
    session = relationship("Session", back_populates="calculator_logs")

