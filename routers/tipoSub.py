from fastapi import APIRouter
from db.schemas.tipoSub import tipoSubSchema , tipoSubsSchema
from db.models.tipoSub import tipoSub
from db.client import db

router = APIRouter(prefix="/tipoSub", tags=["tipoSub"],responses={404: {"message" : "No encontrado"}})

@router.get("")
async def tiposub():
    return { "message" : "Hola tipos de sub" }

def searchTipoSub(field :str, key):
    try:
        tipousub = db.tipoSub.find_one({field: key})
        return tipoSub(**tipoSubSchema(tipousub))
    except:
        return { "error" : "No se ha encontrado el tipo de subscripcion"}