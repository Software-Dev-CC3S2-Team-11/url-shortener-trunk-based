<<<<<<< HEAD
<<<<<<< HEAD
=======
"""
URL-SHORTENER V0
"""

import argparse
>>>>>>> b29e564 (feat: add base function cli and logic for __main__)
=======
import argparse
import sys
>>>>>>> ce62f8e (feat: cli argument parser implemented)
import json
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

VERSION = "-0"

app = FastAPI()


def read_config():
    with open("../config.json") as f:
        config = json.load(f)
        return config


# Lee el HOST y PORT desde el archivo de configuración
config = read_config()
HOST, PORT = config["HOST"], config["PORT"]

# Renderiza los html usando Jinja2
app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="../templates")


# urls acortadas para simular una base de datos
url_mapping = {
    'asd': 'https://www.google.com/search?q=asd&ie=UTF-8',
    'mnp': 'https://www.youtube.com/'
}


@app.get('/{slug}')
async def redirect_url(slug: str):
    """
    Busca en la base de datos la url
    asociada al slug(url_acortada)
    y la redirecciona a su url original
    """

    # esto simula la busqueda del slug en la base de datos
    if slug in url_mapping.keys():
        # redirecciona a la url original
        return RedirectResponse(url_mapping[slug])
    return {"error": "url not found"}


@app.post('/shorter', response_class=HTMLResponse)
async def generated_url(request: Request, url: str = Form(...)):
    """
    Toma la url enviada desde el form del index,
    genera un slug único, almacena los datos
    en la base de datos y luego devuelve una
    plantilla html con los datos de la url generada
    """
    slug = "asd"  # función que genera un slug a partir del url
    shortened_url = f"http://{HOST}:{PORT}/{slug}"

    # Aqui se almacena en la base de datos

    # renderiza el template html con la información de la nueva url acortada
    return templates.TemplateResponse("result.html", {
        "request": request,
        "short_url": shortened_url,
        "original_url": url,
        "created_at": "6/6/2025",
        "expires_at": "6/8/2025",
        "visits": 0
    })


@app.get('/')
async def home(request: Request):
    """
    Renderiza la página principal donde
    se encuentra el formulario que enviará
    el url original
    """
    return templates.TemplateResponse('index.html', {
        "request": request
    })


def cli() -> bool:
    """
    Parsea CLI flags antes de ejecutar el servidor.
    :return: True si se pasan argumentos de línea de comandos,
             False si no se pasan argumentos.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--status", action="store_true", help="Verifica si el servidor está corriendo")
    parser.add_argument("--version", action="store_true", help="Muestra la versión del servidor")

    args, _ = parser.parse_known_args()

    if args.status:
        print("OK")
        return True

    if args.version:
        print(VERSION)
        return True
    return False


if __name__ == "__main__":
<<<<<<< HEAD
    print('Versión 0')

    uvicorn.run("app:app", host=HOST, port=PORT, reload=True)
=======
    """
    Ejecuta el servidor uvicorn, si es que no se pasan
    argumentos de línea de comandos.
    """
    if cli():
        sys.exit(0)

    uvicorn.run("app:app", host=HOST, port=PORT, reload=True)
>>>>>>> b29e564 (feat: add base function cli and logic for __main__)
