import subprocess
from pathlib import Path
import sys

APP_ROUTE = Path(__file__).parent.parent / "app" / "app.py"


def run_cli(flag):
    """
    Test básico para verificar el funcionamiento de las operaciones CLI de root/app/app.py.
    Comprueba que los comandos --status y --version funcionen correctamente.
    """
    result = subprocess.run(
        [sys.executable, str(APP_ROUTE), flag],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def test_status():
    """
    Verifica que el comando --status retorne 'OK'.
    """
    assert run_cli("--status") == 'OK'


def test_version():
    """
    Verifica que el comando --version retorne la versión del servidor.
    """
    assert run_cli("--version") == "-1.0.1"
