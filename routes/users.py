from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from models.users import Users, get_user, save_user, delete_user
from routes.raiz import get_current_user



router_users = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

#------------------USUARIOS-----------------

@router_users.get('/get')
def get_users(username: Optional[str] = None ,user=Depends(get_current_user)):
    if username:
        result = get_user(username)
        return result
    else:
        result = get_user()
        return result
    
@router_users.post('/post')
def save_users(data:Users, newPassword: Optional[str] = None ,user=Depends(get_current_user)):
    result = save_user(data, newPassword, user)
    return result

@router_users.delete('/delete')
def delete_users(username:str ,user=Depends(get_current_user)):
    result = delete_user(username, user)
    return result