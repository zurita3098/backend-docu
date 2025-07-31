from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from database.db import get_db_connection
from fastapi.responses import JSONResponse
from models.log import log, save_log


class Solicitudes(BaseModel):
    usuario_id: str
    tipo: str
    estado: str
    fecha_respuesta: Optional[date] = None
    respuesta: Optional[str] = None
    fecha_creacion: Optional[datetime] = None

def get_solicitud(ced: str):
    query = "SELECT * FROM solicitudes WHERE usuario_id = %s"
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (ced,))
            return cursor.fetchone()


def save_solicitud(cc: Solicitudes, user):
    query = """
        INSERT INTO solicitudes (
            usuario_id, tipo, estado, fecha_respuesta, respuesta, fecha_creacion
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (
                cc.usuario_id, cc.tipo, cc.estado, cc.fecha_respuesta,
                cc.respuesta, datetime.now()
            ))
            connection.commit()

            if cursor.rowcount == 0:
                return JSONResponse(
                    status_code=500,
                    content={"mensaje": "No se pudo registrar la solicitud", "status_code": 500}
                )
            else:
                x = log(email=user["email"], accion=f"Registra Solicitud {cc.usuario_id}")
                save_log(x)
                return JSONResponse(
                    status_code=201,
                    content={"mensaje": "Nueva solicitud registrada", "status_code": 201}
                )


def update_solicitud(cc: Solicitudes, user):
    query = """
        UPDATE solicitudes SET 
            tipo = %s, estado = %s, fecha_respuesta = %s, respuesta = %s
        WHERE usuario_id = %s
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (
                cc.tipo, cc.estado, cc.fecha_respuesta,
                cc.respuesta, cc.usuario_id
            ))
            connection.commit()

            if cursor.rowcount == 0:
                return JSONResponse(
                    status_code=500,
                    content={"mensaje": "No se pudo actualizar la solicitud", "status_code": 500}
                )
            else:
                x = log(email=user["email"], accion=f"Actualiza Solicitud {cc.usuario_id}")
                save_log(x)
                return JSONResponse(
                    status_code=200,
                    content={"mensaje": "Solicitud actualizada", "status_code": 200}
                )


def delete_solicitud(ced: str, user):
    query = "DELETE FROM solicitudes WHERE usuario_id = %s"
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (ced,))
            connection.commit()

            if cursor.rowcount == 0:
                return JSONResponse(
                    status_code=500,
                    content={"mensaje": "No se pudo eliminar la solicitud", "status_code": 500}
                )
            else:
                x = log(email=user["email"], accion=f"Elimina Solicitud {ced}")
                save_log(x)
                return JSONResponse(
                    status_code=200,
                    content={"mensaje": "Solicitud eliminada", "status_code": 200}
                )
