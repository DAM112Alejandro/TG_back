def tipoSubSchema(tipoSub) -> dict:
        return {
            "_id": str(tipoSub["_id"]),
            "descripcion": tipoSub["descripcion"]
        }


def tipoSubsSchema(tipoSubs) -> list:
    return [tipoSubSchema(tipoSub) for tipoSub in tipoSubs]