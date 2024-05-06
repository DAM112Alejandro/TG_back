from fastapi import APIRouter

router = APIRouter(prefix="/reserva", tags=["reserva"],responses={404: {"message" : "No encontrado"}})

@router.get("/")
async def reserva():
    return { "message" : "Hola reservas" }