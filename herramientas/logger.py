from pathlib import Path
from datetime import datetime

# Crear carpeta de logs si no existe
CARPETA_LOGS = Path("logs")
CARPETA_LOGS.mkdir(exist_ok=True)

# Archivo del día y la hora
ARCHIVO_LOG = CARPETA_LOGS / f"robot_{datetime.now():%Y%m%d_%H%M%S}.log"


def log(mensaje: str):

    print(mensaje)

    with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
        archivo.write(mensaje + "\n")