from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crear_estacion():
    response = client.post("/estaciones/", json={
        "id": 1,
        "nombre": "Estación Rímac",
        "ubicacion": "Chosica"
    })
    assert response.status_code == 201
    assert response.json()["data"]["nombre"] == "Estación Rímac"

def test_registrar_lectura():
    response = client.post("/lecturas/", json={
        "estacion_id": 1,
        "valor": 12.5
    })
    assert response.status_code == 201
    assert response.json()["status"] == "Lectura recibida"

def test_riesgo_peligro():
    # Registramos una estación y una lectura alta (> 20.0)
    client.post("/estaciones/", json={"id": 10, "nombre": "Misti", "ubicacion": "Arequipa"})
    client.post("/lecturas/", json={"estacion_id": 10, "valor": 25.5})
    
    response = client.get("/estaciones/10/riesgo")
    assert response.status_code == 200
    assert response.json()["nivel"] == "PELIGRO"

def test_estacion_no_encontrada():
    # Probamos un ID que no existe
    response = client.get("/estaciones/999/riesgo")
    assert response.status_code == 404
    assert response.json()["detail"] == "Estación no encontrada"

def test_historial_y_promedio():
    # 1. Registramos una estación nueva (ID 20)
    client.post("/estaciones/", json={"id": 20, "nombre": "Río Yauli", "ubicacion": "La Oroya"})
    
    # 2. Registramos 3 lecturas: 10.0, 20.0 y 30.0 (Promedio esperado = 20.0)
    client.post("/lecturas/", json={"estacion_id": 20, "valor": 10.0})
    client.post("/lecturas/", json={"estacion_id": 20, "valor": 20.0})
    client.post("/lecturas/", json={"estacion_id": 20, "valor": 30.0})

    # 3. Probamos el nuevo endpoint de historial
    response = client.get("/estaciones/20/historial")
    assert response.status_code == 200
    assert response.json()["conteo"] == 3
    assert response.json()["promedio"] == 20.0        