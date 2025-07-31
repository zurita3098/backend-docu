from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from database.db import get_db_connection
from fastapi.responses import JSONResponse
from models.log import log, save_log


class Solicitudes(BaseModel):
    usuario_id: int
    tipo: int
    pdf_1: Optional[bytes] = None
    jpg_1: Optional[bytes] = None
    observacion: Optional[str] = None
    estado: int
    fecha_respuesta: Optional[datetime] = None
    respuesta: Optional[str] = None
    fecha_creacion: Optional[datetime] = None


def get_solicitud(usuario_id: int):
    query = "SELECT * FROM solicitudes WHERE usuario_id = %s"
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (usuario_id,))
            return cursor.fetchall()


def save_solicitud(cc: Solicitudes, user):
    query = """
        INSERT INTO solicitudes (
            usuario_id, tipo, pdf_1, jpg_1, observacion,
            estado, fecha_creacion, fecha_respuesta, respuesta
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (
                cc.usuario_id, cc.tipo, cc.pdf_1, cc.jpg_1, cc.observacion,
                cc.estado, datetime.now(), cc.fecha_respuesta, cc.respuesta
            ))
            connection.commit()

            if cursor.rowcount == 0:
                return JSONResponse(
                    status_code=500,
                    content={"mensaje": "No se pudo registrar la solicitud", "status_code": 500}
                )
            else:
                x = log(email=user["email"], accion=f"Registra Solicitud de usuario_id={cc.usuario_id}")
                save_log(x)
                return JSONResponse(
                    status_code=201,
                    content={"mensaje": "Nueva solicitud registrada", "status_code": 201}
                )


def update_solicitud(id: int, cc: Solicitudes, user):
    query = """
        UPDATE solicitudes SET 
            tipo = %s, pdf_1 = %s, jpg_1 = %s, observacion = %s,
            estado = %s, fecha_respuesta = %s, respuesta = %s
        WHERE id = %s
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (
                cc.tipo, cc.pdf_1, cc.jpg_1, cc.observacion,
                cc.estado, cc.fecha_respuesta, cc.respuesta, id
            ))
            connection.commit()

            if cursor.rowcount == 0:
                return JSONResponse(
                    status_code=500,
                    content={"mensaje": "No se pudo actualizar la solicitud", "status_code": 500}
                )
            else:
                x = log(email=user["email"], accion=f"Actualiza Solicitud ID={id}")
                save_log(x)
                return JSONResponse(
                    status_code=200,
                    content={"mensaje": "Solicitud actualizada", "status_code": 200}
                )


def delete_solicitud(id: int, user):
    query = "DELETE FROM solicitudes WHERE id = %s"
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (id,))
            connection.commit()

            if cursor.rowcount == 0:
                return JSONResponse(
                    status_code=500,
                    content={"mensaje": "No se pudo eliminar la solicitud", "status_code": 500}
                )
            else:
                x = log(email=user["email"], accion=f"Elimina Solicitud ID={id}")
                save_log(x)
                return JSONResponse(
                    status_code=200,
                    content={"mensaje": "Solicitud eliminada", "status_code": 200}
                )
