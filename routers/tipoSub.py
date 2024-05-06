from fastapi import APIRouter

router = APIRouter(prefix="/tipoSub", tags=["tipoSub"],responses={404: {"message" : "No encontrado"}})

@router.get("")
async def tiposub():
    return { "message" : "Hola tipos de sub" }