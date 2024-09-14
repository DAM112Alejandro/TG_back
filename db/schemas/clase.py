def claseSchema(clase) -> dict:
        return {
            "_id": str(clase["_id"]),
            "descripcion": clase["descripcion"],
            "horario" : clase["horario"],
            "entrenador" : str(clase["entrenador"]),
            "tipo_clase" : str(clase["tipo_clase"])
        }
        
def clasesSchema(clases) -> list:
    return [claseSchema(clase) for clase in clases]