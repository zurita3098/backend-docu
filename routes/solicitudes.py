from fastapi import APIRouter, Depends
from models.solicitudes import Solicitudes, get_solicitud, save_solicitud, delete_solicitud
from routes.raiz import get_current_user

router_com = APIRouter(
    prefix="/solicitudes",
    tags=["solicitudes"],
    responses={404: {"description": "Not found"}},
)


#------------------COMUNIONES-----------------
@router_com.get('/get')
def get_solicitudes(ced:str, user=Depends(get_current_user)):
    result = (ced)
    return result

@router_com.post('/post')
def post_solicitudes(data:Solicitudes, user=Depends(get_current_user)):
    result = save_solicitud(data, user)
    return result

@router_com.delete('/delete')
def delete_solicitudes(ced:str, user=Depends(get_current_user)):
    result = delete_solicitud(ced, user)
    return result



