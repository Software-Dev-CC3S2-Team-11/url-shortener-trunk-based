import pytest
from datetime import datetime, timedelta
from models.Url import URL
from app.services.shorter_url import generate_slug, increment_visits_url, get_urls_by_username, get_by_shorter_url, insert_shorter_url, build_url_entity


def test_generate_slug():
    """
    Verifica que el slug para la misma url y mismo usuario sea la misma
    también que la misma url para usuarios diferentes tenga diferentes 
    slugs
    """
    slug1 = generate_slug("http://example.com", "user1")
    slug2 = generate_slug("http://example.com", "user1")
    slug3 = generate_slug("http://example.com", "user2")

    assert slug1 == slug2
    assert slug2 != slug3

    assert len(slug1) == 8


def test_get_by_shorter_url_found(mock_db):
    """
    Verifica la salida de la función get_by_shorter_url
    para un slug que existe en la base de datos
    """

    mock_url = build_url_entity('http://example.com', 'user1')

    mock_db.query().filter().first.return_value = mock_url

    result = get_by_shorter_url(db=mock_db, slug=mock_url.shorter)
    assert result == "http://example.com"


def test_get_by_shorter_url_not_found(mock_db):
    """
    Verifica la salida de la función get_by_shorter_url
    para un slug que no existe en la base de datos
    """

    mock_db.query().filter().first.return_value = None

    result = get_by_shorter_url(mock_db, "test123")

    assert result is None


def test_gets_urls_by_username(mock_db):
    """
    Verifica la salida de la función gets_urls_by_username
    """
    mock_urls = [URL(username="user1"), URL(username="user1")]
    mock_db.query().filter().all.return_value = mock_urls

    result = get_urls_by_username(db=mock_db, username="user1")

    assert len(result) == 2
    assert all(url.username == "user1" for url in result)


def test_insert_shorter_url_new(mock_db):
    """
    Verifica si es que se agrega a la base de datos
    un url nuevo
    """

    mock_url = build_url_entity("https://example.com", "user1")
    mock_db.query().filter().first.return_value = None

    result = insert_shorter_url(mock_db, mock_url)

    mock_db.add.assert_called_once_with(mock_url)
    mock_db.commit.assert_called_once()
    assert result == mock_url


def test_insert_shorter_url_existing(mock_db):
    """
    Verifica si es que no se agrega a la base de datos
    un url con el mismo hash 
    """

    existing_url = build_url_entity("https://example.com", "user1")
    mock_db.query().filter().first.return_value = existing_url

    result = insert_shorter_url(mock_db, existing_url)

    mock_db.commit.assert_called_once()
    assert not mock_db.add.called
    assert result == existing_url


def test_increment_visits_url(mock_db):
    """
    Verifica que la función increments_visit_url
    llame a la función de update del ORM
    """

    increment_visits_url(mock_db, "abc12345")

    mock_db.query().filter().update.assert_called_once()
    mock_db.commit.assert_called_once()
