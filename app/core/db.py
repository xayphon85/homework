import os
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, DeclarativeBase

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@mysql:3306/calculator_server"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


def wait_for_db(max_retries=30, retry_interval=2):
    """Wait for database to be ready with retry logic."""
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection established")
            return True
        except OperationalError as e:
            if attempt < max_retries - 1:
                logger.warning(f"Database not ready, retrying in {retry_interval}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_interval)
                continue
            else:
                logger.error(f"Failed to connect to database after {max_retries} attempts")
                raise
    return False


def init_db():
    """Create all tables in the database."""
    from app.models import Session, CalculatorLog
    
    # Wait for database to be ready
    wait_for_db()
    
    # Create tables
    Base.metadata.create_all(bind=engine)


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
