from fastapi import APIRouter ,status, HTTPException
from db.models.tipoUsuario import tipoUsuario
from db.client import db
from db.schemas.tipoUsuario import tipoUsuarioSchema ,tipoUsuariosSchema
from bson import ObjectId

router = APIRouter(prefix="/tipoUsuario", tags=["tipoUsuario"],responses={status.HTTP_404_NOT_FOUND: {"message" : "No encontrado"}})

@router.get("" , response_model=list[tipoUsuario])
async def findTipoUsuario():
    return tipoUsuariosSchema(db.tipoUsuario.find())

@router.get("/{id}")
async def searchTipoUsuario(id: str):
    return searchTipoUsuario("_id" , ObjectId(id))

@router.post("/add", response_model=tipoUsuario, status_code=status.HTTP_201_CREATED)
async def addTipoUser(newTipousuario: tipoUsuario):
    
    if type(searchTipoUsuario("descripcion",newTipousuario.descripcion)) == tipoUsuario : 
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND , detail = ("El tipo de usuario ya existe"))
    
    tipoUsuario_dict = dict(newTipousuario)
    del tipoUsuario_dict["id"]
    
    id = db.tipoUsuario.insert_one(tipoUsuario_dict).inserted_id
    new_Tipo_Usuario = tipoUsuarioSchema(db.tipoUsuario.find_one({"_id": ObjectId(id)}))
    
    return tipoUsuario(**new_Tipo_Usuario)

@router.put("/update", response_model=tipoUsuario)
async def updateTipoUsuario(updateTipoUsuario: tipoUsuario):
    tipoUsuario_dict = dict(updateTipoUsuario)
    del tipoUsuario_dict["id"]
    
    try:
        db.tipoUsuario.find_one_and_replace({"_id": ObjectId(updateTipoUsuario.id)}, tipoUsuario_dict)
    except:
        return {"error" : " No se ha actualizado el tipo de usuario"}

    return searchTipoUsuario("_id" , ObjectId(updateTipoUsuario.id))

@router.delete("/delete/{id}" , status_code=status.HTTP_204_NO_CONTENT)
async def deleteTipoUser(id: str):
    found = db.tipoUsuarios.find_one_and_delete({"_id" : id})
    if not found:
        return {"error" : "No se ha eliminado el tipo de usuario"}
    
def searchTipoUsuario(field :str, key):
    try:
        tipousuario = db.tipoUsuario.find_one({field: key})
        return tipoUsuario(**tipoUsuarioSchema(tipousuario))
    except:
        return { "error" : "No se ha encontrado el tipo de usuario"}
    

    
