from typing import Optional
from pydantic import BaseModel ,Field

class reserva(BaseModel):
    id : Optional[str] = Field(None , alias = "_id")
    usuario : Optional[str] = Field(None , alias = "usuario")
    clase: str
    fecha: str