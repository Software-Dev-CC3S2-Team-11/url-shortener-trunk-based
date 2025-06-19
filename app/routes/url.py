from core.settings import HOST, PORT
from fastapi.templating import Jinja2Templates
from database.db import get_db
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import Request, Form, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException
from services.shorter_url import get_by_shorter_url, insert_shorter_url
from services.shorter_url import increment_visits_url, build_url_entity
from services.auth import verify_token

router = APIRouter()

templates = Jinja2Templates(directory="../templates")


@router.post('/shorter', response_class=HTMLResponse)
async def generated_url(request: Request, url: str = Form(...),
                        db: Session = Depends(get_db)):
    """
    Toma la url enviada desde el form del index,
    genera un slug único, almacena los datos
    en la base de datos y luego devuelve una
    plantilla html con los datos de la url generada
    """

    token = request.session.get('token')
    username = 'unknown'

    if token:
        payload = verify_token(token)
        username = payload.get("username")

    url_shorter = build_url_entity(original_url=url, username=username)

    shortened_url = f"http://{HOST}:{PORT}/{url_shorter.shorter}"

    # Aqui se almacena en la base de datos

    url_from_db = insert_shorter_url(db=db, url=url_shorter)

    # renderiza el template html con la información de la nueva url acortada
    return templates.TemplateResponse("result.html", {
        "request": request,
        "short_url": shortened_url,
        "original_url": url_shorter.original,
        "created_at": url_from_db.created_at,
        "expires_at": url_from_db.expires_at,
        "visits": url_from_db.visits,
        "username": username
    })


@router.get('/')
async def home(request: Request):
    """
    Renderiza la página principal donde
    se encuentra el formulario que enviará
    el url original
    """
    token = request.session.get('token')
    username = 'unknown'
    if token:
        payload = verify_token(token)
        username = payload.get("username")
    return templates.TemplateResponse('index.html', {
        "request": request, "username": username
    })


@router.get('/{slug}')
async def redirect_url(slug: str, db: Session = Depends(get_db)):
    """
    Busca en la base de datos la url
    asociada al slug(url_acortada)
    y la redirecciona a su url original
    """
    original_url = get_by_shorter_url(db=db, slug=slug)

    # esto simula la busqueda del slug en la base de datos
    if not original_url:
        raise HTTPException(status_code=404, detail={
            'error': 'la url no existe o expiró'})
        # redirecciona a la url original

    increment_visits_url(db=db, slug=slug)
    return RedirectResponse(original_url)
