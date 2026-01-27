#importaciones 
from fastapi import FastAPI
import asyncio

#instancia del servidor 
app= FastAPI()

#Endpoints
@app.get("/")
async def holamundo():
    return {
        "mensaje":"Hola Mundo FastAPI"
        }

@app.get("/bienvenido")
async def bienvenido():
    # Simula una operación asincrónica que tarda 5 segundos
    await asyncio.sleep(5) 
    return {
        "mensaje":"Bienvenido a mi API con FastAPI",
        "Estatus":"200"
        }


