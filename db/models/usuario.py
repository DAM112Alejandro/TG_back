from typing import Optional
from pydantic import BaseModel ,Field

class usuario (BaseModel):
    id : Optional[str] = Field(None , alias = "_id")
    nombre : str
    apellidos : str
    telefono : str
    email : str 
    contraseña : str
    tipo_sub : str
    tipo_usuario : str 