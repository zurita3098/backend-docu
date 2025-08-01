
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE solicitudes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,               -- ID del usuario que hace la solicitud
    cedula TEXT NOT NULL,
	telefono TEXT,
	tipo INTEGER NOT NULL,                 -- Tipo de solicitud (ej. 'acceso', 'certificado', etc.)
	comentario TEXT,
	pdf_1 BYTEA,
	cedula_jpg BYTEA,
    observacion TEXT,
    estado INTEGER NOT NULL,    -- Estado: pendiente, aprobada, rechazada
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_respuesta TIMESTAMP                 -- Cuándo se resolvió
);


CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    accion TEXT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);