
from ast import List
from databases.interfaces import Record
from src.database import database
from src.exceptions import ErroContaNaoEncontrada
from src.exceptions import ErroRegrasDeNegocios
from src.schemas.transaction import TransactionIn
from src.models.transaction import transactions, TransactionType
from src.models.account import accounts


class TransactionService:
    async def read_all(self, account_id: int, limit: int, skip: int=0) -> List[Record]:
        query = transactions.select().where(transactions.c.account_id==account_id).limit(limit).offset(skip)
        return await database.fetch_all(query)
    
    @database.transaction()
    async def create(self, transaction: TransactionIn) -> Record:
        query = accounts.select().where(accounts.c.id==transaction.account_id)
        account = await database.fetch_one(query)
        if not account:
            raise ErroContaNaoEncontrada
        
        if transaction.type == TransactionType.WITHDRAWAL:
            balance = float(account.balance) - transaction.amount
            if balance < 0:
                raise ErroRegrasDeNegocios("OPERAÇÂO NÃO REALIZADA: SALDO INSUFICIENTE!")
        else:
            balance = float(account.balance) + transaction.amount
        # CRIA ENTRADA PARA Transação
        transaction_id = await self.__regitrar_transacao(transaction)
        # ATUALIZA SALDO EM CONTA
        await self.__atualiza_saldo_em_conta(transaction.account_id, balance)

        query = transactions.select().where(transactions.c.id==transaction_id)
        return await database.fetch_one(query)

    async def __atualiza_saldo_em_conta(self, account_id: int, balance: float) -> None:
        query = accounts.update().where(accounts.c.id==account_id).values(balance=balance)
        await database.execute(query)

    async def __regitrar_transacao(self, transaction: TransactionIn) -> int:
        query = transactions.insert().values(
            account_id = transaction.account_id,
            type = transaction.type,
            amount = transaction.amount,
        )
        return await database.execute(query)
        