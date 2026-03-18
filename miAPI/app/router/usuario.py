from fastapi import FastAPI, status, HTTPException,Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion


router = APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)

# ==========================================
# USUARIO CRUD 
# ==========================================

@router.get("/")
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }

# Aplicamos el modelo "crear_usuario" en lugar de "dict"
@router.post("/", status_code=status.HTTP_201_CREATED)
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
@router.put("/")
async def actualizar_usuario(id: int, usuario_actualizado: crear_usuario):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado.model_dump()
            usuarios[index]["id"] = id  
            return {"mensaje": "Usuario actualizado totalmente", "usuario": usuarios[index]}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# El PATCH lo dejamos con dict porque permite actualizaciones parciales (ej. solo enviar la edad)
@router.patch("/")
async def actualizar_parcial_usuario(id: int, campos: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr.update(campos)
            return {"mensaje": "Campos actualizados correctamente", "usuario": usr}
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int,usuarioAuth: str= Depends(verificar_peticion)):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:

            usuario_eliminado = usuarios.pop(index)
            return {"mensaje": f"Usuario eliminado por {usuarioAuth}"}
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")