from pydantic_settings import BaseSettings


class Configuracion(BaseSettings):
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 480
    environment: str = "development"

    class Config:
        env_file = ".env"


configuracion = Configuracion()
