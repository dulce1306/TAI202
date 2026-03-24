from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as dbUsuario

#simplifica no declarar cada endponit 
router=APIRouter(
    prefix="/v1/usaurios",
    tags=["HTTP CRUD"]
)

#Endpoints
@router.get("/")
async def consulta(db:Session=Depends(get_db)): #aggrego

    queryUsuarios=db.query(dbUsuario).all() #agrego

    return {
        "total":len(queryUsuarios), #remplazo usuarios por queryUsuarios
        "usuarios":queryUsuarios, #remplazo usuarios por queryUsuarios
        "status":"200"
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuarioP:crear_usuario,db:Session=Depends(get_db)):#agrego despues de la, db
    nuevoU=dbUsuario(nombre=usuarioP.nombre, edad=usuarioP.edad)#agrego
    db.add(nuevoU) #agrego
    db.commit() #agrego
    db.refresh(nuevoU) #agrego

    return {
        "mensaje":"usuario agregado",
        "usuario":usuarioP 
    }

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario(id:int, usuario: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario["id"] = id
            usuarios[index] = usuario
            return {
                "mensaje":"usuario actualizado",
                "usuario":usuario,
                "status":"200"      
            }
    raise HTTPException(
        status_code= 404, 
        detail="usuario no encontrado"
        )
#edito eliminar usuario y se agrea para que desde verificar_peticion decida si lo deja pasar o no
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int, usuarioAuth:str=Depends(verificar_peticion)): 
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            del usuarios[index]
            return {
                "mensaje":f"usuario eliminado por {usuarioAuth}",
                "status":"200"      
            }
    raise HTTPException(
        status_code= 404, 
        detail="usuario no encontrado"
        )