from fastapi import APIRouter, HTTPException, Depends, Form, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from typing import Annotated
from datetime import timedelta
from database.db import get_db
from sqlalchemy.orm import Session
from models.User import User
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
import services.auth as auth_service

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

templates = Jinja2Templates(directory="../templates")

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, email: str = Form(...), password: str = Form(...), username: str = Form(...), db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos
    """
    
    hashed_password = auth_service.bcrypt_context.hash(password)
    new_user = User(email=email, password=hashed_password, username=username)
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@router.post("/login")
async def login_user(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    Inicia sesión con el usuario y contraseña proporcionados.
    Redirige al usuario a la página de dashboard si las credenciales son válidas.
    """
    
    user = db.query(User).filter(User.email == email).first()
    if not user or not auth_service.bcrypt_context.verify(password, user.password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    token = auth_service.create_access_token(user.email, user.username)
    request.session['token'] = token
    return RedirectResponse(url="http://localhost:8000/dashboard", status_code=status.HTTP_302_FOUND)

@router.post("/logout")
async def logout_user(request: Request):
    """
    Cierra la sesión del usuario eliminando el token de la sesión.
    Redirige al usuario a la página de inicio de sesión.
    """
    
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
