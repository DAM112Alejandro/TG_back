from typing import Optional
from pydantic import BaseModel ,Field

class tipoClase(BaseModel):
    id : Optional[str] = Field(None , alias = "_id")
    descripcion : str