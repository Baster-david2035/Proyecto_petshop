from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import init_db
from app.controller.client_controller import router as cliente_router
from app.controller.pet_controller import router as mascota_router
from app.controller.extra_service_controller import router as servicio_router
from app.controller.adoption_controller import router as adopcion_router
from app.controller.user_controller import router as usuario_router
from app.controller.solicitud_controller import router as solicitud_router

app = FastAPI(title="Sistema de Adopciones")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
init_db()
app.include_router(cliente_router)
app.include_router(mascota_router)
app.include_router(servicio_router)
app.include_router(usuario_router)
app.include_router(solicitud_router)
app.include_router(adopcion_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)