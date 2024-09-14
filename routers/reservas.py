from bson import ObjectId
from fastapi import APIRouter, Depends ,status, HTTPException
from db.models.reserva import reserva
from db.schemas.reservas import reservaSchema, reservasSchema
from db.client import db
from auth.auth import isLogged, isAdmin


router = APIRouter(prefix="/reserva", tags=["reserva"],responses={404: {"message" : "No encontrado"}})

@router.get("", response_model=list[reserva])
async def find_reservas(token = Depends(isAdmin)):
    return reservasSchema(db.reserva.find())

@router.get("/{id}")
async def find_by_id(id: str,token = Depends(isAdmin)):
    return searchReserva("_id" , ObjectId(id))

@router.get("/usuario/{id}")
async def find_by_usuario(id: str , token = Depends(isLogged)):
    reservas = list(db.reserva.find({"usuario": id}))
    for reserva in reservas:
        clase_id = reserva.get("clase")
        if clase_id:
            clase = db.clase.find_one({"_id": ObjectId(clase_id)}, {"descripcion": 1})
            if clase:
                reserva["clase"] = clase.get("descripcion", "Clase no disponible")
    for reserva in reservas:
        reserva["_id"] = str(reserva["_id"])           

    return reservas

@router.post("/add", response_model=reserva, status_code=status.HTTP_201_CREATED)
async def addReserva(newReserva: reserva ,token = Depends(isLogged)):
    idUser = token.get("_id")    
    reserva_dict = dict(newReserva)
    reserva_dict["usuario"] = str(idUser)
    if "id" in reserva_dict:
        del reserva_dict["id"]
    id = db.reserva.insert_one(reserva_dict).inserted_id
    new_Reserva = reservaSchema(db.reserva.find_one({"_id": ObjectId(id)}))
    return reserva(**new_Reserva)

@router.put("/update", response_model=reserva)
async def updateReserva(updateReserva: reserva, token = Depends(isAdmin)):
    reserva_dict = dict(updateReserva)
    del reserva_dict["id"]
    
    try:
        db.reserva.find_one_and_replace({"_id": ObjectId(updateReserva.id)}, reserva_dict)
    except:
        return {"error" : " No se ha actualizado la reserva"}

    return searchReserva("_id" , ObjectId(updateReserva.id))

@router.delete("/delete/{id}" , status_code=status.HTTP_204_NO_CONTENT)
async def deleteReserva(id: str, token = Depends(isLogged)):
    found = db.reserva.find_one_and_delete({"_id" : ObjectId(id)})
    if not found:
        return {"error" : "No se ha eliminado la reserva"}
    
def searchReserva(field :str, key):
    try:
        reservaf = db.reserva.find_one({field: key})
        return reserva(**reservaSchema(reservaf))
    except:
        return { "error" : "No se ha encontrado la reserva"}
    
