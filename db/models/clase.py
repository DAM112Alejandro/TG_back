from typing import Optional, Type
from pydantic import BaseModel ,Field

class clase(BaseModel):
    id : Optional[str] = Field(None , alias = "_id")
    descripcion: str
    horario : str 
    entrenador : str
    tipo_clase : str
    