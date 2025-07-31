from fastapi import FastAPI
from routes.users import router_users
from routes.raiz import router
from routes.solicitudes import router_com
from fastapi.middleware.cors import CORSMiddleware

import uvicorn


app = FastAPI()

app.include_router(router)
app.include_router(router_users)
app.include_router(router_com)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # o ["*"] para permitir todo (no recomendado en prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info")





