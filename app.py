import json
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

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
    read_config()
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)