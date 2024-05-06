from fastapi import FastAPI
from routers import tipoUsuario, tipoSub, usuario, clases, reservas 

app = FastAPI()
app.include_router(tipoSub.router)
app.include_router(tipoUsuario.router)
app.include_router(usuario.router)
app.include_router(clases.router)
app.include_router(reservas.router)
