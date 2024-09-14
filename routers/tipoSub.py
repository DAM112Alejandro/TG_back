from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException ,status
from db.schemas.tipoSub import tipoSubSchema , tipoSubsSchema
from db.models.tipoSub import tipoSub
from db.client import db
from auth.auth import isLogged, isAdmin

router = APIRouter(prefix="/tipoSub", tags=["tipoSub"],responses={404: {"message" : "No encontrado"}})

@router.get("")
async def tiposub(token = Depends(isAdmin)):
    return tipoSubsSchema(db.tipoSub.find())

@router.get("/{id}")
async def tiposub_id(id: str ,token = Depends(isAdmin)):
    return searchTipoSub("_id", ObjectId(id))

@router.get("/desc/{descripcion}")
async def tiposub_desc(descripcion: str,token = Depends(isAdmin)):
    return tipoSubSchema(db.tipoSub.find_one({"descripcion": descripcion}))


@router.post("/add", response_model=tipoSub, status_code=status.HTTP_201_CREATED)
async def addTipoSub(newTipoSub : tipoSub, token = Depends(isAdmin)):
    if type(searchTipoSub("descripcion",newTipoSub.descripcion)) == tipoSub : 
        raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND , detail = ("El tipo de sub ya existe"))
    
    tipoSub_dict = dict(newTipoSub)
    del tipoSub_dict["id"]
    
    id = db.tipoSub.insert_one(tipoSub_dict).inserted_id
    return tipoSubSchema(db.tipoSub.find_one({"_id": ObjectId(id)}))
    
    
    
@router.put('/update')
async def updateTipoSub(updateTipoSub: tipoSub, token = Depends(isAdmin)):
    tipoSub_dict = dict(updateTipoSub)
    del tipoSub_dict["id"]
    
    try:
        db.tipoSub.find_one_and_replace({"_id": ObjectId(updateTipoSub.id)}, tipoSub_dict)
    except:
        return {"error" : " No se ha actualizado el tipo de usuario"}

    return searchTipoSub("_id" , ObjectId(updateTipoSub.id))

@router.delete("/delete/{id}" , status_code=status.HTTP_204_NO_CONTENT)
async def deleteTipoSub(id: str ,token = Depends(isAdmin)):
    found = db.tipoSub.find_one_and_delete({"_id" : id})
    if not found:
        return {"error" : "No se ha eliminado el tipo de usuario"}
    

def searchTipoSub(field :str, key):
    try:
        tipousub = db.tipoSub.find_one({field: key})
        return tipoSub(**tipoSubSchema(tipousub))
    except:
        return { "error" : "No se ha encontrado el tipo de subscripcion"}