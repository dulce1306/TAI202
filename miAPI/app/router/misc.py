import asyncio
from typing import Optional
from app.data.database import usuarios
from fastapi import APIRouter

misc=APIRouter(tags=["Varios"])

#Endpoints
@misc.get("/")
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI"}

@misc.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje":"Hola mundo FastAPI",
        "estatus":"200"
        }

@misc.get("/v1/ParametroOb/{id}")
async def consultauno(id:int):
    return {"mensaje": "Usuario encontrado", 
            "usuario":id,
            "status":"200"
            }

@misc.get("/v1/ParametroOp/")
async def consultatodos(id:Optional[int]=None):
    if id is not None: 
        for usuariok in usuarios:
            if usuariok["id"] == id:
                return {"mensaje":"Usuario encontrado",
                        "usuario":usuariok}
        return {"mensaje":"usuario no encontrado","status":"200"}
    else:
        return {"mensaje":"No se proporciono un id","status":"200"}