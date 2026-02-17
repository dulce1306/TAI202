from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional

# Instancia del servidor
app = FastAPI(
    title="Mi primer API",
    description="Ivan Isay Guerra L - CRUD Completo",
    version="1.0"
)

# TB ficticia 
usuarios = [
    {"id": 1, "nombre": "Fany", "edad": 21},
    {"id": 2, "nombre": "Aly", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21},
]

# --- ENDPOINTS DE CONSULTA ---

@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje": "Hola Mundo FastAPI"}

@app.get("/bienvenido", tags=['Inicio'])
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje": "Bienvenido a FastAPI",
        "estatus": "200",
    }

@app.get("/v1/parametroOb/{id}", tags=['Parametros'])
async def consultauno(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            return {"mensaje": "usuario encontrado", "usuario": usuario, "status": "200"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.get("/v1/parametroOp/", tags=['Parametros'])
async def consultatodos(id: Optional[int] = None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuarioK}
        return {"mensaje": "usuario no encontrado", "status": "404"}
    return {"mensaje": "No se proporciono id", "status": "200", "usuarios_totales": usuarios}

# --- ENDPOINTS CRUD ---

@app.get("/v1/usuarios/", tags=['HTTP CRUD'])
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }

@app.post("/v1/usuarios/", tags=['HTTP CRUD'], status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail=f"El id {usuario.get('id')} ya existe"
            )
    
    usuarios.append(usuario) 
    return {
        "mensaje": "Usuario Creado",
        "Datos nuevos": usuario
    }

@app.put("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            
            usuarios[index] = usuario_actualizado
            usuarios[index]["id"] = id  
            return {"mensaje": "Usuario actualizado totalmente", "usuario": usuarios[index]}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.patch("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_parcial_usuario(id: int, campos: dict):
    for usr in usuarios:
        if usr["id"] == id:
           
            usr.update(campos)
            return {"mensaje": "Campos actualizados correctamente", "usuario": usr}
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def eliminar_usuario(id: int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(index)
            return {"mensaje": "Usuario eliminado exitosamente", "usuario": usuario_eliminado}
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")