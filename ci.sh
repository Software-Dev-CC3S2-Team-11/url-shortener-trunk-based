# !/bin/bash

#si hay un error se detiene
set -e

#crea el directorio de logs
mkdir -p logs

#la ruta del los logs
LOG_FILE="logs/ci.log"

#vacia los logs 
> "$LOG_FILE"


#Ejecuta flake8 y registrar logs
echo "Running flake8 " | tee -a "$LOG_FILE"
flake8 app/ --max-line-length=88 --exclude=venv,__pycache__ >> "$LOG_FILE"

#Ejecuta pytest y verifica que la cobertura sea mayor al 80%
echo "Running pytest with coverage " | tee -a "$LOG_FILE"
pytest --cov=. --cov-fail-under=80 >> "$LOG_FILE"

echo "All tests passed" | tee -a "$LOG_FILE"