from pydantic import BaseModel


class CredencialesLogin(BaseModel):
    email: str
    contrasena: str


class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UsuarioActual(BaseModel):
    id: str
    email: str
    rol: str
    nombre_completo: str
