from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id: Optional[int] = None
    nombre_usuario: str
    contraseña: str
    
    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    username: str
    password: str