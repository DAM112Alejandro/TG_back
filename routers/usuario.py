from bson import ObjectId
from fastapi import APIRouter ,status, HTTPException
from db.models.usuario import usuario
from db.client import db
from db.schemas.usuario import usuarioSchema , usuariosSchema

router = APIRouter(prefix="/usuario", tags=["usuario"],responses={404: {"message" : "No encontrado"}})

@router.get("",response_model=list[usuario])
async def findUsuarios():
    return usuariosSchema(db.usuario.find())

@router.get("/{id}")
async def searchUsuario(id: str):
    return searchUsuario("_id" , ObjectId(id))

@router.post("/add", response_model=usuario, status_code=status.HTTP_201_CREATED)
async def addUser(newUsuario: usuario):
    
    if type(searchUsuario("email",newUsuario.email)) == usuario : 
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND , detail = ("El usuario ya existe"))
    
    usuario_dict = dict(newUsuario)
    del usuario_dict["id"]
    
    id = db.usuario.insert_one(usuario_dict).inserted_id
    new_Usuario = usuarioSchema(db.usuario.find_one({"_id": ObjectId(id)}))
    
    return usuario(**new_Usuario)

@router.put("/update", response_model=usuario)
async def updateUsuario(updateUsuario: usuario):
    usuario_dict = dict(updateUsuario)
    del usuario_dict["id"]
    
    try:
        db.usuario.find_one_and_replace({"_id": ObjectId(updateUsuario.id)}, usuario_dict)
    except:
        return {"error" : " No se ha actualizado el usuario"}

    return searchUsuario("_id" , ObjectId(updateUsuario.id))

@router.delete("/delete/{id}" , status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(id: str):
    found = db.usuarios.find_one_and_delete({"_id" : id})
    if not found:
        return {"error" : "No se ha eliminado el usuario"}

def searchUsuario(field :str, key):
    try:
        usuario = db.usuario.find_one({field: key})
        return usuarioSchema(**usuarioSchema(usuario))
    except:
        return { "error" : "No se ha encontrado el usuario"}