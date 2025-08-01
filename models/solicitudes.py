from fastapi import File, UploadFile, Form
from datetime import datetime
from fastapi.responses import JSONResponse
from database.db import get_db_connection
from models.log import log, save_log
from typing import Optional
from pydantic import BaseModel
import base64

class Solicitudes(BaseModel):
    usuario_id: int
    cedula: str
    telefono: str
    tipo: int
    comentario: Optional[str] = None
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
            rows = cursor.fetchall()
            for solicitud in rows:
                if solicitud.get("pdf_1") and isinstance(solicitud["pdf_1"], bytes):
                    solicitud["pdf_1"] = base64.b64encode(solicitud["pdf_1"]).decode('utf-8')
                if solicitud.get("cedula_jpg") and isinstance(solicitud["cedula_jpg"], bytes):
                    solicitud["cedula_jpg"] = base64.b64encode(solicitud["cedula_jpg"]).decode('utf-8')


            return rows


async def save_solicitud(
    usuario_id: int = Form(...),
    cedula: str = Form(...),
    telefono: str = Form(...),
    tipo: int = Form(...),
    comentario: Optional[str] = Form(None),
    observacion: Optional[str] = Form(None),
    estado: int = Form(...),
    pdf_1: Optional[UploadFile] = File(None),
    cedula_jpg: Optional[UploadFile] = File(None),
    user: dict = None  # Este debe venir desde el endpoint con Depends si es autenticado
):
    pdf_bytes = await pdf_1.read() if pdf_1 else None
    jpg_bytes = await cedula_jpg.read() if cedula_jpg else None

    query = """
        INSERT INTO solicitudes (
            usuario_id, cedula, telefono, tipo, comentario,
            observacion, estado, fecha_creacion, pdf_1, cedula_jpg
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (
                usuario_id, cedula, telefono, tipo, comentario,
                observacion, estado, datetime.now(), pdf_bytes, jpg_bytes
            ))
            connection.commit()

            if cursor.rowcount == 0:
                return JSONResponse(
                    status_code=500,
                    content={"mensaje": "No se pudo registrar la solicitud", "status_code": 500}
                )
            else:
                x = log(email=user["email"], accion=f"Registra Solicitud de usuario_id={usuario_id}")
                save_log(x)
                return JSONResponse(
                    status_code=201,
                    content={"mensaje": "Solicitud registrada correctamente", "status_code": 201}
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
