# !/bin/sh

# Ejecución del archivo utilizando el PATH para Python, puede variar para Python3, modificar 'python' por 'python3'
# Verifica la existencia del archivo config.json antes de ejecutar el programa app.py
FILE="config.json"
if [ -f "$FILE" ]; then
  echo "El archivo $FILE existe"
  python app.py
  exit 0
fi
echo "El archivo $FILE no existe"
exit 1