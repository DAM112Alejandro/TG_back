from bson import ObjectId
from fastapi import APIRouter, Depends, status , HTTPException
from db.client import db
from db.models.clase import clase
from db.schemas.clase import clasesSchema, claseSchema
from auth.auth import isLogged, isAdmin

router = APIRouter(prefix="/clases", tags=["clases"],responses={404: {"message" : "No encontrado"}})

@router.get("",response_model=list[clase])
async def findClases():
    return clasesSchema(db.clase.find())
    
@router.get("/{id}")
async def searchClase(id: str):
    return searchClase("_id" , ObjectId(id))

@router.post("/add", response_model=clase, status_code=status.HTTP_201_CREATED)
async def addClase(newClase: clase ,token = Depends(isAdmin)):
    
    if type(searchClase("descripcion",newClase.descripcion)) == clase : 
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND , detail = ("La clase ya existe"))
    
    clase_dict = dict(newClase)
    del clase_dict["id"]
    
    id = db.clase.insert_one(clase_dict).inserted_id
    new_Clase = claseSchema(db.clase.find_one({"_id": ObjectId(id)}))
    
    return clase(**new_Clase)

@router.put("/update", response_model=clase)
async def updateClase(updateClase: clase , token = Depends(isAdmin)):
    clase_dict = dict(updateClase)
    del clase_dict["id"]
    
    try:
        db.clase.find_one_and_replace({"_id": ObjectId(updateClase.id)}, clase_dict)
    except:
        return {"error" : " No se ha actualizado la clase"}

    return searchClase("_id" , ObjectId(updateClase.id))

@router.delete("/delete/{id}" , status_code=status.HTTP_204_NO_CONTENT)
async def deleteClase(id: str, token = Depends(isAdmin)):
    found = db.clase.find_one_and_delete({"_id" : id})
    if not found:
        return {"error" : "No se ha eliminado la clase"}

def searchClase(field :str, key):
    try:
        clasef = db.clase.find_one({field: key})
        return clase(**claseSchema(clasef))
    except:
        return { "error" : "No se ha encontrado la clase"}
    
    
    