from fastapi import FastAPI, status, HTTPException,Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

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
# CONFIGURACIÓN OAUTH2 Y JWT
# ==========================================
SECRET_KEY = "mi_clave_secreta_super_segura" # En producción, esta clave debe ser un valor aleatorio y seguro, y no debe estar hardcodeada
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Límite máximo de 30 minutos

# Esta dependencia le dice a FastAPI de dónde sacar el token (de la ruta /login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ============================================
# CREACION DE TOKENS JWT
# ============================================
def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ==========================================
# MODELO DE VALIDACIÓN PYDANTIC (BaseModel)
# ==========================================
class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")

#=============================================
# ENDPOINT DE LOGIN PARA OBTENER EL TOKEN
#=============================================
@app.post("/login", tags=['Autenticación'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validación "Dummy" para la práctica (Aquí normalmente buscarías en la BD)
    if form_data.username != "admin" or form_data.password != "secreta":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generar el token con expiración de 30 minutos
    tiempo_expiracion = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_jwt = crear_token_acceso(
        data={"sub": form_data.username}, expires_delta=tiempo_expiracion
    )
    
    return {"access_token": token_jwt, "token_type": "bearer"}

#=============================================
# FUNCION PARA VALIDAR TOKENS
#=============================================

async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    # Definimos el error estándar si algo sale mal
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales o el token ha expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Intentamos decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
            
    except JWTError:
        # Si el token es inválido o ya expiró (pasaron los 30 minutos), cae aquí
        raise credentials_exception
        
    return username




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
# se modifico el PUT para protegerlo con JWT
# para que de esta forma solo los usuarios autenticados podrán actualizar usuarios en la lista
@app.put("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario(
    id: int, 
    usuario_actualizado: crear_usuario, 
    current_user: str = Depends(obtener_usuario_actual) # <-- ¡Aquí está la protección!
):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado.model_dump()
            usuarios[index]["id"] = id  
            return {"mensaje": "Usuario actualizado totalmente", "usuario": usuarios[index]}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#Igualmente se esta modificando el delete para protegerlo con JWT
# para que solo los usuarios autenticados podrán eliminar usuarios de la lista
@app.delete("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def eliminar_usuario(
    id: int, 
    current_user: str = Depends(obtener_usuario_actual) # <-- ¡Aquí está la protección!
):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(index)
            return {"mensaje": "Usuario eliminado exitosamente", "usuario": usuario_eliminado}
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")