import src.database as database
from src.models.account import accounts
import src.schemas.account as accountIn

class AccountIn:
    user_id: int
    balance: float
    
class AccountService:
    async def read_all(self, limit: int, skip: int = 0):
        query = accounts.select().limit(limit).offset(skip)
        return await database.database.fetch_all(query)
    
    async def create(self, account: accountIn.AccountCreate):
        # ::STANDARD:: query = accounts.insert().values(user_id=account.user_id, balance=account.balance)
        # ::DEPRECATED:: query = accounts.insert().values(**account.dict())
        query = accounts.insert().values(**account.model_dump()) # ::IMPROVED::
        account_id = await database.database.execute(query)
        query = accounts.select().where(accounts.c.id == account_id)
        return await database.database.fetch_one(query)