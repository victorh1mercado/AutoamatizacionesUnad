import os
from dotenv import load_dotenv

load_dotenv()

URL_CAMPUS = os.getenv("URL_CAMPUS")

USUARIO_UNAD = os.getenv("USUARIO_UNAD")
CLAVE_UNAD = os.getenv("CLAVE_UNAD")
CURSO = "AulaA"

# ==========================================
# MODOS DE EJECUCIÓN
# ==========================================

MODO_SIMULACION = 0
MODO_PRODUCCION = 1

# Cambiar únicamente esta variable
MODO = MODO_SIMULACION