from fastapi import FastAPI, status, HTTPException,Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field 
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

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

# ==========================================
# MODELO DE VALIDACIÓN PYDANTIC (BaseModel)
# ==========================================
class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")

# ==========================================
# Seguridad HTTP BASIC
# ==========================================

seciurity = HTTPBasic()
def verificar_peticion( credenciales: HTTPBasicCredentials = Depends(seciurity)):
    usuario_correcto= secrets.compare_digest(credenciales.username, "dulcegarcia")
    contrasena_correcta= secrets.compare_digest(credenciales.password, "123456")

    if not(usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas"
        )
    return credenciales.username

# ==========================================
# ENDPOINTS DE CONSULTA
# ==========================================

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


# ==========================================
# ENDPOINTS CRUD 
# ==========================================

@app.get("/v1/usuarios/", tags=['HTTP CRUD'])
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }

# Aplicamos el modelo "crear_usuario" en lugar de "dict"
@app.post("/v1/usuarios/", tags=['HTTP CRUD'], status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuario: crear_usuario): 
    for usr in usuarios:
        if usr["id"] == usuario.id: # Cambiamos usuario.get("id") por usuario.id
            raise HTTPException(
                status_code=400,
                detail=f"El id {usuario.id} ya existe"
            )
    
    # Convertimos el modelo a diccionario antes de guardarlo en nuestra lista
    usuarios.append(usuario.model_dump()) 
    return {
        "mensaje": "Usuario Creado",
        "Datos nuevos": usuario
    }

# Aplicamos el modelo también en el PUT para asegurar que los datos actualizados sean válidos
@app.put("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario(id: int, usuario_actualizado: crear_usuario):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado.model_dump()
            usuarios[index]["id"] = id  
            return {"mensaje": "Usuario actualizado totalmente", "usuario": usuarios[index]}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# El PATCH lo dejamos con dict porque permite actualizaciones parciales (ej. solo enviar la edad)
@app.patch("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_parcial_usuario(id: int, campos: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr.update(campos)
            return {"mensaje": "Campos actualizados correctamente", "usuario": usr}
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def eliminar_usuario(id: int,usuarioAuth: str= Depends(verificar_peticion)):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:

            usuario_eliminado = usuarios.pop(index)
            return {"mensaje": f"Usuario eliminado por {usuarioAuth}"}
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")