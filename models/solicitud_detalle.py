from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from database.db import get_db_connection
from models.log import log, save_log
from datetime import datetime

class SolicitudDetalle(BaseModel):
    solicitud_id: int
    descripcion: str
    pdf_1: Optional[bytes] = None
    pdf_2: Optional[bytes] = None
    jpg_1: Optional[bytes] = None
    jpg_2: Optional[bytes] = None
    observacion: Optional[str] = None

def get_solicitud_detalle(solicitud_id: int):
    query = "SELECT * FROM solicitud_detalle WHERE solicitud_id = %s"
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (solicitud_id,))
            return cursor.fetchall()


def save_solicitud_detalle(det: SolicitudDetalle, user):
    query = """
        INSERT INTO solicitud_detalle (
            solicitud_id, descripcion, pdf_1, pdf_2, jpg_1, jpg_2, observacion
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (
                det.solicitud_id, det.descripcion, det.pdf_1, det.pdf_2,
                det.jpg_1, det.jpg_2, det.observacion
            ))
            connection.commit()

            if cursor.rowcount == 0:
                return JSONResponse(
                    status_code=500,
                    content={"mensaje": "No se pudo guardar el detalle", "status_code": 500}
                )
            else:
                x = log(email=user["email"], accion=f"Registra detalle solicitud {det.solicitud_id}")
                save_log(x)
                return JSONResponse(
                    status_code=201,
                    content={"mensaje": "Detalle de solicitud guardado", "status_code": 201}
                )


def update_solicitud_detalle(id: int, det: SolicitudDetalle, user):
    query = """
        UPDATE solicitud_detalle SET 
            descripcion = %s, pdf_1 = %s, pdf_2 = %s, jpg_1 = %s, jpg_2 = %s, observacion = %s
        WHERE id = %s
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (
                det.descripcion, det.pdf_1, det.pdf_2,
                det.jpg_1, det.jpg_2, det.observacion, id
            ))
            connection.commit()

            if cursor.rowcount == 0:
                return JSONResponse(
                    status_code=500,
                    content={"mensaje": "No se pudo actualizar el detalle", "status_code": 500}
                )
            else:
                x = log(email=user["email"], accion=f"Actualiza detalle solicitud ID {id}")
                save_log(x)
                return JSONResponse(
                    status_code=200,
                    content={"mensaje": "Detalle actualizado", "status_code": 200}
                )


def delete_solicitud_detalle(id: int, user):
    query = "DELETE FROM solicitud_detalle WHERE id = %s"
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (id,))
            connection.commit()

            if cursor.rowcount == 0:
                return JSONResponse(
                    status_code=500,
                    content={"mensaje": "No se pudo eliminar el detalle", "status_code": 500}
                )
            else:
                x = log(email=user["email"], accion=f"Elimina detalle solicitud ID {id}")
                save_log(x)
                return JSONResponse(
                    status_code=200,
                    content={"mensaje": "Detalle eliminado", "status_code": 200}
                )