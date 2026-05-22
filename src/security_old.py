import time
from typing import Annotated
from pydantic import BaseModel
import jwt
import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET = "senha_top_secret"
ALGORITHM = "HS256"

class AccessToken(BaseModel):
    iss: str
    sub: int
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str

class JWTToken(BaseModel):
    access_token: AccessToken

auth = APIRouter() # REVER ESTA LINHA

def sign_jwt(user_id: int) -> JWTToken:
    now = time.time()
    payload = {
        "iss": "fhp_bancario_fastapi.com.br",
        "sub": user_id,
        "aud": "fhp_bancario_fastapi",
        "exp": now + (60 * 60),  # 60 minutos
        "iat": now,
        "nbf": now,
        "jti": uuid.uuid4().hex,
    } 
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return {"access_token": token }


async def decode_jwt(token: str) -> AccessToken:
    try:
        decoded_token = jwt.decode(token, SECRET, audience="fhp_bancario_fastapi", algorithms=[ALGORITHM])
        _token = JWTToken.model_validate({"access_token": decoded_token})
        # return _token if _token.access_token.exp >= time.time() else None
        return AccessToken.model_validate(decoded_token)
    except Exception:
       return None
    
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> JWTToken:
        authorization =request.headers.get("Authorization", "")
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
        
async def get_current_user(token: Annotated[JWTToken , Depends(JWTBearer())],) -> dict[str, int]:
    return {"user_id": token.access_token.sub}

def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ACESSO NEGADO: USUÁRIO NÃO AUTENTICADO",
        )
    return current_user