from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario, actualizar_usuario
from app.security.auth import verificar_peticion
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as dbUsuario

router = APIRouter(
    prefix="/v1/usaurios",
    tags=["HTTP CRUD"]
)

@router.get("/", status_code=status.HTTP_200_OK)
async def consulta(db: Session = Depends(get_db)):
    queryUsuarios = db.query(dbUsuario).all()
    return {"total": len(queryUsuarios), "usuarios": queryUsuarios, "status": "200"}

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def consulta_por_id(id: int, db: Session = Depends(get_db)):
    usuario = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"usuario": usuario, "status": "200"}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuarioP: crear_usuario, db: Session = Depends(get_db)):
    nuevoU = dbUsuario(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(nuevoU)
    db.commit()
    db.refresh(nuevoU)
    return {"mensaje": "usuario agregado", "usuario": nuevoU, "status": "201"}

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario_completo(id: int, usuarioP: crear_usuario, db: Session = Depends(get_db)):
    usuario = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.nombre = usuarioP.nombre
    usuario.edad   = usuarioP.edad
    db.commit()
    db.refresh(usuario)
    return {"mensaje": "usuario actualizado", "usuario": usuario, "status": "200"}

@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_parcial(id: int, datos: actualizar_usuario, db: Session = Depends(get_db)):
    usuario = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if datos.nombre is not None:
        usuario.nombre = datos.nombre
    if datos.edad is not None:
        usuario.edad = datos.edad
    db.commit()
    db.refresh(usuario)
    return {"mensaje": "usuario actualizado parcialmente", "usuario": usuario, "status": "200"}

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_peticion), db: Session = Depends(get_db)):
    usuario = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"mensaje": f"usuario eliminado por {usuarioAuth}", "status": "200"}
