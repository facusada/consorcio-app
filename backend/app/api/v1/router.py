from fastapi import APIRouter

from app.api.v1.endpoints import auth, periodos, propietarios, unidades

router = APIRouter(prefix="/api/v1")
router.include_router(auth.router)
router.include_router(unidades.router)
router.include_router(propietarios.router)
router.include_router(periodos.router)
