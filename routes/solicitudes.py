from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from models.solicitudes import Solicitudes, get_solicitud, save_solicitud, delete_solicitud
from routes.raiz import get_current_user
from typing import Optional


router_com = APIRouter(
    prefix="/solicitudes",
    tags=["solicitudes"],
    responses={404: {"description": "Not found"}},
)

@router_com.get('/get')
def get_solicitudes(usuario_id:int, user=Depends(get_current_user)):
    result = get_solicitud(usuario_id)
    return result

@router_com.post('/post')
async def post_solicitudes(
    usuario_id: int = Form(...),
    cedula: str = Form(...),
    telefono: str = Form(...),
    tipo: int = Form(...),
    comentario: Optional[str] = Form(None),
    observacion: Optional[str] = Form(None),
    estado: int = Form(...),
    pdf_1: Optional[UploadFile] = File(None),
    cedula_jpg: Optional[UploadFile] = File(None),
    user: dict = Depends(get_current_user)
):
    result = await save_solicitud(
        usuario_id=usuario_id,
        cedula=cedula,
        telefono=telefono,
        tipo=tipo,
        comentario=comentario,
        observacion=observacion,
        estado=estado,
        pdf_1=pdf_1,
        cedula_jpg=cedula_jpg,
        user=user
    )
    return result

@router_com.delete('/delete')
def delete_solicitudes(ced:str, user=Depends(get_current_user)):
    result = delete_solicitud(ced, user)
    return result



