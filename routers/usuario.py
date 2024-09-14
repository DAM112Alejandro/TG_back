from operator import truediv
from unittest import result
from bson import ObjectId
from fastapi import APIRouter, Depends ,status, HTTPException
from db.models.usuario import usuario
from db.client import db
from db.schemas.usuario import usuarioSchema , usuariosSchema
from auth.auth import isLogged, isAdmin

router = APIRouter(prefix="/usuario", tags=["usuario"],responses={404: {"message" : "No encontrado"}})

@router.get("")
async def findUsuarios(token = Depends(isAdmin)):
    usuarios = list(db.usuario.find())
    for usuario in usuarios:
        tipo_usuario_id = usuario.get("tipo_usuario")
        tipo_sub_id = usuario.get("tipo_sub")
        if tipo_usuario_id and tipo_sub_id:
            tipoUsuario = db.tipoUsuario.find_one({"_id": ObjectId(tipo_usuario_id)}, {"descripcion": 1})
            tipoSub = db.tipoSub.find_one({"_id": ObjectId(tipo_sub_id)}, {"descripcion": 1})
            if tipoUsuario and tipoSub:
                usuario["tipo_sub"] = tipoSub.get("descripcion")
                usuario["tipo_usuario"] = tipoUsuario.get("descripcion")
    for usuario in usuarios:
        usuario["_id"] = str(usuario["_id"])           

    return usuarios

@router.get("/{id}")
async def searchUsuario(id: str,token = Depends(isAdmin)):
    return searchUsuario("_id" , ObjectId(id))

@router.post("/add", response_model=usuario, status_code=status.HTTP_201_CREATED)
async def addUser(newUsuario: usuario,token = Depends(isAdmin)):
    
    if type(searchUsuario("email",newUsuario.email)) == usuario : 
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND , detail = ("El usuario ya existe"))
    
    usuario_dict = dict(newUsuario)
    del usuario_dict["id"]
    
    id = db.usuario.insert_one(usuario_dict).inserted_id
    new_Usuario = usuarioSchema(db.usuario.find_one({"_id": ObjectId(id)}))
    
    return usuario(**new_Usuario)

@router.put("/update")
async def updateUsuario(updateUsuario: usuario,token = Depends(isAdmin)):
    usuario_dict = dict(updateUsuario)
    print(usuario_dict)
    del usuario_dict["id"]
    
    try:
       result=db.usuario.find_one_and_update(
           {"_id": ObjectId(updateUsuario.id)}, 
           {"$set": usuario_dict},
           return_document=True)

    except:
        return {"error" : " No se ha actualizado el usuario"}
    
    
    return searchUsuario("_id", ObjectId(updateUsuario.id))


@router.delete("/delete/{id}" , status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(id: str,token = Depends(isAdmin)):
    found = db.usuario.find_one_and_delete({"_id" : ObjectId(id)})
    if not found:
        return {"error" : "No se ha eliminado el usuario"}
    
def searchUsuario(field :str, key):
    try:
        usuariof = db.usuario.find_one({field: key})
        return usuario(**usuarioSchema(usuariof))
    except:
        return { "error" : "No se ha encontrado el usuario"}