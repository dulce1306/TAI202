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
