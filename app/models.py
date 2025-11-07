from sqlmodel import SQLModel, Field

class CalculatorLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    expression: str
    result: float