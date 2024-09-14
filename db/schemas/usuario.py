def usuarioSchema(user) -> dict:
        return {
            "id": str(user.get("_id", "")),  # Convertir ObjectId a str
            "nombre": user.get("nombre", ""),  # Usar "" si el campo es opcional
            "telefono": user.get("telefono", ""),
            "email": user.get("email", ""),
            "contraseña": user.get("contraseña", ""),
            "tipo_sub": user.get("tipo_sub", ""),
            "tipo_usuario": user.get("tipo_usuario", "")
        }
        
def usuariosSchema(users) -> list:
    return [usuarioSchema(user) for user in users]