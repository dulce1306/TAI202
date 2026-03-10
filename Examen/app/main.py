#API de Sistema de reservas de Restaurant
# 1. Contruir una Api Rest con fastAPI para gestionar reservaas
# - Crear reserva, - Listar reserves, -Consiltar por id, -Confirmar reserva, cencelar reserva
#Modelo de datos obligatorio
#nombre cliente minimo 6 caracteres, fecha reserva futura entre 8:00 am y 10:00 pm,numero personas entre 1 y 10 , no permitir reservas en domingo 
#Rutas protegidas con usuario:admin y contraseñas:rest123
#listar reservas , canselar citas 

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import List, Optional
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title="Restaurante API",
    description="Dulce Maria Garcia Subias - CRUD Completo",
    version="1.0"
)
class Usuario(BaseModel):
    usuario: str
    contrasena: str

class crear_reserva(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=6, max_length=50, example="Maria Garcia", description="Nombre del cliente, mínimo 6 caracteres")
    fecha_reserva: datetime = Field(..., description="Fecha y hora de la reserva, debe ser futura y entre 8:00 am y 10:00 pm")
    numero_personas: int = Field(..., gt=0, lt=11, description="Número de personas, entre 1 y 10")
    estado: Optional[str] = Field("pendiente", description="Estado de la reserva, por defecto 'pendiente'")

security = HTTPBasic()

@app.post("/reservas", response_model=crear_reserva, status_code=201)
def crear_reserva(reserva: crear_reserva, credentials: HTTPBasicCredentials = Depends(security)):
    if not (credentials.username == "admin" and credentials.password == "rest123"):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    if reserva.fecha_reserva < datetime.now():
        raise HTTPException(status_code=400, detail="La fecha de reserva debe ser futura")
    
    if not (time(8, 0) <= reserva.fecha_reserva.time() <= time(22, 0)):
        raise HTTPException(status_code=400, detail="La hora de la reserva debe estar entre 8:00 am y 10:00 pm")
    
    if reserva.fecha_reserva.weekday() == 6:  
        raise HTTPException(status_code=400, detail="No se permiten reservas los domingos")
    return reserva

@app.get("/reservas", response_model=List[crear_reserva])
def listar_reservas(credentials: HTTPBasicCredentials = Depends(security)):
    if not (credentials.username == "admin" and credentials.password == "rest123"):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return []  

@app.get("/reservas/{reserva_id}", response_model=crear_reserva)
def consultar_reserva(reserva_id: int, credentials: HTTPBasicCredentials = Depends(security)):
    if not (credentials.username == "admin" and credentials.password == "rest123"):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return crear_reserva(id=reserva_id, nombre="Ejemplo", fecha_reserva=datetime.now(), numero_personas=2)

@app.put("/reservas/{reserva_id}/confirmar", response_model=crear_reserva)
def confirmar_reserva(reserva_id: int, credentials: HTTPBasicCredentials = Depends(security)):
    if not (credentials.username == "admin" and credentials.password == "rest123"):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return crear_reserva(id=reserva_id, nombre="Ejemplo", fecha_reserva=datetime.now(), numero_personas=2, estado="confirmada")

@app.delete("/reservas/{reserva_id}", status_code=204)
def cancelar_reserva(reserva_id: int, credentials: HTTPBasicCredentials = Depends(security)):
    if not (credentials.username == "admin" and credentials.password == "rest123"):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return None
