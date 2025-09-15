from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.calculator import router as calculator_router
from app.routers.history   import router as history_router
#ajsdjf
app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calculator_router)
app.include_router(history_router)
