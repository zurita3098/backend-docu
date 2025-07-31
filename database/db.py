import psycopg  # Usa la nueva versión de psycopg
from contextlib import contextmanager

# Configura la conexión a la base de datos
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "admin@1234",
    "dbname": "db_docu",
    "row_factory": psycopg.rows.dict_row  # Similar a DictCursor
}

@contextmanager
def get_db_connection():
    with psycopg.connect(**DB_CONFIG) as conn:
        yield conn
