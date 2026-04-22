from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Definimos el nombre del archivo de la base de datos (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./smat.db"

# 2. Creamos el motor de conexión
# connect_args={"check_same_thread": False} es necesario solo para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Creamos una fábrica de sesiones para interactuar con la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Clase base para que nuestros modelos hereden de ella
Base = declarative_base()

# 5. Función de dependencia para obtener la sesión de DB en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()