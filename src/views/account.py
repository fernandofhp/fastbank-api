from pydantic import BaseModel, AwareDatetime, NaiveDatetime, PositiveFloat

class AccountOut(BaseModel):
    id: int
    balance: float
    created_at: AwareDatetime | NaiveDatetime