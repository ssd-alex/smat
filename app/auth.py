from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

# Configuración técnica exigida por el Laboratorio 4.4 de la FISI
SECRET_KEY = "UNMSM_FISI_SMAT_SECRET_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Definición del esquema para obtener el token desde el endpoint /token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def crear_token_acceso(data: dict):
    """
    Genera un token JWT firmado digitalmente.
    Incluye un tiempo de expiración de 30 minutos.
    """
    para_encriptar = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    para_encriptar.update({"exp": expiracion})
    return jwt.encode(para_encriptar, SECRET_KEY, algorithm=ALGORITHM)

async def obtener_identidad_actual(token: str = Depends(oauth2_scheme)):
    """
    Inyección de dependencia para proteger rutas.
    Decodifica el token y verifica la identidad del usuario.
    """
    error_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token de acceso",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificación del token usando la llave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise error_credenciales
        return username
    except JWTError:
        # Si el token es inválido o ha expirado
        raise error_credenciales