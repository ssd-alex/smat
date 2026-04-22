from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class EstacionDB(Base):
    """Mapeo de la tabla de estaciones"""
    __tablename__ = "estaciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    ubicacion = Column(String)

    # Relación: permite acceder a las lecturas desde el objeto estación
    # Una estación tiene muchas lecturas
    lecturas = relationship("LecturaDB", back_populates="estacion")

class LecturaDB(Base):
    """Mapeo de la tabla de lecturas de sensores"""
    __tablename__ = "lecturas"

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float)
    
    # Llave foránea para vincular la lectura con una estación específica
    estacion_id = Column(Integer, ForeignKey("estaciones.id"))
    
    # Relación inversa: permite saber a qué estación pertenece la lectura
    estacion = relationship("EstacionDB", back_populates="lecturas")