from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.controllers import account, auth, transaction
from src.database import database
from src.exceptions import ErroContaNaoEncontrada, ErroRegrasDeNegocios
from src.database import database, init_db

router = APIRouter()

@asynccontextmanager
async def lifespan(app: FastAPI):  
    init_db()  
    await database.connect()
    yield
    await database.disconnect()

tags_metadata = [  
    {
        "name": "auth",  
        "description": "operações de autenticação.",
    },
    {
        "name": "transacoes",  
        "description": "operações de saques e depósitos.",
    },
    {
        "name": "contas",  
        "description": "operações de gerenciamento de conta.",
    },
]  

app = FastAPI(
    title="ContaAtivaFlux API",
    version="1.0.0",
    summary="Microserviço de Gerencimanto de Saques e Depósitos em conta corrente atual",
    description="""
        ContaAtivaFlux API é o microserviço que gerencia saques, depósitos e registra tranzações banacárias

        # CONTAS (Account)
        • Cria contas
        • Lista contas
        • Lista Transações da conta por Código (ID)

        # TRANSAÇÕES (TANSACTIONS)
        • Realiza e registra tranzações
    """,
    openapi_tags=tags_metadata,
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["auth"])
app.include_router(account.router, tags=["account"])
app.include_router(transaction.router, tags=["transaction"])

@app.exception_handler(ErroContaNaoEncontrada)
def erro_conta_nao_encontrada_handler(request: Request, exc: ErroContaNaoEncontrada):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "CONTA NÃO ENCONTRADA"})

@app.exception_handler(ErroRegrasDeNegocios)
def erro_regras_negocio_handler(request: Request, exc: ErroRegrasDeNegocios):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})