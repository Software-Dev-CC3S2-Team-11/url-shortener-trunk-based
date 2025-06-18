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


def get_by_shorter_url(db: Session, slug: str) -> str | None:
    """Obtiene la URL original a partir del slug."""
    url = db.query(URL).filter(URL.shorter == slug).first()
    return url.original if url else None


def get_urls_by_username(db: Session, username: str) -> list[URL]:
    """Obtiene todas las URLs de un usuario."""
    return db.query(URL).filter(URL.username == username).all()


def insert_shorter_url(db: Session, url: URL) -> URL:
    """Inserta una nueva URL acortada en la base de datos."""
    url_found = db.query(URL).filter(
        (URL.username == url.username) & (URL.shorter == url.shorter)).first()

    if url_found:
        url_found.created_at = datetime.now()
        url_found.expires_at += timedelta(url_expiration_months*30)
        db.commit()
        return url_found

    db.add(url)
    db.commit()
    return url


def increment_visits_url(db: Session, slug: str):
    """
    Incrementa las vistas de una página al ser redireccionada
    """

    db.query(URL).filter(URL.shorter == slug).update(
        {URL.visits: URL.visits + 1})

    db.commit()
