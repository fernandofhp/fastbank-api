from enum import Enum
from pydantic import BaseModel, ConfigDict, PositiveFloat

class TransactionType(str, Enum):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'

class TransactionIn(BaseModel):
    account_id: int
    type: TransactionType
    amount: PositiveFloat

    class Config:
        # ::OLD:: use_enum_values = True
        # Formato moderno do Pydantic v2:
        model_config = ConfigDict(use_enum_values=True)