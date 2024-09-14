def tipoClaseSchema(tipoClase) -> dict:
        return {
            "_id": str(tipoClase["_id"]),
            "descripcion": tipoClase["descripcion"]
        }


def tipoClasesSchema(tipoClases) -> list:
    return [tipoClaseSchema(tipoClase) for tipoClase in tipoClases]