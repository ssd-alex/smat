from sqlalchemy.orm import Session
from sqlalchemy import func
# Usamos el punto (.) para importaciones relativas dentro del paquete 'app'
from . import models, schemas

def obtener_estacion(db: Session, estacion_id: int):
    """Busca una estación por su ID en la base de datos."""
    return db.query(models.EstacionDB).filter(models.EstacionDB.id == estacion_id).first()

def crear_estacion(db: Session, estacion: schemas.EstacionCreate):
    """Registra una nueva estación física."""
    db_estacion = models.EstacionDB(
        id=estacion.id,
        nombre=estacion.nombre,
        ubicacion=estacion.ubicacion
    )
    db.add(db_estacion)
    db.commit()
    db.refresh(db_estacion)
    return db_estacion

def crear_lectura(db: Session, lectura: schemas.LecturaCreate):
    """Registra una lectura vinculada a una estación existente."""
    db_lectura = models.LecturaDB(
        valor=lectura.valor,
        estacion_id=lectura.estacion_id
    )
    db.add(db_lectura)
    db.commit()
    db.refresh(db_lectura)
    return db_lectura

def obtener_estadisticas(db: Session):
    """
    Reto Lab 4.3: Dashboard de Auditoría.
    Calcula totales y el valor máximo registrado en todo el sistema.
    """
    total_estaciones = db.query(models.EstacionDB).count()
    total_lecturas = db.query(models.LecturaDB).count()
    # Usamos func.max para obtener el punto crítico más alto
    max_valor = db.query(func.max(models.LecturaDB.valor)).scalar()
    
    return {
        "total_estaciones": total_estaciones,
        "total_lecturas": total_lecturas,
        "punto_critico_maximo": max_valor if max_valor else 0.0
    }