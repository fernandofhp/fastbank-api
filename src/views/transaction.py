from pydantic import AwareDatetime, BaseModel, NaiveDatetime

class TransactionOut(BaseModel):
    id: int
    account_id: int
    type: str
    amount: float
    timestamp: AwareDatetime | NaiveDatetime