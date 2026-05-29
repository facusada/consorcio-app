from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import configuracion

ALGORITMO = "HS256"


def hashear_contrasena(contrasena: str) -> str:
    return bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()


def verificar_contrasena(contrasena: str, hash: str) -> bool:
    return bcrypt.checkpw(contrasena.encode(), hash.encode())


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
