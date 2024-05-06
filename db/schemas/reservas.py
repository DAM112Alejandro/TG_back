def reservaSchema(reserva) -> dict:
        return {
            "_id": str(reserva["_id"]),
            "usuario": reserva["usuario"],
            "clase" : reserva["clase"],
            "hora_ins" : reserva["hora_ins"]
        }
        
def reservasSchema(reservas) -> list:
    return [reservaSchema(reserva) for reserva in reservas]