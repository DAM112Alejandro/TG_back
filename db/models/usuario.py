from typing import Optional
from pydantic import BaseModel ,Field

class usuario (BaseModel):
    id : Optional[str] = Field(None , alias = "_id")
    nombre: Optional[str]
    telefono : Optional[str]
    email : Optional[str] 
    contraseña : Optional[str]
    tipo_sub : Optional[str]
    tipo_usuario : Optional[str] 