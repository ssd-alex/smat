from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import models
from database import engine, get_db

# CRITICAL: CREACIÓN DE LA BASE DE DATOS Y TABLAS
# Esta línea crea el archivo 'smat.db' y las tablas al iniciar el servidor
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SMAT Persistente - Lab 03")

# --- Esquemas de Pydantic (Validación de entrada) ---
class EstacionCreate(BaseModel):
    id: int
    nombre: str
    ubicacion: str

class LecturaCreate(BaseModel):
    estacion_id: int
    valor: float

# --- ENDPOINTS ---

@app.post("/estaciones/", status_code=201)
def crear_estacion(estacion: EstacionCreate, db: Session = Depends(get_db)):
    """Guarda una estación en la base de datos SQL."""
    nueva_estacion = models.EstacionDB(
        id=estacion.id, 
        nombre=estacion.nombre,
        ubicacion=estacion.ubicacion
    )
    db.add(nueva_estacion)
    db.commit()
    db.refresh(nueva_estacion)
    return {"msj": "Estación guardada en DB", "data": nueva_estacion}

@app.post("/lecturas/", status_code=201)
def registrar_lectura(lectura: LecturaCreate, db: Session = Depends(get_db)):
    """Registra una lectura validando que la estación existe en SQL."""
    estacion = db.query(models.EstacionDB).filter(models.EstacionDB.id == lectura.estacion_id).first()
    
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no existe")
    
    nueva_lectura = models.LecturaDB(
        valor=lectura.valor,
        estacion_id=lectura.estacion_id
    )
    db.add(nueva_lectura)
    db.commit()
    return {"status": "Lectura guardada en DB"}

@app.get("/estaciones/{id}/riesgo")
def obtener_riesgo(id: int, db: Session = Depends(get_db)):
    """Calcula el riesgo consultando la última lectura desde SQL."""
    # Buscar última lectura de la estación por ID
    ultima = db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == id).order_by(models.LecturaDB.id.desc()).first()
    
    if not ultima:
        return {"id": id, "nivel": "SIN DATOS", "valor": 0}

    if ultima.valor > 20.0:
        nivel = "PELIGRO"
    elif ultima.valor > 10.0:
        nivel = "ALERTA"
    else:
        nivel = "NORMAL"

    return {"id": id, "valor": ultima.valor, "nivel": nivel}

@app.get("/estaciones/{id}/historial")
def obtener_historial(id: int, db: Session = Depends(get_db)):
    """RETO: Historial y promedios usando consultas SQL."""
    # Verificar si la estación existe
    estacion = db.query(models.EstacionDB).filter(models.EstacionDB.id == id).first()
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")

    # Consulta SQL filtrada
    lecturas_db = db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == id).all()
    
    valores = [l.valor for l in lecturas_db]
    conteo = len(valores)
    promedio = sum(valores) / conteo if conteo > 0 else 0.0

    return {
        "estacion_id": id,
        "fuente": "SQLite",
        "lecturas": valores,
        "conteo": conteo,
        "promedio": round(promedio, 2)
    }