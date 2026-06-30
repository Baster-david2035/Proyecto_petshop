from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller.client_controller import router as cliente_router
from controller.pet_controller import router as mascota_router
from controller.extra_service_controller import router as servicio_router
from controller.adoption_controller import router as adopcion_router
from controller.user_controller import router as usuario_router

app = FastAPI(title="Sistema de Adopciones")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cliente_router)
app.include_router(mascota_router)
app.include_router(servicio_router)
app.include_router(adopcion_router)
app.include_router(usuario_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)