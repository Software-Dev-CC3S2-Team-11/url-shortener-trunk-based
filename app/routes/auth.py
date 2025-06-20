from pathlib import Path
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from starlette import status
from fastapi.templating import Jinja2Templates
from database.db import get_db
from sqlalchemy.orm import Session
from models.User import User
import services.auth as auth_service


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

# Ruta Raiz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=BASE_DIR/"templates")


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, email: str = Form(...),
                        password: str = Form(...),
                        username: str = Form(...),
                        db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos
    """

    hashed_password = auth_service.bcrypt_context.hash(password)
    new_user = User(email=email, password=hashed_password, username=username)

    db.add(new_user)
    db.commit()

    token = auth_service.create_access_token(email=email, username=username)
    request.session['token'] = token

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.post("/login")
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Inicia sesión con el usuario y contraseña proporcionados.
    Redirige al usuario a la página de dashboard si
    las credenciales son válidas.
    """

    user = db.query(User).filter(User.email == email).first()
    if not user or not auth_service.bcrypt_context.verify(password,
                                                          user.password):
        return templates.TemplateResponse("login.html",
                                          {"request": request,
                                           "error": "Invalid credentials"})

    token = auth_service.create_access_token(user.email, user.username)
    request.session["token"] = token
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.post("/logout")
async def logout_user(request: Request):
    """
    Cierra la sesión del usuario eliminando el token de la sesión.
    Redirige al usuario a la página de inicio de sesión.
    """
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
