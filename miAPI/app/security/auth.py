from fastapi import status, HTTPException, Depends #agrego
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials,HTTPBasicCredentials#primer impor #agrego
import secrets #se agrego

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