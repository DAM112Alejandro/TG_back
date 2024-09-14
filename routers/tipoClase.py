from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException ,status
from db.schemas.tipoClase import tipoClaseSchema, tipoClasesSchema
from db.models.tipoClase import tipoClase
from db.client import db
from auth.auth import isLogged, isAdmin

router = APIRouter(prefix="/tipoClase", tags=["tipoClase"],responses={404: {"message" : "No encontrado"}})

@router.get("")
async def tipoclase(token = Depends(isAdmin)):
    return tipoClasesSchema(db.tipoClase.find())

@router.get("/{id}")
async def tipoclase_id(id: str,token = Depends(isAdmin)):
    return searchTipoClase("_id", ObjectId(id))

@router.get("/desc/{descripcion}")
async def tipoclase_desc(descripcion: str,token = Depends(isAdmin)):
    return tipoClaseSchema(db.tipoClase.find_one({"descripcion": descripcion}))

@router.post("/add", response_model=tipoClase, status_code=status.HTTP_201_CREATED)
async def addTipoClase(newTipoClase : tipoClase,token = Depends(isAdmin)):
    if type(searchTipoClase("descripcion",newTipoClase.descripcion)) == tipoClase : 
        raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND , detail = ("El tipo de sub ya existe"))
    
    tipoClase_dict = dict(newTipoClase)
    del tipoClase_dict["id"]
    
    id = db.tipoClase.insert_one(tipoClase_dict).inserted_id
    return tipoClaseSchema(db.tipoSub.find_one({"_id": ObjectId(id)}))
    
    
    
@router.put('/update')
async def updateTipoClase(updateTipoClase: tipoClase,token = Depends(isAdmin)):
    tipoClase_dict = dict(updateTipoClase)
    del tipoClase_dict["id"]
    
    try:
        db.tipoClase.find_one_and_replace({"_id": ObjectId(updateTipoClase.id)}, tipoClase_dict)
    except:
        return {"error" : " No se ha actualizado el tipo de clase"}

    return searchTipoClase("_id" , ObjectId(updateTipoClase.id))

@router.delete("/delete/{id}" , status_code=status.HTTP_204_NO_CONTENT)
async def deleteTipoClase(id: str,token = Depends(isAdmin)):
    found = db.tipoClase.find_one_and_delete({"_id" : id})
    if not found:
        return {"error" : "No se ha eliminado el tipo de clase"}
    

def searchTipoClase(field :str, key):
    try:
        tipoclase = db.tipoClase.find_one({field: key})
        return tipoClase(**tipoClaseSchema(tipoclase))
    except:
        return { "error" : "No se ha encontrado el tipo de clase"}