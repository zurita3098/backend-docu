from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database.db import get_db_connection  # Asegúrate que sea para PostgreSQL (psycopg2 o psycopg)

class log(BaseModel):
    email: str
    accion: str
    fecha: Optional[datetime] = None

def get_log(email: Optional[str] = None):
    query = "SELECT * FROM logs WHERE email = %s" if email else "SELECT * FROM logs"

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            if email:
                cursor.execute(query, (email,))  # <- coma importante
                return cursor.fetchall()
            else:
                cursor.execute(query)
                return cursor.fetchall()

def save_log(log: log):
    query = "INSERT INTO logs (email, accion, created_at) VALUES (%s, %s, %s)"
    now = datetime.now()

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (log.email, log.accion, now))
            connection.commit()
