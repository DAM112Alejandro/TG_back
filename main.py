from fastapi import FastAPI
from routers import tipoUsuario, tipoSub, usuario, clases, reservas , tipoClase
from auth import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

app.include_router(tipoSub.router)
app.include_router(tipoUsuario.router)
app.include_router(usuario.router)
app.include_router(clases.router)
app.include_router(reservas.router)
app.include_router(tipoClase.router)
app.include_router(auth.router)
