from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import configuracion

contexto_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITMO = "HS256"


def hashear_contrasena(contrasena: str) -> str:
    return contexto_pwd.hash(contrasena)


def verificar_contrasena(contrasena: str, hash: str) -> bool:
    return contexto_pwd.verify(contrasena, hash)


def crear_token_acceso(datos: dict) -> str:
    payload = datos.copy()
    expira = datetime.now(timezone.utc) + timedelta(
        minutes=configuracion.access_token_expire_minutes
    )
    payload["exp"] = expira
    return jwt.encode(payload, configuracion.secret_key, algorithm=ALGORITMO)


def decodificar_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, configuracion.secret_key, algorithms=[ALGORITMO])
    except JWTError:
        return None
