import argparse
from pathlib import Path
import sys
import uvicorn
from database.db import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from routes.auth import router as auth_router
from services.auth import verify_token
from services.shorter_url import get_urls_by_username
from dotenv import load_dotenv
from os import getenv
from core.settings import HOST, PORT
from routes.url import router as url_router
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request


load_dotenv()

SESSION_SECRET = getenv('SESSION_SECRET')

VERSION = "-1.0.1"

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)
app.include_router(auth_router)

# Path de la raiz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR/"templates")


@app.get('/register', response_class=HTMLResponse)
async def register(request: Request):
    """
    Renderiza la página de registro
    """
    token = request.session.get("token")
    if token:
        payload = verify_token(token)
        if payload:
            return RedirectResponse(url="/")

    return templates.TemplateResponse('register.html', {
        "request": request, "page": "register"
    })


@app.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    """
    Renderiza la página de inicio de sesión
    """
    token = request.session.get("token")
    if token:
        payload = verify_token(token)
        if payload:
            return RedirectResponse(url="/")

    return templates.TemplateResponse('login.html', {
        "request": request, "page": "login"
    })


@app.get('/dashboard', response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """
    Renderiza la página dashboard del usuario
    Este endpoint verifica por un JWT almacenado en la sesión,
    lo valida. Si es válido renderiza su dashboard, de lo contrario,
    lo redirige a la página de inicio
    """
    token = request.session.get("token")

    if not token:
        return RedirectResponse(url="/")

    payload = verify_token(token)

    if not payload:
        return RedirectResponse(url="/")

    username = payload.get("username")
    username_urls = get_urls_by_username(db, username)
    domain_url = f"http://{HOST}:{PORT}/"

    return templates.TemplateResponse('dash.html', {
        "request": request,
        "username": username,
        "username_urls": username_urls,
        "domain": domain_url
    })

app.include_router(url_router)


def cli() -> bool:
    """
    Parsea CLI flags antes de ejecutar el servidor.
    :return: True si se pasan argumentos de línea de comandos,
             False si no se pasan argumentos.
    """
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "--status", action="store_true",
        help="Verifica si el servidor está corriendo"
    )
    parser.add_argument(
        "--version", action="store_true",
        help="Muestra la versión del servidor"
    )

    args, _ = parser.parse_known_args()

    if args.status:
        print("OK")
        return True

    if args.version:
        print(VERSION)
        return True
    return False


if __name__ == "__main__":
    """
    Ejecuta el servidor uvicorn, si es que no se pasan
    argumentos de línea de comandos.
    """
    if cli():
        sys.exit(0)

    uvicorn.run("app:app", host=HOST, port=PORT, reload=True)
