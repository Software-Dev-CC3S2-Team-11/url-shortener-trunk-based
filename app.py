import json
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()


def read_config():
    with open("config.json") as f:
        config = json.load(f)
        return config


# Lee el HOST y PORT desde el archivo de configuración
config = read_config()
HOST, PORT = config["HOST"], config["PORT"]

# Renderiza los html usando Jinja2
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# urls acortadas para simular una base de datos
url_mapping = {
    'asd': 'https://www.google.com/search?q=asd&ie=UTF-8',
    'mnp': 'https://www.youtube.com/'
}


@app.get('/{slug}')
def redirect_url(slug: str):
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


def read_config():
    with open("config.json") as f:
        config = json.load(f)
        print(config)


if __name__ == "__main__":
    print('Versión 0')
    uvicorn.run("app:app", host=HOST, port=PORT, reload=True)
