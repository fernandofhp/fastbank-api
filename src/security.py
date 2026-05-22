import time
from typing import Annotated
from pydantic import BaseModel
import jwt
import uuid
from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.security import HTTPBearer

SECRET = "senha_top_secret"
ALGORITHM = "HS256"

# Modelo que representa exatamente a estrutura interna do payload do seu JWT
class AccessToken(BaseModel):
    iss: str
    sub: str
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str

auth = APIRouter()

def sign_jwt(user_id: int) -> dict:
    now = time.time()
    payload = {
        "iss": "fhp_bancario_fastapi.com.br",
        "sub": str(user_id),
        "aud": "fhp_bancario_fastapi",
        "exp": now + (60 * 60),  # 60 minutos de validade
        "iat": now,
        "nbf": now,
        "jti": uuid.uuid4().hex,
    } 
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

async def decode_jwt(token: str) -> AccessToken | None:
    try:
        # O PyJWT já valida o 'exp' e o 'aud' automaticamente aqui.
        decoded_token = jwt.decode(
            token, 
            SECRET, 
            audience="fhp_bancario_fastapi", 
            algorithms=[ALGORITHM],
            options={"leeway": 300}
        )
        
        # Valida os dados decodificados direto contra o modelo AccessToken
        return AccessToken.model_validate(decoded_token)
        
    except jwt.ExpiredSignatureError:
        print("❌ Validação falhou: O token enviado já está expirado.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"❌ Validação falhou: Assinatura ou token inválido. Erro: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado na validação do Pydantic: {e}")
        return None
    
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> AccessToken:
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        if credentials:
            if not scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="ESQUEMA DE AUTENTICAÇÃO INVÁLIDO",
                )
            
            payload = await decode_jwt(credentials)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="TOKEN DE AUTENTICAÇÃO INVÁLIDO OU EXPIRADO",
                )
            return payload
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="CREDENCIAIS DE AUTENTICAÇÃO NÃO FORNECIDAS OU INVÁLIDAS",
            )
        
async def get_current_user(token: Annotated[AccessToken, Depends(JWTBearer())]) -> dict[str, int]:
    # Como o decode_jwt retorna o AccessToken puro, acessamos o .sub direto aqui
    return {"user_id": int(token.sub)}

def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ACESSO NEGADO: USUÁRIO NÃO AUTENTICADO",
        )
    return current_user