def usuarioSchema(user) -> dict:
        return {
            "_id": str(user["_id"]),
            "nombre": user["nombre"],
            "apellidos" : user["apellidos"],
            "telefono" : user["telefono"],
            "email" : user["email"],
            "contraseña" : user["contraseña"],
            "tipo_sub" : user["tipo_sub"],
            "tipo_usuario" : user["tipo_usuario"]
        }
        
def usuariosSchema(users) -> list:
    return [usuarioSchema(user) for user in users]