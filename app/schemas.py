from pydantic import BaseModel
from typing import List, Optional

# --- Esquemas para Estaciones ---

class EstacionBase(BaseModel):
    """Atributos base compartidos para estaciones."""
    nombre: str
    ubicacion: str

class EstacionCreate(EstacionBase):
    """Esquema para la creación de una estación (incluye el ID manual)."""
    id: int

class Estacion(EstacionBase):
    """Esquema para la lectura de datos de estaciones (respuesta de la API)."""
    id: int

    class Config:
        # Permite que Pydantic trabaje con objetos de SQLAlchemy
        from_attributes = True


# --- Esquemas para Lecturas ---

class LecturaBase(BaseModel):
    """Atributos base para las lecturas de sensores."""
    valor: float
    estacion_id: int

class LecturaCreate(LecturaBase):
    """Esquema para registrar una nueva lectura."""
    pass

class Lectura(LecturaBase):
    """Esquema para la lectura de datos de telemetría."""
    id: int

    class Config:
        from_attributes = True


# --- Esquemas para Seguridad JWT (Lab 4.4) ---

class UserLogin(BaseModel):
    """Esquema para el inicio de sesión del administrador."""
    username: str
    password: str

class Token(BaseModel):
    """Esquema para la respuesta que contiene el token de acceso."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Esquema para los datos contenidos dentro del token (payload)."""
    username: Optional[str] = None