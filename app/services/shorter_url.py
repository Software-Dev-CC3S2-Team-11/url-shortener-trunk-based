import hashlib
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.Url import URL
from core.settings import url_expiration_months


def generate_slug(original_url: str, username: str):
    """
    Se hashea una url teniendo en cuenta la url y el username
    """

    string = f'{original_url}-{username}'
    slug = ((hashlib.sha256(string.encode())).hexdigest())[:8]

    return slug


def generate_date():
    """
    Devuelve la metadata de la fecha de creación y expiración (created_at y expires_at)
    """
    created_at = datetime.now()

    days = url_expiration_months * 30

    expirest_at = created_at + timedelta(days)

    return {"created_at": created_at, "expires_at": expirest_at}


def build_url_entity(original_url: str, username: str = 'unknown') -> URL:
    """
    Se le pasa la url extendida, username, y devuelve un objeto de la 
    clase URL que contiene la url hasheada con las fechas de creación
    y expiración.
    """
    
    slug = generate_slug(original_url, username=username)
    date = generate_date()

    return URL(original=original_url, shorter=slug, username=username,
               visits=0, created_at=date["created_at"],
               expires_at=date["expires_at"])
