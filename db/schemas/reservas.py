def reservaSchema(reserva) -> dict:
        return {
            "_id": str(reserva["_id"]),
            "usuario": reserva["usuario"],
            "clase": str(reserva["clase"]),
            "fecha": reserva["fecha"]
        }  
        
def reservasSchema(reservas) -> list:
    return [reservaSchema(reserva) for reserva in reservas]
