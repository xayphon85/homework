from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.db import init_db
from routers.calculator import router as calculator_router
from routers.history import router as history_router

logger = logging.getLogger(__name__)

app = FastAPI(title="Mini Calculator API")

# CORS configuration
# Note: When allow_credentials=True, browsers don't allow allow_origins=["*"]
# For production, specify exact origins. For development, we allow all origins
# but credentials might not work with wildcard - use specific origin or same-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins like ["http://localhost:3000"]
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,  # Required for cookies to work
    expose_headers=["*"],  # Expose all headers including Set-Cookie
)


@app.on_event("startup")
def startup_event():
    """Initialize database tables on startup."""
    logger.info("Waiting for database connection...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


# Include routers
app.include_router(calculator_router)
app.include_router(history_router)
