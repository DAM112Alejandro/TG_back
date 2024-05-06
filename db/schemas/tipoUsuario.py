def tipoUsuarioSchema(tipoUser) -> dict:
        return {
            "_id": str(tipoUser["_id"]),
            "descripcion": tipoUser["descripcion"]
        }


def tipoUsuariosSchema(tipoUsers) -> list:
    return [tipoUsuarioSchema(user) for user in tipoUsers]