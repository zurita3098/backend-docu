from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database.db import get_db_connection
from fastapi.responses import JSONResponse
from models.log import log, save_log

class Users(BaseModel):
    username: str 
    email: str
    password: str
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    cedula: Optional[str] = None
    nombre_apellido: Optional[str] = None
    activo: Optional[bool] = True

class LoginRequest(BaseModel):
    email: str
    password: str

def login(email: str, password: str):
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (email, password))
                result = cursor.fetchone()
                if result:
                    return result
                else:
                    raise HTTPException(
                        status_code=401,
                        detail="Credenciales inválidas"
                    )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno (favor contactar al (+50764951086)): {str(e)}"
        )

def get_user(email: Optional[str] = None):
    if email:
        query = "SELECT * FROM users WHERE email = %s"
    else:
        query = "SELECT * FROM users"
    
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            if email:
                cursor.execute(query, (email,))
                return cursor.fetchone()
            else:
                cursor.execute(query)
                return cursor.fetchall()

def save_user(bb: Users, newPassword="", user=None):
    if get_user(bb.email):
        return JSONResponse(
            status_code=400,
            content={"mensaje": "Correo ya registrado", "status_code": 400}
        )

    query = """
        INSERT INTO users (username, email, password, fecha_creacion, fecha_actualizacion) 
        VALUES (%s, %s, %s, %s, %s)
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (
                bb.username,
                bb.email,
                bb.password,
                datetime.now(),
                datetime.now()
            ))
            connection.commit()
            if cursor.rowcount == 0:
                return JSONResponse(
                    status_code=500,
                    content={"mensaje": "No se pudo registrar el usuario", "status_code": 500}
                )
            else:
                if user:
                    x = log(username=user["email"], accion=f"Registra Usuario {bb.email}")
                    save_log(x)
                return JSONResponse(
                    status_code=201,
                    content={"mensaje": "Nuevo usuario registrado", "status_code": 201}
                )

def update_user(bb: Users, user):
    query = """
        UPDATE users 
        SET password = %s,
            cedula = %s, 
            nombre_apellido = %s, 
            activo = %s, 
            fecha_actualizacion = %s
        WHERE username = %s
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (
                bb.password,
                bb.cedula, 
                bb.nombre_apellido, 
                bb.activo, 
                datetime.now(), 
                bb.username
            ))
            connection.commit()
            if cursor.rowcount == 0:
                return JSONResponse(
                    status_code=500,
                    content={"mensaje": "No se pudo actualizar el usuario", "status_code": 500}
                )
            else:
                x = log(username=user["username"], accion=f"Actualiza Usuario {bb.username}")
                save_log(x)
                return JSONResponse(
                    status_code=200,
                    content={"mensaje": "Usuario actualizado correctamente", "status_code": 200}
                )

def delete_user(username: str, user):
    query = """
        DELETE FROM users 
        WHERE username = %s 
        AND NOT EXISTS (SELECT 1 FROM log_s WHERE username = %s)
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (username, username))
            connection.commit()
            if cursor.rowcount == 0:
                return JSONResponse(
                    status_code=500,
                    content={"mensaje": "No se puede eliminar usuario si ya hizo cambios", "status_code": 500}
                )
            else:
                x = log(username=user["username"], accion=f"Elimina Usuario {username}")
                save_log(x)
                return JSONResponse(
                    status_code=200,
                    content={"mensaje": "Usuario eliminado", "status_code": 200}
                )
