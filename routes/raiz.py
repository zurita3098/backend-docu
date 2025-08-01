from fastapi import APIRouter, Depends, HTTPException
from models.users import LoginRequest ,login, Users, save_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta


router = APIRouter(
    prefix="",
    tags=["raiz"],
    responses={404: {"description": "Not found"}},
)

# Secreto y algoritmo para firmar tokens
SECRET_KEY = "tu_clave_secreta_muy_segura"
ALGORITHM = "HS256"
#ACCESS_TOKEN_EXPIRE_MINUTES = 30



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post('/login')
def login_user(login_data: LoginRequest):
    user = login(login_data.email, login_data.password)
    if user:
        expires = timedelta(days=3)
        token = create_access_token(data={"sub": user["email"]}, expires_delta=expires)
        return {"usuario_id": user["id"],"access_token": token, "token_type": "bearer"}

@router.post('/register')
def save_userx(data: Users):
    result = save_user(data)
    return result


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"email": email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

