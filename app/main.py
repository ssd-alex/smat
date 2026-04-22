from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# IMPORTACIONES RELATIVAS (Obligatorias para arquitectura modular)
from . import models, schemas, crud, auth
from .database import engine, get_db

# Crear las tablas en smat.db al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMAT - Sistema de Monitoreo de Alerta Temprana",
    description="""
    API profesional para la gestión de desastres y telemetría de sensores.
    Implementa persistencia en SQLite, arquitectura modular y seguridad JWT.
    """,
    version="1.0.0",
    contact={
        "name": "Soporte Técnico SMAT - FISI",
        "email": "desarrollo.smat@unmsm.edu.pe",
    }
)

# Configuración de CORS (Lab 4.3)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINTS DE SEGURIDAD ---

@app.post("/token", tags=["Seguridad"], response_model=schemas.Token)
async def login_para_obtener_token():
    """Genera un token JWT para poder usar los endpoints protegidos."""
    # En un sistema real, aquí validarías usuario/password
    return {"access_token": auth.crear_token_acceso({"sub": "admin_smat"}), "token_type": "bearer"}

# --- ENDPOINTS DE GESTIÓN (PROTEGIDOS) ---

@app.post("/estaciones/", status_code=201, tags=["Gestión de Infraestructura"])
def crear_estacion(
    estacion: schemas.EstacionCreate, 
    db: Session = Depends(get_db),
    usuario: str = Depends(auth.obtener_identidad_actual)
):
    """Registra una estación. REQUIERE TOKEN."""
    return crud.crear_estacion(db=db, estacion=estacion)

@app.post("/lecturas/", status_code=201, tags=["Telemetría de Sensores"])
def registrar_lectura(
    lectura: schemas.LecturaCreate, 
    db: Session = Depends(get_db),
    usuario: str = Depends(auth.obtener_identidad_actual)
):
    """Registra telemetría. Valida que la estación exista. REQUIERE TOKEN."""
    estacion_db = crud.obtener_estacion(db, lectura.estacion_id)
    if not estacion_db:
        raise HTTPException(
            status_code=404, 
            detail="Error de Integridad: La estación no existe en la base de datos."
        )
    return crud.crear_lectura(db=db, lectura=lectura)

# --- ENDPOINTS DE CONSULTA (PÚBLICOS) ---

@app.get("/estaciones/{id}/historial", tags=["Reportes Históricos"])
def obtener_historial(id: int, db: Session = Depends(get_db)):
    """Muestra lecturas y calcula el promedio desde la base de datos."""
    estacion = crud.obtener_estacion(db, id)
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    
    valores = [l.valor for l in estacion.lecturas]
    conteo = len(valores)
    promedio = sum(valores) / conteo if conteo > 0 else 0.0
    
    return {
        "id": id, 
        "fuente": "SQLite",
        "lecturas": valores, 
        "promedio": round(promedio, 2)
    }

@app.get("/estaciones/stats", tags=["Auditoria"])
def obtener_estadisticas_globales(db: Session = Depends(get_db)):
    """Dashboard con total de estaciones y valor máximo (Reto Lab 4.3)."""
    return crud.obtener_estadisticas(db)

