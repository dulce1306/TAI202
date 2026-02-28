from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal, Optional
from datetime import datetime

app = FastAPI(title="API Biblioteca Digital")

# --- MODIFICACIÓN DE ERRORES ---
# FastAPI por defecto devuelve 422 para errores de validación. 
# El requerimiento pide devolver un 400 Bad Request si faltan datos o son inválidos.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Faltan datos o el formato es inválido", "errores": exc.errors()}
    )

# --- MODELOS PYDANTIC (Punto 4) ---
class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2)
    correo: EmailStr

class Libro(BaseModel):
    id_libro: int
    nombre: str = Field(..., min_length=2, max_length=100)
    anio: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: Literal["disponible", "prestado"] = "disponible"

class Prestamo(BaseModel):
    id_prestamo: int
    id_libro: int
    usuario: Usuario

# --- BASE DE DATOS SIMULADA ---
libros_db = []
prestamos_db = []

# --- ENDPOINTS (Punto 2 y 3) ---

# a. Registrar un libro (Devuelve 201)
@app.post("/libros/", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):
    # Verificamos si el ID ya existe
    if any(l.id_libro == libro.id_libro for l in libros_db):
        raise HTTPException(status_code=400, detail="El ID del libro ya existe")
    libros_db.append(libro)
    return {"mensaje": "Libro registrado exitosamente", "libro": libro}

# b. Listar todos los libros disponibles
@app.get("/libros/disponibles/", response_model=List[Libro])
def listar_libros_disponibles():
    disponibles = [l for l in libros_db if l.estado == "disponible"]
    return disponibles

# c. Buscar un libro por su nombre
@app.get("/libros/buscar/{nombre}", response_model=List[Libro])
def buscar_libro(nombre: str):
    encontrados = [l for l in libros_db if nombre.lower() in l.nombre.lower()]
    return encontrados

# d. Registrar el préstamo de un libro a un usuario
@app.post("/prestamos/", status_code=status.HTTP_201_CREATED)
def registrar_prestamo(prestamo: Prestamo):
    libro = next((l for l in libros_db if l.id_libro == prestamo.id_libro), None)
    
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    # Conflicto 409 si el libro ya está prestado
    if libro.estado == "prestado":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro ya está prestado")
    
    # Cambiar estado y guardar préstamo
    libro.estado = "prestado"
    prestamos_db.append(prestamo)
    return {"mensaje": "Préstamo registrado exitosamente", "prestamo": prestamo}

# e. Marcar un libro como devuelto
@app.put("/prestamos/devolver/{id_libro}", status_code=status.HTTP_200_OK)
def devolver_libro(id_libro: int):
    libro = next((l for l in libros_db if l.id_libro == id_libro), None)
    
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado en la base de datos")
    
    # NUEVA LÓGICA: Si el libro ya está disponible, significa que no hay un préstamo activo
    if libro.estado == "disponible":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El registro de préstamo ya no existe o ya fue devuelto")
    
    # Lógica de devolución exitosa
    libro.estado = "disponible"
    return {"mensaje": "Libro devuelto con éxito"}
    
# f. Eliminar el registro de un préstamo
@app.delete("/prestamos/{id_prestamo}", status_code=status.HTTP_200_OK)
def eliminar_prestamo(id_prestamo: int):
    global prestamos_db
    prestamo = next((p for p in prestamos_db if p.id_prestamo == id_prestamo), None)
    
    if not prestamo:
        raise HTTPException(status_code=404, detail="El préstamo no existe")
        
    prestamos_db = [p for p in prestamos_db if p.id_prestamo != id_prestamo]
    return {"mensaje": "Registro de préstamo eliminado exitosamente"}