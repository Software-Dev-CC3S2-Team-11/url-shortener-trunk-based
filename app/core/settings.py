import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.json"

with open(CONFIG_PATH) as f:
    config = json.load(f)

HOST = config.get("HOST", "localhost")
PORT = config.get("PORT", 8000)
url_expiration_months = config.get("url_expiration_months", 3)
