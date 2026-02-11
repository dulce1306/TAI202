from fastapi import FastAPI
import asyncio
from typing import Optional # Importante para definir opcionales

# Instancia del servidor 
app = FastAPI()

# --- Endpoints Originales ---

@app.get("/")
async def holamundo():
    return {
        "mensaje": "Hola Mundo FastAPI"
    }

@app.get("/bienvenido")
async def bienvenido():
    # Simula una operación asincrónica que tarda 5 segundos
    await asyncio.sleep(5) 
    return {
        "mensaje": "Bienvenido a mi API con FastAPI",
        "Estatus": "200"
    }

# --- NUEVOS Endpoints para la Práctica ---

# 1. Ejemplo de Parámetro OBLIGATORIO (Path Parameter)
# El parámetro está dentro de las llaves {} en la ruta.
@app.get("/productos/{producto_id}")
async def obtener_producto(producto_id: int):
    return {
        "producto_id": producto_id,
        "descripcion": "Este parámetro era obligatorio"
    }

# 2. Ejemplo de Parámetro OPCIONAL (Query Parameter)
# El parámetro no está en la ruta. Se define en la función con un valor por defecto (None).
@app.get("/buscar")
async def buscar_algo(termino: Optional[str] = None):
    if termino:
        return {"resultado": f"Buscaste: {termino}"}
    else:
        return {"resultado": "No enviaste ningún término de búsqueda (es opcional)"}